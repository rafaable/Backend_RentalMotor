from fastapi import APIRouter
from datetime import date
from datetime import datetime
from app.core.mongo_connection import log_aktivitas
from app.core.sql_connection import get_connection
from app.schemas.pengembalian_schema import PengembalianPatch
from app.schemas.pengembalian_schema import PengembalianCreate

router = APIRouter()


@router.get("/")
def get_pengembalian(
    id_pengembalian: int = None,
    id_penyewaan: int = None,
    id_karyawan: int = None,
    date_return_up: str = None,
    date_return_down: str = None
):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            query = """
                SELECT *
                FROM pengembalian
                WHERE 1=1
            """

            params = []

            # FILTER ID PENGEMBALIAN
            if id_pengembalian is not None:

                query += """
                    AND id_pengembalian = %s
                """

                params.append(id_pengembalian)

            # FILTER ID PENYEWAAN
            if id_penyewaan is not None:

                query += """
                    AND id_penyewaan = %s
                """

                params.append(id_penyewaan)

            # FILTER ID KARYAWAN
            if id_karyawan is not None:

                query += """
                    AND id_karyawan = %s
                """

                params.append(id_karyawan)

            # FILTER RENTANG TANGGAL
            if date_return_up and date_return_down:

                try:

                    tanggal_awal = date.fromisoformat(
                        date_return_up
                    )

                    tanggal_akhir = date.fromisoformat(
                        date_return_down
                    )

                except ValueError:

                    return {
                        "message": "Gunakan format YYYY-MM-DD"
                    }

                if tanggal_awal > tanggal_akhir:

                    return {
                        "message": "Rentang tanggal tidak valid"
                    }

                query += """
                    AND waktu_pengembalian
                    BETWEEN %s AND %s
                """

                params.append(tanggal_awal)
                params.append(tanggal_akhir)

            cursor.execute(query, params)

            data = cursor.fetchall()

            if not data:

                if id_pengembalian is not None:
                    return {
                        "message": "id pengembalian not found!"
                    }

                if id_penyewaan is not None:
                    return {
                        "message": "id penyewaan not found!"
                    }

                if id_karyawan is not None:
                    return {
                        "message": "id karyawan not found!"
                    }

                if date_return_up and date_return_down:
                    return {
                        "message": "date range not found!"
                    }

                return {
                    "message": "Data pengembalian kosong"
                }

            return data

    finally:
        conn.close()


@router.post("/")
def create_pengembalian(data: PengembalianCreate):

    conn = get_connection()

    try:

        # VALIDASI FIELD KOSONG

        if (
            not data.id_penyewaan
            or not data.id_karyawan
            or not data.waktu_pengembalian
            or not data.kondisi_kendaraan
        ):
            return {
                "message": "Masukkan informasi secara lengkap!"
            }

        # KONDISI KENDARAAN KOSONG / SPASI

        if not data.kondisi_kendaraan.strip():
            return {
                "message": "Kondisi kendaraan harus diisi!"
            }

        with conn.cursor() as cursor:

            # CEK PENYEWAAN

            cursor.execute(
                """
                SELECT
                    p.id_penyewaan,
                    p.id_karyawan,
                    p.id_kendaraan,
                    p.status_penyewaan,
                    p.waktu_mulai,
                    p.waktu_selesai_rencana,
                    k.id_cabang
                FROM penyewaan p
                JOIN karyawan k
                    ON p.id_karyawan = k.id_karyawan
                WHERE p.id_penyewaan = %s
                """,
                (data.id_penyewaan,)
            )

            penyewaan = cursor.fetchone()

            if not penyewaan:
                return {
                    "message": "Tidak ada entri dengan id penyewaan terkait!"
                }

            # STATUS PENYEWAAN

            if penyewaan["status_penyewaan"] == "selesai":
                return {
                    "message": "ID penyewaan tersebut telah selesai!"
                }

            # CEK KARYAWAN

            cursor.execute(
                """
                SELECT
                    id_karyawan,
                    id_cabang
                FROM karyawan
                WHERE id_karyawan = %s
                """,
                (data.id_karyawan,)
            )

            karyawan = cursor.fetchone()

            if not karyawan:
                return {
                    "message": "Karyawan tidak terdaftar!"
                }

            # CEK CABANG

            if (
                penyewaan["id_cabang"]
                !=
                karyawan["id_cabang"]
            ):
                return {
                    "message":
                    "Karyawan pengembalian harus berasal dari cabang yang sama dengan karyawan penyewaan!"
                }

            # CEK DUPLIKAT PENGEMBALIAN

            cursor.execute(
                """
                SELECT id_pengembalian
                FROM pengembalian
                WHERE id_penyewaan = %s
                """,
                (data.id_penyewaan,)
            )

            if cursor.fetchone():
                return {
                    "message": "ID penyewaan tersebut telah selesai!"
                }

            # VALIDASI TANGGAL

            if (
                data.waktu_pengembalian
                <
                penyewaan["waktu_mulai"]
            ):
                return {
                    "message":
                    "Masukkan tanggal pengembalian setelah tanggal mulai penyewaan!"
                }

            # INSERT

            cursor.execute(
                """
                INSERT INTO pengembalian
                (
                    id_penyewaan,
                    id_karyawan,
                    waktu_pengembalian,
                    kondisi_kendaraan
                )
                VALUES
                (%s,%s,%s,%s)
                """,
                (
                    data.id_penyewaan,
                    data.id_karyawan,
                    data.waktu_pengembalian,
                    data.kondisi_kendaraan.strip()
                )
            )

            id_pengembalian = cursor.lastrowid

            # STATUS PENYEWAAN -> SELESAI

            cursor.execute(
                """
                UPDATE penyewaan
                SET status_penyewaan = 'selesai'
                WHERE id_penyewaan = %s
                """,
                (data.id_penyewaan,)
            )

            # STATUS KENDARAAN -> TERSEDIA

            cursor.execute(
                """
                UPDATE kendaraan
                SET status_kendaraan = 'tersedia'
                WHERE id_kendaraan = %s
                """,
                (penyewaan["id_kendaraan"],)
            )

            # CEK KETERLAMBATAN

            if (
                data.waktu_pengembalian
                >
                penyewaan["waktu_selesai_rencana"]
            ):

                selisih_hari = (
                    data.waktu_pengembalian
                    -
                    penyewaan["waktu_selesai_rencana"]
                ).days

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

                nominal_denda = (
                    selisih_hari
                    * 1.5
                    * float(kendaraan["tarif_per_hari"])
                )

                # INSERT DENDA

                cursor.execute(
                    """
                    INSERT INTO denda
                    (
                        id_pengembalian,
                        id_karyawan,
                        alasan_denda,
                        nominal_denda,
                        keterangan
                    )
                    VALUES
                    (%s,%s,%s,%s,%s)
                    """,
                    (
                        id_pengembalian,
                        data.id_karyawan,
                        "keterlambatan_pengembalian",
                        nominal_denda,
                        "-"
                    )
                )
            conn.commit()

            # AMBIL DATA KARYAWAN UNTUK LOG
            cursor.execute(
                """
                SELECT
                    nama_karyawan,
                    jabatan
                FROM karyawan
                WHERE id_karyawan = %s
                """,
                (data.id_karyawan,)
            )

            karyawan_log = cursor.fetchone()

            # LOG KE MONGODB

            log_aktivitas.insert_one(
                {
                    "timestamp": datetime.now(),
                    "action": "insert",
                    "tabel": "pengembalian",
                    "karyawan": {
                        "id_karyawan": data.id_karyawan,
                        "nama": karyawan_log["nama_karyawan"],
                        "jabatan": karyawan_log["jabatan"]
                    },
                    "deskripsi": {
                        "id_pengembalian": id_pengembalian,
                        "id_penyewaan": data.id_penyewaan,
                        "waktu_pengembalian": str(data.waktu_pengembalian),
                        "kondisi": data.kondisi_kendaraan.strip()
                    }
                }
            )

            return {
                "message":
                "Data pengembalian berhasil ditambahkan"
            }

    finally:
        conn.close()

@router.patch("/{id_pengembalian}")
def update_pengembalian(
    id_pengembalian: int,
    data: PengembalianPatch
):

    conn = get_connection()

    try:

        data = data.model_dump(exclude_none=True)

        with conn.cursor() as cursor:

            # CEK ID

            cursor.execute(
                """
                SELECT *
                FROM pengembalian
                WHERE id_pengembalian = %s
                """,
                (id_pengembalian,)
            )

            pengembalian = cursor.fetchone()

            if not pengembalian:
                return {
                    "message": "ID not found"
                }

            # FIELD YANG BOLEH DIUPDATE

            allowed_fields = {
                "id_karyawan",
                "kondisi_kendaraan"
            }

            # CEK FIELD INVALID

            for field in data.keys():

                if field not in allowed_fields:
                    return {
                        "message": "field tidak valid"
                    }

            # VALIDASI KARYAWAN

            if "id_karyawan" in data:

                cursor.execute(
                    """
                    SELECT id_cabang
                    FROM karyawan
                    WHERE id_karyawan = %s
                    """,
                    (data["id_karyawan"],)
                )

                karyawan_baru = cursor.fetchone()

                if not karyawan_baru:
                    return {
                        "message": "Karyawan tidak terdaftar!"
                    }

                cursor.execute(
                    """
                    SELECT k.id_cabang
                    FROM pengembalian p
                    JOIN penyewaan py
                        ON p.id_penyewaan = py.id_penyewaan
                    JOIN karyawan k
                        ON py.id_karyawan = k.id_karyawan
                    WHERE p.id_pengembalian = %s
                    """,
                    (id_pengembalian,)
                )

                cabang_penyewaan = cursor.fetchone()

                if (
                    cabang_penyewaan["id_cabang"]
                    !=
                    karyawan_baru["id_cabang"]
                ):
                    return {
                        "message":
                        "Karyawan pengembalian harus berasal dari cabang yang sama dengan karyawan penyewaan!"
                    }

            # BUILD QUERY DINAMIS

            update_fields = []
            values = []

            for key, value in data.items():

                update_fields.append(
                    f"{key} = %s"
                )

                values.append(value)

            values.append(id_pengembalian)

            query = f"""
                UPDATE pengembalian
                SET {', '.join(update_fields)}
                WHERE id_pengembalian = %s
            """

            cursor.execute(
                query,
                values
            )

            conn.commit()
            
            # LOG AKTIVITAS KE MONGODB

            deskripsi_log = {}

            # JIKA UPDATE KARYAWAN
            if "id_karyawan" in data:

                cursor.execute(
                    """
                    SELECT
                        nama_karyawan,
                        jabatan
                    FROM karyawan
                    WHERE id_karyawan = %s
                    """,
                    (data["id_karyawan"],)
                )

                karyawan_log = cursor.fetchone()

                deskripsi_log["karyawan"] = {
                    "id_karyawan": data["id_karyawan"],
                    "nama": karyawan_log["nama_karyawan"],
                    "jabatan": karyawan_log["jabatan"]
                }

            # JIKA UPDATE KONDISI
            if "kondisi_kendaraan" in data:

                deskripsi_log["kondisi"] = (
                    data["kondisi_kendaraan"].strip()
                )

            log_aktivitas.insert_one(
                {
                    "timestamp": datetime.now(),
                    "action": "update",
                    "tabel": "pengembalian",
                    "deskripsi": deskripsi_log
                }
            )

            return {
                "message":
                "Data pengembalian berhasil diperbarui!"
            }

    finally:
        conn.close()

@router.delete("/{id_pengembalian}")
def delete_pengembalian(id_pengembalian: int):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            # CEK ID

            cursor.execute(
                """
                SELECT *
                FROM pengembalian
                WHERE id_pengembalian = %s
                """,
                (id_pengembalian,)
            )

            pengembalian = cursor.fetchone()

            if not pengembalian:
                return {
                    "message": "ID not found"
                }

            # DATA UNTUK LOG

            cursor.execute(
                """
                SELECT
                    p.id_pengembalian,
                    p.id_penyewaan,
                    p.id_karyawan,
                    p.waktu_pengembalian,
                    p.kondisi_kendaraan,
                    k.nama_karyawan,
                    k.jabatan
                FROM pengembalian p
                JOIN karyawan k
                    ON p.id_karyawan = k.id_karyawan
                WHERE p.id_pengembalian = %s
                """,
                (id_pengembalian,)
            )

            deleted_data = cursor.fetchone()

            # CEK DENDA TERKAIT

            cursor.execute(
                """
                SELECT *
                FROM denda
                WHERE id_pengembalian = %s
                """,
                (id_pengembalian,)
            )

            denda = cursor.fetchone()

            if denda:
                return {
                    "message": "Tidak bisa hapus pengembalian, masih ada denda terkait!"
                }

            # DELETE
            cursor.execute(
                """
                DELETE FROM pengembalian
                WHERE id_pengembalian = %s
                """,
                (id_pengembalian,)
            )

            conn.commit()

            log_aktivitas.insert_one(
                {
                    "timestamp": datetime.now(),
                    "action": "delete",
                    "tabel": "pengembalian",
                    "deleted": {
                        "id_pengembalian":
                            deleted_data["id_pengembalian"],
                        "id_penyewaan":
                            deleted_data["id_penyewaan"],
                        "karyawan": {
                            "id_karyawan":
                                deleted_data["id_karyawan"],
                            "nama":
                                deleted_data["nama_karyawan"],
                            "jabatan":
                                deleted_data["jabatan"]
                        },
                        "waktu_pengembalian":
                            str(deleted_data["waktu_pengembalian"]),
                        "kondisi":
                            deleted_data["kondisi_kendaraan"]
                    }
                }
            )

            return {
                "message": "Data penyewaan berhasil dihapus!"
            }

    finally:
        conn.close()