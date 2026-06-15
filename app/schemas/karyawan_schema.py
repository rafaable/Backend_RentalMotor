from enum import Enum
from pydantic import BaseModel
from typing import Optional

class JabatanEnum(str, Enum):
    branch_manager = "Branch Manager"
    staff_admin = "Staff Admin"
    supervisor = "Supervisor"

class KaryawanCreate(BaseModel):
    id_cabang: int
    nama_karyawan: str
    jabatan: JabatanEnum

class KaryawanUpdate(BaseModel):
    id_cabang: Optional[int] = None
    nama_karyawan: Optional[str] = None
    jabatan: Optional[JabatanEnum] = None