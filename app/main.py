from fastapi import FastAPI
from app.routes import pengguna
from app.routes import cabang

app = FastAPI()

app.include_router(
    pengguna.router,
    prefix="/pengguna",
    tags=["Pengguna"]
)

app.include_router(cabang.router)