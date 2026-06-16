from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class MetodePembayaran(str, Enum):
    transfer_bank = "transfer_bank"
    qris = "qris"
    tunai = "tunai"
    kartu_debit = "kartu_debit"
    kartu_kredit = "kartu_kredit"


class StatusPembayaran(str, Enum):
    lunas = "lunas"
    gagal = "gagal"


class PembayaranCreate(BaseModel):
    id_penyewaan: int
    tanggal_transaksi: date
    metode_pembayaran: MetodePembayaran
    status_pembayaran: StatusPembayaran

class PembayaranPatch(BaseModel):
    tanggal_transaksi: Optional[str] = None
    metode_pembayaran: Optional[str] = None
    status_pembayaran: Optional[str] = None