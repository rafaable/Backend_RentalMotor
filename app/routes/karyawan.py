from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional
from app.core.sql_connection import get_connection
from app.schemas.karyawan_schema import JabatanEnum, KaryawanCreate, KaryawanUpdate

router = APIRouter()

@router.get("/")
def get_karyawan(
    id_karyawan: Optional[int] = Query(None, description="Cari berdasarkan ID Karyawan murni (Integer)"),
    nama_karyawan: Optional[str] = Query(None, description="Cari berdasarkan nama (Partial Match)"),
    id_cabang: Optional[int] = Query(None, description="Cari berdasarkan ID Cabang murni (Integer)"),
    jabatan: Optional[JabatanEnum] = Query(None, description="Pilih jabatan melalui dropdown")
):
    # 1. VALIDASI SPASI KOSONG PADA NAMA
    if nama_karyawan is not None and not nama_karyawan.strip():
        return {
            "message": "Nama tidak boleh kosong!"
        }

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Base Query
            query = "SELECT * FROM karyawan WHERE 1=1"
            params = []

            # Filter ID Karyawan
            if id_karyawan is not None:
                query += " AND id_karyawan = %s"
                params.append(id_karyawan)

            # Filter Nama Karyawan (%LIKE%)
            if nama_karyawan:
                query += " AND nama_karyawan LIKE %s"
                params.append(f"%{nama_karyawan.strip()}%")

            # Filter ID Cabang
            if id_cabang is not None:
                query += " AND id_cabang = %s"
                params.append(id_cabang)

            # Filter Jabatan (Enum)
            if jabatan:
                query += " AND jabatan = %s"
                params.append(jabatan.value)

            cursor.execute(query, params)
            data = cursor.fetchall()

            # 2. PENANGANAN ERROR SITUASIONAL (JIKA DATA KOSONG)
            if not data:
                if id_karyawan is not None:
                    return {"message": "ID karyawan tidak ditemukan"}
                
                if nama_karyawan:
                    return {"message": "Nama karyawan tidak ditemukan"}
                
                if id_cabang is not None:
                    return {"message": "Cabang tidak ditemukan atau tidak memiliki karyawan"}
                
                if jabatan:
                    return {"message": "Jabatan karyawan tidak ditemukan"}

                return {"message": "Data karyawan kosong"}

            return data

    finally:
        conn.close()

# --- ENDPOINT POST KARYAWAN ---
@router.post("/")
def create_karyawan(payload: KaryawanCreate):
    # 1. Validasi Spasi Kosong pada Nama
    if not payload.nama_karyawan or not payload.nama_karyawan.strip():
        return {"message": "Nama tidak boleh kosong!"}
        
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 2. Validasi Keberadaan Cabang menggunakan COUNT (Lebih Aman)
            check_cabang_query = "SELECT COUNT(*) as total FROM cabang WHERE id_cabang = %s"
            cursor.execute(check_cabang_query, [payload.id_cabang])
            result = cursor.fetchone()
            
            # Menangani jika hasil fetchone berupa dictionary atau tuple/list biasa
            if isinstance(result, dict):
                total_cabang = result.get('total', 0)
            elif isinstance(result, (tuple, list)):
                total_cabang = result[0]
            else:
                total_cabang = 0

            if total_cabang == 0:
                return {"message": "Cabang tidak ditemukan!"}
                
            # 3. Insert Data Karyawan Baru
            insert_query = """
                INSERT INTO karyawan (id_cabang, nama_karyawan, jabatan) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, [
                payload.id_cabang, 
                payload.nama_karyawan.strip(), 
                payload.jabatan.value
            ])
            conn.commit() # Commit biar masuk database aman
            
            return {"message": "Data karyawan berhasil ditambahkan"}
            
    except Exception as e:
        # Jika masih ada kendala, kembalikan pesan eror aslinya biar kita bisa lacak
        return {"message": "Terjadi kesalahan pada server", "error_details": str(e)}
        
    finally:
        conn.close()

# --- ENDPOINT PATCH KARYAWAN  ---
@router.patch("/{id_karyawan}")
def update_karyawan(id_karyawan: int, payload: KaryawanUpdate):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. Validasi: Cek apakah ID Karyawan terdaftar di database
            check_karyawan_query = "SELECT id_karyawan FROM karyawan WHERE id_karyawan = %s"
            cursor.execute(check_karyawan_query, [id_karyawan])
            karyawan_exist = cursor.fetchone()
            
            if not karyawan_exist:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID karyawan tidak ditemukan"
                )
            
            # Siapkan daftar kolom yang akan di-update secara dinamis
            update_fields = []
            params = []
            
            # 2. Validasi & Penyiapan data Nama (jika dikirim)
            if payload.nama_karyawan is not None:
                if not payload.nama_karyawan.strip():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Nama tidak boleh kosong!"
                    )
                update_fields.append("nama_karyawan = %s")
                params.append(payload.nama_karyawan.strip())
                
            # 3. Validasi & Penyiapan data Cabang (jika dikirim)
            if payload.id_cabang is not None:
                check_cabang_query = "SELECT id_cabang FROM cabang WHERE id_cabang = %s"
                cursor.execute(check_cabang_query, [payload.id_cabang])
                cabang_exist = cursor.fetchone()
                
                if not cabang_exist:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Cabang tidak ditemukan!"
                    )
                update_fields.append("id_cabang = %s")
                params.append(payload.id_cabang)
                
            # 4. Penyiapan data Jabatan (jika dikirim)
            if payload.jabatan is not None:
                update_fields.append("jabatan = %s")
                params.append(payload.jabatan.value)
                
            # Jika user melakukan execute tapi body JSON kosong ({})
            if not update_fields:
                return {"message": "Tidak ada data yang diubah"}
                
            # Susun query UPDATE SQL secara dinamis
            query = f"UPDATE karyawan SET {', '.join(update_fields)} WHERE id_karyawan = %s"
            params.append(id_karyawan)
            
            cursor.execute(query, params)
            conn.commit() # Simpan perubahan permanen ke MySQL
            
            return {"message": "Data karyawan berhasil diperbarui"}
            
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(e)}"
        )
    finally:
        conn.close()

# --- ENDPOINT DELETE KARYAWAN  ---
@router.delete("/{id_karyawan}")
def delete_karyawan(id_karyawan: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. Validasi: Cek apakah ID Karyawan terdaftar di database
            check_karyawan_query = "SELECT id_karyawan FROM karyawan WHERE id_karyawan = %s"
            cursor.execute(check_karyawan_query, [id_karyawan])
            karyawan_exist = cursor.fetchone()
            
            if not karyawan_exist:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID karyawan tidak ditemukan"
                )
            
            # 2. Eksekusi Penghapusan Data
            delete_query = "DELETE FROM karyawan WHERE id_karyawan = %s"
            cursor.execute(delete_query, [id_karyawan])
            conn.commit() # Wajib commit agar data benar-benar terhapus di MySQL
            
            return {"message": "Data karyawan berhasil dihapus"}
            
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(e)}"
        )
    finally:
        conn.close()