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

from ..utils import solve_parabolic_equation_2d

router = APIRouter(prefix="/api/parabolic2d", tags=["parabolic2d"])

class MethodType(str, Enum):
    explicit = 'explicit'
    adi = 'ADI'
    lods = 'LODS'
    
class SolveRequest(BaseModel):
    T: float
    Lx: float
    Ly: float
    N: int
    Mx: int
    My: int
    a: float
    init_cond: Optional[Union[str, float]] = None
    init_values: Optional[List[float]] = None
    left_bc:  Optional[Union[str, float]] = None
    left_values: Optional[List[float]] = None
    right_bc: Optional[Union[str, float]] = None
    right_values: Optional[List[float]] = None
    bottom_bc:  Optional[Union[str, float]] = None
    bottom_values: Optional[List[float]] = None
    top_bc: Optional[Union[str, float]] = None
    top_values: Optional[List[float]] = None
    method: MethodType
    # f можно передать как выражение от x (строку), число или список значений
    f_expr: Optional[Union[str, float]] = None
    f_values: Optional[List[float]] = None

def _parse_f_3d(T, N, Lx, Ly, Mx, My, f_expr=None, f_values=None):
    t = np.linspace(0, T, N+1)
    x = np.linspace(0, Lx, Mx+1)
    y = np.linspace(0, Ly, My+1)

    # ---- Если задан массив значений ----
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape != (Mx+1, My+1, N+1):
            raise ValueError(
                "f_values должен иметь форму (Mx+1, My+1, N+1)"
            )
        return lambda xx, yy, tt: arr  # игнорируем вход

    # ---- Если задано выражение ----
    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda xarr, yarr, tarr: np.full_like(xarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def f_callable(xarr, yarr, tarr):
            try:
                val = eval(
                    f_expr,
                    {"__builtins__": {}},
                    {
                        **allowed,
                        "x": xarr,
                        "y": yarr,
                        "t": tarr
                    }
                )
                # если результат — число, делаем массив
                if np.isscalar(val):
                    val = np.full_like(xarr, float(val))
                return val
            except Exception as e:
                raise ValueError(
                    "Ошибка в выражении правой части: " + str(e)
                )

        return f_callable

    raise ValueError("Нужно передать либо f_expr, либо f_values")


def _parse_init(Lx, Ly, Mx, My, f_expr=None, f_values=None):
    x = np.linspace(0, Lx, Mx+1)
    y = np.linspace(0, Ly, My+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape != (Mx+1, My+1):
            raise ValueError("f_values должен иметь длину (Mx+1, My+1)")
        return lambda xx, yy: arr  # возвращаем массив (игнорируем xx)

    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda xarr, yarr: np.full_like(xarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def init_callable(xarr, yarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "x": xarr, "y": yarr})
                # если результат — число, преобразуем в массив той же длины, что xarr
                if np.isscalar(val):
                    val = np.full_like(xarr, float(val))
                return val
            except Exception as e:
                #raise ValueError(f"Нет переменной x в функции правой части")
                raise ValueError(f"Неизвестная переменная для начального условия"+str(e))
        return init_callable

    raise ValueError("Нужно передать либо f_expr, либо f_values")

def _parse_boundary_lr(T, N, Ly, My, f_expr=None, f_values=None):
    t = np.linspace(0, T, N+1)
    y = np.linspace(0, Ly, My+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape != (N+1, My+1):
            raise ValueError("f_values должен иметь длину (M+1, Ny+1)")
        return lambda yy, tt: arr  # возвращаем массив (игнорируем xx)

    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda yarr, tarr: np.full_like(yarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def boundary_callable(yarr, tarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "y":yarr, "t": tarr})
                # если результат — число, преобразуем в массив той же длины, что xarr
                if np.isscalar(val):
                    val = np.full_like(yarr, float(val))
                
                return val
            except Exception as e:
                #raise ValueError(f"Нет переменной x в функции правой части")
                raise ValueError(f"Неизвестная переменная для левого/правого ГУ "+str(e))
        return boundary_callable

    raise ValueError("Нужно передать либо f_expr, либо f_values")

def _parse_boundary_bt(T, N, Lx, Mx, f_expr=None, f_values=None):
    t = np.linspace(0, T, N+1)
    x = np.linspace(0, Lx, Mx+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape != (N+1, Mx+1):
            raise ValueError("f_values должен иметь длину (M+1, Nx+1)")
        return lambda xx, tt: arr  # возвращаем массив (игнорируем xx)

    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda xarr, tarr: np.full_like(xarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def boundary_callable(xarr, tarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "x":xarr, "t": tarr})
                # если результат — число, преобразуем в массив той же длины, что xarr
                if np.isscalar(val):
                    val = np.full_like(xarr, float(val))
                
                return val
            except Exception as e:
                #raise ValueError(f"Нет переменной x в функции правой части")
                raise ValueError(f"Неизвестная переменная для нижнего/верхнего ГУ "+str(e))
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
        f_callable = _parse_f_3d(req.T, req.N, req.Lx, req.Ly, req.Mx, req.My, req.f_expr, req.f_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        init_callable = _parse_init(req.Lx, req.Ly, req.Mx, req.My, req.init_cond, req.init_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        left_callable = _parse_boundary_lr(req.T, req.N, req.Ly, req.My, req.left_bc, req.left_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        right_callable = _parse_boundary_lr(req.T, req.N, req.Ly, req.My, req.right_bc, req.right_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        bottom_callable = _parse_boundary_bt(req.T, req.N, req.Lx, req.Mx, req.bottom_bc, req.bottom_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        top_callable = _parse_boundary_bt(req.T, req.N, req.Lx, req.Mx, req.top_bc, req.top_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        #start_time = time.time()
        #if req.method == MethodType.explicit:
        u = solve_parabolic_equation_2d(req.T, req.Lx, req.Ly, req.N, req.Mx, req.My, req.a, init_callable, left_callable, right_callable, bottom_callable, top_callable, f_callable)
        #else:
        #    x, u = solve_parabolic_equation_implicit(req.T, req.L, req.N, req.M, req.a, init_callable, left_callable, right_callable, f_callable)
        #elapsed_time = time.perf_counter() - start_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка решения: {e}")

    # --- 1D plot (последний момент времени) ---
    fig1 = plt.figure(figsize=(6, 4))
    plt.imshow(u[0][:][:].T)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Решение u при t = 0')
    plt.colorbar()
    img_line1 = _plot_to_base64(fig1)

    fig2 = plt.figure(figsize=(6, 4))
    plt.imshow(u[len(u)//2][:][:].T)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Решение u при t = T/2')
    plt.colorbar()
    img_line2 = _plot_to_base64(fig2)

    fig3 = plt.figure(figsize=(6, 4))
    plt.imshow(u[len(u)-1][:][:].T)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Решение u при t = T')
    plt.colorbar()
    img_line3 = _plot_to_base64(fig3)

    return {
        "u": u.tolist(),
        "img_line1": img_line1,
        "img_line2": img_line2,
        "img_line3": img_line3
    }
