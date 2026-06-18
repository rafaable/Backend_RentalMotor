-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3305
-- Generation Time: Jun 18, 2026 at 08:38 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rental_motor`
--

-- --------------------------------------------------------

--
-- Table structure for table `cabang`
--

CREATE TABLE `cabang` (
  `id_cabang` int(11) NOT NULL,
  `nama_cabang` varchar(100) NOT NULL,
  `alamat` text NOT NULL,
  `kota` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cabang`
--

INSERT INTO `cabang` (`id_cabang`, `nama_cabang`, `alamat`, `kota`) VALUES
(1, 'SDJ', 'Jl. Ahmad Yani No. 45, Kecamatan Sidoarjo', 'Sidoarjo'),
(2, 'SBY', 'Jl. Tunjungan No. 12, Genteng', 'Surabaya'),
(3, 'MJK', 'Jl. Gajah Mada No. 88, Magersari', 'Mojokerto');

-- --------------------------------------------------------

--
-- Table structure for table `denda`
--

CREATE TABLE `denda` (
  `id_denda` int(11) NOT NULL,
  `id_pengembalian` int(11) NOT NULL,
  `id_karyawan` int(11) NOT NULL,
  `alasan_denda` enum('kerusakan_kendaraan','pelanggaran_lalu_lintas','keterlambatan_pengembalian') NOT NULL,
  `nominal_denda` decimal(12,2) NOT NULL,
  `keterangan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `denda`
--

INSERT INTO `denda` (`id_denda`, `id_pengembalian`, `id_karyawan`, `alasan_denda`, `nominal_denda`, `keterangan`) VALUES
(1, 1, 3, 'kerusakan_kendaraan', 500000.00, 'Spion kanan pecah dan goresan pada pintu samping'),
(2, 2, 6, 'pelanggaran_lalu_lintas', 250000.00, 'Terkena e-tilang karena melanggar lampu merah'),
(3, 3, 9, 'kerusakan_kendaraan', 1200000.00, 'Bumper depan penyok cukup dalam');

-- --------------------------------------------------------

--
-- Table structure for table `karyawan`
--

CREATE TABLE `karyawan` (
  `id_karyawan` int(11) NOT NULL,
  `id_cabang` int(11) NOT NULL,
  `nama_karyawan` varchar(100) NOT NULL,
  `jabatan` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `karyawan`
--

INSERT INTO `karyawan` (`id_karyawan`, `id_cabang`, `nama_karyawan`, `jabatan`) VALUES
(1, 1, 'Arkananta Malik', 'Branch Manager'),
(2, 1, 'Baskara Raditya', 'Staff Admin'),
(3, 1, 'Damar Dewanka', 'Supervisor'),
(4, 2, 'Elang Gibran', 'Branch Manager'),
(5, 2, 'Gavin Mahendra', 'Staff Admin'),
(6, 2, 'Kala Anaking', 'Supervisor'),
(7, 3, 'Narendra Danadyaksa', 'Branch Manager'),
(8, 3, 'Rayyan Danendra', 'Staff Admin'),
(9, 3, 'Satria Aksara', 'Supervisor');

-- --------------------------------------------------------

--
-- Table structure for table `kendaraan`
--

CREATE TABLE `kendaraan` (
  `id_kendaraan` int(11) NOT NULL,
  `id_cabang` int(11) NOT NULL,
  `merek` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `tahun` year(4) NOT NULL,
  `nomor_polisi` varchar(15) NOT NULL,
  `tarif_per_hari` decimal(10,2) NOT NULL,
  `status_kendaraan` enum('tersedia','disewa','dalam_perbaikan') NOT NULL DEFAULT 'tersedia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kendaraan`
--

INSERT INTO `kendaraan` (`id_kendaraan`, `id_cabang`, `merek`, `model`, `tahun`, `nomor_polisi`, `tarif_per_hari`, `status_kendaraan`) VALUES
(1, 1, 'Honda', 'Beat Fi', '2018', 'W 4123 AB', 50000.00, 'tersedia'),
(2, 1, 'Honda', 'Vario 150', '2021', 'W 5234 CD', 75000.00, 'tersedia'),
(3, 1, 'Yamaha', 'Mio M3', '2019', 'W 6345 EF', 55000.00, 'tersedia'),
(4, 1, 'Yamaha', 'NMAX', '2022', 'W 2456 GH', 90000.00, 'disewa'),
(5, 1, 'Honda', 'Scoopy All New', '2020', 'W 3567 IJ', 65000.00, 'dalam_perbaikan'),
(6, 2, 'Honda', 'Beat Street', '2020', 'L 2189 ZA', 60000.00, 'tersedia'),
(7, 2, 'Honda', 'Vario 160', '2023', 'L 3290 XB', 85000.00, 'tersedia'),
(8, 2, 'Yamaha', 'Fazzio', '2022', 'L 4301 WC', 75000.00, 'tersedia'),
(9, 2, 'Yamaha', 'Aerox 155', '2021', 'L 5412 VD', 85000.00, 'disewa'),
(10, 2, 'Honda', 'Supra X 125', '2017', 'L 6523 UE', 45000.00, 'dalam_perbaikan'),
(11, 3, 'Honda', 'Genio', '2021', 'S 3145 OP', 65000.00, 'tersedia'),
(12, 3, 'Yamaha', 'Gear 125', '2022', 'S 4256 QR', 60000.00, 'tersedia'),
(13, 3, 'Honda', 'Scoopy Fi', '2018', 'S 5367 ST', 55000.00, 'disewa'),
(14, 3, 'Yamaha', 'NMAX', '2020', 'S 6478 UV', 80000.00, 'disewa'),
(15, 3, 'Honda', 'Beat Sporty', '2019', 'S 7589 WX', 50000.00, 'dalam_perbaikan');

-- --------------------------------------------------------

--
-- Table structure for table `pembayaran`
--

CREATE TABLE `pembayaran` (
  `id_pembayaran` int(11) NOT NULL,
  `id_penyewaan` int(11) NOT NULL,
  `tanggal_transaksi` date NOT NULL DEFAULT curdate(),
  `metode_pembayaran` enum('transfer_bank','qris','tunai','kartu_debit','kartu_kredit') NOT NULL,
  `jumlah_pembayaran` decimal(12,2) NOT NULL,
  `status_pembayaran` enum('lunas','gagal') NOT NULL DEFAULT 'lunas'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pembayaran`
--

INSERT INTO `pembayaran` (`id_pembayaran`, `id_penyewaan`, `tanggal_transaksi`, `metode_pembayaran`, `jumlah_pembayaran`, `status_pembayaran`) VALUES
(1, 1, '2026-06-01', 'transfer_bank', 100000.00, 'lunas'),
(2, 2, '2026-06-10', 'qris', 150000.00, 'lunas'),
(3, 3, '2026-06-02', 'tunai', 60000.00, 'lunas'),
(4, 4, '2026-06-11', 'transfer_bank', 255000.00, 'lunas'),
(5, 5, '2026-05-28', 'qris', 65000.00, 'lunas'),
(6, 6, '2026-06-11', 'tunai', 60000.00, 'lunas');

-- --------------------------------------------------------

--
-- Table structure for table `pengembalian`
--

CREATE TABLE `pengembalian` (
  `id_pengembalian` int(11) NOT NULL,
  `id_penyewaan` int(11) NOT NULL,
  `id_karyawan` int(11) NOT NULL,
  `waktu_pengembalian` date NOT NULL,
  `kondisi_kendaraan` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengembalian`
--

INSERT INTO `pengembalian` (`id_pengembalian`, `id_penyewaan`, `id_karyawan`, `waktu_pengembalian`, `kondisi_kendaraan`) VALUES
(1, 1, 3, '2026-06-03', 'Kondisi mulus, bensin terisi penuh, mesin aman.'),
(2, 3, 6, '2026-06-03', 'Ada baret halus di bagian spion kanan, fungsi normal.'),
(3, 5, 9, '2026-05-29', 'Kondisi baik, ban belakang agak kurang angin tapi aman.');

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `id_pengguna` int(11) NOT NULL,
  `kartu_identitas` varchar(20) NOT NULL,
  `nomor_telepon` varchar(15) NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `nomor_sim` varchar(20) NOT NULL,
  `tanggal_kadaluarsa_sim` date NOT NULL,
  `status_verifikasi` enum('belum_diverifikasi','terverifikasi','ditolak','expired') NOT NULL DEFAULT 'belum_diverifikasi'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengguna`
--

INSERT INTO `pengguna` (`id_pengguna`, `kartu_identitas`, `nomor_telepon`, `nama_lengkap`, `nomor_sim`, `tanggal_kadaluarsa_sim`, `status_verifikasi`) VALUES
(1, '3515011203000001', '081234567890', 'Aksa Sadajiwa', '950112345678', '2028-03-12', 'terverifikasi'),
(2, '3515011507010002', '081345678901', 'Bumi Semesta', '960712345679', '2029-07-15', 'terverifikasi'),
(3, '3515012210990003', '081456789012', 'Kala Argantara', '991012345680', '2027-10-22', 'belum_diverifikasi'),
(4, '3515010505980004', '081567890123', 'Renjana Arutala', '980512345681', '2025-05-05', 'expired'),
(5, '3515013011020005', '081678901234', 'Abisatya Hanasta', '021112345682', '2030-11-30', 'terverifikasi'),
(6, '3515012104020006', '081789012345', 'Asmaralaya Citra', '020412345683', '2029-04-21', 'terverifikasi'),
(7, '3515011708000007', '081890123456', 'Lintang Amreta', '000812345684', '2028-08-17', 'terverifikasi'),
(8, '3515010205010008', '081901234567', 'Niskala Arunika', '010512345685', '2027-05-02', 'belum_diverifikasi'),
(9, '3515011402030009', '081212345678', 'Raya Nayaka', '030212345686', '2024-02-14', 'ditolak'),
(10, '3515012512990010', '081313456789', 'Gendis Kirana', '991212345687', '2028-12-25', 'terverifikasi'),
(11, '3515011203123001', '088234447890', 'Firas Atlas', '950112777678', '2028-03-12', 'terverifikasi');

-- --------------------------------------------------------

--
-- Table structure for table `penyewaan`
--

CREATE TABLE `penyewaan` (
  `id_penyewaan` int(11) NOT NULL,
  `id_pengguna` int(11) NOT NULL,
  `id_kendaraan` int(11) NOT NULL,
  `id_karyawan` int(11) NOT NULL,
  `waktu_mulai` date NOT NULL,
  `waktu_selesai_rencana` date NOT NULL,
  `status_penyewaan` enum('aktif','selesai','dibatalkan') NOT NULL DEFAULT 'aktif'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penyewaan`
--

INSERT INTO `penyewaan` (`id_penyewaan`, `id_pengguna`, `id_kendaraan`, `id_karyawan`, `waktu_mulai`, `waktu_selesai_rencana`, `status_penyewaan`) VALUES
(1, 1, 1, 1, '2026-06-01', '2026-06-03', 'selesai'),
(2, 2, 2, 2, '2026-06-10', '2026-06-12', 'aktif'),
(3, 5, 6, 4, '2026-06-02', '2026-06-03', 'selesai'),
(4, 6, 7, 5, '2026-06-11', '2026-06-14', 'aktif'),
(5, 7, 11, 7, '2026-05-28', '2026-05-29', 'selesai'),
(6, 10, 12, 8, '2026-06-11', '2026-06-12', 'aktif'),
(7, 11, 13, 8, '2026-06-17', '2026-06-20', 'aktif');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cabang`
--
ALTER TABLE `cabang`
  ADD PRIMARY KEY (`id_cabang`);

--
-- Indexes for table `denda`
--
ALTER TABLE `denda`
  ADD PRIMARY KEY (`id_denda`),
  ADD KEY `id_pengembalian` (`id_pengembalian`),
  ADD KEY `id_karyawan` (`id_karyawan`);

--
-- Indexes for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD PRIMARY KEY (`id_karyawan`),
  ADD KEY `id_cabang` (`id_cabang`);

--
-- Indexes for table `kendaraan`
--
ALTER TABLE `kendaraan`
  ADD PRIMARY KEY (`id_kendaraan`),
  ADD UNIQUE KEY `nomor_polisi` (`nomor_polisi`),
  ADD KEY `id_cabang` (`id_cabang`);

--
-- Indexes for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD PRIMARY KEY (`id_pembayaran`),
  ADD UNIQUE KEY `id_penyewaan` (`id_penyewaan`);

--
-- Indexes for table `pengembalian`
--
ALTER TABLE `pengembalian`
  ADD PRIMARY KEY (`id_pengembalian`),
  ADD UNIQUE KEY `id_penyewaan` (`id_penyewaan`),
  ADD KEY `id_karyawan` (`id_karyawan`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`id_pengguna`),
  ADD UNIQUE KEY `kartu_identitas` (`kartu_identitas`),
  ADD UNIQUE KEY `nomor_sim` (`nomor_sim`);

--
-- Indexes for table `penyewaan`
--
ALTER TABLE `penyewaan`
  ADD PRIMARY KEY (`id_penyewaan`),
  ADD KEY `id_pengguna` (`id_pengguna`),
  ADD KEY `id_kendaraan` (`id_kendaraan`),
  ADD KEY `id_karyawan` (`id_karyawan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cabang`
--
ALTER TABLE `cabang`
  MODIFY `id_cabang` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `denda`
--
ALTER TABLE `denda`
  MODIFY `id_denda` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `karyawan`
--
ALTER TABLE `karyawan`
  MODIFY `id_karyawan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `kendaraan`
--
ALTER TABLE `kendaraan`
  MODIFY `id_kendaraan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `pembayaran`
--
ALTER TABLE `pembayaran`
  MODIFY `id_pembayaran` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `pengembalian`
--
ALTER TABLE `pengembalian`
  MODIFY `id_pengembalian` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `pengguna`
--
ALTER TABLE `pengguna`
  MODIFY `id_pengguna` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `penyewaan`
--
ALTER TABLE `penyewaan`
  MODIFY `id_penyewaan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `denda`
--
ALTER TABLE `denda`
  ADD CONSTRAINT `denda_ibfk_1` FOREIGN KEY (`id_pengembalian`) REFERENCES `pengembalian` (`id_pengembalian`),
  ADD CONSTRAINT `denda_ibfk_2` FOREIGN KEY (`id_karyawan`) REFERENCES `karyawan` (`id_karyawan`);

--
-- Constraints for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD CONSTRAINT `karyawan_ibfk_1` FOREIGN KEY (`id_cabang`) REFERENCES `cabang` (`id_cabang`);

--
-- Constraints for table `kendaraan`
--
ALTER TABLE `kendaraan`
  ADD CONSTRAINT `kendaraan_ibfk_1` FOREIGN KEY (`id_cabang`) REFERENCES `cabang` (`id_cabang`);

--
-- Constraints for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD CONSTRAINT `pembayaran_ibfk_1` FOREIGN KEY (`id_penyewaan`) REFERENCES `penyewaan` (`id_penyewaan`);

--
-- Constraints for table `pengembalian`
--
ALTER TABLE `pengembalian`
  ADD CONSTRAINT `pengembalian_ibfk_1` FOREIGN KEY (`id_penyewaan`) REFERENCES `penyewaan` (`id_penyewaan`),
  ADD CONSTRAINT `pengembalian_ibfk_2` FOREIGN KEY (`id_karyawan`) REFERENCES `karyawan` (`id_karyawan`);

--
-- Constraints for table `penyewaan`
--
ALTER TABLE `penyewaan`
  ADD CONSTRAINT `penyewaan_ibfk_1` FOREIGN KEY (`id_pengguna`) REFERENCES `pengguna` (`id_pengguna`),
  ADD CONSTRAINT `penyewaan_ibfk_2` FOREIGN KEY (`id_kendaraan`) REFERENCES `kendaraan` (`id_kendaraan`),
  ADD CONSTRAINT `penyewaan_ibfk_3` FOREIGN KEY (`id_karyawan`) REFERENCES `karyawan` (`id_karyawan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
