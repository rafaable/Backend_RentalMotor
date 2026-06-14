from pydantic import BaseModel

class CabangResponse(BaseModel):
    id_cabang: int
    nama_cabang: str
    alamat: str
    kota: str

    class Config:
        from_attributes = True