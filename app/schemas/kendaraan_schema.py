from pydantic import BaseModel
from typing import Optional
from enum import Enum

class StatusKendaraan(str, Enum):
    tersedia = "tersedia"
    disewa = "disewa"
    dalam_perbaikan = "dalam_perbaikan"

class KendaraanCreate(BaseModel):
    id_cabang: int
    merek: str
    model: str
    tahun: int
    nomor_polisi: str
    tarif_per_hari: float
    status_kendaraan: StatusKendaraan

class KendaraanPatch(BaseModel):
    id_cabang: Optional[int] = None
    merek: Optional[str] = None
    model: Optional[str] = None
    tahun: Optional[int] = None
    nomor_polisi: Optional[str] = None
    tarif_per_hari: Optional[float] = None
    status_kendaraan: Optional[str] = None