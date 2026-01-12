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

from ..utils import solve_elliptic_equation_2d

router = APIRouter(prefix="/api/elliptic2d", tags=["elliptic2d"])

#class MethodType(str, Enum):
#    explicit = 'explicit'
#    adi = 'ADI'
#    lods = 'LODS'

class SolveRequest(BaseModel):
    Lx: float
    Ly: float
    M: int
    k: float
    left_bc: Optional[Union[str, float]] = None
    left_values: Optional[List[float]] = None
    right_bc: Optional[Union[str, float]] = None
    right_values: Optional[List[float]] = None
    bottom_bc:  Optional[Union[str, float]] = None
    bottom_values: Optional[List[float]] = None
    top_bc: Optional[Union[str, float]] = None
    top_values: Optional[List[float]] = None
    #method: MethodType
    # f можно передать как строку-выражение от x (например "np.sin(x) + x**2"),
    # либо как список чисел (len = M+1)
    f_expr: Optional[str] = None
    f_values: Optional[list] = None

def _parse_f(Lx, Ly, M, f_expr=None, f_values=None):
    x = np.linspace(0, Lx, M+1)
    y = np.linspace(0, Ly, M+1)

    # ---- Если задан массив значений ----
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape != (M+1, M+1):
            raise ValueError(
                "f_values должен иметь форму (N+1, N+1)"
            )
        return lambda xx, yy: arr

    # ---- Если задано выражение ----
    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda xarr, yarr: np.full_like(xarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def f_callable(xarr, yarr):
            try:
                val = eval(
                    f_expr,
                    {"__builtins__": {}},
                    {
                        **allowed,
                        "x": xarr,
                        "y": yarr
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

def _parse_boundary_lr(Ly, M, f_expr=None, f_values=None):
    y = np.linspace(0, Ly, M+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape != (M+1):
            raise ValueError("f_values должен иметь длину (N+1)")
        return lambda yy: arr  # возвращаем массив (игнорируем xx)

    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda yarr: np.full_like(yarr, float(f_expr))
        
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }
        
        def boundary_callable(yarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "y":yarr})
                # если результат — число, преобразуем в массив той же длины, что xarr
                if np.isscalar(val):
                    val = np.full_like(yarr, float(val))
                
                return val
            except Exception as e:
                #raise ValueError(f"Нет переменной x в функции правой части")
                raise ValueError(f"Неизвестная переменная для граничного условия "+str(e))
        return boundary_callable

    raise ValueError("Нужно передать либо f_expr, либо f_values")

def _parse_boundary_bt(Lx, M, f_expr=None, f_values=None):
    x = np.linspace(0, Lx, M+1)
    if f_values is not None:
        arr = np.asarray(f_values, dtype=float)
        if arr.shape != (M+1):
            raise ValueError("f_values должен иметь длину (N+1)")
        return lambda xx: arr  # возвращаем массив (игнорируем xx)

    if f_expr is not None:
        if isinstance(f_expr, (int, float)):
            return lambda yarr: np.full_like(yarr, float(f_expr))
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }

        def boundary_callable(xarr):
            try:
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "x":xarr})
                # если результат — число, преобразуем в массив той же длины, что xarr
                if np.isscalar(val):
                    val = np.full_like(xarr, float(val))
                
                return val
            except Exception as e:
                #raise ValueError(f"Нет переменной x в функции правой части")
                raise ValueError(f"Неизвестная переменная для граничного условия "+str(e))
        return boundary_callable

    raise ValueError("Нужно передать либо f_expr, либо f_values")

def _plot_to_base64(fig):
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return img_base64

@router.post("/solve")
def solve(req: SolveRequest):
    try:
        f_callable = _parse_f(req.Lx, req.Ly, req.M, req.f_expr, req.f_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    
    try:
        left_callable = _parse_boundary_lr(req.Ly, req.M, req.left_bc, req.left_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        right_callable = _parse_boundary_lr(req.Ly, req.M, req.right_bc, req.right_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        bottom_callable = _parse_boundary_bt(req.Lx, req.M, req.bottom_bc, req.bottom_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        top_callable = _parse_boundary_bt(req.Lx, req.M, req.top_bc, req.top_values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    try:
        x, y, u = solve_elliptic_equation_2d(req.Lx, req.Ly, req.M, req.k, left_callable, right_callable, bottom_callable, top_callable, f_callable)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

    fig, ax = plt.subplots()

    contour1 = ax.contourf(x, y, u, levels=20)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title("Решение")
    fig.colorbar(contour1, ax=ax)

    img_line = _plot_to_base64(fig)
    plt.close(fig)
    
    return {
        "x": x.tolist(),
        "u": u.tolist(),
        "img_line": img_line,
    }
