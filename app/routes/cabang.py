from fastapi import APIRouter, Query, Body
from app.core.sql_connection import get_connection

router = APIRouter(prefix="/cabang", tags=["Cabang"])


@router.get("/")
def get_cabang(
    id_cabang: int = None,
    kota: str = None
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            query = """
                SELECT *
                FROM cabang
                WHERE 1=1
            """

            params = []

            # filter id
            if id_cabang is not None:
                query += " AND id_cabang = %s"
                params.append(id_cabang)

            # filter kota
            if kota:
                query += " AND kota = %s"
                params.append(kota)

            cursor.execute(query, params)
            data = cursor.fetchall()

            if not data:

                if id_cabang:
                    return {"message": "id not found"}

                if kota:
                    return {"message": "Not found!"}

                return {"message": "data pengguna kosong"}

            return data

    finally:
        conn.close()
        
@router.post("/")
def create_cabang(
    nama_cabang: str = Body(...),
    alamat: str = Body(...),
    kota: str = Body(...)
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # 1. VALIDASI EMPTY / SPASI
            if (
                not nama_cabang or not alamat or not kota or
                nama_cabang.strip() == "" or
                alamat.strip() == "" or
                kota.strip() == ""
            ):
                return {
                    "message": "Masukkan informasi secara lengkap!"
                }

            nama_cabang = nama_cabang.strip()
            alamat = alamat.strip()
            kota = kota.strip()

            # 2. CEK DUPLIKAT (nama + kota)
            cursor.execute("""
                SELECT id_cabang
                FROM cabang
                WHERE nama_cabang = %s AND kota = %s
            """, (nama_cabang, kota))

            existing = cursor.fetchone()

            if existing:
                return {
                    "message": "Nama cabang di kota tersebut sudah terdaftar!"
                }

            # 3. INSERT DATA
            cursor.execute("""
                INSERT INTO cabang (nama_cabang, alamat, kota)
                VALUES (%s, %s, %s)
            """, (nama_cabang, alamat, kota))

            conn.commit()

            return {
                "message": "Cabang berhasil ditambahkan",
                "data": {
                    "nama_cabang": nama_cabang,
                    "alamat": alamat,
                    "kota": kota
                }
            }

    finally:
        conn.close()