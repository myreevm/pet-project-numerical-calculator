from .derivative_router import router as derivative_router
from .integral_router import router as integral_router
from .parabolic1d_router import router as parabolic1d_router
from .parabolic2d_router import router as parabolic2d_router
from .frac_parabolic1d_router import router as frac_parabolic1d_router
from .inverse_parabolic_1d_router import router as inverse_parabolic1d_router
from .hyperbolic1d_router import router as hyperbolic1d_router
from .elliptic1d_router import router as elliptic1d_router
from .elliptic2d_router import router as elliptic2d_router
from .inverse_elliptic_1d_router import router as inverse_elliptic1d_router
from .ode1_router import router as ode1_router
from .ode2_router import router as ode2_router
from .nonlinear_router import router as nonlinear_router
from .wastewater_router import router as wastewater_router
from .stg_router import router as stg_router

__all__ = [
    'derivative_router',
    'integral_router',
    'parabolic1d_router',
    'parabolic2d_router',
    'frac_parabolic1d_router',
    'inverse_parabolic1d_router',
    'hyperbolic1d_router',
    'elliptic1d_router',
    'elliptic2d_router',
    'inverse_elliptic1d_router',
    'ode1_router',
    'ode2_router',
    'nonlinear_router',
    'wastewater_router',
    'stg_router',
]