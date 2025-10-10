from .derivative_router import router as derivative_router
from .integral_router import router as integral_router
from .parabolic1d_router import router as parabolic1d_router
from .elliptic_router import router as elliptic_router

__all__ = [
    'derivative_router',
    'integral_router',
    'parabolic1d_router',
    'elliptic_router'
    
]