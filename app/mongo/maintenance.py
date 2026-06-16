from fastapi import APIRouter
from bson import ObjectId
from app.core.mongo_connection import db

router = APIRouter()

# GET


@router.get("/")
def get_maintenance(
    id_kendaraan: int = None,
    id_karyawan: int = None,
    jenis_maintenance: str = None,
    status: str = None,
    tanggal: str = None
):
    query = {}

    if id_kendaraan is not None:
        query["id_kendaraan"] = id_kendaraan
    if id_karyawan is not None:
        query["id_karyawan"] = id_karyawan
    if jenis_maintenance is not None:
        valid_jenis = {"servis_rutin", "perbaikan_berat", "pengecekan_berkala"}
        if jenis_maintenance not in valid_jenis:
            return {"message": "Jenis tidak valid! Gunakan 'servis_rutin', 'perbaikan_berat', atau 'pengecekan_berkala'"}
        query["jenis_maintenance"] = jenis_maintenance
    if status is not None:
        valid_status = {"selesai", "dalam_proses"}
        if status not in valid_status:
            return {"message": "Status tidak valid! Gunakan 'selesai' atau 'dalam_proses'"}
        query["status"] = status
    if tanggal is not None:
        query["tanggal"] = tanggal

    data = list(db.riwayat_maintenance.find(query, {"_id": 0}))

    if not data:
        if id_kendaraan is not None:
            return {"message": "Maintenance dengan id_kendaraan tersebut tidak ditemukan"}
        if id_karyawan is not None:
            return {"message": "Maintenance dengan id_karyawan tersebut tidak ditemukan"}
        if jenis_maintenance is not None:
            return {"message": f"Maintenance dengan jenis '{jenis_maintenance}' tidak ditemukan"}
        if status is not None:
            return {"message": f"Maintenance dengan status '{status}' tidak ditemukan"}
        return {"message": "Data maintenance kosong"}

    return data


# POST
@router.post("/")
def create_maintenance(data: dict):

    required_fields = ["id_kendaraan", "id_karyawan", "tanggal",
                       "jenis_maintenance", "status", "detail", "total_biaya"]
    for field in required_fields:
        if field not in data or data[field] is None:
            return {"message": f"Field '{field}' wajib diisi!"}

    if not isinstance(data["id_kendaraan"], int):
        return {"message": "id_kendaraan harus berupa angka!"}
    if not isinstance(data["id_karyawan"], int):
        return {"message": "id_karyawan harus berupa angka!"}

    valid_jenis = {"servis_rutin", "perbaikan_berat", "pengecekan_berkala"}
    if data["jenis_maintenance"] not in valid_jenis:
        return {"message": "Jenis tidak valid! Gunakan 'servis_rutin', 'perbaikan_berat', atau 'pengecekan_berkala'"}

    valid_status = {"selesai", "dalam_proses"}
    if data["status"] not in valid_status:
        return {"message": "Status tidak valid! Gunakan 'selesai' atau 'dalam_proses'"}

    if not isinstance(data["total_biaya"], (int, float)) or data["total_biaya"] < 0:
        return {"message": "total_biaya harus berupa angka positif!"}

    if not isinstance(data["detail"], list) or len(data["detail"]) == 0:
        return {"message": "Detail harus berupa list dan tidak boleh kosong!"}

    for item in data["detail"]:
        if "komponen" not in item or "tindakan" not in item or "keterangan" not in item or "biaya" not in item:
            return {"message": "Setiap detail harus memiliki field 'komponen', 'tindakan', 'keterangan', dan 'biaya'"}
        if not isinstance(item["biaya"], (int, float)) or item["biaya"] < 0:
            return {"message": f"Biaya untuk '{item['komponen']}' harus berupa angka positif!"}

    db.riwayat_maintenance.insert_one(data)
    data.pop("_id", None)

    return {"message": "Data maintenance berhasil ditambahkan", "data": data}


# PATCH
@router.patch("/{id}")
def update_maintenance(id: str, data: dict):

    if not ObjectId.is_valid(id):
        return {"message": "Format ID tidak valid!"}

    existing = db.riwayat_maintenance.find_one({"_id": ObjectId(id)})
    if not existing:
        return {"message": "Data maintenance tidak ditemukan!"}

    allowed_fields = {"tanggal", "jenis_maintenance",
                      "status", "detail", "total_biaya", "catatan_tambahan"}
    for field in data.keys():
        if field not in allowed_fields:
            return {"message": f"Field '{field}' tidak boleh diubah!"}

    if "jenis_maintenance" in data:
        if data["jenis_maintenance"] not in {"servis_rutin", "perbaikan_berat", "pengecekan_berkala"}:
            return {"message": "Jenis tidak valid!"}

    if "status" in data:
        if data["status"] not in {"selesai", "dalam_proses"}:
            return {"message": "Status tidak valid! Gunakan 'selesai' atau 'dalam_proses'"}

    if "total_biaya" in data:
        if not isinstance(data["total_biaya"], (int, float)) or data["total_biaya"] < 0:
            return {"message": "total_biaya harus berupa angka positif!"}

    if "detail" in data:
        if not isinstance(data["detail"], list) or len(data["detail"]) == 0:
            return {"message": "Detail harus berupa list dan tidak boleh kosong!"}
        for item in data["detail"]:
            if "komponen" not in item or "tindakan" not in item or "keterangan" not in item or "biaya" not in item:
                return {"message": "Setiap detail harus memiliki field 'komponen', 'tindakan', 'keterangan', dan 'biaya'"}

    db.riwayat_maintenance.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )

    return {"message": "Data maintenance berhasil diperbarui!"}


# DELETE
@router.delete("/{id}")
def delete_maintenance(id: str):

    if not ObjectId.is_valid(id):
        return {"message": "Format ID tidak valid!"}

    existing = db.riwayat_maintenance.find_one({"_id": ObjectId(id)})
    if not existing:
        return {"message": "Data maintenance tidak ditemukan!"}

    db.riwayat_maintenance.delete_one({"_id": ObjectId(id)})

    return {"message": "Data maintenance berhasil dihapus!"}
