from pydantic import BaseModel
from datetime import date


class PengembalianCreate(BaseModel):
    id_penyewaan: int
    id_karyawan: int
    waktu_pengembalian: date
    kondisi_kendaraan: str

from typing import Optional


class PengembalianPatch(BaseModel):
    id_karyawan: Optional[int] = None
    kondisi_kendaraan: Optional[str] = None