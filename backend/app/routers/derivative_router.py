# routers/elliptic_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from enum import Enum

from ..utils import left_derivative, central_derivative, right_derivative

router = APIRouter(prefix="/api/derivative", tags=["derivative"])

class MethodType(str, Enum):
    left = "left-derivative"
    central = "central-derivative"
    right = "right-derivative"
# модель запроса
class SolveRequest(BaseModel):
    x: float
    h: float
    method: MethodType
    # f можно передать как строку-выражение от x (например "np.sin(x) + x**2"),
    # либо как список чисел (len = M+1)
    f_expr: Optional[str] = None

def _parse_f(f_expr=None):    
    if f_expr is not None:
        # Разрешённые имена в eval
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi
        }
        def f_callable(xarr):
            # Безопасно вычисляем выражение: доступна переменная x (numpy array)
            try:
                return eval(f_expr, {"__builtins__": {}}, {**allowed, "x": xarr})
            except Exception as e:
                raise ValueError(f"Ошибка при вычислении f_expr: {e}")
        return f_callable
    raise ValueError("Нужно передать либо f_expr, либо f_values")

@router.post("/solve")
def solve(req: SolveRequest):
    try:
        f_callable = _parse_f(req.f_expr)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        if req.method == MethodType.left:
            result = left_derivative(f_callable, req.x, req.h)
        elif req.method == MethodType.central:
            result = central_derivative(f_callable, req.x, req.h)
        elif req.method == MethodType.right:
            result = right_derivative(f_callable, req.x, req.h)
        else:
            raise HTTPException(status_code=400, detail="Неизвестный метод вычисления производной.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка решения: {e}")


    return {
        "result": result
    }
