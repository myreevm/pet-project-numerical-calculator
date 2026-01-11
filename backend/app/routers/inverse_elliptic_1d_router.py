# routers/elliptic_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Union, List
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from enum import Enum
import numexpr as ne
import sympy as sp

from ..utils import simple_iter_method, tikhonov_method

router = APIRouter(prefix="/api/inverse_elliptic1d", tags=["inverse_elliptic1d"])

class MethodType(str, Enum):
    simple_iter = 'simple_iter'
    tikhonov = 'tikhonov'
    
class SolveRequest(BaseModel):
    L: float
    M: int
    a: float
    noise: float
    left_bc: float
    right_bc: float
    method: MethodType
    # f можно передать как выражение от x (строку), число или список значений
    f_expr: Optional[Union[str, float]] = None
    f_values: Optional[List[float]] = None
    max_iter: int

def _parse_f(L, M, f_expr=None, f_values=None):
    x = np.linspace(0, L, M+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape[0] != x.shape[0]:
            raise ValueError("f_values должен иметь длину M+1")
        return lambda xx: arr  # возвращаем массив (игнорируем xx)

    if f_expr is not None:
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def f_callable(xarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "x": xarr})
                # если результат — число, преобразуем в массив той же длины, что xarr
                if np.isscalar(val):
                    val = np.full_like(xarr, float(val))
                return val
            except Exception as e:
                #raise ValueError(f"Нет переменной x в функции правой части")
                raise ValueError(f"Неизвестная переменная")
        return f_callable

    raise ValueError("Нужно передать либо f_expr, либо f_values")

def _plot_to_base64(fig):
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("ascii")
    plt.close(fig)
    return "data:image/png;base64," + b64

@router.post("/solve")
def solve(req: SolveRequest):
    try:
        f_callable = _parse_f(req.L, req.M, req.f_expr, req.f_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        #start_time = time.time()
        if req.method == MethodType.simple_iter:
            fk, f = simple_iter_method(req.L, req.M, req.a, req.noise, req.left_bc, req.right_bc, f_callable, req.max_iter)
        else:
            fk, f = tikhonov_method(req.L, req.M, req.a, req.noise, req.left_bc, req.right_bc, f_callable)
        #elapsed_time = time.perf_counter() - start_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка решения: {e}")

    # --- 1D plot ---
    fig1 = plt.figure(figsize=(6,4))
    plt.plot(fk, label='прибл.')
    plt.plot(f, label='точная')
    plt.legend()
    plt.grid()
    img_line = _plot_to_base64(fig1)

    return {
        "img_line": img_line,
    }
