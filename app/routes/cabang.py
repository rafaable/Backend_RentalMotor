from fastapi import APIRouter, Query, Body
from app.core.sql_connection import get_connection
from app.schemas.cabang_schema import CabangPatch

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


@router.patch("/{id_cabang}")
def update_cabang(
    id_cabang: int,
    data: CabangPatch
):

    conn = get_connection()

    try:
        data = data.model_dump(exclude_none=True)

        with conn.cursor() as cursor:

            # CEK ID
            cursor.execute(
                """
                SELECT *
                FROM cabang
                WHERE id_cabang = %s
                """,
                (id_cabang,)
            )

            cabang = cursor.fetchone()

            if not cabang:
                return {
                    "message": "ID not found"
                }

            # FIELD YANG BOLEH DIUPDATE
            allowed_fields = {
                "nama_cabang",
                "alamat",
                "kota"
            }

            # CEK FIELD INVALID
            for field in data.keys():

                if field == "id_cabang":
                    return {
                        "message": "field tidak valid"
                    }

                if field not in allowed_fields:
                    return {
                        "message": "field tidak valid"
                    }

            # VALIDASI SATU PER SATU
            if "nama_cabang" in data:

                nama_cabang = str(data["nama_cabang"])

                if not nama_cabang.strip():
                    return {
                        "message": "Nama cabang tidak valid!"
                    }

                if len(nama_cabang) > 100:
                    return {
                        "message": "Nama cabang terlalu panjang!"
                    }

            if "alamat" in data:

                alamat = str(data["alamat"])

                if not alamat.strip():
                    return {
                        "message": "Alamat tidak valid!"
                    }

            if "kota" in data:

                kota = str(data["kota"])

                if not kota.strip():
                    return {
                        "message": "Kota tidak valid!"
                    }

                if len(kota) > 50:
                    return {
                        "message": "Nama kota terlalu panjang!"
                    }

            # BUILD QUERY DINAMIS

            update_fields = []
            values = []

            for key, value in data.items():

                update_fields.append(f"{key} = %s")
                values.append(value)

            values.append(id_cabang)

            query = f"""
                UPDATE cabang
                SET {', '.join(update_fields)}
                WHERE id_cabang = %s
            """

            cursor.execute(query, values)

            conn.commit()

            return {
                "message": "Data cabang berhasil diperbarui!"
            }

    finally:
        conn.close()


@router.delete("/{id_cabang}")
def delete_cabang(id_cabang: int):

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # CEK ID
            cursor.execute(
                """
                SELECT *
                FROM cabang
                WHERE id_cabang = %s
                """,
                (id_cabang,)
            )

            cabang = cursor.fetchone()

            if not cabang:
                return {
                    "message": "ID not found"
                }

            # CEK RELASI KE KARYAWAN
            cursor.execute(
                """
                SELECT id_karyawan
                FROM karyawan
                WHERE id_cabang = %s
                """,
                (id_cabang,)
            )

            if cursor.fetchone():
                return {
                    "message": "Tidak bisa hapus cabang, masih ada karyawan terkait!"
                }

            # CEK RELASI KE KENDARAAN
            cursor.execute(
                """
                SELECT id_kendaraan
                FROM kendaraan
                WHERE id_cabang = %s
                """,
                (id_cabang,)
            )

            if cursor.fetchone():
                return {
                    "message": "Tidak bisa hapus cabang, masih ada kendaraan terkait!"
                }

            # DELETE DATA
            cursor.execute(
                """
                DELETE FROM cabang
                WHERE id_cabang = %s
                """,
                (id_cabang,)
            )

            conn.commit()

            return {
                "message": "Data cabang berhasil dihapus!"
            }

    finally:
        conn.close()