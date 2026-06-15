from pydantic import BaseModel
from datetime import date

from enum import Enum


class StatusPenyewaan(str, Enum):
    aktif = "aktif"
    selesai = "selesai"
    dibatalkan = "dibatalkan"

class PenyewaanCreate(BaseModel):
    id_pengguna: int
    id_kendaraan: int
    id_karyawan: int
    waktu_mulai: date
    waktu_selesai_rencana: date

class PenyewaanCreate(BaseModel):
    id_pengguna: int
    id_kendaraan: int
    id_karyawan: int
    waktu_mulai: str
    waktu_selesai_rencana: str
    status_penyewaan: str

from typing import Optional

class PenyewaanPatch(BaseModel):
    id_pengguna: Optional[int] = None
    id_kendaraan: Optional[int] = None
    id_karyawan: Optional[int] = None
    waktu_mulai: Optional[str] = None
    waktu_selesai_rencana: Optional[str] = None
    status_penyewaan: Optional[str] = None

