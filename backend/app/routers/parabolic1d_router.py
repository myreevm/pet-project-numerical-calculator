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

from ..utils import solve_parabolic_equation_explicit, solve_parabolic_equation_implicit

router = APIRouter(prefix="/api/parabolic1d", tags=["parabolic1d"])

class MethodType(str, Enum):
    explicit = 'solve-parabolic-equation-explicit'
    implicit = 'solve-parabolic-equation-implicit'
    
class SolveRequest(BaseModel):
    T: float
    L: float
    N: int
    M: int
    a: float
    init_cond: Optional[Union[str, float]] = None
    init_values: Optional[List[float]] = None
    left_bc:  Optional[Union[str, float]] = None
    left_values: Optional[List[float]] = None
    right_bc: Optional[Union[str, float]] = None
    right_values: Optional[List[float]] = None
    method: MethodType
    # f можно передать как выражение от x (строку), число или список значений
    f_expr: Optional[Union[str, float]] = None
    f_values: Optional[List[float]] = None

def _parse_function(var_name: str, var_end: float, N: int, expr=None, values=None):
    """
    Универсальный парсер для функций от одной переменной (x или t).
    Поддерживает:
      - expr: число, строку (например "sin(x) + x**2")
      - values: список чисел длиной N+1
    """
    var = np.linspace(0, var_end, N + 1)

    # --- табличные значения ---
    if values is not None:
        arr = np.asarray(values, dtype=float)
        if arr.shape[0] != var.shape[0]:
            raise ValueError(f"{var_name}_values должен иметь длину {N+1}")
        return lambda _: arr.copy()

    # --- константа ---
    if isinstance(expr, (int, float)):
        return lambda _: np.full_like(var, float(expr))

    # --- аналитическое выражение ---
    if isinstance(expr, str):
        def func(v):
            try:
                val = ne.evaluate(expr, local_dict={var_name: v, "np": np})
                val = np.asarray(val, dtype=float)
                if val.ndim == 0:  # если скаляр
                    val = np.full_like(v, float(val))
                return val
            except Exception as e:
                raise ValueError(f"Ошибка при вычислении {var_name}-выражения: {e}")
        return func

    raise ValueError(f"Нужно передать либо {var_name}_expr, либо {var_name}_values")






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
        #f_callable = _parse_function("x", req.L, req.M, req.f_expr, req.f_values)
        #init_callable = _parse_function("x", req.L, req.M, req.init_cond, req.init_values)
        #left_bc_callable = _parse_function("t", req.T, req.N, req.left_bc, req.left_values)
        #right_bc_callable = _parse_function("t", req.T, req.N, req.right_bc, req.right_values)
        
        initial_condition = req.init_cond
        left_boundary_condition = req.left_bc
        right_boundary_condition = req.right_bc
        right_side_function = req.f_expr
        
        def _safe_replace(expr):
            return expr.replace('^', '**') if isinstance(expr, str) else expr

        initial_condition = _safe_replace(req.init_cond)
        left_boundary_condition = _safe_replace(req.left_bc)
        right_boundary_condition = _safe_replace(req.right_bc)
        right_side_function = _safe_replace(req.f_expr)


        x_sym = sp.Symbol('x')
        t_sym = sp.Symbol('t')
        
        if initial_condition is None:
            raise HTTPException(status_code=400, detail="Не задано начальное условие init_cond")

        
        init_cond = sp.sympify(initial_condition)
        left_cond = sp.sympify(left_boundary_condition)
        right_cond = sp.sympify(right_boundary_condition)
        f_ = sp.sympify(right_side_function)
        
        init = sp.lambdify((x_sym), init_cond, modules=["numpy"])
        left = sp.lambdify((t_sym), left_cond, modules=["numpy"])
        right = sp.lambdify((t_sym), right_cond, modules=["numpy"])
        f = sp.lambdify((x_sym, t_sym), f_, modules=["numpy"])
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


    try:
        #start_time = time.time()
        if req.method == MethodType.explicit:
            x, u = solve_parabolic_equation_explicit(req.T, req.L, req.N, req.M, req.a, init, left, right, f)
        else:
            x, u = solve_parabolic_equation_implicit(req.T, req.L, req.N, req.M, req.a, init, left, right, f)
        #elapsed_time = time.perf_counter() - start_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка решения: {e}")

    # --- 1D plot (последний момент времени) ---
    fig1 = plt.figure(figsize=(6, 4))
    plt.plot(x, u[-1, :], marker='o')
    plt.xlabel('x')
    plt.ylabel('u(x, T)')
    plt.title('Решение u(x, T) при t = T')
    plt.grid(True)
    img_line = _plot_to_base64(fig1)

    # --- 2D heatmap: эволюция решения во времени ---
    fig2 = plt.figure(figsize=(6, 4))
    # u имеет размерность (N+1, M+1): время x пространство
    plt.imshow(u, aspect='auto', origin='lower', 
            extent=[x[0], x[-1], 0, 1],  # если время нормировано до [0,1]; можно заменить extent=[x[0], x[-1], 0, T]
            interpolation='nearest')
    plt.colorbar(label='u(x, t)')
    plt.xlabel('x')
    plt.ylabel('t (нормированное)')
    plt.title('Эволюция решения u(x, t)')
    img_heat = _plot_to_base64(fig2)


    return {
        "x": x.tolist(),
        "u": u.tolist(),
        "img_line": img_line,
        "img_heat": img_heat
    }
