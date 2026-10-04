#!/usr/bin/env python3
"""
Generator bank soal UNO-Atom — VERSI MODUL (20 soal).

Menulis ulang:
  src/data/kuis.ts     (BANK_SOAL, 20 soal)
  src/data/funfact.ts  (SEMUA_FUNFACT)

Rancangan (selaras modul Bab 3 "Pengenalan Atom dan Komponennya"):
  - 4 TP x 5 soal = 20 soal.
  - Tiap golongan (warna kartu) punya TEPAT 1 soal untuk tiap TP (5 x 4 = 20).
  - Tingkat: mudah 7 (kartu +2), sedang 7 & sulit 6 (kartu Reaksi Eksplosif);
    tiap tingkat mencakup keempat TP.
Angka pada soal hitungan (TP3/TP4) DIHITUNG dari data unsur di bawah.
Versi lama 107 soal diarsipkan di scripts/gen-soal-atom-107.py.

Jalankan:  npm run gen:soal   (lalu npm test && npm run sync:supabase)
"""
import json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rng = random.Random(20261005)

# (nama, Z, A isotop paling melimpah) — HARUS sama dengan src/data/unsur.ts
U = {
    'Na': ('Natrium', 11, 23), 'Sr': ('Stronsium', 38, 88), 'Ca': ('Kalsium', 20, 40),
    'Mg': ('Magnesium', 12, 24), 'Cl': ('Klorin', 17, 35), 'Br': ('Bromin', 35, 79),
    'Ne': ('Neon', 10, 20), 'Ar': ('Argon', 18, 40), 'Fe': ('Besi', 26, 56),
}
SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
def notasi(sim, A=None, Z=None):
    _, z, a = U[sim]
    return f'{str(a if A is None else A).translate(SUP)}{str(z if Z is None else Z).translate(SUB)}{sim}'
def muatan(q):
    return {1: '⁺', -1: '⁻', 2: '²⁺', -2: '²⁻', 3: '³⁺'}[q]

SOAL = []
counter = {'mudah': 0, 'sedang': 0, 'sulit': 0}
PREFIX = {'mudah': 'm', 'sedang': 's', 'sulit': 'x'}

def soal(gol, tingkat, tp, kunci, pertanyaan, benar, salah, pembahasan):
    pilihan = [benar] + list(salah)
    assert len(pilihan) == 4 and len(set(pilihan)) == 4, (pertanyaan, pilihan)
    rng.shuffle(pilihan)
    counter[tingkat] += 1
    SOAL.append(dict(id=f'{PREFIX[tingkat]}{counter[tingkat]:02d}', pertanyaan=pertanyaan, pilihan=pilihan,
                     jawabanBenar=pilihan.index(benar), golonganTerkait=gol, tingkatKesulitan=tingkat,
                     tpTerkait=[tp], pembahasan=pembahasan, _kunci=set(kunci)))

# ═══════════════ TP1 — Perkembangan model atom (C2) ═══════════════
soal('alkali', 'mudah', 1, ['dalton', 'dalton-lemah', 'urutan'],
     'Ilmuwan yang pertama kali menyatakan bahwa atom adalah partikel terkecil yang tidak dapat dibagi lagi adalah…',
     'John Dalton', ['J.J. Thomson', 'Ernest Rutherford', 'Niels Bohr'],
     'Dalton (1803) menggambarkan atom sebagai bola pejal yang tidak dapat dibagi lagi.')
soal('gasMulia', 'mudah', 1, ['bohr', 'bohr-nyala', 'bohr-lemah'],
     'Menurut Bohr, elektron bergerak mengelilingi inti pada lintasan dengan energi tertentu yang disebut…',
     'kulit atau tingkat energi', ['inti atom', 'sinar katode', 'ruang hampa'],
     'Bohr: elektron hanya menempati lintasan (kulit) dengan tingkat energi tertentu.')
soal('alkaliTanah', 'sedang', 1, ['alfa-tembus', 'rutherford', 'alfa-pantul', 'rutherford-lemah'],
     'Pada percobaan Rutherford, sebagian besar sinar alfa diteruskan tanpa dibelokkan saat menembus lempeng emas tipis. Hal ini menunjukkan bahwa…',
     'sebagian besar atom berupa ruang kosong', ['atom bermuatan negatif', 'elektron tersebar merata di dalam atom', 'atom tidak memiliki inti'],
     'Sinar alfa menembus lurus karena sebagian besar volume atom adalah ruang kosong.')
soal('transisi', 'sedang', 1, ['urutan', 'kuantum', 'kuantum-posisi'],
     'Urutan perkembangan model atom yang benar adalah…',
     'Dalton → Thomson → Rutherford → Bohr → Mekanika kuantum',
     ['Thomson → Dalton → Bohr → Rutherford → Mekanika kuantum', 'Dalton → Rutherford → Thomson → Bohr → Mekanika kuantum', 'Dalton → Thomson → Bohr → Rutherford → Mekanika kuantum'],
     'Setiap model memperbaiki kelemahan model sebelumnya sesuai urutan waktu penemuannya.')
soal('halogen', 'sulit', 1, ['thomson', 'thomson-elektron', 'rutherford'],
     'Perbedaan utama model atom Thomson dan model atom Rutherford terletak pada…',
     'letak muatan positif: tersebar merata (Thomson), terpusat di inti (Rutherford)',
     ['jumlah elektron: model Thomson lebih banyak', 'Thomson sudah mengenal neutron, Rutherford belum', 'Rutherford menganggap atom tidak dapat dibagi'],
     'Thomson: muatan positif tersebar merata seperti roti kismis. Rutherford: muatan positif terpusat di inti yang kecil.')

# ═══════════════ TP2 — Partikel penyusun atom (C2) ═══════════════
soal('alkaliTanah', 'mudah', 2, ['neutron', 'chadwick'],
     'Partikel penyusun atom yang tidak bermuatan (netral) adalah…',
     'neutron', ['proton', 'elektron', 'ion'],
     'Neutron tidak bermuatan dan berada di inti bersama proton (ditemukan Chadwick, 1932).')
soal('transisi', 'mudah', 2, ['proton', 'sinar-kanal', 'inti'],
     'Partikel bermuatan positif yang terdapat di dalam inti atom adalah…',
     'proton', ['elektron', 'neutron', 'foton'],
     'Proton bermuatan +1 dan berada di inti atom.')
soal('alkali', 'sedang', 2, ['netral', 'elektron', 'sinar-katode'],
     'Atom bersifat netral (tidak bermuatan) karena…',
     'jumlah proton sama dengan jumlah elektron',
     ['jumlah neutron sama dengan jumlah proton', 'atom tidak memiliki elektron', 'jumlah neutron sama dengan jumlah elektron'],
     'Muatan +1 setiap proton diimbangi muatan −1 setiap elektron.')
soal('halogen', 'sedang', 2, ['massa-inti', 'massa-rasio', 'inti'],
     'Massa atom dianggap terpusat pada inti karena…',
     'massa proton dan neutron jauh lebih besar daripada massa elektron',
     ['elektron tidak memiliki muatan', 'jumlah elektron selalu lebih sedikit daripada proton', 'inti atom berukuran sangat besar'],
     'Massa elektron hanya ±1/1836 massa proton, sehingga massa atom hampir seluruhnya berasal dari inti.')
soal('gasMulia', 'sulit', 2, ['tabel-partikel', 'elektron', 'beda-unsur', 'nomor-atom'],
     'Pernyataan yang benar tentang partikel penyusun atom adalah…',
     'elektron: muatan −1, massa sangat kecil, berada di kulit atom',
     ['proton: muatan 0, massa ±1 sma, berada di kulit atom', 'neutron: muatan +1, massa sangat kecil, berada di inti', 'elektron: muatan +1, massa ±1 sma, berada di inti'],
     'Proton (+1, ±1 sma, inti); neutron (0, ±1 sma, inti); elektron (−1, ≈0 sma, kulit).')

# ═══════════════ TP3 — p, n, e atom netral dari notasi (C3) ═══════════════
nama, Z, A = U['Sr']
soal('alkaliTanah', 'mudah', 3, ['tp3-proton', 'nomor-atom'],
     f'Atom {nama} (Sr) memiliki nomor atom {Z} dan nomor massa {A}. Jumlah proton dalam atom Sr adalah…',
     str(Z), [str(A - Z), str(A), str(A + Z)], f'Jumlah proton = nomor atom = {Z}.')
nama, Z, A = U['Br']
soal('halogen', 'mudah', 3, ['tp3-arti-z', 'tp3-notasi'],
     f'Kartu {nama} bertuliskan notasi {notasi("Br")}. Angka {Z} pada notasi tersebut menyatakan…',
     'nomor atom (jumlah proton)', ['nomor massa (jumlah proton + neutron)', 'jumlah neutron', 'nomor periode'],
     f'Pada notasi atom, angka atas = nomor massa ({A}) dan angka bawah = nomor atom ({Z}) = jumlah proton.')
nama, Z, A = U['Ar']
soal('gasMulia', 'sedang', 3, ['tp3-neutron', 'nomor-massa'],
     f'Perhatikan notasi atom {notasi("Ar")}. Jumlah neutron dalam atom tersebut adalah…',
     str(A - Z), [str(A), str(Z), str(A + Z)], f'Neutron = A − Z = {A} − {Z} = {A - Z}.')
nama, Z, A = U['Na']
n = A - Z
soal('alkali', 'sulit', 3, ['tp3-notasi', 'tp3-massa', 'nomor-massa'],
     f'Suatu atom {nama} memiliki {Z} proton, {Z} elektron, dan {n} neutron. Notasi atom yang tepat adalah…',
     notasi('Na'), [notasi('Na', A=Z, Z=A), notasi('Na', A=n, Z=Z), notasi('Na', A=A, Z=n)],
     f'Z = proton = {Z} (ditulis di bawah); A = {Z} + {n} = {A} (ditulis di atas): {notasi("Na")}.')
nama, Z, A = U['Fe']
n = A - Z
soal('transisi', 'sulit', 3, ['tp3-triplet', 'tp3-elektron', 'tp3-neutron', 'netral'],
     f'Atom netral {notasi("Fe")} memiliki jumlah proton, elektron, dan neutron berturut-turut…',
     f'{Z}, {Z}, dan {n}', [f'{Z}, {n}, dan {Z}', f'{A}, {Z}, dan {n}', f'{Z}, {Z}, dan {A}'],
     f'p = e = Z = {Z}; n = A − Z = {A} − {Z} = {n}.')

# ═══════════════ TP4 — Ion: kation & anion (C2/C3) ═══════════════
soal('alkali', 'mudah', 4, ['kation', 'tp4-terbentuk', 'tp4-proton'],
     'Ion Na⁺ terbentuk ketika atom Na…',
     'melepas 1 elektron', ['menerima 1 elektron', 'melepas 1 proton', 'menerima 1 proton'],
     'Muatan +1 berarti atom kekurangan 1 elektron (Na → Na⁺ + e⁻); jumlah proton tidak berubah.')
nama, Z, A = U['Cl']
soal('halogen', 'sedang', 4, ['anion', 'tp4-elektron', 'tp4-elektron-anion'],
     f'Atom Cl bernomor atom {Z}. Jumlah elektron pada ion Cl⁻ adalah…',
     str(Z + 1), [str(Z), str(Z - 1), str(A)],
     f'Cl menerima 1 elektron: elektron Cl⁻ = Z − muatan = {Z} − (−1) = {Z + 1}.')
nama, Z, A = U['Mg']
soal('gasMulia', 'sedang', 4, ['tp4-isoelek', 'tp4-gm-stabil', 'tp4-elektron'],
     f'Ion Mg²⁺ (nomor atom Mg = {Z}) memiliki jumlah elektron yang sama dengan atom gas mulia…',
     'Neon (Ne)', ['Argon (Ar)', 'Kripton (Kr)', 'Helium (He)'],
     f'Elektron Mg²⁺ = {Z} − 2 = {Z - 2}, sama dengan atom Ne (Z = 10).')
nama, Z, A = U['Ca']
n, e = A - Z, Z - 2
soal('alkaliTanah', 'sulit', 4, ['kation', 'tp4-elektron', 'tp4-proton'],
     f'Ion {notasi("Ca")}²⁺ memiliki jumlah proton, neutron, dan elektron berturut-turut…',
     f'{Z}, {n}, dan {e}', [f'{Z}, {n}, dan {Z}', f'{e}, {n}, dan {Z}', f'{Z}, {A}, dan {e}'],
     f'p = Z = {Z}; n = A − Z = {A} − {Z} = {n}; e = Z − muatan = {Z} − 2 = {e}.')
nama, Z, A = U['Fe']
n, e = A - Z, Z - 3
soal('transisi', 'sulit', 4, ['tp4-transisi', 'tp4-elektron', 'nomor-massa'],
     f'Ion besi bermuatan +3 (Fe³⁺) memiliki {e} elektron dan {n} neutron. Nomor massa ion tersebut adalah…',
     str(A), [str(e + n), str(Z), str(A + 3)],
     f'Proton = elektron + muatan = {e} + 3 = {Z}; A = p + n = {Z} + {n} = {A}.')

FUNFACT = [
    ('ff-dalton', 'John Dalton (1803) menganggap atom sebagai bola pejal kecil yang tidak dapat dibagi lagi — mirip bola biliar. Model ini belum mengenal elektron.', 'alkali', '🎱', ['dalton', 'dalton-lemah']),
    ('ff-thomson', 'J.J. Thomson (1897) menemukan elektron lewat sinar katode, lalu menggambarkan atom seperti roti kismis: bola bermuatan positif bertabur elektron.', 'alkaliTanah', '🍞', ['thomson', 'thomson-elektron']),
    ('ff-rutherford', 'Pada percobaan lempeng emas, sebagian besar sinar alfa menembus lurus (atom banyak ruang kosong), sebagian kecil terpental (ada inti kecil, padat, dan positif).', 'halogen', '🎯', ['rutherford', 'alfa-tembus', 'alfa-pantul']),
    ('ff-rutherford-lemah', 'Menurut fisika klasik, elektron yang terus berputar akan kehilangan energi dan jatuh ke inti. Model Rutherford tidak bisa menjelaskan mengapa itu tidak terjadi.', 'gasMulia', '🌀', ['rutherford-lemah']),
    ('ff-bohr', 'Niels Bohr (1913): elektron hanya boleh berada di kulit dengan energi tertentu. Saat elektron turun ke kulit lebih rendah, energi dipancarkan sebagai cahaya.', 'gasMulia', '💡', ['bohr', 'bohr-nyala']),
    ('ff-uji-nyala', 'Uji nyala di lab analisis: natrium kuning, kalium ungu, tembaga hijau-biru. Warnanya muncul dari elektron yang kembali ke tingkat energi lebih rendah — bukti model Bohr.', 'alkali', '🔥', ['bohr-nyala']),
    ('ff-bohr-lemah', 'Model Bohr sangat tepat untuk atom hidrogen, tetapi gagal menjelaskan spektrum atom yang elektronnya banyak.', 'halogen', '📉', ['bohr-lemah']),
    ('ff-kuantum', 'Model atom modern (mekanika kuantum) tidak menggambar lintasan elektron. Yang bisa ditentukan hanya daerah peluang terbesar menemukan elektron: orbital atau "awan elektron".', 'transisi', '☁️', ['kuantum', 'kuantum-posisi']),
    ('ff-urutan', 'Urutan model atom: Dalton → Thomson → Rutherford → Bohr → Mekanika Kuantum. Setiap model memperbaiki kelemahan model sebelumnya.', 'transisi', '🧭', ['urutan']),
    ('ff-elektron', 'Elektron bermuatan −1 dan massanya hanya sekitar 1/1836 massa proton, sehingga sering dianggap nol.', 'alkali', '⚡', ['elektron', 'massa-rasio', 'tabel-partikel']),
    ('ff-proton', 'Proton bermuatan +1 dan berada di inti. Sinar kanal yang diamati Eugen Goldstein menjadi petunjuk awal adanya partikel bermuatan positif.', 'transisi', '➕', ['proton', 'sinar-kanal']),
    ('ff-neutron', 'Neutron ditemukan James Chadwick pada tahun 1932. Neutron tidak bermuatan dan massanya hampir sama dengan proton.', 'alkaliTanah', '⚪', ['neutron', 'chadwick']),
    ('ff-inti', 'Hampir seluruh massa atom terpusat di inti, padahal diameter inti hanya sekitar 1/100.000 diameter atom. Sisanya ruang kosong tempat elektron bergerak.', 'alkaliTanah', '🏟️', ['inti', 'massa-inti', 'alfa-tembus']),
    ('ff-sinar-katode', 'Sinar katode dibelokkan ke kutub positif medan listrik — bukti bahwa sinar ini tersusun atas partikel bermuatan negatif, yaitu elektron.', 'halogen', '📺', ['sinar-katode', 'thomson-elektron']),
    ('ff-netral', 'Atom netral selalu memiliki jumlah proton = jumlah elektron, sehingga muatan positif dan negatifnya saling meniadakan.', 'gasMulia', '⚖️', ['netral', 'tp3-elektron']),
    ('ff-nomor-atom', 'Nomor atom (Z) = jumlah proton. Inilah "KTP" sebuah unsur: atom dengan jumlah proton berbeda pasti unsur yang berbeda.', 'halogen', '🪪', ['nomor-atom', 'beda-unsur', 'tp3-proton', 'tp3-arti-z']),
    ('ff-nomor-massa', 'Nomor massa (A) = jumlah proton + jumlah neutron. Jadi jumlah neutron = A − Z.', 'alkali', '🧮', ['nomor-massa', 'tp3-neutron', 'tp3-massa']),
    ('ff-notasi-kartu', 'Lihat pojok kiri lambang unsur di kartumu! Angka atas = nomor massa (A), angka bawah = nomor atom (Z). Contoh ²³₁₁Na: 11 proton, 11 elektron, 12 neutron.', 'transisi', '🏷️', ['tp3-arti-z', 'tp3-notasi', 'tp3-triplet']),
    ('ff-isotop-kartu', 'Nomor massa di kartu adalah isotop yang paling melimpah. Klorin di alam kebanyakan ³⁵Cl dan sebagian ³⁷Cl — itulah sebabnya massa atom relatif Cl ≈ 35,5.', 'halogen', '🔬', ['tp3-neutron']),
    ('ff-kation', 'Atom logam cenderung melepas elektron membentuk ion positif (kation). Contoh: Na → Na⁺ + e⁻. Jumlah protonnya tetap 11!', 'alkali', '🔋', ['kation', 'tp4-terbentuk', 'tp4-proton']),
    ('ff-anion', 'Atom nonlogam seperti halogen cenderung menerima elektron membentuk ion negatif (anion). Contoh: Cl + e⁻ → Cl⁻, sehingga elektronnya menjadi 18.', 'halogen', '🧲', ['anion', 'tp4-elektron-anion', 'tp4-terbentuk']),
    ('ff-rumus-ion', 'Rumus cepat jumlah elektron ion: e = Z − muatan. Mg²⁺: 12 − 2 = 10. Cl⁻: 17 − (−1) = 18.', 'alkaliTanah', '✏️', ['tp4-elektron', 'tp4-elektron-anion']),
    ('ff-isoelektronik', 'Banyak ion memiliki jumlah elektron sama dengan gas mulia terdekat: Na⁺, Mg²⁺, dan F⁻ sama-sama memiliki 10 elektron, seperti neon.', 'gasMulia', '🎈', ['tp4-isoelek']),
    ('ff-transisi-ion', 'Logam transisi dapat membentuk lebih dari satu jenis ion, misalnya Fe²⁺ dan Fe³⁺. Keduanya tetap memiliki 26 proton; yang berbeda hanya jumlah elektronnya.', 'transisi', '🧲', ['tp4-transisi', 'tp4-proton']),
    ('ff-gm-stabil', 'Gas mulia hampir tidak pernah membentuk ion karena susunan elektronnya sudah stabil: 2 elektron untuk helium, 8 elektron di kulit terluar untuk yang lain.', 'gasMulia', '🛡️', ['tp4-gm-stabil']),
    ('ff-uji-klorida', 'Di laboratorium kimia analisis, ion Cl⁻ dalam sampel air dapat dideteksi dengan larutan AgNO₃: terbentuk endapan putih AgCl.', 'halogen', '🧪', ['anion']),
    ('ff-air-sadah', 'Air sadah mengandung ion Ca²⁺ dan Mg²⁺. Analis menentukan kadarnya dengan titrasi kompleksometri menggunakan EDTA.', 'alkaliTanah', '💧', ['kation', 'tp4-elektron']),
    ('ff-jembatan-spu', 'Tabel periodik modern disusun berdasarkan kenaikan nomor atom (jumlah proton). Jadi, menghitung proton sama dengan menemukan "alamat" unsur di tabel periodik.', 'transisi', '🗺️', ['nomor-atom', 'beda-unsur']),
    ('ff-lapangan', 'Jika inti atom sebesar bola pingpong di tengah lapangan sepak bola, elektron berada di sekitar tribun penonton. Atom sebagian besar adalah ruang kosong!', 'alkali', '⚽', ['alfa-tembus', 'inti']),
]

# Fun Fact yang tak punya kunci cocok ditautkan ke soal se-TP-nya.
TP_KUNCI = {
    1: {'dalton', 'dalton-lemah', 'thomson', 'thomson-elektron', 'rutherford', 'rutherford-lemah', 'alfa-tembus',
        'alfa-pantul', 'bohr', 'bohr-nyala', 'bohr-lemah', 'kuantum', 'kuantum-posisi', 'urutan'},
    2: {'elektron', 'proton', 'neutron', 'chadwick', 'inti', 'massa-inti', 'massa-rasio', 'netral', 'sinar-katode',
        'sinar-kanal', 'tabel-partikel', 'beda-unsur', 'nomor-atom'},
}
def tp_dari(kunci):
    for tp, ks in TP_KUNCI.items():
        if set(kunci) & ks: return tp
    return 4 if any(k.startswith('tp4') or k in ('kation', 'anion') for k in kunci) else 3

def ids_untuk(kunci):
    out = [q['id'] for q in SOAL if q['_kunci'] & set(kunci)]
    return out or [q['id'] for q in SOAL if tp_dari(kunci) in q['tpTerkait']]

# ── Validasi rancangan ──
from collections import Counter
GOLS = ['alkali', 'alkaliTanah', 'halogen', 'gasMulia', 'transisi']
assert len(SOAL) == 20
for g in GOLS:
    assert sorted(q['tpTerkait'][0] for q in SOAL if q['golonganTerkait'] == g) == [1, 2, 3, 4], g
for t in ['mudah', 'sedang', 'sulit']:
    assert {q['tpTerkait'][0] for q in SOAL if q['tingkatKesulitan'] == t} == {1, 2, 3, 4}, t

def ts(s): return json.dumps(s, ensure_ascii=False)
baris = ["import type { SoalKuis } from './types';", '', '/**',
         ' * Bank soal UNO-Atom — VERSI MODUL: 20 soal (4 TP x 5 soal).',
         ' * Tiap golongan punya tepat 1 soal untuk tiap TP; tiap tingkat mencakup keempat TP.',
         ' *   TP1 perkembangan model atom · TP2 partikel penyusun atom ·',
         ' *   TP3 p/n/e atom netral dari notasi · TP4 ion (kation & anion).',
         ' * DIBANGKITKAN oleh scripts/gen-soal-atom.py — jangan diedit manual.',
         ' * Dipakai QuizModal: draw2 -> `mudah`, wild4 -> `sedang`/`sulit`.', ' */',
         'export const BANK_SOAL: SoalKuis[] = [']
for t in ['mudah', 'sedang', 'sulit']:
    baris.append(f'  // ─────────────── {t.upper()} ───────────────')
    for q in [x for x in SOAL if x['tingkatKesulitan'] == t]:
        baris += ['  {', f"    id: '{q['id']}',", f"    pertanyaan: {ts(q['pertanyaan'])},",
                  f"    pilihan: [{', '.join(ts(p) for p in q['pilihan'])}],", f"    jawabanBenar: {q['jawabanBenar']},",
                  f"    golonganTerkait: '{q['golonganTerkait']}',", f"    tingkatKesulitan: '{q['tingkatKesulitan']}',",
                  f"    tpTerkait: {json.dumps(q['tpTerkait'])},", f"    pembahasan: {ts(q['pembahasan'])},", '  },']
baris.append('];\n')
(ROOT / 'src/data/kuis.ts').write_text('\n'.join(baris), encoding='utf-8')

fb = ["import type { FunFact } from './types';", '', '/**',
      f' * Bank Fun Fact UNO-Atom — {len(FUNFACT)} fakta tentang model atom, partikel penyusun atom,',
      ' * notasi atom, dan ion. `bantuSoal` menautkan ke soal terkait di src/data/kuis.ts.',
      ' * DIBANGKITKAN oleh scripts/gen-soal-atom.py — jangan diedit manual.', ' */',
      'export const SEMUA_FUNFACT: FunFact[] = [']
for fid, teks, gol, ikon, kunci in FUNFACT:
    fb += ['  {', f"    id: '{fid}',", f'    teks: {ts(teks)},', f"    golongan: '{gol}',", f"    ikon: '{ikon}',",
           f"    bantuSoal: [{', '.join(repr(i) for i in ids_untuk(kunci))}],", '  },']
fb.append('];\n')
(ROOT / 'src/data/funfact.ts').write_text('\n'.join(fb), encoding='utf-8')

print('soal:', len(SOAL), dict(Counter(q['tingkatKesulitan'] for q in SOAL)), dict(Counter(q['tpTerkait'][0] for q in SOAL)))
print('funfact:', len(FUNFACT))

# ── Dokumen rekap untuk lampiran modul ──
NAMA_GOL = {'alkali': 'Alkali (merah)', 'alkaliTanah': 'Alkali Tanah (oranye)', 'halogen': 'Halogen (kuning)',
            'gasMulia': 'Gas Mulia (hijau)', 'transisi': 'Transisi (biru)'}
TP_NAMA = {1: 'Perkembangan model atom', 2: 'Partikel penyusun atom', 3: 'p, n, e atom netral dari notasi', 4: 'Ion (kation & anion)'}
md = ['# Bank Soal UNO-Atom — Versi Modul (20 soal)', '',
      'Dibangkitkan oleh `scripts/gen-soal-atom.py`. Kunci jawaban **dicetak tebal**.', '',
      '| No | ID | TP | Tingkat | Golongan (warna kartu) |', '|---|---|---|---|---|']
urut = sorted(SOAL, key=lambda q: (q['tpTerkait'][0], ['mudah', 'sedang', 'sulit'].index(q['tingkatKesulitan'])))
for i, q in enumerate(urut, 1):
    md.append(f"| {i} | {q['id']} | TP{q['tpTerkait'][0]} | {q['tingkatKesulitan']} | {NAMA_GOL[q['golonganTerkait']]} |")
for tp in [1, 2, 3, 4]:
    md += ['', f'## TP{tp} — {TP_NAMA[tp]}', '']
    for i, q in enumerate(urut, 1):
        if q['tpTerkait'][0] != tp: continue
        md.append(f"**{i}. ({q['tingkatKesulitan']}, {NAMA_GOL[q['golonganTerkait']]})** {q['pertanyaan']}  ")
        for j, p in enumerate(q['pilihan']):
            huruf = 'ABCD'[j]
            md.append(f"{huruf}. **{p}**  " if j == q['jawabanBenar'] else f'{huruf}. {p}  ')
        md += [f"_Pembahasan:_ {q['pembahasan']}", '']
(ROOT / 'docs/BANK-SOAL-20.md').write_text('\n'.join(md), encoding='utf-8')
