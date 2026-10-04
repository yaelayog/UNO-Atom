# UNO-Chem Edisi Struktur Atom — Panduan Setup Proyek Baru

Repo ini adalah salinan UNO-Chem (SPU kelas XI) yang dialihkan ke materi
**Pengenalan Atom dan Komponennya** untuk **Dasar-Dasar Kimia Analisis, Fase E,
kelas X SMK**. Mekanik UNO tidak berubah (warna = golongan, angka = periode);
yang berubah adalah isi pembelajaran.

## Apa yang berubah dibanding UNO-Chem asli

| Bagian | Perubahan |
|---|---|
| `src/data/unsur.ts`, `types.ts` | Tiap unsur punya `nomorMassa` (isotop paling melimpah; unsur radioaktif = isotop paling stabil). |
| `src/components/Card.tsx` | Kartu unsur menampilkan notasi atom: nomor massa di atas, nomor atom di bawah, di kiri lambang. |
| `src/data/cptp.ts` | 4 TP baru: (1) perkembangan model atom, (2) partikel penyusun atom, (3) p/n/e atom netral dari notasi, (4) ion (kation & anion). |
| `src/data/kuis.ts` | 107 soal baru. Setiap golongan × tingkat kesulitan punya soal untuk keempat TP. |
| `src/data/funfact.ts` | 29 Fun Fact baru bertema struktur atom, terhubung ke soal terkait. |
| `scripts/gen-soal-atom.py` | **Generator** kuis.ts & funfact.ts. Soal hitungan (TP3/TP4) dihitung otomatis dari data unsur. |
| `BelajarScreen`, `InfoScreen`, `MainMenu` | Panel "Kenali Atom", rincian p/e/n per unsur, petunjuk membaca notasi, branding. |
| `src/data/data.test.ts` | Test baru: nomor massa valid & notasi di soal selalu cocok dengan data unsur. |

**Mengubah soal:** edit `scripts/gen-soal-atom.py`, lalu jalankan
`npm run gen:soal` → `npm test` → `npm run sync:supabase`.
Jangan mengedit `kuis.ts`/`funfact.ts` langsung (akan tertimpa generator).

## Langkah setup (sekali saja)

### 1. Repo GitHub baru
```bash
git init && git add . && git commit -m "UNO-Chem Edisi Struktur Atom"
git branch -M main
git remote add origin https://github.com/<akun>/<repo-baru>.git
git push -u origin main
```

### 2. Project Supabase baru
Ikuti `docs/ONLINE.md`, dengan catatan berikut:
1. Buat project baru → salin **Project URL** & **anon key** ke `.env`
   (lihat `.env.example`). Aktifkan **Anonymous sign-in**.
2. Skema: `supabase link --project-ref <ref-baru>` → `supabase db push`
   (atau tempel `supabase/skema.sql` di SQL Editor).
3. **Wajib sebelum deploy fungsi:** `npm run sync:supabase` (menyalin engine &
   bank soal BARU ke `supabase/functions/_shared/`). Tanpa langkah ini, mode
   online memakai soal yang salah.
4. Deploy: `supabase functions deploy aksi --no-verify-jwt`,
   `supabase functions deploy akun --no-verify-jwt`,
   `supabase functions deploy reset-mingguan --no-verify-jwt`.
5. `supabase secrets set CRON_SECRET=<acak-panjang>` lalu pasang jadwal pg_cron
   seperti di `docs/ONLINE.md` — **ganti URL dengan project baru**.
6. (Opsional) TURN server untuk suara chat: isi `VITE_TURN_*` di `.env`.

### 3. Project Vercel baru
Import repo baru → isi Environment Variables `VITE_SUPABASE_URL` &
`VITE_SUPABASE_ANON_KEY` (project BARU) → Deploy. Lihat `docs/DEPLOY-VERCEL.md`.

## Hal yang SENGAJA tidak diubah
- **`android-twa/` & `public/.well-known/assetlinks.json`** masih menunjuk ke
  `uno-chem.vercel.app` / `com.chemuno.app`. Jika ingin APK Edisi Atom, ganti
  `packageId`, `host`, buat keystore baru, dan perbarui assetlinks (lihat `docs/APK.md`).
- **`src/data/kredit.ts` → `kompetisi`** dan logo panitia FORKOM di menu utama:
  hapus/ubah jika aplikasi dipakai untuk kelas, bukan lomba.
- **`src/data/golongan.ts`** (fakta golongan) & Kartu Peristiwa: tetap, karena
  mekanik warna = golongan dipertahankan sebagai jembatan ke materi SPU berikutnya.
- Logo `public/logo-chemuno.png` masih logo asli.
