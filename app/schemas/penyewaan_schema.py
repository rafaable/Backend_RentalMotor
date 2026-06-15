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

