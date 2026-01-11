# routers/elliptic_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
import base64
from io import BytesIO
from enum import Enum
import matplotlib.pyplot as plt

from ..utils import solve_nonlinear_equation

router = APIRouter(prefix="/api/nonlinear", tags=["nonlinear"])

#class MethodType(str, Enum):
#    euler = 'euler_method'
#    symmetric_euler = 'symmetric_euler_method'

class SolveRequest(BaseModel):
    eps: float
    init_cond: float
    #method: MethodType
    f_expr: Optional[str] = None
    f_values: Optional[list] = None

def _parse_f(f_expr=None, f_values=None):
    #x = np.linspace(0, L, M+1)
    #if f_values is not None:
    #    arr = np.asarray(f_values, dtype=float)
    #    if arr.shape[0] != x.shape[0]:
    #        raise ValueError("f_values должен иметь длину M+1")
    #    return lambda xx: arr  # возвращаем массив (игнорируем xx)

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

def _to_python_type(val):
    if isinstance(val, np.ndarray):
        return val.tolist()
    elif np.isscalar(val):
        return float(val)
    else:
        return val  # уже нормальный Python объект

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
        f_callable = _parse_f(req.f_expr, req.f_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    #print("solving")
    try:
        result = solve_nonlinear_equation(req.eps, req.init_cond, f_callable)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

    # --- 1D plot ---
    #fig1 = plt.figure(figsize=(6,4))
    #plt.plot(x, u, marker='o')
    #plt.xlabel('x')
    #plt.ylabel('u(x)')
    #plt.grid()
    #plt.title('Решение u(x)')
    #img_line = _plot_to_base64(fig1)

    return {
        "result": _to_python_type(result)
    }
