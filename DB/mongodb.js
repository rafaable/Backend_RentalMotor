// ============================================================
//  COLLECTION 1: laporan_kondisi
//  Berdasarkan tabel pengembalian (id 1,2,3) + tambahan check-in
// ============================================================

db = db.getSiblingDB("rental_motor");
db.laporan_kondisi.drop();
db.log_aktivitas.drop();
db.riwayat_maintenance.drop();

db.laporan_kondisi.insertMany([
  {
    "id_pengembalian": 1,
    "id_penyewaan": 1,
    "id_kendaraan": 1,
    "tipe": "check-in",
    "dicatat_pada": "2026-06-01",
    "dicatat_oleh_karyawan": 1,
    "kondisi": [
      { "bagian": "body depan", "status": "normal", "deskripsi": "tidak ada kerusakan", "foto_url": "https://storage.rental.com/checkin/p1_body_depan.jpg" },
      { "bagian": "body belakang", "status": "normal", "deskripsi": "tidak ada kerusakan", "foto_url": "https://storage.rental.com/checkin/p1_body_belakang.jpg" },
      { "bagian": "spion kiri", "status": "normal", "deskripsi": "terpasang dengan baik", "foto_url": null },
      { "bagian": "spion kanan", "status": "normal", "deskripsi": "terpasang dengan baik", "foto_url": null },
      { "bagian": "ban depan", "status": "normal", "deskripsi": "tekanan angin 32 psi", "foto_url": null },
      { "bagian": "ban belakang", "status": "normal", "deskripsi": "tekanan angin 30 psi", "foto_url": null },
      { "bagian": "lampu depan", "status": "normal", "deskripsi": "berfungsi normal", "foto_url": null }
    ]
  },
  {
    "id_pengembalian": 1,
    "id_penyewaan": 1,
    "id_kendaraan": 1,
    "tipe": "check-out",
    "dicatat_pada": "2026-06-03",
    "dicatat_oleh_karyawan": 1,
    "kondisi": [
      { "bagian": "body depan", "status": "normal", "deskripsi": "tidak ada kerusakan", "foto_url": "https://storage.rental.com/checkout/p1_body_depan.jpg" },
      { "bagian": "body belakang", "status": "normal", "deskripsi": "tidak ada kerusakan", "foto_url": "https://storage.rental.com/checkout/p1_body_belakang.jpg" },
      { "bagian": "spion kiri", "status": "normal", "deskripsi": "terpasang dengan baik", "foto_url": null },
      { "bagian": "spion kanan", "status": "normal", "deskripsi": "terpasang dengan baik", "foto_url": null },
      { "bagian": "ban depan", "status": "normal", "deskripsi": "tekanan angin 31 psi", "foto_url": null },
      { "bagian": "ban belakang", "status": "normal", "deskripsi": "tekanan angin 30 psi", "foto_url": null },
      { "bagian": "lampu depan", "status": "normal", "deskripsi": "berfungsi normal", "foto_url": null }
    ]
  },
  {
    "id_pengembalian": 2,
    "id_penyewaan": 3,
    "id_kendaraan": 6,
    "tipe": "check-in",
    "dicatat_pada": "2026-06-02",
    "dicatat_oleh_karyawan": 4,
    "kondisi": [
      { "bagian": "body depan", "status": "normal", "deskripsi": "tidak ada kerusakan", "foto_url": "https://storage.rental.com/checkin/p2_body_depan.jpg" },
      { "bagian": "spion kiri", "status": "normal", "deskripsi": "terpasang dengan baik", "foto_url": "https://storage.rental.com/checkin/p2_spion_kiri.jpg" },
      { "bagian": "body samping", "status": "normal", "deskripsi": "tidak ada goresan", "foto_url": "https://storage.rental.com/checkin/p2_body_samping.jpg" },
      { "bagian": "ban depan", "status": "normal", "deskripsi": "tekanan angin 32 psi", "foto_url": null },
      { "bagian": "ban belakang", "status": "normal", "deskripsi": "tekanan angin 30 psi", "foto_url": null }
    ]
  },
  {
    "id_pengembalian": 2,
    "id_penyewaan": 3,
    "id_kendaraan": 6,
    "tipe": "check-out",
    "dicatat_pada": "2026-06-03",
    "dicatat_oleh_karyawan": 4,
    "kondisi": [
      { "bagian": "body depan", "status": "normal", "deskripsi": "tidak ada kerusakan", "foto_url": "https://storage.rental.com/checkout/p2_body_depan.jpg" },
      { "bagian": "spion kiri", "status": "rusak", "deskripsi": "terdapat goresan pada spion kiri", "foto_url": "https://storage.rental.com/checkout/p2_spion_kiri.jpg" },
      { "bagian": "body samping", "status": "rusak", "deskripsi": "lecet ringan pada body samping kanan", "foto_url": "https://storage.rental.com/checkout/p2_body_samping.jpg" },
      { "bagian": "ban depan", "status": "normal", "deskripsi": "tekanan angin 31 psi", "foto_url": null },
      { "bagian": "ban belakang", "status": "normal", "deskripsi": "kondisi baik", "foto_url": null }
    ]
  },
  {
    "id_pengembalian": 3,
    "id_penyewaan": 5,
    "id_kendaraan": 11,
    "tipe": "check-in",
    "dicatat_pada": "2026-05-28",
    "dicatat_oleh_karyawan": 7,
    "kondisi": [
      { "bagian": "body depan", "status": "normal", "deskripsi": "kondisi baik", "foto_url": "https://storage.rental.com/checkin/p3_body_depan.jpg" },
      { "bagian": "spion kanan", "status": "normal", "deskripsi": "terpasang dengan baik", "foto_url": null },
      { "bagian": "lampu depan", "status": "normal", "deskripsi": "berfungsi normal", "foto_url": null },
      { "bagian": "ban depan", "status": "normal", "deskripsi": "tekanan angin 30 psi", "foto_url": null },
      { "bagian": "ban belakang", "status": "normal", "deskripsi": "tekanan angin 28 psi", "foto_url": null }
    ]
  },
  {
    "id_pengembalian": 3,
    "id_penyewaan": 5,
    "id_kendaraan": 11,
    "tipe": "check-out",
    "dicatat_pada": "2026-05-29",
    "dicatat_oleh_karyawan": 7,
    "kondisi": [
      { "bagian": "body depan", "status": "normal", "deskripsi": "kondisi baik", "foto_url": "https://storage.rental.com/checkout/p3_body_depan.jpg" },
      { "bagian": "spion kanan", "status": "normal", "deskripsi": "terpasang dengan baik", "foto_url": null },
      { "bagian": "lampu depan", "status": "normal", "deskripsi": "berfungsi normal", "foto_url": null },
      { "bagian": "ban depan", "status": "normal", "deskripsi": "tekanan angin 30 psi", "foto_url": null },
      { "bagian": "ban belakang", "status": "normal", "deskripsi": "tekanan angin 28 psi", "foto_url": null }
    ]
  },

]);



// ============================================================
//  COLLECTION 2: log_aktivitas
// ============================================================

db.log_aktivitas.insertMany([

  // ── Verifikasi SIM ──
{
    "tanggal": "2025-01-01",
    "dilakukan_oleh": { "id": 2, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 1, "nama_pengguna": "Aksa Sadajiwa", "status_baru": "terverifikasi" }
  },
  {
    "tanggal": "2025-01-02",
    "dilakukan_oleh": { "id": 2, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 2, "nama_pengguna": "Bumi Semesta", "status_baru": "terverifikasi" }
  },
  {
    "tanggal": "2025-01-03",
    "dilakukan_oleh": { "id": 2, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 3, "nama_pengguna": "Kala Argantara", "status_baru": "belum_diverifikasi" }
  },
  {
    "tanggal": "2025-01-04",
    "dilakukan_oleh": { "id": 2, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 4, "nama_pengguna": "Renjana Arutala", "status_baru": "expired" }
  },
  {
    "tanggal": "2025-01-05",
    "dilakukan_oleh": { "id": 2, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 5, "nama_pengguna": "Abisatya Hanasta", "status_baru": "terverifikasi" }
  },
  {
    "tanggal": "2025-01-06",
    "dilakukan_oleh": { "id": 5, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 6, "nama_pengguna": "Asmaralaya Citra", "status_baru": "terverifikasi" }
  },
  {
    "tanggal": "2025-01-07",
    "dilakukan_oleh": { "id": 5, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 7, "nama_pengguna": "Lintang Amreta", "status_baru": "terverifikasi" }
  },
  {
    "tanggal": "2025-01-08",
    "dilakukan_oleh": { "id": 5, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 8, "nama_pengguna": "Niskala Arunika", "status_baru": "belum_diverifikasi" }
  },
  {
    "tanggal": "2025-01-09",
    "dilakukan_oleh": { "id": 5, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 9, "nama_pengguna": "Raya Nayaka", "status_baru": "ditolak" }
  },
  {
    "tanggal": "2025-01-10",
    "dilakukan_oleh": { "id": 5, "tipe": "Staff Admin" },
    "aksi": "verifikasi_sim",
    "detail": { "id_pengguna": 10, "nama_pengguna": "Gendis Kirana", "status_baru": "terverifikasi" }
  },
  
  // ── Proses Pembayaran ──
{
    "tanggal": "2026-06-01",
    "dilakukan_oleh": { "id": 2, "tipe": "Staff Admin" },
    "aksi": "proses_pembayaran",
    "detail": {
      "id_pembayaran": 1,
      "id_penyewaan": 1,
      "metode_pembayaran": "transfer_bank",
      "jumlah_pembayaran": 100000.00,
      "status_pembayaran": "lunas"
    }
  },
  {
    "tanggal": "2026-06-10",
    "dilakukan_oleh": { "id": 2, "tipe": "Staff Admin" },
    "aksi": "proses_pembayaran",
    "detail": {
      "id_pembayaran": 2,
      "id_penyewaan": 2,
      "metode_pembayaran": "qris",
      "jumlah_pembayaran": 150000.00,
      "status_pembayaran": "lunas"
    }
  },
  {
    "tanggal": "2026-06-02",
    "dilakukan_oleh": { "id": 5, "tipe": "Staff Admin" },
    "aksi": "proses_pembayaran",
    "detail": {
      "id_pembayaran": 3,
      "id_penyewaan": 3,
      "metode_pembayaran": "tunai",
      "jumlah_pembayaran": 60000.00,
      "status_pembayaran": "lunas"
    }
  },
  {
    "tanggal": "2026-06-11",
    "dilakukan_oleh": { "id": 5, "tipe": "Staff Admin" },
    "aksi": "proses_pembayaran",
    "detail": {
      "id_pembayaran": 4,
      "id_penyewaan": 4,
      "metode_pembayaran": "transfer_bank",
      "jumlah_pembayaran": 255000.00,
      "status_pembayaran": "lunas"
    }
  },
  {
    "tanggal": "2026-05-28",
    "dilakukan_oleh": { "id": 8, "tipe": "Staff Admin" },
    "aksi": "proses_pembayaran",
    "detail": {
      "id_pembayaran": 5,
      "id_penyewaan": 5,
      "metode_pembayaran": "qris",
      "jumlah_pembayaran": 65000.00,
      "status_pembayaran": "lunas"
    }
  },
  {
    "tanggal": "2026-06-11",
    "dilakukan_oleh": { "id": 8, "tipe": "Staff Admin" },
    "aksi": "proses_pembayaran",
    "detail": {
      "id_pembayaran": 6,
      "id_penyewaan": 6,
      "metode_pembayaran": "tunai",
      "jumlah_pembayaran": 60000.00,
      "status_pembayaran": "lunas"
    }
  },

  // ── Proses Pengembalian ──
{
    "tanggal": "2026-06-03",
    "dilakukan_oleh": { "id": 3, "tipe": "Supervisor" },
    "aksi": "proses_pengembalian",
    "detail": { 
      "id_pengembalian": 1, 
      "id_penyewaan": 1, 
      "status_kondisi": "baik", 
      "ada_denda": false
    }
  },
  {
    "tanggal": "2026-06-03",
    "dilakukan_oleh": { "id": 6, "tipe": "Supervisor" },
    "aksi": "proses_pengembalian",
    "detail": { 
      "id_pengembalian": 2, 
      "id_penyewaan": 3, 
      "status_kondisi": "rusak_ringan", 
      "ada_denda": true
    }
  },
  {
    "tanggal": "2026-05-29",
    "dilakukan_oleh": { "id": 9, "tipe": "Supervisor" },
    "aksi": "proses_pengembalian",
    "detail": { 
      "id_pengembalian": 3, 
      "id_penyewaan": 5, 
      "status_kondisi": "baik", 
      "ada_denda": false
    }
  }

]);


// ============================================================
//  COLLECTION 3: riwayat_maintenance
// ============================================================

db.riwayat_maintenance.insertMany([

{
    "id_kendaraan": 1,
    "id_karyawan": 3,
    "tanggal": "2026-01-05",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli standar", "biaya": 65000 },
      { "komponen": "busi", "tindakan": "ganti", "keterangan": "busi baru NGK", "biaya": 25000 }
    ],
    "total_biaya": 90000,
    "catatan_tambahan": "mesin halus, siap jalan"
  },
  {
    "id_kendaraan": 2,
    "id_karyawan": 3,
    "tanggal": "2026-01-06",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli SPX2", "biaya": 85000 },
      { "komponen": "filter udara", "tindakan": "bersihkan", "keterangan": "dibersihkan pakai kompresor", "biaya": 15000 }
    ],
    "total_biaya": 100000,
    "catatan_tambahan": "motor siap pakai, kondisi prima"
  },
  {
    "id_kendaraan": 3,
    "id_karyawan": 2,
    "tanggal": "2026-01-10",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli Yamalube Matik", "biaya": 60000 },
      { "komponen": "v-belt", "tindakan": "cek", "keterangan": "kondisi masih layak", "biaya": 0 }
    ],
    "total_biaya": 60000,
    "catatan_tambahan": "aman digunakan pelajar"
  },
  {
    "id_kendaraan": 4,
    "id_karyawan": 3,
    "tanggal": "2026-01-12",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli matik besar", "biaya": 95000 },
      { "komponen": "oli gardan", "tindakan": "ganti", "keterangan": "ganti oli gardan", "biaya": 25000 },
      { "komponen": "kampas rem depan", "tindakan": "ganti", "keterangan": "ganti kampas baru", "biaya": 60000 }
    ],
    "total_biaya": 180000,
    "catatan_tambahan": "rem pakem, tarikan mantap"
  },
  {
    "id_kendaraan": 5,
    "id_karyawan": 3,
    "tanggal": "2026-01-15",
    "jenis_maintenance": "perbaikan_berat",
    "status": "sedang_berjalan",
    "detail": [
      { "komponen": "aki motor", "tindakan": "ganti", "keterangan": "aki soak, diganti aki baru GS Astra", "biaya": 245000 },
      { "komponen": "sistem kelistrikan", "tindakan": "perbaiki", "keterangan": "urut kabel bodi jalur starter", "biaya": 50000 }
    ],
    "total_biaya": 295000,
    "catatan_tambahan": "menunggu proses pemasangan bodi motor kembali"
  },
  {
    "id_kendaraan": 6,
    "id_karyawan": 6,
    "tanggal": "2026-01-05",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli MPX2", "biaya": 65000 },
      { "komponen": "roller CVT", "tindakan": "ganti", "keterangan": "ganti 1 set roller standar", "biaya": 75000 }
    ],
    "total_biaya": 140000,
    "catatan_tambahan": "tarikan gas sudah tidak gredek"
  },
  {
    "id_kendaraan": 7,
    "id_karyawan": 6,
    "tanggal": "2026-01-08",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli SPX2", "biaya": 85000 },
      { "komponen": "kampas rem belakang", "tindakan": "ganti", "keterangan": "kampas rem belakang baru", "biaya": 55000 }
    ],
    "total_biaya": 140000,
    "catatan_tambahan": "motor keluaran baru, mesin sangat prima"
  },
  {
    "id_kendaraan": 8,
    "id_karyawan": 5,
    "tanggal": "2026-01-11",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli Yamalube", "biaya": 65000 },
      { "komponen": "filter udara", "tindakan": "ganti", "keterangan": "ganti filter udara baru karena kotor", "biaya": 45000 }
    ],
    "total_biaya": 110000,
    "catatan_tambahan": "filtrasi udara optimal kembali"
  },
  {
    "id_kendaraan": 9,
    "id_karyawan": 6,
    "tanggal": "2026-01-14",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli mesin sport matik", "biaya": 95000 },
      { "komponen": "cairan radiator", "tindakan": "kuras", "keterangan": "kuras dan isi air radiator baru", "biaya": 35000 }
    ],
    "total_biaya": 130000,
    "catatan_tambahan": "suhu mesin stabil, siap sewa jarak jauh"
  },
  {
    "id_kendaraan": 10,
    "id_karyawan": 6,
    "tanggal": "2026-01-18",
    "jenis_maintenance": "perbaikan_berat",
    "status": "sedang_berjalan",
    "detail": [
      { "komponen": "ban belakang", "tindakan": "ganti", "keterangan": "ban botak, diganti ban tubeless FDR", "biaya": 220000 },
      { "komponen": "gir set", "tindakan": "ganti", "keterangan": "gir dan rantai aus diganti 1 set Tajima", "biaya": 165000 }
    ],
    "total_biaya": 385000,
    "catatan_tambahan": "motor masih di atas paddock menunggu penyetelan rantai"
  },
  {
    "id_kendaraan": 11,
    "id_karyawan": 9,
    "tanggal": "2026-01-04",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli MPX2", "biaya": 65000 },
      { "komponen": "rem", "tindakan": "cek", "keterangan": "pembersihan debu kampas rem", "biaya": 10000 }
    ],
    "total_biaya": 75000,
    "catatan_tambahan": "motor irit, fungsional lancar"
  },
  {
    "id_kendaraan": 12,
    "id_karyawan": 9,
    "tanggal": "2026-01-09",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli standar Yamaha", "biaya": 60000 }
    ],
    "total_biaya": 60000,
    "catatan_tambahan": "perawatan minimalis, performa stabil"
  },
  {
    "id_kendaraan": 13,
    "id_karyawan": 8,
    "tanggal": "2026-01-12",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli SPX2", "biaya": 85000 },
      { "komponen": "busi", "tindakan": "ganti", "keterangan": "ganti busi standar denso", "biaya": 20000 }
    ],
    "total_biaya": 105000,
    "catatan_tambahan": "vibe motor klasik terawat"
  },
  {
    "id_kendaraan": 14,
    "id_karyawan": 9,
    "tanggal": "2026-01-15",
    "jenis_maintenance": "servis_rutin",
    "status": "selesai",
    "detail": [
      { "komponen": "oli mesin", "tindakan": "ganti", "keterangan": "ganti oli matik besar", "biaya": 95000 },
      { "komponen": "v-belt CVT", "tindakan": "ganti", "keterangan": "ganti v-belt kit original", "biaya": 140000 }
    ],
    "total_biaya": 235000,
    "catatan_tambahan": "habis servis besar bagian CVT, akselerasi mantap"
  },
  {
    "id_kendaraan": 15,
    "id_karyawan": 9,
    "tanggal": "2026-01-20",
    "jenis_maintenance": "perbaikan_berat",
    "status": "sedang_berjalan",
    "detail": [
      { "komponen": "skor klep & paking bodi", "tindakan": "perbaiki", "keterangan": "servis besar, bersihkan kerak ruang bakar akibat oli rembes", "biaya": 350000 }
    ],
    "total_biaya": 350000,
    "catatan_tambahan": "mesin dibongkar setengah, pengerjaan estimasi selesai 2 hari"
  }

]);
