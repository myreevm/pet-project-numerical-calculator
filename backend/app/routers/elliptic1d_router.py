# routers/elliptic_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt

from ..utils import solve_elliptic_equation

router = APIRouter(prefix="/api/elliptic1d", tags=["elliptic1d"])

class SolveRequest(BaseModel):
    L: float
    M: int
    a: float
    left_bc: float
    right_bc: float
    # f можно передать как строку-выражение от x (например "np.sin(x) + x**2"),
    # либо как список чисел (len = M+1)
    f_expr: Optional[str] = None
    f_values: Optional[list] = None

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
        x, u = solve_elliptic_equation(req.L, req.M, req.a, req.left_bc, req.right_bc, f_callable)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

    # --- 1D plot ---
    fig1 = plt.figure(figsize=(6,4))
    plt.plot(x, u, marker='o')
    plt.xlabel('x')
    plt.ylabel('u(x)')
    plt.title('Решение u(x)')
    img_line = _plot_to_base64(fig1)

    return {
        "x": x.tolist(),
        "u": u.tolist(),
        "img_line": img_line,
    }
