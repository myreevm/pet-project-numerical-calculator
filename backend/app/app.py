# app.py (или в app/__init__.py)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import derivative_router
from .routers import integral_router
from .routers import parabolic1d_router
from .routers import parabolic2d_router
from .routers import frac_parabolic1d_router
from .routers import inverse_parabolic1d_router
from .routers import hyperbolic1d_router
from .routers import elliptic1d_router
from .routers import elliptic2d_router
from .routers import inverse_elliptic1d_router
from .routers import ode1_router
from .routers import ode2_router
from .routers import nonlinear_router
from .routers import wastewater_router
from .routers import stg_router

app = FastAPI(title="NumMethods Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проде ограничьте доменами фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(derivative_router)
app.include_router(integral_router)
app.include_router(parabolic1d_router)
app.include_router(parabolic2d_router)
app.include_router(frac_parabolic1d_router)
app.include_router(inverse_parabolic1d_router)
app.include_router(hyperbolic1d_router)
app.include_router(elliptic1d_router)
app.include_router(elliptic2d_router)
app.include_router(inverse_elliptic1d_router)
app.include_router(ode1_router)
app.include_router(ode2_router)
app.include_router(nonlinear_router)
app.include_router(wastewater_router)
app.include_router(stg_router)
