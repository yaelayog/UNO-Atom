import { useState } from 'react';
import { SEMUA_GOLONGAN, WARNA_GOLONGAN } from '../data/golongan';
import { DAFTAR_UNSUR } from '../data/unsur';
import type { Golongan, KartuKimia } from '../data/types';
import { GAYA_GOLONGAN } from '../lib/tampilan';
import { Card } from '../components/Card';
import { useGameStore } from '../store/gameStore';

function kartuDariUnsur(u: (typeof DAFTAR_UNSUR)[number]): KartuKimia {
  return {
    id: u.simbol,
    simbol: u.simbol,
    namaUnsur: u.namaUnsur,
    nomorAtom: u.nomorAtom,
    nomorMassa: u.nomorMassa,
    periode: u.periode,
    golongan: u.golongan,
    warnaUno: WARNA_GOLONGAN[u.golongan],
    jenis: 'angka',
  };
}

export function BelajarScreen() {
  const keLayar = useGameStore((s) => s.keLayar);
  const [aktif, setAktif] = useState<Golongan>('alkali');

  const info = SEMUA_GOLONGAN.find((g) => g.key === aktif)!;
  const unsur = DAFTAR_UNSUR.filter((u) => u.golongan === aktif).sort(
    (a, b) => a.nomorAtom - b.nomorAtom,
  );

  return (
    <main className="mx-auto flex min-h-full max-w-md flex-col gap-4 p-5 no-select">
      <button
        type="button"
        onClick={() => keLayar('menu')}
        className="w-fit rounded-full bg-white px-3 py-1 text-xs font-bold text-tinta/70 shadow-empuk cursor-pointer hover:bg-kertas"
      >
        ← Menu
      </button>

      <h1 className="font-display text-2xl font-extrabold text-lab">Mode Belajar</h1>
      <p className="-mt-2 text-sm text-tinta/60">
        Kenali atom, lalu jelajahi unsur tiap golongan. Tanpa skor — santai saja.
      </p>

      {/* Ringkasan materi struktur atom */}
      <details className="rounded-3xl border border-black/10 bg-white p-4 shadow-empuk" open>
        <summary className="cursor-pointer font-display text-lg font-extrabold text-lab">
          ⚛ Kenali Atom
        </summary>
        <p className="mt-2 text-xs font-extrabold text-tinta/70">Partikel penyusun atom</p>
        <div className="mt-1 overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="text-tinta/60">
                <th className="py-1 pr-2">Partikel</th>
                <th className="py-1 pr-2">Muatan</th>
                <th className="py-1 pr-2">Massa</th>
                <th className="py-1 pr-2">Letak</th>
                <th className="py-1">Penemu</th>
              </tr>
            </thead>
            <tbody className="text-tinta/85">
              <tr><td className="py-0.5 pr-2 font-bold">Proton</td><td>+1</td><td>±1 sma</td><td>inti</td><td>Goldstein/Rutherford</td></tr>
              <tr><td className="py-0.5 pr-2 font-bold">Neutron</td><td>0</td><td>±1 sma</td><td>inti</td><td>Chadwick (1932)</td></tr>
              <tr><td className="py-0.5 pr-2 font-bold">Elektron</td><td>−1</td><td>≈ 0 (1/1836)</td><td>kulit</td><td>Thomson (1897)</td></tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-xs font-extrabold text-tinta/70">Notasi atom <sup>A</sup><sub>Z</sub>X</p>
        <p className="mt-1 text-xs text-tinta/80">
          A = nomor massa (proton + neutron), Z = nomor atom (proton). Neutron = A − Z.
          Atom netral: elektron = Z. Ion: elektron = Z − muatan
          (kation melepas elektron, anion menerima elektron).
        </p>
        <p className="mt-3 text-xs font-extrabold text-tinta/70">Perkembangan model atom</p>
        <ol className="mt-1 list-inside list-decimal text-xs text-tinta/80">
          <li><b>Dalton (1803)</b> — bola pejal tak terbagi.</li>
          <li><b>Thomson (1897)</b> — roti kismis; elektron tersebar dalam bola positif.</li>
          <li><b>Rutherford (1911)</b> — inti kecil positif, sebagian besar ruang kosong.</li>
          <li><b>Bohr (1913)</b> — elektron di kulit dengan energi tertentu.</li>
          <li><b>Mekanika kuantum</b> — elektron dalam orbital (awan elektron).</li>
        </ol>
      </details>

      <div className="scroll-halus flex gap-2 overflow-x-auto">
        {SEMUA_GOLONGAN.map((g) => (
          <button
            key={g.key}
            type="button"
            onClick={() => setAktif(g.key)}
            className={`shrink-0 rounded-full px-3 py-1.5 text-xs font-extrabold transition cursor-pointer ${
              aktif === g.key
                ? GAYA_GOLONGAN[g.key].fill
                : 'bg-white text-tinta/60 shadow-empuk hover:bg-kertas'
            }`}
          >
            {g.nama}
          </button>
        ))}
      </div>

      <section
        className={`rounded-3xl border border-black/10 p-4 shadow-empuk ${GAYA_GOLONGAN[aktif].soft}`}
      >
        <div className="flex items-baseline justify-between">
          <h2 className="font-display text-lg font-extrabold">{info.nama}</h2>
          <span className="text-xs font-bold opacity-70">
            Golongan {info.nomorGolongan}
          </span>
        </div>
        <p className="mt-1 text-sm">{info.deskripsi}</p>
        <ul className="mt-2 list-inside list-disc text-xs opacity-80">
          {info.fakta.slice(0, 3).map((f, i) => (
            <li key={i}>{f}</li>
          ))}
        </ul>
      </section>

      <div className="flex flex-col gap-3 pb-6">
        {unsur.map((u) => (
          <div
            key={u.simbol}
            className="flex gap-3 rounded-2xl border border-black/10 bg-white p-3 shadow-empuk"
          >
            <Card kartu={kartuDariUnsur(u)} ukuran="sm" />
            <div className="min-w-0">
              <p className="font-display text-sm font-extrabold text-tinta">
                {u.namaUnsur}{' '}
                <span className="text-tinta/50">
                  ({u.simbol}) · Periode {u.periode}
                </span>
              </p>
              <p className="mt-0.5 text-xs font-bold text-lab">
                Z = {u.nomorAtom} · A = {u.nomorMassa} → p = {u.nomorAtom}, e ={' '}
                {u.nomorAtom}, n = {u.nomorMassa - u.nomorAtom}
              </p>
              {u.fakta && (
                <p className="mt-0.5 text-xs text-tinta/70">{u.fakta}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
