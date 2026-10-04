import { describe, it, expect } from 'vitest';
import { DAFTAR_UNSUR } from './unsur';
import { BANK_SOAL } from './kuis';
import { GOLONGAN } from './golongan';
import { CPTP } from './cptp';
import { soalByKesulitan, unsurByGolongan, cariUnsur, soalAcak } from './index';
import type { Golongan } from './types';

describe('DAFTAR_UNSUR', () => {
  it('berisi minimal 40 unsur (brief: 40+)', () => {
    expect(DAFTAR_UNSUR.length).toBeGreaterThanOrEqual(40);
  });

  it('nomor atom unik', () => {
    const set = new Set(DAFTAR_UNSUR.map((u) => u.nomorAtom));
    expect(set.size).toBe(DAFTAR_UNSUR.length);
  });

  it('simbol unik', () => {
    const set = new Set(DAFTAR_UNSUR.map((u) => u.simbol));
    expect(set.size).toBe(DAFTAR_UNSUR.length);
  });

  it('periode selalu 1-7', () => {
    for (const u of DAFTAR_UNSUR) {
      expect(u.periode).toBeGreaterThanOrEqual(1);
      expect(u.periode).toBeLessThanOrEqual(7);
    }
  });

  it('golongan valid & kelima golongan terisi', () => {
    const keys = Object.keys(GOLONGAN) as Golongan[];
    for (const k of keys) {
      expect(unsurByGolongan(k).length).toBeGreaterThan(0);
    }
  });

  it('nomor atom & periode konsisten (unsur ber-periode tinggi punya nomor atom lebih besar dari periode 1)', () => {
    const p1 = DAFTAR_UNSUR.filter((u) => u.periode === 1);
    for (const u of p1) expect(u.nomorAtom).toBeLessThanOrEqual(2);
  });

  it('cariUnsur bekerja case-insensitive', () => {
    expect(cariUnsur('na')?.namaUnsur).toBe('Natrium');
    expect(cariUnsur('FE')?.namaUnsur).toBe('Besi');
    expect(cariUnsur('xx')).toBeUndefined();
  });
});

describe('BANK_SOAL', () => {
  it('versi modul: tepat 20 soal, 5 soal per TP', () => {
    expect(BANK_SOAL).toHaveLength(20);
    for (const { no } of CPTP.tujuan) {
      expect(BANK_SOAL.filter((q) => q.tpTerkait.includes(no))).toHaveLength(5);
    }
  });

  it('id soal unik', () => {
    const set = new Set(BANK_SOAL.map((q) => q.id));
    expect(set.size).toBe(BANK_SOAL.length);
  });

  it('setiap soal punya tepat 4 pilihan & jawabanBenar index valid', () => {
    for (const q of BANK_SOAL) {
      expect(q.pilihan).toHaveLength(4);
      expect(q.jawabanBenar).toBeGreaterThanOrEqual(0);
      expect(q.jawabanBenar).toBeLessThan(q.pilihan.length);
    }
  });

  it('tidak ada pilihan duplikat dalam satu soal', () => {
    for (const q of BANK_SOAL) {
      expect(new Set(q.pilihan).size).toBe(q.pilihan.length);
    }
  });

  it('ketiga tingkat kesulitan tersedia untuk QuizModal', () => {
    expect(soalByKesulitan('mudah').length).toBeGreaterThanOrEqual(5);
    expect(soalByKesulitan('sedang').length).toBeGreaterThanOrEqual(5);
    expect(soalByKesulitan('sulit').length).toBeGreaterThanOrEqual(5);
  });

  it('tpTerkait hanya berisi nomor TP yang ada di CPTP', () => {
    const tpValid = new Set(CPTP.tujuan.map((t) => t.no));
    for (const q of BANK_SOAL) {
      expect(q.tpTerkait.length).toBeGreaterThan(0);
      for (const tp of q.tpTerkait) expect(tpValid.has(tp)).toBe(true);
    }
  });

  // pilihSoal mengutamakan golongan kartu penyerang. Versi modul (20 soal):
  // tiap golongan punya tepat 1 soal per TP, dan tiap tingkat mencakup semua TP.
  it('tiap golongan punya tepat 1 soal untuk setiap TP', () => {
    for (const g of Object.keys(GOLONGAN) as Golongan[]) {
      const tp = BANK_SOAL.filter((q) => q.golonganTerkait === g).flatMap((q) => q.tpTerkait);
      expect(tp.sort(), g).toEqual(CPTP.tujuan.map((t) => t.no));
    }
  });

  it('tiap tingkat kesulitan mencakup semua TP', () => {
    for (const t of ['mudah', 'sedang', 'sulit'] as const) {
      for (const { no } of CPTP.tujuan) {
        expect(soalByKesulitan(t).some((q) => q.tpTerkait.includes(no)), `${t} TP${no}`).toBe(true);
      }
    }
  });

  it('soalAcak deterministik dengan rng ter-inject', () => {
    const q = soalAcak('mudah', () => 0);
    expect(q).toBe(soalByKesulitan('mudah')[0]);
  });
});

// ── Edisi Struktur Atom ──────────────────────────────────────────────
const SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹';
const SUB = '₀₁₂₃₄₅₆₇₈₉';
const angkaDari = (s: string, peta: string) =>
  Number([...s].map((c) => peta.indexOf(c)).join(''));

describe('Edisi Struktur Atom — data & soal', () => {
  it('setiap unsur punya nomor massa ≥ nomor atom', () => {
    for (const u of DAFTAR_UNSUR) {
      expect(Number.isInteger(u.nomorMassa)).toBe(true);
      expect(u.nomorMassa).toBeGreaterThanOrEqual(u.nomorAtom);
    }
  });

  it('notasi ᴬ_Z X pada pertanyaan soal cocok dengan data unsur', () => {
    // Hanya memeriksa PERTANYAAN (notasi pada pilihan jawaban sengaja ada yang salah).
    const re = new RegExp(`([${SUP}]+)([${SUB}]+)([A-Z][a-z]?)`, 'g');
    let diperiksa = 0;
    for (const q of BANK_SOAL) {
      for (const m of q.pertanyaan.matchAll(re)) {
        const u = cariUnsur(m[3]);
        expect(u, `${q.id}: unsur ${m[3]}`).toBeDefined();
        expect(angkaDari(m[1], SUP), `${q.id}: A ${m[3]}`).toBe(u!.nomorMassa);
        expect(angkaDari(m[2], SUB), `${q.id}: Z ${m[3]}`).toBe(u!.nomorAtom);
        diperiksa++;
      }
    }
    expect(diperiksa).toBeGreaterThanOrEqual(3);
  });

  it('CPTP berisi 4 TP struktur atom & setiap TP punya soal di ketiga tingkat', () => {
    expect(CPTP.tujuan.map((t) => t.no)).toEqual([1, 2, 3, 4]);
    for (const { no } of CPTP.tujuan) {
      for (const t of ['mudah', 'sedang', 'sulit'] as const) {
        expect(soalByKesulitan(t).some((q) => q.tpTerkait.includes(no))).toBe(true);
      }
    }
  });
});
