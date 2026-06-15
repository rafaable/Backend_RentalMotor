from fastapi import FastAPI
from app.routes import pengguna
from app.routes import cabang
from app.routes import penyewaan

app = FastAPI()

app.include_router(
    pengguna.router,
    prefix="/pengguna",
    tags=["Pengguna"]
)

app.include_router(
    penyewaan.router,
    prefix="/penyewaan",
    tags=["Penyewaan"]
)