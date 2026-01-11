# routers/elliptic_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
import base64
from io import BytesIO
from enum import Enum
import matplotlib.pyplot as plt

from ..utils import solve_solid_tumor_with_diffusion, solve_solid_tumor_without_diffusion

router = APIRouter(prefix="/api/stg", tags=["stg"])

class MethodType(str, Enum):
    withdiffusion = 'withdiffusion'
    withoutdiffusion = 'withoutdiffusion'

class SolveRequest(BaseModel):
    u10: float
    u20: float
    u30: float
    t0: float
    t_end: float
    h: float
    mu1: float
    mu2: float
    gamma1: float
    gamma2: float
    gamma3: float
    method: MethodType

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
        if req.method == MethodType.withdiffusion:
            t, u1, u2, u3 = solve_solid_tumor_with_diffusion(req.u10, req.u20, req.u30, req.t0, req.t_end, req.h, req.mu1, req.mu2, req.gamma1, req.gamma2, req.gamma3)
        else:
            t, u1, u2, u3 = solve_solid_tumor_without_diffusion(req.u10, req.u20, req.u30, req.t0, req.t_end, req.h, req.mu1, req.mu2, req.gamma1, req.gamma2, req.gamma3)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

    fig1 = plt.figure(figsize=(6,4))
    plt.plot(t, u1, label='Хищник', color='red')
    plt.plot(t, u2, label='Жертва', color='green')
    plt.plot(t, u3, label='Мертвые клетки', color='blue')
    plt.xlabel('Время t')
    plt.ylabel('Плотность клеток')
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
