import type { Progres } from '../lib/progres';

/** Identitas murid ringan (Nama + PIN). `Budi#4821` = `nama` + `#` + `kodeUnik`. */
export interface AkunMurid {
  id: string;
  nama: string;
  kodeUnik: string;
  kelasId: string | null;
  kelasNama: string | null;
}

/** Progres persisten di akun (lapisan Fase 4 + blob localStorage lama). */
export interface ProgresAkun {
  totalPoin: number;
  peringkatGolonganAktif: number;
  peringkatGolonganRekor: number;
  badgeDiraih: string[];
  riwayatAkurasiPerGolongan: Record<string, { benar: number; total: number }>;
  progresLokal: Partial<Progres>;
}

export interface PilihanAkun {
  kodeUnik: string;
  kelasNama: string | null;
}

export interface MisiProgres {
  misiId: string;
  progres: number;
  selesai: boolean;
  selesaiPada: string | null;
}

export interface MisiSelesai {
  id: string;
  judul: string;
  poinReward: number;
  badgeReward: string | null;
  /** misi = jangka panjang; harian; lengkap = bonus 3/3 harian; lencana = lencana harian. */
  jenis?: 'misi' | 'harian' | 'lengkap' | 'lencana';
}

/** Status Misi Harian hari ini (WIB) dari server. */
export interface HarianAkun {
  /** 'YYYY-MM-DD' WIB menurut server — definisi misi dihitung dari sini. */
  tanggal: string;
  progres: { misiId: string; progres: number; selesai: boolean }[];
  /** Streak yang masih menyala (0 bila sudah putus). */
  streak: number;
  streakTerbaik: number;
  totalLengkap: number;
  lengkapHariIni: boolean;
}

/** Balasan Edge Function `akun`. */
export interface HasilAkun {
  murid?: AkunMurid;
  progres?: ProgresAkun | null;
  misiProgres?: MisiProgres[];
  misiSelesai?: MisiSelesai[];
  /** null bila fitur harian belum aktif di server. */
  harian?: HarianAkun | null;
  token?: string;
  /** Diisi bila > 1 akun cocok Nama+PIN — murid harus memilih kode uniknya. */
  pilihan?: PilihanAkun[];
  ok?: boolean;
  error?: string;
}

export const namaTampil = (m: AkunMurid) => `${m.nama}#${m.kodeUnik}`;

/**
 * Akun guru boleh pakai teks apa saja ("Pak Budi", "budi@sekolah", ...).
 * Supabase Auth tetap butuh format email, jadi teks yang bukan email dipetakan
 * ke alamat sintetis di domain ini — konsisten saat daftar maupun masuk.
 */
const DOMAIN_GURU = 'guru.uno-atom.app';
const POLA_EMAIL = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/;

export function emailGuru(masukan: string): string {
  const t = masukan.trim().toLowerCase();
  if (POLA_EMAIL.test(t)) return t;
  const slug = t.replace(/[^a-z0-9._-]+/g, '-').replace(/^[-.]+|[-.]+$/g, '');
  return `${slug || 'guru'}@${DOMAIN_GURU}`;
}

/** Tampilkan nama guru tanpa domain sintetis. */
export function labelGuru(email: string): string {
  return email.endsWith(`@${DOMAIN_GURU}`) ? email.slice(0, -DOMAIN_GURU.length - 1) : email;
}
