from fastapi import APIRouter
from app.core.mongo_connection import db

router = APIRouter()

# GET log aktivitas


@router.get("/")
def get_log_aktivitas(
    aksi: str = None,
    id_karyawan: int = None,
    tipe_karyawan: str = None,
    tanggal: str = None,
    ada_denda: bool = None
):
    query = {}

    if aksi is not None:
        valid_aksi = {"verifikasi_sim",
                      "proses_pembayaran", "proses_pengembalian"}
        if aksi not in valid_aksi:
            return {"message": "Aksi tidak valid! Gunakan 'verifikasi_sim', 'proses_pembayaran', atau 'proses_pengembalian'"}
        query["aksi"] = aksi

    if id_karyawan is not None:
        query["dilakukan_oleh.id"] = id_karyawan

    if tipe_karyawan is not None:
        valid_tipe = {"Staff Admin", "Supervisor", "Branch Manager"}
        if tipe_karyawan not in valid_tipe:
            return {"message": "Tipe karyawan tidak valid! Gunakan 'Staff Admin', 'Supervisor', atau 'Branch Manager'"}
        query["dilakukan_oleh.tipe"] = tipe_karyawan

    if tanggal is not None:
        query["tanggal"] = tanggal

    if ada_denda is not None:
        query["detail.ada_denda"] = ada_denda

    data = list(db.log_aktivitas.find(query, {"_id": 0}))

    if not data:
        if aksi is not None:
            return {"message": f"Log dengan aksi '{aksi}' tidak ditemukan"}
        if id_karyawan is not None:
            return {"message": "Log dengan id_karyawan tersebut tidak ditemukan"}
        if tanggal is not None:
            return {"message": f"Log pada tanggal '{tanggal}' tidak ditemukan"}
        if ada_denda is not None:
            return {"message": "Log dengan filter denda tersebut tidak ditemukan"}
        return {"message": "Data log aktivitas kosong"}

    return data


# POST log aktivitas baru
@router.post("/")
def create_log_aktivitas(data: dict):

    # VALIDASI FIELD WAJIB
    required_fields = ["tanggal", "dilakukan_oleh", "aksi", "detail"]
    for field in required_fields:
        if field not in data or data[field] is None:
            return {"message": f"Field '{field}' wajib diisi!"}

    # VALIDASI AKSI
    valid_aksi = {"verifikasi_sim", "proses_pembayaran", "proses_pengembalian"}
    if data["aksi"] not in valid_aksi:
        return {"message": "Aksi tidak valid! Gunakan 'verifikasi_sim', 'proses_pembayaran', atau 'proses_pengembalian'"}

    # VALIDASI DILAKUKAN OLEH
    if "id" not in data["dilakukan_oleh"] or "tipe" not in data["dilakukan_oleh"]:
        return {"message": "Field 'dilakukan_oleh' harus memiliki 'id' dan 'tipe'"}

    if not isinstance(data["dilakukan_oleh"]["id"], int):
        return {"message": "id karyawan harus berupa angka!"}

    valid_tipe = {"Staff Admin", "Supervisor", "Branch Manager"}
    if data["dilakukan_oleh"]["tipe"] not in valid_tipe:
        return {"message": "Tipe karyawan tidak valid! Gunakan 'Staff Admin', 'Supervisor', atau 'Branch Manager'"}

    # VALIDASI DETAIL HARUS DICT
    if not isinstance(data["detail"], dict):
        return {"message": "Detail harus berupa object/dictionary!"}

    db.log_aktivitas.insert_one(data)
    data.pop("_id", None)

    return {"message": "Log aktivitas berhasil ditambahkan", "data": data}
