from fastapi import FastAPI
from app.routes import pengguna

app = FastAPI()

app.include_router(
    pengguna.router,
    prefix="/pengguna",
    tags=["Pengguna"]
)