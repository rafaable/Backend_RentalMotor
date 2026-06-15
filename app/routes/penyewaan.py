from fastapi import APIRouter
from datetime import date
from app.core.sql_connection import get_connection
from app.schemas.penyewaan_schema import StatusPenyewaan

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

            # FILTER ID PENYEWAAN
            if id_penyewaan is not None:
                query += """
                    AND id_penyewaan = %s
                """
                params.append(id_penyewaan)

            # FILTER ID PENGGUNA
            if id_pengguna is not None:

                cursor.execute(
                    """
                    SELECT status_verifikasi
                    FROM pengguna
                    WHERE id_pengguna = %s
                    """,
                    (id_pengguna,)
                )

                pengguna = cursor.fetchone()

                if pengguna:

                    if (
                        pengguna["status_verifikasi"]
                        != "terverifikasi"
                    ):
                        return {
                            "message":
                            "Input gagal, pengguna belum terverifikasi"
                        }

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
                        "message": "Not found!"
                    }

                if id_pengguna:
                    return {
                        "message": "Not found!"
                    }

                if id_kendaraan:
                    return {
                        "message": "Not found!"
                    }

                if id_karyawan:
                    return {
                        "message": "Not found!"
                    }

                if (
                    waktu_kembali_down
                    and
                    waktu_kembali_up
                ):
                    return {
                        "message": "Not found!"
                    }

                if status_penyewaan:
                    return {
                        "message": "Not found!"
                    }

                return {
                    "message":
                    "Data penyewaan kosong"
                }

            return data

    finally:
        conn.close()