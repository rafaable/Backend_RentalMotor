from pydantic import BaseModel
from typing import Optional

class CabangResponse(BaseModel):
    id_cabang: int
    nama_cabang: str
    alamat: str
    kota: str

    class Config:
        from_attributes = True

class CabangPatch(BaseModel):
    nama_cabang: Optional[str] = None
    alamat: Optional[str] = None
    kota: Optional[str] = None