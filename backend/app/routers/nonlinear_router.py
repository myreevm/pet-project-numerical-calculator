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
    if f_expr is not None:
        allowed = {
            "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }
        def f_callable(x):
            try:
                # Поддержка как скаляров, так и массивов
                val = eval(f_expr, {"__builtins__": {}}, {**allowed, "x": x})
                return val
            except Exception as e:
                raise ValueError(f"Ошибка в выражении: {e}")
        return f_callable
    
    if f_values is not None:
        # Если передан массив значений, интерполируем
        arr = np.asarray(f_values, dtype=float)
        return lambda x: np.interp(x, np.linspace(0, 1, len(arr)), arr)
    
    raise ValueError("Нужно передать либо f_expr, либо f_values")

def _to_python_type(val):
    if isinstance(val, np.ndarray):
        # Если массив из одного элемента, вернуть скаляр
        if val.size == 1:
            return float(val.item())
        return val.tolist()
    elif isinstance(val, (np.integer, np.floating)):
        return float(val)
    else:
        return val

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
    
    try:
        result, iter, end_time = solve_nonlinear_equation(req.eps, req.init_cond, f_callable)
        #print(f"Raw result: {result}, type: {type(result)}")
        
        converted = _to_python_type(result)
        #print(f"Converted: {converted}, type: {type(converted)}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка решения: {e}")
    
    return {
        "result": converted,
        "iter": iter,
        "end_time": end_time,
    }
