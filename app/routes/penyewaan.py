from fastapi import APIRouter
from datetime import date, datetime
from app.core.sql_connection import get_connection
from app.core.mongo_connection import log_aktivitas
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
            query = "SELECT * FROM penyewaan WHERE 1=1"
            params = []

            if id_pengguna is not None:
                query += " AND id_pengguna = %s"
                params.append(id_pengguna)
            if id_kendaraan is not None:
                query += " AND id_kendaraan = %s"
                params.append(id_kendaraan)
            if id_karyawan is not None:
                query += " AND id_karyawan = %s"
                params.append(id_karyawan)
            if waktu_kembali_down is not None and waktu_kembali_up is not None:
                if waktu_kembali_down > waktu_kembali_up:
                    return {"message": "Rentang tanggal tidak valid"}
                query += " AND waktu_selesai_rencana BETWEEN %s AND %s"
                params.append(waktu_kembali_down)
                params.append(waktu_kembali_up)
            if status_penyewaan:
                query += " AND status_penyewaan = %s"
                params.append(status_penyewaan)

            cursor.execute(query, params)
            data = cursor.fetchall()

            if not data:
                if id_penyewaan:
                    return {"message": "id penyewaan not found!"}
                if id_pengguna:
                    return {"message": "id pengguna not found!"}
                if id_kendaraan:
                    return {"message": "id kendaraan not found!"}
                if id_karyawan:
                    return {"message": "id karyawan not found!"}
                if waktu_kembali_down and waktu_kembali_up:
                    return {"message": "date range not found!"}
                if status_penyewaan:
                    return {"message": "status not found!"}
                return {"message": "Data penyewaan kosong"}

            return data
    finally:
        conn.close()


@router.post("/")
def create_penyewaan(data: PenyewaanCreate):
    conn = get_connection()
    try:
        if (
            data.id_pengguna is None
            or data.id_kendaraan is None
            or data.id_karyawan is None
            or not str(data.waktu_mulai).strip()
            or not str(data.waktu_selesai_rencana).strip()
            or not str(data.status_penyewaan).strip()
        ):
            return {"message": "Masukkan informasi secara lengkap!"}

        try:
            waktu_mulai = date.fromisoformat(data.waktu_mulai)
            waktu_selesai_rencana = date.fromisoformat(
                data.waktu_selesai_rencana)
        except ValueError:
            return {"message": "Gunakan format YYYY-MM-DD"}

        if waktu_mulai > waktu_selesai_rencana:
            return {"message": "Rentang tanggal tidak valid!"}

        if data.status_penyewaan != "aktif":

            return {
                "message": "Awal input, status penyewaan harus aktif"
            }
            return {"message": "Status penyewaan harus aktif"}

        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT * FROM pengguna WHERE id_pengguna = %s", (data.id_pengguna,))
            pengguna = cursor.fetchone()
            if not pengguna:
                return {"message": "Pengguna tidak terdaftar"}
            if pengguna["status_verifikasi"] != "terverifikasi":
                return {"message": "Pengguna tidak terverifikasi"}

            cursor.execute(
                "SELECT id_penyewaan FROM penyewaan WHERE id_pengguna = %s AND status_penyewaan = 'aktif'",
                (data.id_pengguna,)
            )
            if cursor.fetchone():
                return {"message": "Pengguna masih memiliki penyewaan aktif"}

            cursor.execute(
                "SELECT * FROM kendaraan WHERE id_kendaraan = %s", (data.id_kendaraan,))
            kendaraan = cursor.fetchone()
            if not kendaraan:
                return {"message": "Kendaraan tidak tersedia!"}
            if kendaraan["status_kendaraan"] != "tersedia":
                return {"message": "Kendaraan tidak tersedia!"}

            cursor.execute(
                "SELECT * FROM karyawan WHERE id_karyawan = %s", (data.id_karyawan,))
            karyawan = cursor.fetchone()
            if not karyawan:
                return {"message": "Karyawan tidak terdaftar"}

            if kendaraan["id_cabang"] != karyawan["id_cabang"]:
                return {"message": "Karyawan dan kendaraan tidak berasal dari cabang yang sama!"}

            cursor.execute(
                """
                INSERT INTO penyewaan
                (id_pengguna, id_kendaraan, id_karyawan, waktu_mulai, waktu_selesai_rencana, status_penyewaan)
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (data.id_pengguna, data.id_kendaraan, data.id_karyawan,
                 waktu_mulai, waktu_selesai_rencana, data.status_penyewaan)
            )
            id_baru = cursor.lastrowid

            cursor.execute(
                "UPDATE kendaraan SET status_kendaraan = 'disewa' WHERE id_kendaraan = %s",
                (data.id_kendaraan,)
            )
            conn.commit()

            # LOG INSERT PENYEWAAN
            log_aktivitas.insert_one({
                "timestamp": datetime.now(),
                "action": "insert",
                "tabel": "penyewaan",
                "karyawan": {
                    "id_karyawan": data.id_karyawan,
                    "nama": karyawan["nama_karyawan"],
                    "jabatan": karyawan["jabatan"]
                },
                "deskripsi": {
                    "id_penyewaan": id_baru,
                    "id_pengguna": data.id_pengguna,
                    "id_kendaraan": data.id_kendaraan,
                    "waktu_mulai": str(waktu_mulai),
                    "waktu_selesai_rencana": str(waktu_selesai_rencana),
                    "status_penyewaan": data.status_penyewaan
                }
            })

            return {"message": "Data penyewaan berhasil ditambahkan"}

    finally:
        conn.close()


@router.patch("/{id_penyewaan}")
def update_penyewaan(id_penyewaan: int, data: PenyewaanPatch):
    conn = get_connection()
    try:
        data = data.model_dump(exclude_none=True)

        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT * FROM penyewaan WHERE id_penyewaan = %s", (id_penyewaan,))
            penyewaan = cursor.fetchone()
            if not penyewaan:
                return {"message": "id not found"}

            if penyewaan["status_penyewaan"] == "selesai":
                return {"message": "Status penyewaan yang sudah selesai tidak dapat diubah"}

            if "id_penyewaan" in data:
                return {"message": "id_penyewaan tidak boleh diubah!"}

            allowed_fields = {"id_pengguna", "id_kendaraan", "id_karyawan",
                              "waktu_mulai", "waktu_selesai_rencana", "status_penyewaan"}
            for field in data.keys():
                if field not in allowed_fields:
                    return {"message": "field tidak valid"}

            if "id_pengguna" in data:
                cursor.execute(
                    "SELECT * FROM pengguna WHERE id_pengguna = %s", (data["id_pengguna"],))
                pengguna = cursor.fetchone()
                if not pengguna:
                    return {"message": "id_pengguna tidak terdaftar!"}
                if pengguna["status_verifikasi"] != "terverifikasi":
                    return {"message": "Pengguna tidak terverifikasi"}

            if "id_kendaraan" in data:
                cursor.execute(
                    "SELECT * FROM kendaraan WHERE id_kendaraan = %s", (data["id_kendaraan"],))
                kendaraan = cursor.fetchone()
                if not kendaraan:
                    return {"message": "id_kendaraan tidak terdapat dalam entri!"}
                if kendaraan["status_kendaraan"] != "tersedia":
                    return {"message": "Kendaraan tidak tersedia!"}

                    return {
                        "message":
                        "id_kendaraan tidak terdapat dalam daftar!"
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
                    "SELECT * FROM karyawan WHERE id_karyawan = %s", (data["id_karyawan"],))
                karyawan = cursor.fetchone()
                if not karyawan:
                    return {"message": "id_karyawan tidak terdapat dalam entri!"}

                    return {
                        "message":
                        "id_karyawan tidak terdapat dalam daftar!"
                    }

            # VALIDASI FORMAT TANGGAL
            if "waktu_mulai" in data:
                try:
                    date.fromisoformat(str(data["waktu_mulai"]))
                except ValueError:
                    return {"message": "Gunakan format YYYY-MM-DD"}

            if "waktu_selesai_rencana" in data:
                try:
                    date.fromisoformat(str(data["waktu_selesai_rencana"]))
                except ValueError:
                    return {"message": "Gunakan format YYYY-MM-DD"}

            waktu_mulai = date.fromisoformat(
                str(data.get("waktu_mulai", penyewaan["waktu_mulai"])))
            waktu_selesai = date.fromisoformat(
                str(data.get("waktu_selesai_rencana", penyewaan["waktu_selesai_rencana"])))
            if waktu_mulai > waktu_selesai:
                return {"message": "Rentang tanggal tidak valid!"}

            if "status_penyewaan" in data:
                if data["status_penyewaan"] not in {"aktif", "dibatalkan"}:
                    return {"message": "Pilih salah satu dari status penyewaan berikut : aktif, dibatalkan"}

                valid_status = {
                    "dibatalkan"
                }

                if (
                    data["status_penyewaan"]
                    not in valid_status
                ):

                    return {
                        "message":
                        "Fitur ini hanya untuk mengubah status aktif menjadi dibatalkan!"
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
            kendaraan_id = data.get("id_kendaraan", penyewaan["id_kendaraan"])
            karyawan_id = data.get("id_karyawan", penyewaan["id_karyawan"])

            cursor.execute(
                "SELECT id_cabang FROM kendaraan WHERE id_kendaraan = %s", (kendaraan_id,))
            kendaraan_cabang = cursor.fetchone()

            cursor.execute(
                "SELECT id_cabang FROM karyawan WHERE id_karyawan = %s", (karyawan_id,))
            karyawan_cabang = cursor.fetchone()

            if kendaraan_cabang["id_cabang"] != karyawan_cabang["id_cabang"]:
                return {"message": "Karyawan dan kendaraan tidak berasal dari cabang yang sama!"}

            update_fields = []
            values = []
            for key, value in data.items():
                update_fields.append(f"{key} = %s")
                values.append(value)
            values.append(id_penyewaan)

            cursor.execute(
                f"UPDATE penyewaan SET {', '.join(update_fields)} WHERE id_penyewaan = %s", values)
            conn.commit()

            # AMBIL DATA KARYAWAN UNTUK LOG
            cursor.execute(
                "SELECT * FROM karyawan WHERE id_karyawan = %s", (karyawan_id,))
            karyawan_log = cursor.fetchone()

            # LOG UPDATE PENYEWAAN
            log_aktivitas.insert_one({
                "timestamp": datetime.now(),
                "action": "update",
                "tabel": "penyewaan",
                "karyawan": {
                    "id_karyawan": karyawan_id,
                    "nama": karyawan_log["nama_karyawan"],
                    "jabatan": karyawan_log["jabatan"]
                },
                "deskripsi": {
                    "id_penyewaan": id_penyewaan,
                    "fields_updated": data
                }
            })

            return {"message": "Data penyewaan berhasil diperbarui!"}

    finally:
        conn.close()


@router.delete("/{id_penyewaan}")
def delete_penyewaan(id_penyewaan: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT * FROM penyewaan WHERE id_penyewaan = %s", (id_penyewaan,))
            penyewaan = cursor.fetchone()
            if not penyewaan:
                return {"message": "ID not found"}

            cursor.execute(
                "SELECT id_pengembalian FROM pengembalian WHERE id_penyewaan = %s LIMIT 1", (id_penyewaan,))
            if cursor.fetchone():
                return {"message": "Tidak bisa hapus penyewaan, masih ada pengembalian terkait!"}

            cursor.execute(
                "SELECT id_pembayaran FROM pembayaran WHERE id_penyewaan = %s LIMIT 1", (id_penyewaan,))
            if cursor.fetchone():
                return {"message": "Tidak bisa hapus penyewaan, masih ada pembayaran terkait!"}

            # AMBIL DATA KARYAWAN UNTUK LOG
            cursor.execute(
                "SELECT * FROM karyawan WHERE id_karyawan = %s", (penyewaan["id_karyawan"],))
            karyawan_log = cursor.fetchone()

            cursor.execute(
                "DELETE FROM penyewaan WHERE id_penyewaan = %s", (id_penyewaan,))
            conn.commit()

            # LOG DELETE PENYEWAAN
            log_aktivitas.insert_one({
                "timestamp": datetime.now(),
                "action": "delete",
                "tabel": "penyewaan",
                "karyawan": {
                    "id_karyawan": penyewaan["id_karyawan"],
                    "nama": karyawan_log["nama_karyawan"],
                    "jabatan": karyawan_log["jabatan"]
                },
                "deskripsi": {
                    "id_penyewaan": id_penyewaan,
                    "id_pengguna": penyewaan["id_pengguna"],
                    "id_kendaraan": penyewaan["id_kendaraan"],
                    "waktu_mulai": str(penyewaan["waktu_mulai"]),
                    "waktu_selesai_rencana": str(penyewaan["waktu_selesai_rencana"]),
                    "status_penyewaan": penyewaan["status_penyewaan"]
                }
            })

            return {"message": "Data penyewaan berhasil dihapus!"}

    finally:
        conn.close()
