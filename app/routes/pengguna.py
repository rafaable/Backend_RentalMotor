from fastapi import APIRouter
from fastapi import Query
from fastapi import Body
from datetime import date
from app.core.sql_connection import get_connection
from app.schemas.pengguna_schema import PenggunaCreate
from app.schemas.pengguna_schema import PenggunaPatch

router = APIRouter()

@router.get("/")
def get_pengguna(
    id_pengguna: int = None,
    nama_lengkap: str = None,
    tahun_kadaluarsa: int = None,
    tahun_awal: int = None,
    tahun_akhir: int = None,
    status_verifikasi: str = None
):

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            query = """
                SELECT *
                FROM pengguna
                WHERE 1=1
            """

            params = []

            # Filter ID
            if id_pengguna is not None:
                query += " AND id_pengguna = %s"
                params.append(id_pengguna)

            # Filter nama LIKE
            if nama_lengkap:
                query += " AND nama_lengkap LIKE %s"
                params.append(f"%{nama_lengkap}%")

            # Filter tahun kadaluarsa
            if tahun_kadaluarsa:
                query += """
                    AND YEAR(tanggal_kadaluarsa_sim) = %s
                """
                params.append(tahun_kadaluarsa)

            # Filter rentang tahun
            if tahun_awal and tahun_akhir:

                if tahun_awal > tahun_akhir:
                    return {
                        "message": "Rentang tahun tidak valid"
                    }

                query += """
                    AND YEAR(tanggal_kadaluarsa_sim)
                    BETWEEN %s AND %s
                """

                params.append(tahun_awal)
                params.append(tahun_akhir)

            # Filter status
            if status_verifikasi:
                query += """
                    AND status_verifikasi = %s
                """
                params.append(status_verifikasi)

            cursor.execute(query, params)

            data = cursor.fetchall()

            if not data:

                if id_pengguna:
                    return {
                        "message": "ID tidak ditemukan"
                    }

                if nama_lengkap:
                    return {
                        "message": "Nama tidak ditemukan"
                    }

                if tahun_kadaluarsa:
                    return {
                        "message": "Tahun kadaluarsa tidak ditemukan"
                    }

                if tahun_awal and tahun_akhir:
                    return {
                        "message": "Data tidak ditemukan"
                    }

                if status_verifikasi:
                    return {
                        "message": "Status verifikasi tidak ditemukan"
                    }

                return {
                    "message": "Data pengguna kosong"
                }

            return data

    finally:
        conn.close()

@router.post("/")
def create_pengguna(data: PenggunaCreate):

    conn = get_connection()

    try:
        # VALIDASI FIELD KOSONG
        if (
            not data.kartu_identitas
            or not data.nomor_telepon
            or not data.nama_lengkap
            or not data.nomor_sim
            or not data.tanggal_kadaluarsa_sim
            or not data.status_verifikasi
        ):
            return {
                "message": "Masukkan informasi secara lengkap!"
            }

        # NAMA HANYA SPASI
        if not data.nama_lengkap.strip():
            return {
                "message": "Nama lengkap tidak valid!"
            }

        # KARTU IDENTITAS ANGKA
        if not data.kartu_identitas.isdigit():
            return {
                "message": "Kartu identitas harus berupa angka!"
            }

        # KARTU IDENTITAS 16 DIGIT
        if len(data.kartu_identitas) != 16:
            return {
                "message": "Kartu identitas harus 16 digit!"
            }

        # NOMOR SIM ANGKA
        if not data.nomor_sim.isdigit():
            return {
                "message": "Nomor SIM harus berupa angka!"
            }

        # NOMOR TELEPON ANGKA
        if not data.nomor_telepon.isdigit():
            return {
                "message": "Nomor telepon harus berupa angka!"
            }

        # NOMOR TELEPON 10-15 DIGIT
        if len(data.nomor_telepon) < 10 or len(data.nomor_telepon) > 15:
            return {
                "message": "Nomor telepon harus 10 sampai 15 digit!"
            }

        with conn.cursor() as cursor:

            # CEK DUPLIKAT KARTU IDENTITAS
            cursor.execute(
                """
                SELECT id_pengguna
                FROM pengguna
                WHERE kartu_identitas = %s
                """,
                (data.kartu_identitas,)
            )

            if cursor.fetchone():
                return {
                    "message": "Kartu identitas duplikat!"
                }

            # CEK DUPLIKAT NOMOR SIM
            cursor.execute(
                """
                SELECT id_pengguna
                FROM pengguna
                WHERE nomor_sim = %s
                """,
                (data.nomor_sim,)
            )

            if cursor.fetchone():
                return {
                    "message": "Nomor SIM duplikat!"
                }

            today = date.today()

            # TENTUKAN STATUS VERIFIKASI OTOMATIS
            status_verifikasi = data.status_verifikasi.value

            if data.tanggal_kadaluarsa_sim <= today:
                status_verifikasi = "expired"

            elif data.tanggal_kadaluarsa_sim > date(
                today.year + 5,
                today.month,
                today.day
            ):
                status_verifikasi = "ditolak"

            # INSERT DATA
            cursor.execute(
                """
                INSERT INTO pengguna
                (
                    kartu_identitas,
                    nomor_telepon,
                    nama_lengkap,
                    nomor_sim,
                    tanggal_kadaluarsa_sim,
                    status_verifikasi
                )
                VALUES
                (%s,%s,%s,%s,%s,%s)
                """,
                (
                    data.kartu_identitas,
                    data.nomor_telepon,
                    data.nama_lengkap.strip(),
                    data.nomor_sim,
                    data.tanggal_kadaluarsa_sim,
                    status_verifikasi
                )
            )

            conn.commit()

            if status_verifikasi == "expired":
                return {
                    "message": "Data pengguna berhasil ditambahkan, status : expired"
                }

            if status_verifikasi == "ditolak":
                return {
                    "message": "Data pengguna berhasil ditambahkan, status : ditolak"
                }

            return {
                "message": "Data pengguna berhasil ditambahkan"
            }

    finally:
        conn.close()


@router.patch("/{id_pengguna}")
def update_pengguna(
    id_pengguna: int,
    data: PenggunaPatch
):
    conn = get_connection()

    try:
        data = data.model_dump(exclude_none=True)
        with conn.cursor() as cursor:

            # CEK ID
            cursor.execute(
                """
                SELECT *
                FROM pengguna
                WHERE id_pengguna = %s
                """,
                (id_pengguna,)
            )

            pengguna = cursor.fetchone()

            if not pengguna:
                return {
                    "message": "ID not found"
                }

            # FIELD YANG BOLEH DIUPDATE
            allowed_fields = {
                "nomor_telepon",
                "nama_lengkap",
                "nomor_sim",
                "tanggal_kadaluarsa_sim",
                "status_verifikasi"
            }

            # CEK FIELD INVALID
            for field in data.keys():

                if field == "id_pengguna":
                    return {
                        "message": "field tidak valid"
                    }

                if field not in allowed_fields:
                    return {
                        "message": "field tidak valid"
                    }

            # VALIDASI ENUM
            valid_status = {
                "belum_diverifikasi",
                "terverifikasi",
                "ditolak",
                "expired"
            }

            # VALIDASI SATU PER SATU
            if "nomor_sim" in data:

                nomor_sim = str(data["nomor_sim"])

                if not nomor_sim.isdigit():
                    return {
                        "message": "Nomor SIM harus berupa angka!"
                    }

                cursor.execute(
                    """
                    SELECT id_pengguna
                    FROM pengguna
                    WHERE nomor_sim = %s
                    AND id_pengguna != %s
                    """,
                    (nomor_sim, id_pengguna)
                )

                if cursor.fetchone():
                    return {
                        "message": "Nomor SIM duplikat!"
                    }

            if "nama_lengkap" in data:

                nama_lengkap = str(data["nama_lengkap"])

                if not nama_lengkap.strip():
                    return {
                        "message": "Nama lengkap tidak valid!"
                    }

            if "nomor_telepon" in data:

                nomor_telepon = str(data["nomor_telepon"])

                if not nomor_telepon.isdigit():
                    return {
                        "message": "Nomor telepon harus berupa angka!"
                    }

                if len(nomor_telepon) < 10 or len(nomor_telepon) > 15:
                    return {
                        "message": "Nomor telepon harus 10 sampai 15 digit!"
                    }

            if "tanggal_kadaluarsa_sim" in data:

                try:

                    tanggal = date.fromisoformat(
                        str(data["tanggal_kadaluarsa_sim"])
                    )

                except ValueError:

                    return {
                        "message": "Masukkan format tanggal YYYY-MM-DD"
                    }

                today = date.today()

                max_date = date(
                    today.year + 5,
                    today.month,
                    today.day
                )

                if tanggal < today or tanggal > max_date:

                    return {
                        "message": "tanggal kadaluarsa tidak valid!"
                    }

            if "status_verifikasi" in data:

                if data["status_verifikasi"] not in valid_status:

                    return {
                        "message": "Status verifikasi tidak valid!"
                    }

            # BUILD QUERY DINAMIS

            update_fields = []
            values = []

            for key, value in data.items():

                update_fields.append(f"{key} = %s")
                values.append(value)

            values.append(id_pengguna)

            query = f"""
                UPDATE pengguna
                SET {', '.join(update_fields)}
                WHERE id_pengguna = %s
            """

            cursor.execute(query, values)

            conn.commit()

            return {
                "message": "Data pengguna berhasil diperbarui!"
            }

    finally:
        conn.close()

        
@router.delete("/{id_pengguna}")
def delete_pengguna(id_pengguna: int):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            # CEK ID ADA ATAU TIDAK

            cursor.execute(
                """
                SELECT id_pengguna
                FROM pengguna
                WHERE id_pengguna = %s
                """,
                (id_pengguna,)
            )

            pengguna = cursor.fetchone()

            if not pengguna:
                return {
                    "message": "Data not found"
                }

            # CEK RELASI KE PENYEWAAN

            cursor.execute(
                """
                SELECT id_penyewaan
                FROM penyewaan
                WHERE id_pengguna = %s
                LIMIT 1
                """,
                (id_pengguna,)
            )

            penyewaan = cursor.fetchone()

            if penyewaan:
                return {
                    "message": "Failed : Memiliki entri di tabel lain"
                }

            # DELETE

            cursor.execute(
                """
                DELETE FROM pengguna
                WHERE id_pengguna = %s
                """,
                (id_pengguna,)
            )

            conn.commit()

            return {
                "message": "Deleted"
            }

    finally:
        conn.close()