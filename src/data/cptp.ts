// Ditampilkan di layar "CP & Tujuan Pembelajaran" (src/screens/CPTPScreen.tsx)
// dan dipakai dashboard guru (akurasi per-TP). Nomor TP dirujuk oleh
// `tpTerkait` di src/data/kuis.ts — JANGAN ubah nomor tanpa memperbarui bank soal.

export interface TujuanPembelajaran {
  no: number;
  /** Teks TP; verba operasional ditandai **tebal**. */
  teks: string;
  dimensi: 'C2' | 'C3';
  dimensiLabel: string;
  /** Catatan kecil opsional untuk TP tertentu. */
  catatan?: string;
}

export const CPTP: {
  mataPelajaran: string;
  fase: string;
  kelas: string;
  elemen: string;
  materi: string;
  cpKutipan: string;
  cpElaborasi: string;
  tujuan: TujuanPembelajaran[];
} = {
  mataPelajaran: 'Dasar-Dasar Kimia Analisis',
  fase: 'E',
  kelas: 'X SMK (Program Keahlian Kimia Analisis)',
  elemen: 'Bab 3 Sistem Periodik Unsur (ATP sekolah)',
  materi: 'Pengenalan Atom dan Komponennya',

  cpKutipan:
    'memahami atom sebagai penyusun materi beserta partikel-partikel penyusunnya ' +
    'sebagai dasar memahami sistem periodik unsur',
  cpElaborasi:
    'Pada akhir materi ini, murid mampu menjelaskan perkembangan model atom, ' +
    'mengenali partikel penyusun atom (proton, neutron, elektron), menentukan ' +
    'jumlah partikel tersebut dari notasi atom (nomor massa di atas, nomor atom di bawah lambang unsur, misalnya ²³₁₁Na), serta menjelaskan ' +
    'pembentukan ion positif (kation) dan ion negatif (anion). Pemahaman ini ' +
    'menjadi jembatan menuju letak unsur dalam sistem periodik: nomor atom ' +
    '(jumlah proton) yang dihitung murid adalah dasar penyusunan tabel periodik ' +
    'modern — itulah sebabnya warna kartu tetap golongan dan angka kartu tetap periode.',

  tujuan: [
    {
      no: 1,
      dimensi: 'C2',
      dimensiLabel: 'Memahami',
      teks:
        'Peserta didik mampu **menjelaskan** perkembangan model atom (Dalton, ' +
        'Thomson, Rutherford, Bohr, hingga mekanika kuantum) beserta kelebihan ' +
        'dan kelemahannya secara singkat.',
    },
    {
      no: 2,
      dimensi: 'C2',
      dimensiLabel: 'Memahami',
      teks:
        'Peserta didik mampu **menjelaskan** partikel penyusun atom (proton, ' +
        'neutron, elektron) berdasarkan muatan, massa relatif, letak, dan penemunya.',
    },
    {
      no: 3,
      dimensi: 'C3',
      dimensiLabel: 'Menerapkan',
      teks:
        'Peserta didik mampu **menentukan** jumlah proton, neutron, dan elektron ' +
        'suatu atom netral berdasarkan nomor atom dan nomor massa pada notasi atom (misalnya ²³₁₁Na).',
    },
    {
      no: 4,
      dimensi: 'C3',
      dimensiLabel: 'Menerapkan',
      teks:
        'Peserta didik mampu **menentukan** jumlah proton, neutron, dan elektron ' +
        'pada ion (kation dan anion) serta **menjelaskan** pembentukannya melalui ' +
        'pelepasan atau penerimaan elektron.',
    },
  ],
};
