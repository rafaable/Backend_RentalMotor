from fastapi import FastAPI
from app.routes import pengguna
from app.routes import cabang
from app.routes import penyewaan
from app.routes import pengembalian
from app.routes import karyawan
from app.routes import denda
from app.routes import kendaraan
from app.mongo import vehicle_condition, maintenance
from app.routes import pembayaran

app = FastAPI()

app.include_router(
    pengguna.router,
    prefix="/pengguna",
    tags=["Pengguna"]
)

app.include_router(
    cabang.router,
    prefix="/cabang",
    tags=["Cabang"]
)

app.include_router(
    penyewaan.router,
    prefix="/penyewaan",
    tags=["Penyewaan"]
)

app.include_router(
    pengembalian.router,
    prefix="/pengembalian",
    tags=["Pengembalian"]
)

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

app.include_router(
    vehicle_condition.router,
    prefix="/laporan-kondisi",
    tags=["Laporan Kondisi"]
)

app.include_router(
    maintenance.router,
    prefix="/maintenance",
    tags=["Maintenance"]
)


app.include_router(
    pembayaran.router,
    prefix="/pembayaran",
    tags=["Pembayaran"]
)