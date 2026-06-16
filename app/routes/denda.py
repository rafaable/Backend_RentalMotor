from fastapi import APIRouter
from app.core.sql_connection import get_connection
from app.schemas.denda_schema import AlasanDendaGet
from app.schemas.denda_schema import DendaCreate
from app.schemas.denda_schema import DendaPatch


router = APIRouter()


@router.get("/")
def get_denda(
    id_denda: int = None,
    id_pengembalian: int = None,
    alasan_denda: AlasanDendaGet = None,
    keterangan: str = None
):

    conn = get_connection()

    try:

        filters = [
            id_denda,
            id_pengembalian,
            alasan_denda,
            keterangan
        ]

        jumlah_filter = sum(
            value is not None
            for value in filters
        )

        if jumlah_filter > 1:
            return {
                "message": "Gunakan satu filter pencarian saja"
            }

        with conn.cursor() as cursor:

            query = """
                SELECT *
                FROM denda
                WHERE 1=1
            """

            params = []

            # FILTER ID DENDA
            if id_denda is not None:

                query += """
                    AND id_denda = %s
                """

                params.append(id_denda)

            # FILTER ID PENGEMBALIAN
            elif id_pengembalian is not None:

                cursor.execute(
                    """
                    SELECT id_pengembalian
                    FROM pengembalian
                    WHERE id_pengembalian = %s
                    """,
                    (id_pengembalian,)
                )

                if not cursor.fetchone():
                    return {
                        "message": "ID pengembalian tidak ditemukan"
                    }

                query += """
                    AND id_pengembalian = %s
                """

                params.append(id_pengembalian)

            # FILTER ALASAN DENDA
            elif alasan_denda is not None:

                query += """
                    AND alasan_denda = %s
                """

                params.append(alasan_denda.value)

            # FILTER KETERANGAN
            elif keterangan:

                query += """
                    AND keterangan LIKE %s
                """

                params.append(
                    f"%{keterangan}%"
                )

            cursor.execute(query, params)

            data = cursor.fetchall()

            if not data:

                if id_denda is not None:
                    return {
                        "message": "ID tidak ditemukan"
                    }

                if id_pengembalian is not None:
                    return {
                        "message": "Data denda tidak ditemukan"
                    }

                if alasan_denda is not None:
                    return {
                        "message": "Data tidak ditemukan"
                    }

                if keterangan:
                    return {
                        "message": "Keterangan tidak ditemukan"
                    }

                return {
                    "message": "Data denda kosong"
                }

            return data

    finally:
        conn.close()

@router.post("/")
def create_denda(data: DendaCreate):

    conn = get_connection()

    try:

        # VALIDASI FIELD WAJIB
        if (
            data.id_pengembalian is None
            or data.id_karyawan is None
            or data.alasan_denda is None
            or data.nominal_denda is None
        ):
            return {
                "message": "Masukkan informasi secara lengkap!"
            }

        # NOMINAL DENDA
        if data.nominal_denda <= 0:
            return {
                "message": "Nominal denda harus lebih dari 0!"
            }

        # KETERANGAN
        if (
            data.keterangan is not None
            and not data.keterangan.strip()
        ):
            return {
                "message": "Keterangan tidak valid!"
            }

        with conn.cursor() as cursor:

            # CEK ID PENGEMBALIAN

            cursor.execute(
                """
                SELECT id_pengembalian
                FROM pengembalian
                WHERE id_pengembalian = %s
                """,
                (data.id_pengembalian,)
            )

            if not cursor.fetchone():
                return {
                    "message": "ID pengembalian tidak ditemukan!"
                }

            # CEK ID KARYAWAN

            cursor.execute(
                """
                SELECT id_karyawan
                FROM karyawan
                WHERE id_karyawan = %s
                """,
                (data.id_karyawan,)
            )

            if not cursor.fetchone():
                return {
                    "message": "ID karyawan tidak ditemukan!"
                }

            # CEK DUPLIKAT
            # id_pengembalian + alasan_denda

            cursor.execute(
                """
                SELECT id_denda
                FROM denda
                WHERE id_pengembalian = %s
                AND alasan_denda = %s
                """,
                (
                    data.id_pengembalian,
                    data.alasan_denda.value
                )
            )

            if cursor.fetchone():
                return {
                    "message":
                    "Alasan denda sudah terdaftar untuk pengembalian ini!"
                }

            # INSERT

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
                    data.id_pengembalian,
                    data.id_karyawan,
                    data.alasan_denda.value,
                    data.nominal_denda,
                    data.keterangan.strip()
                    if data.keterangan
                    else None
                )
            )

            conn.commit()

            return {
                "message": "Data denda berhasil ditambahkan",
                "id_denda": cursor.lastrowid
            }

    finally:
        conn.close()

@router.patch("/{id_denda}")
def update_denda(
    id_denda: int,
    data: DendaPatch
):

    conn = get_connection()

    try:

        data = data.model_dump(exclude_none=True)

        with conn.cursor() as cursor:

            # CEK ID DENDA

            cursor.execute(
                """
                SELECT *
                FROM denda
                WHERE id_denda = %s
                """,
                (id_denda,)
            )

            denda = cursor.fetchone()

            if not denda:
                return {
                    "message": "ID not found"
                }

            # FIELD VALID

            allowed_fields = {
                "id_karyawan",
                "alasan_denda",
                "nominal_denda",
                "keterangan"
            }

            for field in data.keys():

                if field == "id_denda":
                    return {
                        "message": "field tidak valid"
                    }

                if field == "id_pengembalian":
                    return {
                        "message": "field tidak valid"
                    }

                if field not in allowed_fields:
                    return {
                        "message": "field tidak valid"
                    }

            # VALIDASI ID KARYAWAN

            if "id_karyawan" in data:

                cursor.execute(
                    """
                    SELECT id_karyawan
                    FROM karyawan
                    WHERE id_karyawan = %s
                    """,
                    (data["id_karyawan"],)
                )

                if not cursor.fetchone():
                    return {
                        "message": "ID karyawan tidak ditemukan!"
                    }

            # VALIDASI NOMINAL

            if "nominal_denda" in data:

                if data["nominal_denda"] <= 0:
                    return {
                        "message": "Nominal denda harus lebih dari 0!"
                    }

            # VALIDASI KETERANGAN

            if "keterangan" in data:

                if (
                    data["keterangan"] is not None
                    and not data["keterangan"].strip()
                ):
                    return {
                        "message": "Keterangan tidak valid!"
                    }

            # CEK DUPLIKAT ALASAN

            if "alasan_denda" in data:

                cursor.execute(
                    """
                    SELECT id_denda
                    FROM denda
                    WHERE id_pengembalian = %s
                    AND alasan_denda = %s
                    AND id_denda != %s
                    """,
                    (
                        denda["id_pengembalian"],
                        data["alasan_denda"].value,
                        id_denda
                    )
                )

                if cursor.fetchone():
                    return {
                        "message":
                        "Alasan denda sudah terdaftar untuk pengembalian ini!"
                    }

            # BUILD QUERY DINAMIS

            update_fields = []
            values = []

            for key, value in data.items():

                if key == "alasan_denda":
                    value = value.value

                if (
                    key == "keterangan"
                    and value is not None
                ):
                    value = value.strip()

                update_fields.append(
                    f"{key} = %s"
                )

                values.append(value)

            if not update_fields:
                return {
                    "message": "Tidak ada data yang diperbarui"
                }

            values.append(id_denda)

            query = f"""
                UPDATE denda
                SET {', '.join(update_fields)}
                WHERE id_denda = %s
            """

            cursor.execute(
                query,
                values
            )

            conn.commit()

            return {
                "message": "Data denda berhasil diperbarui!"
            }

    finally:
        conn.close()

@router.delete("/{id_denda}")
def delete_denda(id_denda: int):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            # CEK ID

            cursor.execute(
                """
                SELECT id_denda
                FROM denda
                WHERE id_denda = %s
                """,
                (id_denda,)
            )

            if not cursor.fetchone():
                return {
                    "message": "ID not found"
                }

            # DELETE

            cursor.execute(
                """
                DELETE FROM denda
                WHERE id_denda = %s
                """,
                (id_denda,)
            )

            conn.commit()

            return {
                "message": "Data denda berhasil dihapus!"
            }

    finally:
        conn.close()