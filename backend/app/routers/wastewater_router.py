# routers/elliptic_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
import base64
from io import BytesIO
from enum import Enum
import matplotlib.pyplot as plt

from ..utils import solve_wastewater

router = APIRouter(prefix="/api/wastewater", tags=["wastewater"])

#class MethodType(str, Enum):
#    euler = 'euler_method'
#    symmetric_euler = 'symmetric_euler_method'

class SolveRequest(BaseModel):
    T: float
    N: int
    mu_m: float
    K_L: float
    Y: float
    X0: float
    L0: float

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
        t, sol = solve_wastewater(req.T, req.N, req.mu_m, req.K_L, req.Y, req.X0, req.L0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

    fig1 = plt.figure(figsize=(6,4))
    plt.plot(t, sol[:, 0], label="X", color='green')
    plt.plot(t, sol[:, 1], label="L", color='red')
    plt.xlabel("Время (сут)")
    plt.ylabel("Концентрация (мг/л)")
    plt.legend()
    plt.grid()
    # --- 1D plot ---
    #fig1 = plt.figure(figsize=(6,4))
    #plt.plot(x, u, marker='o')
    #plt.xlabel('x')
    #plt.ylabel('u(x)')
    #plt.grid()
    #plt.title('Решение u(x)')
    img_line = _plot_to_base64(fig1)

    return {
        "img_line": img_line
    }
