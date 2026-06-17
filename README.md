# Sistem Database Rental Motor
Disusun oleh kelompok 6:
> 1. **Salsabila Rafa Syafira** (5027251059)
> 2. **Arjunina Maqbulin Usman** (5027251007)
> 3. **Naila Anggun Eka Rizqy** (5027251122)
> 4. **Malikha Syarifa Dewi** (5027251032)

## Deskripsi Proyek

Proyek ini merupakan pengembangan backend untuk sistem **Rental Motor**, yang dibangun menggunakan **FastAPI** sebagai framework utama dan **Swagger UI** sebagai antarmuka dokumentasi serta pengujian API. Backend ini dirancang untuk terhubung dengan dua jenis basis data sekaligus, yaitu **MySQL** untuk data relasional dan **MongoDB** untuk data non-relasional (data koleksi).

## Struktur Basis Data

### Tabel Relasional (MySQL)

Basis data relasional digunakan untuk menyimpan data inti operasional rental motor, dengan tabel dan relasi sebagai berikut:

**cabang** — tabel induk yang menyimpan data cabang rental motor, tidak memiliki *foreign key*.

**karyawan** — memiliki *foreign key* `id_cabang`.
```
cabang  1 ----- N  karyawan
```

**pengguna** — tabel independen yang menyimpan data pelanggan/pengguna layanan rental, tidak memiliki *foreign key*.

**kendaraan** — memiliki *foreign key* `id_cabang`.
```
cabang  1 ----- N  kendaraan
```

**penyewaan** — memiliki *foreign key* `id_pengguna`, `id_kendaraan`, dan `id_karyawan`.
```
pengguna   1 ----- N  penyewaan
kendaraan  1 ----- N  penyewaan
karyawan   1 ----- N  penyewaan
```

**pengembalian** — memiliki *foreign key* `id_penyewaan` dan `id_karyawan`.
```
penyewaan  1 ----- 1  pengembalian
karyawan   1 ----- N  pengembalian
```

**pembayaran** — memiliki *foreign key* `id_penyewaan`.
```
penyewaan  1 ----- 1  pembayaran
```

**denda** — memiliki *foreign key* `id_pengembalian` dan `id_karyawan`.
```
pengembalian  1 ----- N  denda
karyawan      1 ----- N  denda
```

### Data Koleksi (MongoDB)

Basis data non-relasional digunakan untuk menyimpan data yang bersifat lebih dinamis dan tidak terstruktur secara kaku, meliputi:

- **laporan_kondisi** — menyimpan laporan kondisi kendaraan.
- **log_aktivitas** — menyimpan jejak aktivitas pengguna maupun sistem.
- **maintenance** — menyimpan data pemeliharaan/perawatan kendaraan.

## Struktur Folder Proyek

```
Backend_RentalMotor/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── sql_connection.py
│   │   └── mongo_connection.py
│   │
│   ├── routes/
│   │   ├── cabang.py
│   │   ├── pengguna.py
│   │   ├── karyawan.py
│   │   ├── kendaraan.py
│   │   ├── penyewaan.py
│   │   ├── pengembalian.py
│   │   ├── pembayaran.py
│   │   └── denda.py
│   │
│   ├── schemas/
│   │   ├── cabang_schema.py
│   │   ├── pengguna_schema.py
│   │   ├── karyawan_schema.py
│   │   ├── kendaraan_schema.py
│   │   ├── penyewaan_schema.py
│   │   ├── pengembalian_schema.py
│   │   ├── pembayaran_schema.py
│   │   └── denda_schema.py
│   │
│   └── mongo/
│       ├── activity_log.py
│       ├── vehicle_condition.py
│       └── maintenance.py
│
├── .env
├── requirements.txt
├── DB
│   ├── sql.txt
│   └── mongodb.json
└── report.md
```

## Penjelasan Fungsi Tiap Folder

### Folder `app`

Folder ini merupakan inti dari aplikasi backend. File `main.py` di dalamnya berfungsi sebagai *entry point* yang menjalankan aplikasi FastAPI, termasuk inisialisasi server, pendaftaran seluruh *router*, dan konfigurasi awal lainnya.

### Folder `core`

Folder ini berisi komponen-komponen dasar yang mendukung jalannya aplikasi secara keseluruhan:

- `config.py` mengatur konfigurasi umum aplikasi, seperti variabel lingkungan dan parameter global.
- `sql_connection.py` menangani koneksi ke basis data MySQL.
- `mongo_connection.py` menangani koneksi ke basis data MongoDB.

### Folder `routes`

Folder ini berisi definisi *endpoint* API untuk setiap entitas dalam sistem. Setiap file merepresentasikan satu modul fitur, seperti `cabang.py` untuk endpoint terkait data cabang, `pengguna.py` untuk data pengguna, dan seterusnya untuk `karyawan`, `kendaraan`, `penyewaan`, `pengembalian`, `pembayaran`, dan `denda`. Setiap *route* menangani permintaan HTTP (GET, POST, PUT, DELETE) yang berkaitan dengan entitas masing-masing.

### Folder `schemas`

Folder ini berisi definisi struktur data (model) menggunakan Pydantic, yang berfungsi untuk validasi data masuk maupun keluar pada setiap endpoint. Setiap file skema berpasangan dengan modul route yang sesuai, misalnya `cabang_schema.py` mendefinisikan struktur data untuk entitas cabang, dan seterusnya untuk seluruh entitas relasional lainnya.

### Folder `mongo`

Folder ini berisi logika dan model untuk berinteraksi dengan koleksi-koleksi pada MongoDB. File `activity_log.py` menangani data log aktivitas, `vehicle_condition.py` menangani data laporan kondisi kendaraan, dan `maintenance.py` menangani data pemeliharaan kendaraan.

## Spesifikasi Business Logic per Endpoint

Bagian ini menjelaskan aturan validasi, penanganan error, dan logika bisnis yang diterapkan pada setiap operasi CRUD (GET, POST, PATCH, DELETE) untuk masing-masing tabel:

---

### Tabel Pengguna
**GET**
- GET all — jika data kosong, pesan "data pengguna kosong"
- Berdasarkan id — jika tidak ada, pesan "id not found"
- Berdasarkan nama lengkap (`%LIKE%`) — jika tidak ditemukan, pesan "nama tidak ditemukan"
- Berdasarkan tahun kadaluarsa SIM — jika tidak ditemukan, pesan "not found"
- Berdasarkan rentang tahun kadaluarsa SIM — jika tidak ditemukan, pesan "not found"
- Berdaarkan status verifikasi (dropdown enum) — jika tidak ditemukan, pesan "not found"
- `tanggal_kadaluarsa_sim` harus berformat *date*, jika tidak sesuai dikembalikan pesan error
- `nomor_telepon` harus berupa angka

**POST**
- Nomor kartu identitas dan nomor SIM harus berupa angka dan dipastikan unik sebelum input; jika tidak unik, pesan "Kartu identitas duplikat!" atau "Nomor SIM duplikat!"
- Kartu identitas wajib 16 digit, jika tidak dikembalikan pesan error
- Error handling jika nama lengkap kosong namun mengandung karakter spasi
- Panjang nomor telepon harus 10–15 digit
- Seluruh elemen wajib diisi (*not null*); jika ada yang kurang, pesan "Masukkan informasi secara lengkap!"
- `tanggal_kadaluarsa_sim` harus berformat *date* dan maksimal 5 tahun dari tanggal hari ini; jika tidak memenuhi, data tetap diinput dengan pesan "Kartu SIM tidak valid!", dan *trigger* `AFTER INSERT` mengubah `status_verifikasi` menjadi `ditolak`
- Jika `tanggal_kadaluarsa_sim` sudah lewat tanggal hari ini, data tetap diinput dengan pesan "Kartu SIM kadaluarsa!", dan *trigger* `AFTER INSERT` mengubah `status_verifikasi` menjadi `expired`
- `nomor_telepon` harus berupa angka, disertai error handling
- `status_verifikasi` harus sesuai enum, jika tidak dikembalikan pesan error

**PATCH**
- Pencarian berdasarkan id saja; jika tidak ada, pesan "id not found"
- Modifikasi bersifat dinamis (satu, beberapa, atau seluruh kolom) dengan aturan validasi serupa POST:
  - Kartu identitas dan nomor SIM harus angka dan unik; jika tidak, pesan "Kartu identitas duplikat!" atau "Nomor SIM duplikat!"
  - Kartu identitas wajib 16 digit, jika tidak dikembalikan pesan error
  - Error handling jika nama lengkap kosong namun mengandung karakter spasi
  - Panjang nomor telepon 10–15 digit, disertai error handling
  - `tanggal_kadaluarsa_sim` setelah edit harus berada di antara hari ini hingga 5 tahun ke depan, jika tidak pesan "tanggal kadaluarsa tidak valid!"
  - `nomor_telepon` harus berupa angka, disertai error handling
  - `status_verifikasi` harus sesuai enum, jika tidak dikembalikan pesan error
  - Field yang tidak ada di tabel, pesan "field tidak valid"
- Jika `nomor_sim` diubah ke nilai miliknya sendiri, diperbolehkan (tidak dianggap duplikat)
- `id_pengguna` tidak boleh diupdate
- Jika update berhasil, pesan "Data pengguna berhasil diperbarui!"

**DELETE**
- Tidak boleh delete tanpa filter karena seluruh data akan terhapus
- Delete berdasarkan ID
- Output: "Not found" atau "Deleted"

---

### Tabel Cabang

**GET**
- GET all — jika data kosong, pesan "data pengguna kosong"
- Berdasarkan id — jika tidak ditemukan, pesan "id not found"
- Berdasarkan kota — jika tidak ditemukan, pesan "Not found!"

**POST**
- Seluruh elemen wajib diisi (*not null*); jika ada elemen yang kurang atau kosong, pesan "Masukkan informasi secara lengkap!"
- Error handling jika `nama_cabang` atau `kota` kosong namun hanya berisi karakter spasi
- Nama cabang harus unik per kota untuk menghindari duplikasi; jika sudah ada, pesan "Nama cabang di kota tersebut sudah terdaftar!"

**PATCH**
- Seluruh elemen wajib diisi, jika tidak pesan "Masukkan informasi secara lengkap!"
- Nama cabang wajib diisi, tidak boleh hanya spasi kosong, jika kosong dikembalikan error handling
- Tidak boleh input nama cabang yang sama dengan yang sudah ada di database, pesan "Nama cabang telah dipakai!"
- `id_pengguna` tidak boleh diubah; jika field tersebut disertakan, pesan "id pengguna tidak boleh diubah!"
- Jika update berhasil, pesan "Data pengguna berhasil diperbarui!"

**DELETE**
- Jika ID yang ingin dihapus tidak ditemukan, pesan "ID not found"
- Jika cabang masih memiliki entri karyawan, pesan "Tidak bisa hapus cabang, masih ada karyawan terkait!"
- Jika cabang masih memiliki entri kendaraan, pesan "Tidak bisa hapus cabang, masih ada kendaraan terkait!"
- Jika berhasil terhapus, pesan "Data cabang berhasil dihapus!"

---

### Tabel Penyewaan

**GET**
- GET all — jika data kosong, pesan "data penyewaan kosong"
- Berdasarkan `id_penyewaan` — jika tidak ada, pesan "Not found!"
- Berdasarkan `id_pengguna` — jika tidak ada, pesan "Not found!"
- Berdasarkan `id_kendaraan` — jika tidak ada, pesan "Not found!"
- Berdasarkan `id_karyawan` — jika tidak ada, pesan "Not found!"
- Berdasarkan rentang `waktu_selesai_rencana`, `waktu_kembali_up`, dan `waktu_kembali_down`
- Berdasarkan status penyewaan (dropdown)
- Setiap parameter id harus berupa integer, jika tidak pesan "id harus berupa angka!"
- Rentang `waktu_selesai_rencana`, `date_kembali_up`, dan `date_kembali_down` harus berformat *date*, jika tidak pesan "Gunakan format YYYY-MM-DD"
- Dicek apakah id pengguna yang diinput sudah terverifikasi; jika belum, pesan "Input gagal, pengguna belum terverifikasi"

**POST**
- Seluruh elemen wajib diisi (*not null*); jika ada yang kurang atau kosong, pesan "Masukkan informasi secara lengkap!"
- `id_penyewaan` tidak disertakan dalam request karena bersifat *auto increment*
- Jika pengguna yang sama sudah memiliki penyewaan aktif pada database, pesan "pengguna masih memiliki penyewaan aktif"
- `id_pengguna` harus terdaftar dan terverifikasi; jika tidak terdaftar, pesan "Pengguna tidak terdaftar", jika belum terverifikasi, pesan "Pengguna tidak terverifikasi"
- `id_kendaraan` harus ada dan berstatus tersedia; jika tidak ada atau statusnya bukan "tersedia", pesan "Kendaraan tidak tersedia!"
- Karyawan dan kendaraan harus berasal dari cabang yang sama, jika tidak pesan "Karyawan dan kendaraan tidak berasal dari cabang yang sama!"
- Format tanggal tetap divalidasi secara manual untuk mencegah error
- Status penyewaan hanya menerima input "aktif" (status "selesai" ditangani trigger pengembalian, status "dibatalkan" ditangani via PATCH)

**PATCH**
- Pencarian berdasarkan id saja; jika tidak ada, pesan "id not found"
- Modifikasi bersifat dinamis (satu, beberapa, atau seluruh data) dengan aturan validasi serupa POST:
  - `id_penyewaan` tidak boleh diubah, pesan "id_penyewaan tidak boleh diubah!"
  - `id_pengguna` jika tidak ada, pesan "id_pengguna tidak terdaftar!"
  - `id_pengguna` harus terverifikasi, jika tidak pesan "Pengguna tidak terverifikasi"
  - `id_kendaraan` jika tidak ada, pesan "id_kendaraan tidak terdapat dalam entri!"
  - `id_kendaraan` harus berstatus tersedia, jika tidak pesan "Kendaraan tidak tersedia!"
  - `id_karyawan` jika tidak ada, pesan "id_karyawan tidak terdapat dalam entri!"
  - Karyawan dan kendaraan harus berasal dari cabang yang sama, jika tidak pesan "Karyawan dan kendaraan tidak berasal dari cabang yang sama!"
  - Format tanggal tetap divalidasi secara manual
  - Status penyewaan tetap diinput biasa, namun jika selain enum yang ditentukan, pesan "Pilih salah satu dari status penyewaan berikut : aktif, dibatalkan"
  - Status penyewaan yang sudah "selesai" tidak boleh diubah

**DELETE**
- Tidak boleh delete tanpa filter karena seluruh data akan terhapus
- Pencarian berdasarkan ID; jika tidak ditemukan, pesan "ID not found"
- Jika penyewaan masih memiliki entri pada tabel pengembalian, pesan "Tidak bisa hapus penyewaan, masih ada pengembalian terkait!"
- Jika penyewaan masih memiliki entri pada tabel pembayaran, pesan "Tidak bisa hapus penyewaan, masih ada pembayaran terkait!"
- Jika berhasil terhapus, pesan "Data penyewaan berhasil dihapus!"

---

### Tabel Pengembalian

**GET**
- GET all — jika data kosong, pesan "data pengembalian kosong"
- Berdasarkan `id_pengembalian` — jika tidak ada, pesan "Not found!"
- Berdasarkan `id_penyewaan` — jika tidak ada, pesan "Not found!"
- Berdasarkan `id_karyawan` — jika tidak ada, pesan "Not found!"
- Berdasarkan rentang `waktu_pengembalian` (`date_return_up` dan `date_return_down`) — jika tidak ada, pesan "Not found!"
- Setiap parameter id harus berupa integer, jika tidak pesan "id harus berupa angka!"
- Rentang `waktu_pengembalian` harus berformat *date*, jika tidak pesan "Gunakan format YYYY-MM-DD"

**POST**
- Seluruh field wajib diisi; jika ada yang kurang atau kosong, pesan "Masukkan informasi secara lengkap!"
- `id_pengembalian` tidak disertakan dalam request karena bersifat *auto increment* dari MySQL
- `id_penyewaan` harus berupa angka
- Jika `id_penyewaan` yang diinput statusnya sudah "selesai", input ditolak dengan pesan "ID penyewaan tersebut telah selesai!"
- Jika `id_penyewaan` tidak ada di tabel penyewaan, pesan "Tidak ada entri dengan id penyewaan terkait!"
- `id_karyawan` harus berupa angka
- Jika `id_karyawan` tidak terdaftar pada tabel karyawan, pesan "Karyawan tidak terdaftar!"
- Cek `id_karyawan` pada penyewaan terkait dibandingkan dengan `id_karyawan` yang diinput (berdasarkan informasi cabang di tabel karyawan); keduanya harus berasal dari cabang yang sama, jika tidak pesan "Karyawan pengembalian harus berasal dari cabang yang sama dengan karyawan penyewaan!"
- Waktu pengembalian harus berformat *date*, jika tidak pesan "Waktu pengembalian harus menggunakan format YYYY-MM-DD"
- Waktu pengembalian tidak boleh kurang dari waktu mulai pada tabel penyewaan, jika tidak pesan "Masukkan tanggal pengembalian setelah tanggal mulai penyewaan!"
- Kondisi kendaraan bebas diisi oleh user, namun wajib terisi dan bukan spasi kosong, jika tidak pesan "Kondisi kendaraan harus diisi!"
- Jika berhasil, pesan "Data pengembalian berhasil ditambahkan"
- *Trigger* `AFTER INSERT` `ubah_status_setelah_pengembalian`: jika POST berhasil, status penyewaan terkait berubah jadi "selesai" dan status kendaraan terkait berubah jadi "tersedia"
- *Trigger* `AFTER INSERT` `denda_keterlambatan`: jika `waktu_pengembalian` lebih dari `waktu_selesai_rencana`, sistem menyisipkan data ke tabel denda (`id_pengembalian`, `id_karyawan`, `alasan_denda`, `nominal_denda`, `keterangan`) — `id_pengembalian` dan `id_karyawan` menyesuaikan data pengembalian yang baru diinput, `alasan_denda` berisi "keterlambatan_pengembalian", `nominal_denda` dihitung Rp100.000 per hari keterlambatan, dan `keterangan` diisi "-"

**PATCH**
- Pencarian berdasarkan id saja; jika tidak ada, pesan "id not found"
- Modifikasi bersifat dinamis dengan aturan validasi serupa POST, namun hanya `id_karyawan` dan kondisi kendaraan yang dapat diubah:
  - `id_pengembalian` tidak boleh diubah
  - `id_karyawan` harus berupa angka
  - Jika `id_karyawan` tidak terdaftar pada tabel karyawan, pesan "Karyawan tidak terdaftar!"
  - Cek `id_karyawan` pada penyewaan terkait dibandingkan dengan `id_karyawan` yang diinput (berdasarkan informasi cabang di tabel karyawan); keduanya harus berasal dari cabang yang sama, jika tidak pesan "Karyawan pengembalian harus berasal dari cabang yang sama dengan karyawan penyewaan!"
  - Kondisi kendaraan bebas diisi oleh user, namun wajib terisi dan bukan spasi kosong, jika tidak pesan "Kondisi kendaraan harus diisi!"

**DELETE**
- Tidak boleh delete tanpa filter karena seluruh data akan terhapus
- Pencarian berdasarkan ID; jika tidak ditemukan, pesan "ID not found"
- Jika pengembalian masih memiliki entri pada tabel denda, pesan "Tidak bisa hapus pengembalian, masih ada denda terkait!"
- Jika berhasil terhapus, pesan "Data penyewaan berhasil dihapus!"

---

### Tabel Pembayaran

**GET**
- GET all — jika data kosong, pesan "Data pembayaran kosong"
- Berdasarkan id_pembayaran — jika tidak ada, pesan "ID pembayaran tidak ditemukan"
- Berdasarkan id_penyewaan — jika tidak ada, pesan "ID penyewaan tidak ditemukan"
- Berdasarkan tanggal_transaksi — jika tidak ada, pesan "Tanggal transaksi tidak ditemukan"
- Berdasarkan tahun_transaksi — jika tidak ada, pesan "Tahun transaksi tidak ditemukan"
- Berdasarkan metode_pembayaran (dropdown/enum) — jika tidak ada, pesan "Metode pembayaran tidak ditemukan"
- Berdasarkan status_pembayaran (dropdown/enum) — jika tidak ada, pesan "Status pembayaran tidak ditemukan"
- Berdasarkan jumlah_pembayaran — jika tidak ada, pesan "Jumlah pembayaran tidak ditemukan"
- Setiap parameter id (id_pembayaran, id_penyewaan), dan tahun_transaksi harus berupa angka (integer).
- tanggal_transaksi harus berformat date (YYYY-MM-DD), jika tidak sesuai maka sistem akan mengembalikan pesan error validasi bawaan.
- jumlah_pembayaran harus berupa angka desimal (float).

**POST**
- Seluruh elemen wajib diisi (not null); validasi tipe data akan ditangani oleh schema.
- Mengecek ketersediaan id_penyewaan di tabel penyewaan — jika tidak ada, pesan "ID penyewaan tidak ditemukan"
- Dicek apakah status penyewaan yang bersangkutan adalah "aktif" — jika tidak, pesan "Pembayaran hanya bisa dilakukan untuk penyewaan yang masih aktif!"
- Dipastikan bahwa satu penyewaan hanya bisa memiliki satu pembayaran (mencegah duplikat) — jika sudah ada, pesan "Penyewaan ini sudah memiliki pembayaran!"
- tanggal_transaksi harus berformat date dan tidak boleh melebihi tanggal mulai sewa — jika melebihi, pesan "Tanggal transaksi tidak boleh melebihi tanggal mulai sewa!"
- Sistem akan otomatis menghitung jumlah_pembayaran dengan mengalikan tarif kendaraan per hari dengan jumlah hari penyewaan.
- Jika data berhasil ditambahkan, dikembalikan pesan "Data pembayaran berhasil ditambahkan" beserta hasil perhitungan jumlah pembayarannya.

**PATCH**
- Berdasarkan id_pembayaran — jika tidak ada di database, pesan "ID pembayaran tidak ditemukan"
- Field yang diizinkan untuk di-update hanya tanggal_transaksi, metode_pembayaran, dan status_pembayaran — jika menginputkan field selain itu, pesan "field tidak valid"
- tanggal_transaksi harus berformat date — jika formatnya salah, pesan "Format tanggal transaksi tidak valid
- Jika tanggal_transaksi diubah, nilainya tetap tidak boleh melebihi tanggal mulai sewa — jika melanggar, pesan "Tanggal transaksi tidak boleh melebihi tanggal mulai sewa!"
- metode_pembayaran harus sesuai pilihan enum (transfer_bank, qris, tunai, kartu_debit, kartu_kredit) — jika tidak sesuai, pesan "Metode pembayaran tidak sesuai pilihan yang tersedia"
- status_pembayaran harus sesuai pilihan enum (lunas, gagal) — jika tidak sesuai, pesan "Status pembayaran tidak sesuai pilihan yang tersedia"
- Jika berhasil diubah, pesan "Data pembayaran berhasil diperbarui!"

**DELETE**
- Berdasarkan id_pembayaran — jika tidak ada di database, pesan "ID pembayaran tidak ditemukan"
- Menghapus data pembayaran secara permanen dari database.
- Jika berhasil, pesan "Data pembayaran berhasil dihapus!"

---

## Tabel Denda

**GET**
- Hanya mengizinkan satu parameter pencarian pada satu waktu — jika lebih dari satu filter dikirimkan, pesan "Gunakan satu filter pencarian saja"
- GET all — jika data kosong, pesan "Data denda kosong"
- Berdasarkan id_denda — jika tidak ada, pesan "ID tidak ditemukan"
- Berdasarkan id_pengembalian — sistem memvalidasi ketersediaan ID di tabel pengembalian; jika tidak ada, pesan "ID pengembalian tidak ditemukan". Jika ID ada namun belum memiliki denda, pesan "Data denda tidak ditemukan"
- Berdasarkan alasan_denda (dropdown enum: kerusakan_kendaraan, pelanggaran_lalu_lintas, keterlambatan_pengembalian) — jika tidak ada, pesan "Data tidak ditemukan"
- Berdasarkan keterangan (pencarian kata/LIKE) — jika kata tidak ditemukan, pesan "Keterangan tidak ditemukan"

**POST**
- Seluruh elemen wajib diisi kecuali keterangan (id_pengembalian, id_karyawan, alasan_denda, nominal_denda); jika ada yang kurang, pesan "Masukkan informasi secara lengkap!"
- Pilihan alasan_denda dibatasi untuk input manual (enum: kerusakan_kendaraan, pelanggaran_lalu_lintas).
- nominal_denda harus lebih besar dari 0 — jika kurang atau sama dengan 0, pesan "Nominal denda harus lebih dari 0!"
- Menghindari spasi kosong: Jika keterangan diisi, tidak boleh hanya berisi karakter spasi/kosong — jika melanggar, pesan "Keterangan tidak valid!"
- Mengecek ketersediaan id_pengembalian di tabel pengembalian — jika tidak terdaftar, pesan "ID pengembalian tidak ditemukan!"
- Mengecek ketersediaan id_karyawan di tabel karyawan — jika tidak terdaftar, pesan "ID karyawan tidak ditemukan!"
- Mencegah duplikasi data: Sistem memastikan satu transaksi pengembalian tidak boleh memiliki alasan denda yang sama lebih dari satu kali — jika duplikat, pesan "Alasan denda sudah terdaftar untuk pengembalian ini!"
- Jika data berhasil ditambahkan, dikembalikan pesan "Data denda berhasil ditambahkan" beserta id_denda yang baru dibuat.

**PATCH**
- Berdasarkan id_denda — jika tidak ada di database, pesan "ID not found"
- Field id_denda dan id_pengembalian dikunci dan tidak diizinkan untuk di-update.
- Field yang diizinkan untuk di-update hanya id_karyawan, alasan_denda, nominal_denda, dan keterangan — jika ada field selain itu, pesan "field tidak valid"
- Jika id_karyawan diubah, divalidasi ke tabel karyawan — jika tidak ada, pesan "ID karyawan tidak ditemukan!"
- Jika nominal_denda diubah, nilainya harus lebih dari 0 — jika melanggar, pesan "Nominal denda harus lebih dari 0!"
- Jika keterangan diubah, nilainya tidak boleh hanya berisi spasi kosong — jika melanggar, pesan "Keterangan tidak valid!"
- Jika alasan_denda diubah (hanya menerima kerusakan_kendaraan atau pelanggaran_lalu_lintas), sistem kembali mengecek duplikasi pada ID pengembalian tersebut — jika duplikat, pesan "Alasan denda sudah terdaftar untuk pengembalian ini!"
- Jika berhasil diperbarui, pesan "Data denda berhasil diperbarui!"

**DELETE**
- Berdasarkan id_denda — jika tidak ada di database, pesan "ID not found"
- Menghapus data denda secara permanen dari tabel database.
- Jika berhasil, pesan "Data denda berhasil dihapus!"

---

##Tabel Kendaraan 

**GET**
- GET all- jika data kosong, pesan "Data kendaraan kosong"
- Berdasarkan id_kendaraan - jika tidak ditemukan, pesan "ID tidak ditemukan" 
- Berdasarkan id_cabang - jika tidak ditemukan, pesan "Cabang tidak ditemukan"
- Berdasarkan merek - jika tidak ditemukan, pesan "Merek tidak ditemukan"
- Berdasarkan model - jika tidak ditemukan, pesan "Model tidak ditemukan"
- Berdasarkan nomor_polisi - jika tidak ditemukan, pesan "Nomor polisi tidak ditemuka"
- Berdasarkan tahun - jika tidak ditemukan, pesan "Tidak ada kendaraan untuk tahun tersebut"
- Berdasarkan renatang tahun_awal dan tahun_akhir, jika `tahun_awal` > `tahun_akhir`, pesan "Rentang tahun tidak valid!", jika tidak ditemukan, pesan "Tidak ada kendaraan pada rentang tahun tersebut"
- Berdasarkan rentang tarif tarif_min dan tarif_max, jika `tarif_min` > `tarif_max`, pesan "Rentang tarif tidak valid!", jika tidak ditemukan, pesan "Tidak ada kendaraan pada rentang tarif tersebut"
- Berdasarkan status_kendaran terdapat enum (`tersedia`, `disewa`, `dalam_perbaikan`), jika tidak ditemukan, pesan "Tidak ada kendaraan dengan status tersebut" 

**POST**
- Seluruh elemen wajib diisi (not null), jika ada yang kurang, pesan "Masukkan informasi secara lengkap!"
-  Berdasarkan merek tidak boleh kosong / hanya spasi, jika tidak pesan "Merek tidak boleh kosong!"
- Berdasarkan model tidak boleh kosong / hanya spasi, jika tidak pesan "Model tidak boleh kosong!"
- Berdasarkan nomor_polisi tidak boleh kosong / hanya spasi, jika tidak pesan "Nomor polisi tidak boleh kosong!"
- Berdasarkan tahun harus berada di antara 1990 hingga tahun berjalan saat ini, jika tidak pesan "Tahun tidak valid!"
- Berdasarkan tarif_per_hari harus berupa angka positif (lebih dari 0), jika tidak pesan "Tarif harus berupa angka positif!"
- Berdasarkan id_cabang harus terdaftar di tabel cabang, jika tidak pesan "Cabang tidak ditemukan!"
- Berdasarkan nomor_polisi harus unik; jika sudah terdaftar, pesan "Nomor polisi sudah terdaftar!"
- Berdasarkan status_kendaraan harus sesuai enum (`tersedia`, `disewa`, `dalam_perbaikan`)
- Jika berhasil ditambahkan, pesan "Data kendaraan berhasil ditambahkan!"

**PATCH**
- Pencarian berdasarkan id_kendaraan saja - jika tidak ada, pesan "ID tidak ditemukan"
- Bisa update satu field, beberapa field, atau seluruh field sekaligus, sesuai dengan kebutuhan, tidak harus mengisi semuanya misal (satu, beberapa, atau seluruh kolom)
- Berdasarkan merek tidak boleh kosong / hanya spasi, jika tidak pesan "Merek tidak boleh kosong!"
- Berdasarkan model tidak boleh kosong / hanya spasi, jika tidak pesan "Model tidak boleh kosong!"
- Berdasarkan nomor_polisi tidak boleh kosong / hanya spasi, jika tidak pesan "Nomor polisi tidak boleh kosong!"
- Berdasarkan nomor_polisi harus unik (kecuali milik sendiri); jika sudah dipakai kendaraan lain, pesan "Nomor polisi sudah terdaftar!"
- Berdasarkan tahun harus berada di antara 1990 hingga tahun berjalan saat ini, jika tidak pesan "Tahun tidak valid!"
- Berdasarkan tarif_per_hari harus berupa angka positif (lebih dari 0), jika tidak pesan "Tarif harus berupa angka positif!"
- Berdasarkan status_kendaraan harus sesuai enum (`tersedia`, `disewa`, `dalam_perbaikan`), jika tidak pesan "Status kendaraan tidak valid!"
- Berdasarkan id_cabang harus terdaftar di tabel cabang, jika tidak pesan "Cabang tidak ditemukan!"
- Jika update berhasil, pesan "Data kendaraan berhasil diperbarui!"

**DELETE**
- Tidak boleh delete tanpa filter karena seluruh data akan terhapus 
- Delete berdasarkan id_kendaraan - jika tidak ada, pesan "ID tidak ditemukan" 
- Cek Foreign Key di tabel penyewaan — jika id_kendaraan masih digunakan di data penyewaan, pesan "Tidak bisa hapus kendaraan, masih ada data penyewaan terkait!"
- Jika hapus kendaraan berhasil, pesan "Data Kendaraan berhasil dihapus!"

---

# Dokumentasi MongoDB - Sistem Rental Motor

## Struktur Collection MongoDB

Sistem rental motor ini menggunakan **dua jenis database** secara bersamaan (*polyglot persistence*):
- **MySQL** → data transaksional utama (cabang, karyawan, pengguna, kendaraan, penyewaan, pembayaran, pengembalian, denda)
- **MongoDB** → data yang bersifat fleksibel, nested, dan variatif

Bagian yang dikerjakan adalah perancangan dan implementasi **3 collection MongoDB** beserta backend API-nya.

---

## Collection 1: `laporan_kondisi`

### Latar Belakang
Tabel `pengembalian` di MySQL hanya menyimpan field `kondisi_kendaraan` berupa string sederhana. Padahal dalam praktiknya, laporan kondisi kendaraan membutuhkan pencatatan per bagian motor (body, spion, ban, lampu, dll) yang jumlah dan strukturnya berbeda-beda tiap kendaraan. Data ini tidak efisien jika dipaksakan ke dalam tabel relasional.

### Keputusan Desain
- **Embedding** untuk array `kondisi` karena data kondisi per bagian selalu dibaca bersama laporannya
- **Referencing** untuk `id_penyewaan` dan `id_kendaraan` karena data aslinya sudah ada di tabel MySQL

### Struktur Document
```json
{
  "id_penyewaan": 1,
  "id_kendaraan": 1,
  "tipe": "check-in",
  "tanggal_mulai": "2026-06-01",
  "tanggal_selesai": "2026-06-03",
  "kondisi": [
    {
      "bagian": "spion kanan",
      "status": "rusak",
      "deskripsi": "spion kanan pecah"
    },
    {
      "bagian": "body depan",
      "status": "normal",
      "deskripsi": "tidak ada kerusakan"
    }
  ]
}
```

### Fitur API
| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/laporan-kondisi/` | Tampilkan semua laporan, bisa filter by `id_penyewaan`, `id_kendaraan`, `tipe`, `status_kondisi`, `tanggal_mulai`, `tanggal_selesai` |
| POST | `/laporan-kondisi/` | Tambah laporan kondisi baru |
| PATCH | `/laporan-kondisi/{id}` | Update laporan berdasarkan MongoDB `_id` |
| DELETE | `/laporan-kondisi/{id}` | Hapus laporan berdasarkan MongoDB `_id` |

---

## Collection 2: `riwayat_maintenance`

### Latar Belakang
Data maintenance kendaraan tidak ada di ERD MySQL karena strukturnya sangat variatif — tiap servis bisa melibatkan komponen yang berbeda-beda, dengan tindakan dan biaya yang berbeda pula. Jumlah komponen yang ditangani tidak tetap tiap maintenance. Jika dipaksakan ke SQL, dibutuhkan tabel tambahan yang kompleks padahal data ini selalu dibaca bersama.

### Keputusan Desain
- **Embedding** untuk array `detail` karena komponen yang diservis selalu dibaca bersama data maintenance
- **Referencing** untuk `id_kendaraan` dan `id_karyawan` karena data aslinya ada di tabel MySQL

### Struktur Document
```json
{
  "id_kendaraan": 5,
  "id_karyawan": 3,
  "tanggal": "2026-01-15",
  "jenis_maintenance": "perbaikan_berat",
  "status": "dalam_proses",
  "detail": [
    {
      "komponen": "aki motor",
      "tindakan": "ganti",
      "keterangan": "aki soak, diganti aki baru GS Astra",
      "biaya": 245000
    },
    {
      "komponen": "sistem kelistrikan",
      "tindakan": "perbaiki",
      "keterangan": "urut kabel bodi jalur starter",
      "biaya": 50000
    }
  ],
  "total_biaya": 295000,
  "catatan_tambahan": "menunggu proses pemasangan bodi motor kembali"
}
```

### Fitur API
| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/maintenance/` | Tampilkan semua maintenance, bisa filter by `id_kendaraan`, `id_karyawan`, `jenis_maintenance`, `status`, `tanggal` |
| POST | `/maintenance/` | Tambah data maintenance baru |
| PATCH | `/maintenance/{id}` | Update maintenance berdasarkan MongoDB `_id` |
| DELETE | `/maintenance/{id}` | Hapus maintenance berdasarkan MongoDB `_id` |

---

## Collection 3: `log_aktivitas`

### Latar Belakang
Sistem membutuhkan **audit trail** — catatan semua aksi INSERT, UPDATE, DELETE yang terjadi pada tabel `penyewaan` dan `pengembalian`. Data log bersifat dinamis karena field `deskripsi` berbeda strukturnya tergantung jenis aksi dan tabel yang terlibat. Volume log juga tinggi dan tidak perlu di-JOIN dengan tabel lain, sehingga MongoDB lebih cocok daripada SQL.

### Keputusan Desain
- **Embedding** untuk field `karyawan` dan `deskripsi` karena selalu dibaca bersama log
- Log **tidak memiliki endpoint sendiri** — diisi otomatis setiap kali ada aksi di `routes/penyewaan.py` dan `routes/pengembalian.py`

### Struktur Document
```json
{
  "timestamp": "2026-06-16T10:30:00",
  "action": "insert",
  "tabel": "penyewaan",
  "karyawan": {
    "id_karyawan": 2,
    "nama": "Baskara Raditya",
    "jabatan": "Staff Admin"
  },
  "deskripsi": {
    "id_penyewaan": 7,
    "id_pengguna": 1,
    "id_kendaraan": 3,
    "waktu_mulai": "2026-06-16",
    "waktu_selesai_rencana": "2026-06-18",
    "status_penyewaan": "aktif"
  }
}
```

### Cara Kerja
Log tidak diisi manual oleh user. Setiap kali ada transaksi di MySQL (INSERT/UPDATE/DELETE penyewaan atau pengembalian), fungsi `log_aktivitas.insert_one()` otomatis dipanggil dari dalam routes SQL sehingga log tersimpan ke MongoDB secara real-time.

---

## Implementasi Backend

Backend menggunakan **FastAPI** dengan **PyMongo** untuk koneksi ke MongoDB.

Koneksi MongoDB dikelola di `core/mongo_connection.py`:
```python
from pymongo import MongoClient
from app.core.config import *

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
log_aktivitas = db["log_aktivitas"]
```

Konfigurasi disimpan di file `.env`:
```
MONGO_URI=mongodb://localhost:27017

MONGO_DB=rental_motor
```
---

## Justifikasi Pemilihan MongoDB

| Data | Alasan MongoDB |
|---|---|
| `laporan_kondisi` | Array kondisi variatif, jumlah bagian berbeda tiap kendaraan, tidak efisien di SQL |
| `riwayat_maintenance` | Array komponen variatif, jenis tindakan berbeda tiap servis, tidak efisien di SQL |
| `log_aktivitas` | Field deskripsi berbeda tiap jenis aksi, volume tinggi, tidak perlu di-JOIN |


| 2 | ID format tidak valid | `id=abc123` | `"Format ID tidak valid!"` |
| 3 | ID tidak ditemukan | `id=6a311c4b9842e48fc7abc999` | `"Data maintenance tidak ditemukan!"` |
