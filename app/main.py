from fastapi import FastAPI
from app.routes import pengguna
from app.routes import cabang
from app.routes import penyewaan
from app.routes import karyawan
from app.routes import denda
from app.routes import kendaraan

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
app.include_router(cabang.router)

app.include_router(
    karyawan.router,
    prefix="/karyawan",
    tags=["Karyawan"]
)

app.include_router(
    denda.router,
    prefix="/denda",
    tags=["Denda"]
)

app.include_router(
    kendaraan.router,
    prefix="/kendaraan",
    tags=["Kendaraan"]
)