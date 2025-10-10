# app.py (или в app/__init__.py)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import derivative_router
from .routers import integral_router
from .routers import parabolic1d_router
from .routers import elliptic_router

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
app.include_router(elliptic_router)
