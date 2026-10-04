// Identitas & dokumentasi wajib untuk halaman "Tentang" (lomba media pembelajaran).
// ISI bagian bertanda TODO sesuai data timmu sebelum submit.

export const KREDIT = {
  // ── Identitas pengembang ──────────────────────────────────────────
  namaTim: 'Tim UNO-Chem',
  anggota: [
    { nama: 'Putra Yoga Nugraha', nim: '2305026024' },
    { nama: 'M. Rian Jafar Shodiq', nim: '2505026010' },
    { nama: 'Fico Fristand Thomas', nim: '2505026024' },
  ],
  instansi: 'Universitas Mulawarman',
  pembimbing: '' as string, // belum ada dosen pembimbing — dikosongkan (tidak ditampilkan)
  tahun: '2026',

  // ── Sasaran ───────────────────────────────────────────────────────
  // Ringkas; CP & TP detail ada di layar "CP & Tujuan Pembelajaran".
  jenjang: 'SMK Kelas X Kimia Analisis — Dasar-Dasar Kimia Analisis (Fase E) · Materi: Pengenalan Atom dan Komponennya',

  // ── Petunjuk penggunaan singkat ─────────────────────────────────
  petunjuk: [
    'Buka aplikasi di browser HP atau komputer. Bisa dipasang (PWA) agar jalan tanpa internet.',
    'Pilih "Mulai Main (vs Bot)" untuk latihan sendiri, atau "Main Online" untuk bermain bersama teman lewat kode room.',
    'Cocokkan kartu di tangan dengan kartu teratas berdasarkan WARNA (golongan) atau ANGKA (periode).',
    'Perhatikan notasi atom di tiap kartu (nomor massa di atas, nomor atom di bawah) — kuis sering menanyakan jumlah proton, neutron, dan elektronnya.',
    'Kartu aksi memunculkan kuis struktur atom — jawaban benar mengurangi hukuman kartu.',
    'Buat akun (Nama + PIN) untuk menyimpan progres, naik Peringkat Golongan, dan ikut leaderboard.',
    'Guru dapat membuat kelas dan memantau progres murid lewat menu Akun → Guru.',
  ],
} as const;
