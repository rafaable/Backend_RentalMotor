from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class StatusVerifikasi(str, Enum):
    belum_diverifikasi = "belum_diverifikasi"
    terverifikasi = "terverifikasi"
    ditolak = "ditolak"
    expired = "expired"


class PenggunaCreate(BaseModel):
    kartu_identitas: str
    nomor_telepon: str
    nama_lengkap: str
    nomor_sim: str
    tanggal_kadaluarsa_sim: date
    status_verifikasi: StatusVerifikasi

class PenggunaPatch(BaseModel):
    nomor_telepon: Optional[str] = None
    nama_lengkap: Optional[str] = None
    nomor_sim: Optional[str] = None
    tanggal_kadaluarsa_sim: Optional[str] = None
    status_verifikasi: Optional[str] = None