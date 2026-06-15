from fastapi import APIRouter
from app.core.sql_connection import get_connection
from app.schemas.denda_schema import AlasanDenda

router = APIRouter()


@router.get("/")
def get_denda(
    id_denda: int = None,
    id_pengembalian: int = None,
    alasan_denda: AlasanDenda = None,
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