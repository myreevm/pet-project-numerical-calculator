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

from ..utils import solve_inverse_parabolic

router = APIRouter(prefix="/api/inverse_parabolic1d", tags=["inverse_parabolic1d"])

#class MethodType(str, Enum):
#    explicit = 'solve-parabolic-equation-explicit'
#    implicit = 'solve-parabolic-equation-implicit'
    
class SolveRequest(BaseModel):
    T: float
    L: float
    N: int
    M: int
    a: float
    noise: float
    init_cond: Optional[Union[str, float]] = None
    init_values: Optional[List[float]] = None
    left_bc:  Optional[Union[str, float]] = None
    left_values: Optional[List[float]] = None
    right_bc: Optional[Union[str, float]] = None
    right_values: Optional[List[float]] = None
    # f можно передать как выражение от x (строку), число или список значений
    f_expr: Optional[Union[str, float]] = None
    f_values: Optional[List[float]] = None
    max_iter: int

def _parse_f(T, N, L, M, f_expr=None, f_values=None):
    t = np.linspace(0, T, N+1)
    x = np.linspace(0, L, M+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape != (M+1, N+1):
            raise ValueError("f_values должен иметь форму (M+1, N+1)")
        return lambda xx, tt: arr  # игнорируем вход, возвращаем массив

    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda xarr, tarr: np.full_like(xarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def f_callable(xarr, tarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "x": xarr, "t": tarr})
                # если результат — число, преобразуем в массив той же формы
                if np.isscalar(val):
                    val = np.full_like(xarr, float(val))
                return val
            except Exception as e:
                raise ValueError("Неизвестная переменная для функции правой части"+str(e))
        return f_callable

    raise ValueError("Нужно передать либо f_expr, либо f_values")

def _parse_init(L, M, f_expr=None, f_values=None):
    x = np.linspace(0, L, M+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape[0] != x.shape[0]:
            raise ValueError("f_values должен иметь длину M+1")
        return lambda xx: arr  # возвращаем массив (игнорируем xx)

    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda xarr: np.full_like(xarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def init_callable(xarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "x": xarr})
                # если результат — число, преобразуем в массив той же длины, что xarr
                if np.isscalar(val):
                    val = np.full_like(xarr, float(val))
                return val
            except Exception as e:
                #raise ValueError(f"Нет переменной x в функции правой части")
                raise ValueError(f"Неизвестная переменная для начального условия"+str(e))
        return init_callable

    raise ValueError("Нужно передать либо f_expr, либо f_values")

def _parse_boundary(T, N, f_expr=None, f_values=None):
    t = np.linspace(0, T, N+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape[0] != t.shape[0]:
            raise ValueError("f_values должен иметь длину M+1")
        return lambda tt: arr  # возвращаем массив (игнорируем xx)

    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda tarr: np.full_like(tarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def boundary_callable(tarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "t": tarr})
                # если результат — число, преобразуем в массив той же длины, что xarr
                if np.isscalar(val):
                    val = np.full_like(tarr, float(val))
                
                return val
            except Exception as e:
                #raise ValueError(f"Нет переменной x в функции правой части")
                raise ValueError(f"Неизвестная переменная для граничного условия "+str(e))
        return boundary_callable

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
        f_callable = _parse_f(req.T, req.N, req.L, req.M, req.f_expr, req.f_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        init_callable = _parse_init(req.L, req.M, req.init_cond, req.init_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        left_callable = _parse_boundary(req.T, req.N, req.left_bc, req.left_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        right_callable = _parse_boundary(req.T, req.N, req.right_bc, req.right_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        #start_time = time.time()
        x, f_k, f_exact = solve_inverse_parabolic(req.T, req.L, req.N, req.M, req.a, req.noise, init_callable, left_callable, right_callable, f_callable, req.max_iter)
        #elapsed_time = time.perf_counter() - start_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка решения: {e}")


    fig1 = plt.figure(figsize=(6, 4))
    plt.plot(x, f_k[len(f_k)//2], label='Восстановленный f')
    plt.plot(x, f_exact[len(f_exact)//2], label='Точный f')
    plt.xlabel('x')
    plt.ylabel('f(x, t)')
    plt.title('t = 0.5')
    plt.legend()
    plt.grid()
    img_line = _plot_to_base64(fig1)


    return {
        "img_line": img_line
    }
