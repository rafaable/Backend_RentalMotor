from fastapi import APIRouter
from app.core.sql_connection import get_connection
from app.schemas.kendaraan_schema import StatusKendaraan, KendaraanCreate, KendaraanPatch
import datetime

router = APIRouter()

@router.get("/")
def get_kendaraan(
    id_kendaraan: int = None,
    id_cabang: int = None,
    merek: str = None,
    model: str = None,
    tahun: int = None,
    tahun_awal: int = None,
    tahun_akhir: int = None,
    nomor_polisi: str = None,
    tarif_min: float = None,
    tarif_max: float = None,
    status_kendaraan: StatusKendaraan = None
):
    # VALIDASI RENTANG TAHUN
    if tahun_awal is not None and tahun_akhir is not None:
        if tahun_awal > tahun_akhir:
            return {"message": "Rentang tahun tidak valid!"}

    # VALIDASI RENTANG TARIF
    if tarif_min is not None and tarif_max is not None:
        if tarif_min > tarif_max:
            return {"message": "Rentang tarif tidak valid!"}

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM kendaraan WHERE 1=1"
            params = []

            if id_kendaraan is not None:
                query += " AND id_kendaraan = %s"
                params.append(id_kendaraan)

            if id_cabang is not None:
                query += " AND id_cabang = %s"
                params.append(id_cabang)

            if merek:
                query += " AND merek LIKE %s"
                params.append(f"%{merek}%")

            if model:
                query += " AND model LIKE %s"
                params.append(f"%{model}%")

            if tahun is not None:
                query += " AND tahun = %s"
                params.append(tahun)

            if tahun_awal is not None and tahun_akhir is not None:
                query += " AND tahun BETWEEN %s AND %s"
                params.append(tahun_awal)
                params.append(tahun_akhir)

            if nomor_polisi:
                query += " AND nomor_polisi = %s"
                params.append(nomor_polisi)

            if tarif_min is not None and tarif_max is not None:
                query += " AND tarif_per_hari BETWEEN %s AND %s"
                params.append(tarif_min)
                params.append(tarif_max)

            if status_kendaraan is not None:
                query += " AND status_kendaraan = %s"
                params.append(status_kendaraan.value)

            cursor.execute(query, params)
            data = cursor.fetchall()

            if not data:
                if id_kendaraan is not None:
                    return {"message": "ID tidak ditemukan"}
                if id_cabang is not None:
                    return {"message": "Cabang tidak ditemukan"}
                if merek:
                    return {"message": "Merek tidak ditemukan"}
                if model:
                    return {"message": "Model tidak ditemukan"}
                if nomor_polisi:
                    return {"message": "Nomor polisi tidak ditemukan"}
                if tahun is not None:
                    return {"message": "Tidak ada kendaraan untuk tahun tersebut"}
                if tahun_awal is not None and tahun_akhir is not None:
                    return {"message": "Tidak ada kendaraan pada rentang tahun tersebut"}
                if tarif_min is not None and tarif_max is not None:
                    return {"message": "Tidak ada kendaraan pada rentang tarif tersebut"}
                if status_kendaraan is not None:
                    return {"message": "Tidak ada kendaraan dengan status tersebut"}
                return {"message": "Data kendaraan kosong"}

            return data
    finally:
        conn.close()


##  POST Kendaraan 
@router.post("/")
def create_kendaraan(data: KendaraanCreate):
    # VALIDASI FIELD KOSONG
    if (
        not data.merek
        or not data.model
        or not data.nomor_polisi
        or data.id_cabang is None
        or data.tahun is None
        or data.tarif_per_hari is None
        or data.status_kendaraan is None
    ):
        return {"message": "Masukkan informasi secara lengkap!"}

    # VALIDASI MEREK HANYA SPASI
    if not data.merek.strip():
        return {"message": "Merek tidak boleh kosong!"}

    # VALIDASI MODEL HANYA SPASI
    if not data.model.strip():
        return {"message": "Model tidak boleh kosong!"}

    # VALIDASI NOMOR POLISI HANYA SPASI
    if not data.nomor_polisi.strip():
        return {"message": "Nomor polisi tidak boleh kosong!"}

    # VALIDASI TAHUN
    tahun_sekarang = datetime.date.today().year
    if data.tahun < 1990 or data.tahun > tahun_sekarang:
        return {"message": "Tahun tidak valid!"}

    # VALIDASI TARIF POSITIF
    if data.tarif_per_hari <= 0:
        return {"message": "Tarif harus berupa angka positif!"}

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # CEK ID CABANG
            cursor.execute(
                "SELECT id_cabang FROM cabang WHERE id_cabang = %s",
                (data.id_cabang,)
            )
            if not cursor.fetchone():
                return {"message": "Cabang tidak ditemukan!"}

            # CEK DUPLIKAT NOMOR POLISI
            cursor.execute(
                "SELECT id_kendaraan FROM kendaraan WHERE nomor_polisi = %s",
                (data.nomor_polisi.strip(),)
            )
            if cursor.fetchone():
                return {"message": "Nomor polisi sudah terdaftar!"}

            # INSERT DATA
            cursor.execute(
                """
                INSERT INTO kendaraan
                (id_cabang, merek, model, tahun, nomor_polisi, tarif_per_hari, status_kendaraan)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data.id_cabang,
                    data.merek.strip(),
                    data.model.strip(),
                    data.tahun,
                    data.nomor_polisi.strip(),
                    data.tarif_per_hari,
                    data.status_kendaraan.value
                )
            )
            conn.commit()
            return {"message": "Data kendaraan berhasil ditambahkan!"}
    finally:
        conn.close()

##  PATCH Kendaraan 
@router.patch("/{id_kendaraan}")
def update_kendaraan(
    id_kendaraan: int,
    data: KendaraanPatch
):
    conn = get_connection()
    try:
        data = data.model_dump(exclude_none=True)

        with conn.cursor() as cursor:
            # CEK ID
            cursor.execute(
                "SELECT * FROM kendaraan WHERE id_kendaraan = %s",
                (id_kendaraan,)
            )
            if not cursor.fetchone():
                return {"message": "ID tidak ditemukan"}

            # FIELD YANG BOLEH DIUPDATE
            allowed_fields = {
                "id_cabang",
                "merek",
                "model",
                "tahun",
                "nomor_polisi",
                "tarif_per_hari",
                "status_kendaraan"
            }

            # CEK FIELD INVALID
            for field in data.keys():
                if field == "id_kendaraan":
                    return {"message": "Field tidak valid!"}
                if field not in allowed_fields:
                    return {"message": "Field tidak valid!"}

            tahun_sekarang = datetime.date.today().year
            valid_status = {"tersedia", "disewa", "dalam_perbaikan"}

            # VALIDASI PER FIELD
            if "merek" in data:
                if not str(data["merek"]).strip():
                    return {"message": "Merek tidak boleh kosong!"}

            if "model" in data:
                if not str(data["model"]).strip():
                    return {"message": "Model tidak boleh kosong!"}

            if "nomor_polisi" in data:
                nomor_polisi = str(data["nomor_polisi"]).strip()
                if not nomor_polisi:
                    return {"message": "Nomor polisi tidak boleh kosong!"}
                cursor.execute(
                    """
                    SELECT id_kendaraan FROM kendaraan
                    WHERE nomor_polisi = %s
                    AND id_kendaraan != %s
                    """,
                    (nomor_polisi, id_kendaraan)
                )
                if cursor.fetchone():
                    return {"message": "Nomor polisi sudah terdaftar!"}
                data["nomor_polisi"] = nomor_polisi

            if "tahun" in data:
                tahun = int(data["tahun"])
                if tahun < 1990 or tahun > tahun_sekarang:
                    return {"message": "Tahun tidak valid!"}

            if "tarif_per_hari" in data:
                if float(data["tarif_per_hari"]) <= 0:
                    return {"message": "Tarif harus berupa angka positif!"}

            if "status_kendaraan" in data:
                if data["status_kendaraan"] not in valid_status:
                    return {"message": "Status kendaraan tidak valid!"}

            if "id_cabang" in data:
                cursor.execute(
                    "SELECT id_cabang FROM cabang WHERE id_cabang = %s",
                    (data["id_cabang"],)
                )
                if not cursor.fetchone():
                    return {"message": "Cabang tidak ditemukan!"}

            # BUILD QUERY DINAMIS
            update_fields = []
            values = []
            for key, value in data.items():
                update_fields.append(f"{key} = %s")
                values.append(value)
            values.append(id_kendaraan)

            query = f"""
                UPDATE kendaraan
                SET {', '.join(update_fields)}
                WHERE id_kendaraan = %s
            """
            cursor.execute(query, values)
            conn.commit()
            return {"message": "Data kendaraan berhasil diperbarui!"}
    finally:
        conn.close()

## Delete Kendaraan 
@router.delete("/{id_kendaraan}")
def delete_kendaraan(id_kendaraan: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # CEK ID
            cursor.execute(
                "SELECT * FROM kendaraan WHERE id_kendaraan = %s",
                (id_kendaraan,)
            )
            if not cursor.fetchone():
                return {"message": "ID tidak ditemukan"}

            # CEK RELASI KE PENYEWAAN
            cursor.execute(
                """
                SELECT id_penyewaan FROM penyewaan
                WHERE id_kendaraan = %s
                """,
                (id_kendaraan,)
            )
            if cursor.fetchone():
                return {
                    "message": "Tidak bisa hapus kendaraan, masih ada data penyewaan terkait!"
                }

            # DELETE DATA
            cursor.execute(
                "DELETE FROM kendaraan WHERE id_kendaraan = %s",
                (id_kendaraan,)
            )
            conn.commit()
            return {"message": "Data kendaraan berhasil dihapus!"}
    finally:
        conn.close()
