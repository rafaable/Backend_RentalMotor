from pydantic import BaseModel
from datetime import date
from enum import Enum


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