from fastapi import APIRouter
from datetime import date
from app.core.sql_connection import get_connection
from app.schemas.penyewaan_schema import StatusPenyewaan
from app.schemas.penyewaan_schema import PenyewaanCreate
from app.schemas.penyewaan_schema import PenyewaanPatch

router = APIRouter()


@router.get("/")
def get_penyewaan(
    id_penyewaan: int = None,
    id_pengguna: int = None,
    id_kendaraan: int = None,
    id_karyawan: int = None,
    waktu_kembali_down: date = None,
    waktu_kembali_up: date = None,
    status_penyewaan: StatusPenyewaan | None = None
):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            query = """
                SELECT *
                FROM penyewaan
                WHERE 1=1
            """

            params = []

            # FILTER ID PENGGUNA
            if id_pengguna is not None:
                
                query += """
                    AND id_pengguna = %s
                """
                params.append(id_pengguna)

            # FILTER ID KENDARAAN
            if id_kendaraan is not None:
                query += """
                    AND id_kendaraan = %s
                """
                params.append(id_kendaraan)

            # FILTER ID KARYAWAN
            if id_karyawan is not None:
                query += """
                    AND id_karyawan = %s
                """
                params.append(id_karyawan)

            # FILTER RANGE TANGGAL
            if (
                waktu_kembali_down is not None
                and
                waktu_kembali_up is not None
            ):

                if waktu_kembali_down > waktu_kembali_up:
                    return {
                        "message":
                        "Rentang tanggal tidak valid"
                    }

                query += """
                    AND waktu_selesai_rencana
                    BETWEEN %s AND %s
                """

                params.append(waktu_kembali_down)
                params.append(waktu_kembali_up)

            # FILTER STATUS
            if status_penyewaan:

                query += """
                    AND status_penyewaan = %s
                """

                params.append(status_penyewaan)

            cursor.execute(query, params)

            data = cursor.fetchall()

            if not data:

                if id_penyewaan:
                    return {
                        "message": "id penyewaan not found!"
                    }

                if id_pengguna:
                    return {
                        "message": "id pengguna not found!"
                    }

                if id_kendaraan:
                    return {
                        "message": "id kendaraan not found!"
                    }

                if id_karyawan:
                    return {
                        "message": "id karyawan not found!"
                    }

                if (
                    waktu_kembali_down
                    and
                    waktu_kembali_up
                ):
                    return {
                        "message": "date range not found!"
                    }

                if status_penyewaan:
                    return {
                        "message": "status not found!"
                    }

                return {
                    "message":
                    "Data penyewaan kosong"
                }

            return data

    finally:
        conn.close()

@router.post("/")
def create_penyewaan(data: PenyewaanCreate):

    conn = get_connection()

    try:

        # VALIDASI FIELD KOSONG
        if (
            data.id_pengguna is None
            or data.id_kendaraan is None
            or data.id_karyawan is None
            or not str(data.waktu_mulai).strip()
            or not str(data.waktu_selesai_rencana).strip()
            or not str(data.status_penyewaan).strip()
        ):
            return {
                "message": "Masukkan informasi secara lengkap!"
            }

        # VALIDASI FORMAT TANGGAL
        try:

            waktu_mulai = date.fromisoformat(
                data.waktu_mulai
            )

            waktu_selesai_rencana = date.fromisoformat(
                data.waktu_selesai_rencana
            )

        except ValueError:

            return {
                "message": "Gunakan format YYYY-MM-DD"
            }

        # VALIDASI RENTANG TANGGAL
        if waktu_mulai > waktu_selesai_rencana:

            return {
                "message": "Rentang tanggal tidak valid!"
            }

        # VALIDASI STATUS
        if data.status_penyewaan != "aktif":

            return {
                "message": "Status penyewaan harus aktif"
            }

        with conn.cursor() as cursor:

            # CEK PENGGUNA
            cursor.execute(
                """
                SELECT *
                FROM pengguna
                WHERE id_pengguna = %s
                """,
                (data.id_pengguna,)
            )

            pengguna = cursor.fetchone()

            if not pengguna:

                return {
                    "message": "Pengguna tidak terdaftar"
                }

            # CEK STATUS VERIFIKASI
            if (
                pengguna["status_verifikasi"]
                != "terverifikasi"
            ):

                return {
                    "message": "Pengguna tidak terverifikasi"
                }

            # CEK PENYEWAAN AKTIF
            cursor.execute(
                """
                SELECT id_penyewaan
                FROM penyewaan
                WHERE id_pengguna = %s
                AND status_penyewaan = 'aktif'
                """,
                (data.id_pengguna,)
            )

            if cursor.fetchone():

                return {
                    "message":
                    "Pengguna masih memiliki penyewaan aktif"
                }

            # CEK KENDARAAN
            cursor.execute(
                """
                SELECT *
                FROM kendaraan
                WHERE id_kendaraan = %s
                """,
                (data.id_kendaraan,)
            )

            kendaraan = cursor.fetchone()

            if not kendaraan:

                return {
                    "message": "Kendaraan tidak tersedia!"
                }

            if (
                kendaraan["status_kendaraan"]
                != "tersedia"
            ):

                return {
                    "message": "Kendaraan tidak tersedia!"
                }

            # CEK KARYAWAN
            cursor.execute(
                """
                SELECT *
                FROM karyawan
                WHERE id_karyawan = %s
                """,
                (data.id_karyawan,)
            )

            karyawan = cursor.fetchone()

            if not karyawan:

                return {
                    "message": "Karyawan tidak terdaftar"
                }

            # CEK CABANG KARYAWAN & KENDARAAN
            if (
                kendaraan["id_cabang"]
                !=
                karyawan["id_cabang"]
            ):

                return {
                    "message":
                    "Karyawan dan kendaraan tidak berasal dari cabang yang sama!"
                }

            # INSERT
            cursor.execute(
                """
                INSERT INTO penyewaan
                (
                    id_pengguna,
                    id_kendaraan,
                    id_karyawan,
                    waktu_mulai,
                    waktu_selesai_rencana,
                    status_penyewaan
                )
                VALUES
                (%s,%s,%s,%s,%s,%s)
                """,
                (
                    data.id_pengguna,
                    data.id_kendaraan,
                    data.id_karyawan,
                    waktu_mulai,
                    waktu_selesai_rencana,
                    data.status_penyewaan
                )
            )

            # UBAH STATUS KENDARAAN MENJADI DISEWA
            cursor.execute(
                """
                UPDATE kendaraan
                SET status_kendaraan = 'disewa'
                WHERE id_kendaraan = %s
                """,
                (data.id_kendaraan,)
            )

            conn.commit()

            return {
                "message":
                "Data penyewaan berhasil ditambahkan"
            }

    finally:
        conn.close()

@router.patch("/{id_penyewaan}")
def update_penyewaan(
    id_penyewaan: int,
    data: PenyewaanPatch
):

    conn = get_connection()

    try:

        data = data.model_dump(exclude_none=True)

        with conn.cursor() as cursor:

            # CEK ID PENYEWAAN
            cursor.execute(
                """
                SELECT *
                FROM penyewaan
                WHERE id_penyewaan = %s
                """,
                (id_penyewaan,)
            )

            penyewaan = cursor.fetchone()

            if not penyewaan:

                return {
                    "message": "id not found"
                }

            # STATUS SELESAI TIDAK BOLEH DIUBAH
            if (
                penyewaan["status_penyewaan"]
                == "selesai"
            ):

                return {
                    "message":
                    "Status penyewaan yang sudah selesai tidak dapat diubah"
                }

            # ID PENYEWAAN TIDAK BOLEH DIUBAH
            if "id_penyewaan" in data:

                return {
                    "message":
                    "id_penyewaan tidak boleh diubah!"
                }

            # VALIDASI FIELD
            allowed_fields = {
                "id_pengguna",
                "id_kendaraan",
                "id_karyawan",
                "waktu_mulai",
                "waktu_selesai_rencana",
                "status_penyewaan"
            }

            for field in data.keys():

                if field not in allowed_fields:

                    return {
                        "message":
                        "field tidak valid"
                    }

            # VALIDASI ID PENGGUNA
            if "id_pengguna" in data:

                cursor.execute(
                    """
                    SELECT *
                    FROM pengguna
                    WHERE id_pengguna = %s
                    """,
                    (data["id_pengguna"],)
                )

                pengguna = cursor.fetchone()

                if not pengguna:

                    return {
                        "message":
                        "id_pengguna tidak terdaftar!"
                    }

                if (
                    pengguna["status_verifikasi"]
                    != "terverifikasi"
                ):

                    return {
                        "message":
                        "Pengguna tidak terverifikasi"
                    }

            # VALIDASI ID KENDARAAN
            if "id_kendaraan" in data:

                cursor.execute(
                    """
                    SELECT *
                    FROM kendaraan
                    WHERE id_kendaraan = %s
                    """,
                    (data["id_kendaraan"],)
                )

                kendaraan = cursor.fetchone()

                if not kendaraan:

                    return {
                        "message":
                        "id_kendaraan tidak terdapat dalam entri!"
                    }

                if (
                    kendaraan["status_kendaraan"]
                    != "tersedia"
                ):

                    return {
                        "message":
                        "Kendaraan tidak tersedia!"
                    }

            # VALIDASI ID KARYAWAN
            if "id_karyawan" in data:

                cursor.execute(
                    """
                    SELECT *
                    FROM karyawan
                    WHERE id_karyawan = %s
                    """,
                    (data["id_karyawan"],)
                )

                karyawan = cursor.fetchone()

                if not karyawan:

                    return {
                        "message":
                        "id_karyawan tidak terdapat dalam entri!"
                    }

            # VALIDASI FORMAT TANGGAL
            if "waktu_mulai" in data:

                try:

                    date.fromisoformat(
                        str(data["waktu_mulai"])
                    )

                except ValueError:

                    return {
                        "message":
                        "Gunakan format YYYY-MM-DD"
                    }

            if "waktu_selesai_rencana" in data:

                try:

                    date.fromisoformat(
                        str(
                            data[
                                "waktu_selesai_rencana"
                            ]
                        )
                    )

                except ValueError:

                    return {
                        "message":
                        "Gunakan format YYYY-MM-DD"
                    }

            # VALIDASI RENTANG TANGGAL
            waktu_mulai = date.fromisoformat(
                str(
                    data.get(
                        "waktu_mulai",
                        penyewaan["waktu_mulai"]
                    )
                )
            )

            waktu_selesai = date.fromisoformat(
                str(
                    data.get(
                        "waktu_selesai_rencana",
                        penyewaan[
                            "waktu_selesai_rencana"
                        ]
                    )
                )
            )

            if waktu_mulai > waktu_selesai:

                return {
                    "message":
                    "Rentang tanggal tidak valid!"
                }

            # VALIDASI STATUS PENYEWAAN
            if "status_penyewaan" in data:

                valid_status = {
                    "aktif",
                    "dibatalkan"
                }

                if (
                    data["status_penyewaan"]
                    not in valid_status
                ):

                    return {
                        "message":
                        "Pilih salah satu dari status penyewaan berikut : aktif, dibatalkan"
                    }

            # VALIDASI CABANG
            kendaraan_id = data.get(
                "id_kendaraan",
                penyewaan["id_kendaraan"]
            )

            karyawan_id = data.get(
                "id_karyawan",
                penyewaan["id_karyawan"]
            )

            cursor.execute(
                """
                SELECT id_cabang
                FROM kendaraan
                WHERE id_kendaraan = %s
                """,
                (kendaraan_id,)
            )

            kendaraan_cabang = cursor.fetchone()

            cursor.execute(
                """
                SELECT id_cabang
                FROM karyawan
                WHERE id_karyawan = %s
                """,
                (karyawan_id,)
            )

            karyawan_cabang = cursor.fetchone()

            if (
                kendaraan_cabang["id_cabang"]
                !=
                karyawan_cabang["id_cabang"]
            ):

                return {
                    "message":
                    "Karyawan dan kendaraan tidak berasal dari cabang yang sama!"
                }

            # BUILD QUERY DINAMIS
            update_fields = []
            values = []

            for key, value in data.items():

                update_fields.append(
                    f"{key} = %s"
                )

                values.append(value)

            values.append(id_penyewaan)

            query = f"""
                UPDATE penyewaan
                SET {', '.join(update_fields)}
                WHERE id_penyewaan = %s
            """

            cursor.execute(
                query,
                values
            )

            conn.commit()

            return {
                "message":
                "Data penyewaan berhasil diperbarui!"
            }

    finally:

        conn.close()


@router.delete("/{id_penyewaan}")
def delete_penyewaan(id_penyewaan: int):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            # CEK ID PENYEWAAN
            cursor.execute(
                """
                SELECT *
                FROM penyewaan
                WHERE id_penyewaan = %s
                """,
                (id_penyewaan,)
            )

            penyewaan = cursor.fetchone()

            if not penyewaan:

                return {
                    "message": "ID not found"
                }

            # CEK PENGEMBALIAN TERKAIT
            cursor.execute(
                """
                SELECT id_pengembalian
                FROM pengembalian
                WHERE id_penyewaan = %s
                LIMIT 1
                """,
                (id_penyewaan,)
            )

            if cursor.fetchone():

                return {
                    "message":
                    "Tidak bisa hapus penyewaan, masih ada pengembalian terkait!"
                }

            # CEK PEMBAYARAN TERKAIT
            cursor.execute(
                """
                SELECT id_pembayaran
                FROM pembayaran
                WHERE id_penyewaan = %s
                LIMIT 1
                """,
                (id_penyewaan,)
            )

            if cursor.fetchone():

                return {
                    "message":
                    "Tidak bisa hapus penyewaan, masih ada pembayaran terkait!"
                }

            # HAPUS DATA
            cursor.execute(
                """
                DELETE FROM penyewaan
                WHERE id_penyewaan = %s
                """,
                (id_penyewaan,)
            )

            conn.commit()

            return {
                "message":
                "Data penyewaan berhasil dihapus!"
            }

    finally:

        conn.close()