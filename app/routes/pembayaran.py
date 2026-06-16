from fastapi import APIRouter
from datetime import date
from app.schemas.pembayaran_schema import PembayaranCreate
from app.core.sql_connection import get_connection
from app.schemas.pembayaran_schema import PembayaranPatch


router = APIRouter()


@router.get("/")
def get_pembayaran(
    id_pembayaran: int = None,
    id_penyewaan: int = None,
    tanggal_transaksi: date = None,
    tahun_transaksi: int = None,
    metode_pembayaran: str = None,
    status_pembayaran: str = None,
    jumlah_pembayaran: float = None
):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            query = """
                SELECT *
                FROM pembayaran
                WHERE 1=1
            """

            params = []

            # FILTER ID PEMBAYARAN
            if id_pembayaran is not None:
                query += """
                    AND id_pembayaran = %s
                """
                params.append(id_pembayaran)

            # FILTER ID PENYEWAAN
            if id_penyewaan is not None:
                query += """
                    AND id_penyewaan = %s
                """
                params.append(id_penyewaan)

            # FILTER TANGGAL TRANSAKSI
            if tanggal_transaksi is not None:
                query += """
                    AND tanggal_transaksi = %s
                """
                params.append(tanggal_transaksi)

            # FILTER TAHUN TRANSAKSI
            if tahun_transaksi is not None:
                query += """
                    AND YEAR(tanggal_transaksi) = %s
                """
                params.append(tahun_transaksi)

            # FILTER METODE PEMBAYARAN
            if metode_pembayaran:
                query += """
                    AND metode_pembayaran = %s
                """
                params.append(metode_pembayaran)

            # FILTER STATUS PEMBAYARAN
            if status_pembayaran:
                query += """
                    AND status_pembayaran = %s
                """
                params.append(status_pembayaran)

            # FILTER JUMLAH PEMBAYARAN
            if jumlah_pembayaran is not None:
                query += """
                    AND jumlah_pembayaran = %s
                """
                params.append(jumlah_pembayaran)

            cursor.execute(query, params)

            data = cursor.fetchall()

            if not data:

                if id_pembayaran is not None:
                    return {
                        "message": "ID pembayaran tidak ditemukan"
                    }

                if id_penyewaan is not None:
                    return {
                        "message": "ID penyewaan tidak ditemukan"
                    }

                if tanggal_transaksi is not None:
                    return {
                        "message": "Tanggal transaksi tidak ditemukan"
                    }

                if tahun_transaksi is not None:
                    return {
                        "message": "Tahun transaksi tidak ditemukan"
                    }

                if metode_pembayaran:
                    return {
                        "message": "Metode pembayaran tidak ditemukan"
                    }

                if status_pembayaran:
                    return {
                        "message": "Status pembayaran tidak ditemukan"
                    }

                if jumlah_pembayaran is not None:
                    return {
                        "message": "Jumlah pembayaran tidak ditemukan"
                    }

                return {
                    "message": "Data pembayaran kosong"
                }

            return data

    finally:
        conn.close()


@router.post("/")
def create_pembayaran(data: PembayaranCreate):

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # CEK ID_PENYEWAAN
            cursor.execute(
                """
                SELECT id_kendaraan, waktu_mulai,
                       waktu_selesai_rencana, status_penyewaan
                FROM penyewaan
                WHERE id_penyewaan = %s
                """,
                (data.id_penyewaan,)
            )

            penyewaan = cursor.fetchone()

            if not penyewaan:
                return {
                    "message": "ID penyewaan tidak ditemukan"
                }

            # CEK STATUS PENYEWAAN AKTIF
            if penyewaan["status_penyewaan"] != "aktif":
                return {
                    "message": "Pembayaran hanya bisa dilakukan untuk penyewaan yang masih aktif!"
                }

            # CEK DUPLIKAT PEMBAYARAN
            cursor.execute(
                """
                SELECT id_pembayaran
                FROM pembayaran
                WHERE id_penyewaan = %s
                """,
                (data.id_penyewaan,)
            )

            if cursor.fetchone():
                return {
                    "message": "Penyewaan ini sudah memiliki pembayaran!"
                }

            # CEK TANGGAL TRANSAKSI
            if data.tanggal_transaksi > penyewaan["waktu_mulai"]:
                return {
                    "message": "Tanggal transaksi tidak boleh melebihi tanggal mulai sewa!"
                }

            # AMBIL TARIF KENDARAAN
            cursor.execute(
                """
                SELECT tarif_per_hari
                FROM kendaraan
                WHERE id_kendaraan = %s
                """,
                (penyewaan["id_kendaraan"],)
            )

            kendaraan = cursor.fetchone()

            # HITUNG JUMLAH PEMBAYARAN
            jumlah_hari = (
                penyewaan["waktu_selesai_rencana"] - penyewaan["waktu_mulai"]
            ).days

            jumlah_pembayaran = round(
                float(kendaraan["tarif_per_hari"]) * jumlah_hari, 2
            )

            # INSERT DATA
            cursor.execute(
                """
                INSERT INTO pembayaran
                (
                    id_penyewaan,
                    tanggal_transaksi,
                    metode_pembayaran,
                    jumlah_pembayaran,
                    status_pembayaran
                )
                VALUES
                (%s,%s,%s,%s,%s)
                """,
                (
                    data.id_penyewaan,
                    data.tanggal_transaksi,
                    data.metode_pembayaran.value,
                    jumlah_pembayaran,
                    data.status_pembayaran.value
                )
            )

            conn.commit()

        return {
            "message": "Data pembayaran berhasil ditambahkan",
            "jumlah_pembayaran": jumlah_pembayaran
        }

    finally:
        conn.close()

@router.patch("/{id_pembayaran}")
def update_pembayaran(
    id_pembayaran: int,
    data: PembayaranPatch
):
    conn = get_connection()

    try:
        data = data.model_dump(exclude_none=True)
        with conn.cursor() as cursor:

            # CEK ID
            cursor.execute(
                """
                SELECT *
                FROM pembayaran
                WHERE id_pembayaran = %s
                """,
                (id_pembayaran,)
            )

            pembayaran = cursor.fetchone()

            if not pembayaran:
                return {
                    "message": "ID pembayaran tidak ditemukan"
                }

            # FIELD YANG BOLEH DIUPDATE
            allowed_fields = {
                "tanggal_transaksi",
                "metode_pembayaran",
                "status_pembayaran"
            }

            # CEK FIELD INVALID
            for field in data.keys():

                if field not in allowed_fields:
                    return {
                        "message": "field tidak valid"
                    }

            valid_metode = {
                "transfer_bank",
                "qris",
                "tunai",
                "kartu_debit",
                "kartu_kredit"
            }

            valid_status = {
                "lunas",
                "gagal"
            }

            # VALIDASI SATU PER SATU
            if "tanggal_transaksi" in data:

                try:
                    tanggal = date.fromisoformat(
                        str(data["tanggal_transaksi"])
                    )
                except ValueError:
                    return {
                        "message": "Format tanggal transaksi tidak valid"
                    }

                cursor.execute(
                    """
                    SELECT waktu_mulai
                    FROM penyewaan
                    WHERE id_penyewaan = %s
                    """,
                    (pembayaran["id_penyewaan"],)
                )

                penyewaan = cursor.fetchone()

                if tanggal > penyewaan["waktu_mulai"]:
                    return {
                        "message": "Tanggal transaksi tidak boleh melebihi tanggal mulai sewa!"
                    }

                data["tanggal_transaksi"] = tanggal

            if "metode_pembayaran" in data:

                if data["metode_pembayaran"] not in valid_metode:
                    return {
                        "message": "Metode pembayaran tidak sesuai pilihan yang tersedia"
                    }

            if "status_pembayaran" in data:

                if data["status_pembayaran"] not in valid_status:
                    return {
                        "message": "Status pembayaran tidak sesuai pilihan yang tersedia"
                    }

            # BUILD QUERY DINAMIS
            update_fields = []
            values = []

            for key, value in data.items():
                update_fields.append(f"{key} = %s")
                values.append(value)

            values.append(id_pembayaran)

            query = f"""
                UPDATE pembayaran
                SET {', '.join(update_fields)}
                WHERE id_pembayaran = %s
            """

            cursor.execute(query, values)

            conn.commit()

            return {
                "message": "Data pembayaran berhasil diperbarui!"
            }

    finally:
        conn.close()

@router.delete("/{id_pembayaran}")
def delete_pembayaran(id_pembayaran: int):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # CEK KETERSEDIAAN DATA
            cursor.execute(
                """
                SELECT id_pembayaran
                FROM pembayaran
                WHERE id_pembayaran = %s
                """,
                (id_pembayaran,)
            )

            pembayaran = cursor.fetchone()

            if not pembayaran:
                return {
                    "message": "ID pembayaran tidak ditemukan"
                }

            # EKSEKUSI DELETE
            cursor.execute(
                """
                DELETE FROM pembayaran
                WHERE id_pembayaran = %s
                """,
                (id_pembayaran,)
            )

            conn.commit()

            return {
                "message": "Data pembayaran berhasil dihapus!"
            }

    finally:
        conn.close()
