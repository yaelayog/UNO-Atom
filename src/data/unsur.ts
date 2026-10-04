import type { Unsur } from './types';

/**
 * Daftar master unsur UNO-Chem — 47 unsur representatif dari 5 golongan.
 * `periode` dipakai sebagai "angka" kartu UNO (1-7).
 *
 * `nomorMassa` = nomor massa ISOTOP PALING MELIMPAH di alam (untuk unsur
 * radioaktif/sintetis: isotop paling stabil yang dikenal). Dipakai pada notasi
 * ᴬ_Z X di kartu dan sebagai dasar soal jumlah proton–neutron–elektron.
 *
 * Golongan transisi dibatasi pada periode 4-6 (yang paling sering dipelajari
 * di SMP/SMA) agar sebaran periode antar-golongan tetap seimbang untuk deck.
 */
export const DAFTAR_UNSUR: Unsur[] = [
  // ── Logam Alkali (IA) ─────────────────────────────────────────────
  { simbol: 'Li', namaUnsur: 'Litium', nomorAtom: 3, nomorMassa: 7, periode: 2, golongan: 'alkali', fakta: 'Logam paling ringan; dipakai pada baterai litium-ion.' },
  { simbol: 'Na', namaUnsur: 'Natrium', nomorAtom: 11, nomorMassa: 23, periode: 3, golongan: 'alkali', fakta: 'Bersama klor membentuk garam dapur (NaCl).' },
  { simbol: 'K', namaUnsur: 'Kalium', nomorAtom: 19, nomorMassa: 39, periode: 4, golongan: 'alkali', fakta: 'Penting untuk kerja saraf dan otot; banyak pada pisang.' },
  { simbol: 'Rb', namaUnsur: 'Rubidium', nomorAtom: 37, nomorMassa: 85, periode: 5, golongan: 'alkali', fakta: 'Meleleh sedikit di atas suhu tubuh manusia (39 °C).' },
  { simbol: 'Cs', namaUnsur: 'Sesium', nomorAtom: 55, nomorMassa: 133, periode: 6, golongan: 'alkali', fakta: 'Dasar penetapan satuan waktu "detik" pada jam atom.' },
  { simbol: 'Fr', namaUnsur: 'Fransium', nomorAtom: 87, nomorMassa: 223, periode: 7, golongan: 'alkali', fakta: 'Sangat langka dan radioaktif; logam alkali paling reaktif.' },

  // ── Logam Alkali Tanah (IIA) ──────────────────────────────────────
  { simbol: 'Be', namaUnsur: 'Berilium', nomorAtom: 4, nomorMassa: 9, periode: 2, golongan: 'alkaliTanah', fakta: 'Ringan dan kaku; dipakai pada komponen pesawat dan satelit.' },
  { simbol: 'Mg', namaUnsur: 'Magnesium', nomorAtom: 12, nomorMassa: 24, periode: 3, golongan: 'alkaliTanah', fakta: 'Atom pusat pada klorofil, pigmen hijau daun.' },
  { simbol: 'Ca', namaUnsur: 'Kalsium', nomorAtom: 20, nomorMassa: 40, periode: 4, golongan: 'alkaliTanah', fakta: 'Komponen utama tulang, gigi, dan cangkang telur.' },
  { simbol: 'Sr', namaUnsur: 'Stronsium', nomorAtom: 38, nomorMassa: 88, periode: 5, golongan: 'alkaliTanah', fakta: 'Memberi warna merah terang pada kembang api.' },
  { simbol: 'Ba', namaUnsur: 'Barium', nomorAtom: 56, nomorMassa: 138, periode: 6, golongan: 'alkaliTanah', fakta: 'Senyawa BaSO₄ diminum sebagai "bubur barium" untuk rontgen lambung.' },
  { simbol: 'Ra', namaUnsur: 'Radium', nomorAtom: 88, nomorMassa: 226, periode: 7, golongan: 'alkaliTanah', fakta: 'Radioaktif; dulu keliru dipakai untuk cat jam yang menyala.' },

  // ── Halogen (VIIA) ────────────────────────────────────────────────
  { simbol: 'F', namaUnsur: 'Fluorin', nomorAtom: 9, nomorMassa: 19, periode: 2, golongan: 'halogen', fakta: 'Unsur paling elektronegatif; senyawanya menguatkan email gigi.' },
  { simbol: 'Cl', namaUnsur: 'Klorin', nomorAtom: 17, nomorMassa: 35, periode: 3, golongan: 'halogen', fakta: 'Gas kuning-hijau; dipakai mendisinfeksi air minum.' },
  { simbol: 'Br', namaUnsur: 'Bromin', nomorAtom: 35, nomorMassa: 79, periode: 4, golongan: 'halogen', fakta: 'Satu-satunya nonlogam yang berwujud cair pada suhu kamar.' },
  { simbol: 'I', namaUnsur: 'Iodin', nomorAtom: 53, nomorMassa: 127, periode: 5, golongan: 'halogen', fakta: 'Padatan ungu-hitam yang menyublim; penting untuk kelenjar tiroid.' },
  { simbol: 'At', namaUnsur: 'Astatin', nomorAtom: 85, nomorMassa: 210, periode: 6, golongan: 'halogen', fakta: 'Salah satu unsur paling langka di kerak Bumi.' },
  { simbol: 'Ts', namaUnsur: 'Tenesin', nomorAtom: 117, nomorMassa: 294, periode: 7, golongan: 'halogen', fakta: 'Unsur buatan yang baru disintesis tahun 2010.' },

  // ── Gas Mulia (VIIIA) ─────────────────────────────────────────────
  { simbol: 'He', namaUnsur: 'Helium', nomorAtom: 2, nomorMassa: 4, periode: 1, golongan: 'gasMulia', fakta: 'Unsur kedua paling melimpah di alam semesta setelah hidrogen.' },
  { simbol: 'Ne', namaUnsur: 'Neon', nomorAtom: 10, nomorMassa: 20, periode: 2, golongan: 'gasMulia', fakta: 'Bersinar merah-oranye pada lampu tabung "neon".' },
  { simbol: 'Ar', namaUnsur: 'Argon', nomorAtom: 18, nomorMassa: 40, periode: 3, golongan: 'gasMulia', fakta: 'Mengisi bola lampu pijar agar filamen tidak cepat putus.' },
  { simbol: 'Kr', namaUnsur: 'Kripton', nomorAtom: 36, nomorMassa: 84, periode: 4, golongan: 'gasMulia', fakta: 'Dipakai pada beberapa lampu berkinerja tinggi dan laser.' },
  { simbol: 'Xe', namaUnsur: 'Xenon', nomorAtom: 54, nomorMassa: 132, periode: 5, golongan: 'gasMulia', fakta: 'Lampu xenon menghasilkan cahaya putih mirip sinar matahari.' },
  { simbol: 'Rn', namaUnsur: 'Radon', nomorAtom: 86, nomorMassa: 222, periode: 6, golongan: 'gasMulia', fakta: 'Gas radioaktif yang bisa terkumpul di ruang bawah tanah.' },
  { simbol: 'Og', namaUnsur: 'Oganeson', nomorAtom: 118, nomorMassa: 294, periode: 7, golongan: 'gasMulia', fakta: 'Unsur dengan nomor atom tertinggi yang pernah dibuat.' },

  // ── Logam Transisi — Periode 4 ────────────────────────────────────
  { simbol: 'Sc', namaUnsur: 'Skandium', nomorAtom: 21, nomorMassa: 45, periode: 4, golongan: 'transisi', fakta: 'Paduan aluminium-skandium dipakai pada rangka sepeda ringan.' },
  { simbol: 'Ti', namaUnsur: 'Titanium', nomorAtom: 22, nomorMassa: 48, periode: 4, golongan: 'transisi', fakta: 'Kuat, ringan, dan tahan karat; dipakai untuk implan tulang.' },
  { simbol: 'V', namaUnsur: 'Vanadium', nomorAtom: 23, nomorMassa: 51, periode: 4, golongan: 'transisi', fakta: 'Menambah kekuatan baja perkakas dan pegas.' },
  { simbol: 'Cr', namaUnsur: 'Kromium', nomorAtom: 24, nomorMassa: 52, periode: 4, golongan: 'transisi', fakta: 'Lapisan krom membuat logam mengkilap dan tahan karat.' },
  { simbol: 'Mn', namaUnsur: 'Mangan', nomorAtom: 25, nomorMassa: 55, periode: 4, golongan: 'transisi', fakta: 'Bilangan oksidasinya bervariasi dari +2 hingga +7.' },
  { simbol: 'Fe', namaUnsur: 'Besi', nomorAtom: 26, nomorMassa: 56, periode: 4, golongan: 'transisi', fakta: 'Logam paling banyak dipakai manusia; inti bumi kaya besi.' },
  { simbol: 'Co', namaUnsur: 'Kobalt', nomorAtom: 27, nomorMassa: 59, periode: 4, golongan: 'transisi', fakta: 'Memberi warna biru khas pada kaca dan keramik.' },
  { simbol: 'Ni', namaUnsur: 'Nikel', nomorAtom: 28, nomorMassa: 58, periode: 4, golongan: 'transisi', fakta: 'Campuran utama pada baja tahan karat dan koin.' },
  { simbol: 'Cu', namaUnsur: 'Tembaga', nomorAtom: 29, nomorMassa: 63, periode: 4, golongan: 'transisi', fakta: 'Penghantar listrik sangat baik; senyawanya sering berwarna biru.' },
  { simbol: 'Zn', namaUnsur: 'Seng', nomorAtom: 30, nomorMassa: 64, periode: 4, golongan: 'transisi', fakta: 'Melapisi besi agar tidak berkarat (galvanisasi).' },

  // ── Logam Transisi — Periode 5 ────────────────────────────────────
  { simbol: 'Y', namaUnsur: 'Itrium', nomorAtom: 39, nomorMassa: 89, periode: 5, golongan: 'transisi', fakta: 'Dipakai pada fosfor merah layar tabung dan LED putih.' },
  { simbol: 'Zr', namaUnsur: 'Zirkonium', nomorAtom: 40, nomorMassa: 90, periode: 5, golongan: 'transisi', fakta: 'Sangat tahan panas dan korosi; dipakai di reaktor nuklir.' },
  { simbol: 'Nb', namaUnsur: 'Niobium', nomorAtom: 41, nomorMassa: 93, periode: 5, golongan: 'transisi', fakta: 'Paduannya menjadi superkonduktor pada suhu sangat rendah.' },
  { simbol: 'Mo', namaUnsur: 'Molibdenum', nomorAtom: 42, nomorMassa: 98, periode: 5, golongan: 'transisi', fakta: 'Menambah kekuatan baja pada suhu tinggi.' },
  { simbol: 'Ag', namaUnsur: 'Perak', nomorAtom: 47, nomorMassa: 107, periode: 5, golongan: 'transisi', fakta: 'Penghantar listrik dan panas terbaik di antara semua logam.' },
  { simbol: 'Cd', namaUnsur: 'Kadmium', nomorAtom: 48, nomorMassa: 114, periode: 5, golongan: 'transisi', fakta: 'Beracun; dulu umum pada baterai nikel-kadmium (NiCd).' },

  // ── Logam Transisi — Periode 6 ────────────────────────────────────
  { simbol: 'Hf', namaUnsur: 'Hafnium', nomorAtom: 72, nomorMassa: 180, periode: 6, golongan: 'transisi', fakta: 'Menyerap neutron dengan baik; dipakai pada batang kendali reaktor.' },
  { simbol: 'Ta', namaUnsur: 'Tantalum', nomorAtom: 73, nomorMassa: 181, periode: 6, golongan: 'transisi', fakta: 'Dipakai pada kapasitor kecil di ponsel dan komputer.' },
  { simbol: 'W', namaUnsur: 'Wolfram', nomorAtom: 74, nomorMassa: 184, periode: 6, golongan: 'transisi', fakta: 'Titik leleh tertinggi di antara semua logam (3.422 °C).' },
  { simbol: 'Pt', namaUnsur: 'Platina', nomorAtom: 78, nomorMassa: 195, periode: 6, golongan: 'transisi', fakta: 'Katalis pada knalpot kendaraan untuk mengurangi gas beracun.' },
  { simbol: 'Au', namaUnsur: 'Emas', nomorAtom: 79, nomorMassa: 197, periode: 6, golongan: 'transisi', fakta: 'Sangat tidak reaktif sehingga tidak berkarat atau memudar.' },
  { simbol: 'Hg', namaUnsur: 'Raksa', nomorAtom: 80, nomorMassa: 202, periode: 6, golongan: 'transisi', fakta: 'Satu-satunya logam yang cair pada suhu kamar.' },
];
