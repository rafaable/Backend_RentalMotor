from pydantic import BaseModel
from typing import Optional
from enum import Enum


class AlasanDendaGet(str, Enum):
    kerusakan_kendaraan = "kerusakan_kendaraan"
    pelanggaran_lalu_lintas = "pelanggaran_lalu_lintas"
    keterlambatan_pengembalian = "keterlambatan_pengembalian"


class AlasanDendaManual(str, Enum):
    kerusakan_kendaraan = "kerusakan_kendaraan"
    pelanggaran_lalu_lintas = "pelanggaran_lalu_lintas"


class DendaCreate(BaseModel):
    id_pengembalian: int
    id_karyawan: int
    alasan_denda: AlasanDendaManual
    nominal_denda: float
    keterangan: Optional[str] = None


class DendaPatch(BaseModel):
    id_karyawan: Optional[int] = None
    alasan_denda: Optional[AlasanDendaManual] = None
    nominal_denda: Optional[float] = None
    keterangan: Optional[str] = None