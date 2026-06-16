from fastapi import APIRouter
from bson import ObjectId
from app.core.mongo_connection import db

router = APIRouter()

# GET


@router.get("/")
def get_laporan_kondisi(
    id_penyewaan: int = None,
    id_kendaraan: int = None,
    tipe: str = None,
    status_kondisi: str = None,
    tanggal_mulai: str = None,
    tanggal_selesai: str = None
):
    query = {}

    if id_penyewaan is not None:
        query["id_penyewaan"] = id_penyewaan
    if id_kendaraan is not None:
        query["id_kendaraan"] = id_kendaraan
    if tipe is not None:
        valid_tipe = {"check-in", "check-out"}
        if tipe not in valid_tipe:
            return {"message": "Tipe tidak valid! Gunakan 'check-in' atau 'check-out'"}
        query["tipe"] = tipe
    if status_kondisi is not None:
        valid_status = {"normal", "rusak"}
        if status_kondisi not in valid_status:
            return {"message": "Status kondisi tidak valid! Gunakan 'normal' atau 'rusak'"}
        query["kondisi"] = {"$elemMatch": {"status": status_kondisi}}
    if tanggal_mulai is not None:
        query["tanggal_mulai"] = tanggal_mulai
    if tanggal_selesai is not None:
        query["tanggal_selesai"] = tanggal_selesai

    data = list(db.laporan_kondisi.find(query, {"_id": 0}))

    if not data:
        if id_penyewaan is not None:
            return {"message": "Laporan dengan id_penyewaan tersebut tidak ditemukan"}
        if id_kendaraan is not None:
            return {"message": "Laporan dengan id_kendaraan tersebut tidak ditemukan"}
        if tipe is not None:
            return {"message": f"Laporan dengan tipe '{tipe}' tidak ditemukan"}
        if status_kondisi is not None:
            return {"message": f"Laporan dengan kondisi '{status_kondisi}' tidak ditemukan"}
        return {"message": "Data laporan kondisi kosong"}

    return data


# POST
@router.post("/")
def create_laporan_kondisi(data: dict):

    required_fields = ["id_penyewaan", "id_kendaraan",
                       "tipe", "tanggal_mulai", "tanggal_selesai", "kondisi"]
    for field in required_fields:
        if field not in data or data[field] is None:
            return {"message": f"Field '{field}' wajib diisi!"}

    valid_tipe = {"check-in", "check-out"}
    if data["tipe"] not in valid_tipe:
        return {"message": "Tipe tidak valid! Gunakan 'check-in' atau 'check-out'"}

    if not isinstance(data["id_penyewaan"], int):
        return {"message": "id_penyewaan harus berupa angka!"}
    if not isinstance(data["id_kendaraan"], int):
        return {"message": "id_kendaraan harus berupa angka!"}

    if not isinstance(data["kondisi"], list) or len(data["kondisi"]) == 0:
        return {"message": "Kondisi harus berupa list dan tidak boleh kosong!"}

    for item in data["kondisi"]:
        if "bagian" not in item or "status" not in item or "deskripsi" not in item:
            return {"message": "Setiap kondisi harus memiliki field 'bagian', 'status', dan 'deskripsi'"}
        if item["status"] not in {"normal", "rusak"}:
            return {"message": f"Status kondisi '{item['status']}' tidak valid! Gunakan 'normal' atau 'rusak'"}

    db.laporan_kondisi.insert_one(data)
    data.pop("_id", None)

    return {"message": "Laporan kondisi berhasil ditambahkan", "data": data}


# PATCH
@router.patch("/{id}")
def update_laporan_kondisi(id: str, data: dict):

    # VALIDASI ID FORMAT
    if not ObjectId.is_valid(id):
        return {"message": "Format ID tidak valid!"}

    # CEK ID ADA ATAU TIDAK
    existing = db.laporan_kondisi.find_one({"_id": ObjectId(id)})
    if not existing:
        return {"message": "Laporan kondisi tidak ditemukan!"}

    # FIELD YANG BOLEH DIUPDATE
    allowed_fields = {"tipe", "tanggal_mulai", "tanggal_selesai", "kondisi"}
    for field in data.keys():
        if field not in allowed_fields:
            return {"message": f"Field '{field}' tidak boleh diubah!"}

    # VALIDASI TIPE
    if "tipe" in data:
        if data["tipe"] not in {"check-in", "check-out"}:
            return {"message": "Tipe tidak valid! Gunakan 'check-in' atau 'check-out'"}

    # VALIDASI KONDISI
    if "kondisi" in data:
        if not isinstance(data["kondisi"], list) or len(data["kondisi"]) == 0:
            return {"message": "Kondisi harus berupa list dan tidak boleh kosong!"}
        for item in data["kondisi"]:
            if "bagian" not in item or "status" not in item or "deskripsi" not in item:
                return {"message": "Setiap kondisi harus memiliki field 'bagian', 'status', dan 'deskripsi'"}
            if item["status"] not in {"normal", "rusak"}:
                return {"message": f"Status '{item['status']}' tidak valid!"}

    db.laporan_kondisi.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )

    return {"message": "Laporan kondisi berhasil diperbarui!"}


# DELETE
@router.delete("/{id}")
def delete_laporan_kondisi(id: str):

    # VALIDASI ID FORMAT
    if not ObjectId.is_valid(id):
        return {"message": "Format ID tidak valid!"}

    # CEK ID ADA ATAU TIDAK
    existing = db.laporan_kondisi.find_one({"_id": ObjectId(id)})
    if not existing:
        return {"message": "Laporan kondisi tidak ditemukan!"}

    db.laporan_kondisi.delete_one({"_id": ObjectId(id)})

    return {"message": "Laporan kondisi berhasil dihapus!"}
