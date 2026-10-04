#!/usr/bin/env python3
"""
Generator bank soal & Fun Fact UNO-Chem Edisi Struktur Atom.

Menulis ulang:
  src/data/kuis.ts     (BANK_SOAL)
  src/data/funfact.ts  (SEMUA_FUNFACT)

Soal TP3 & TP4 (hitungan proton/neutron/elektron) DIHITUNG dari data unsur di
bawah ini, sehingga tidak ada salah hitung manual. Soal TP1 & TP2 (konsep)
ditulis manual. Jalankan ulang setelah mengubah isi:  python3 scripts/gen-soal-atom.py
"""
import json, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rng = random.Random(20261004)

# ── Data unsur (Z, A isotop paling melimpah) — HARUS sama dengan src/data/unsur.ts ──
U = {
    'Li': ('Litium', 3, 7), 'Na': ('Natrium', 11, 23), 'K': ('Kalium', 19, 39),
    'Rb': ('Rubidium', 37, 85), 'Cs': ('Sesium', 55, 133),
    'Be': ('Berilium', 4, 9), 'Mg': ('Magnesium', 12, 24), 'Ca': ('Kalsium', 20, 40),
    'Sr': ('Stronsium', 38, 88), 'Ba': ('Barium', 56, 138),
    'F': ('Fluorin', 9, 19), 'Cl': ('Klorin', 17, 35), 'Br': ('Bromin', 35, 79), 'I': ('Iodin', 53, 127),
    'He': ('Helium', 2, 4), 'Ne': ('Neon', 10, 20), 'Ar': ('Argon', 18, 40),
    'Kr': ('Kripton', 36, 84), 'Xe': ('Xenon', 54, 132),
    'Fe': ('Besi', 26, 56), 'Cu': ('Tembaga', 29, 63), 'Zn': ('Seng', 30, 64), 'Ag': ('Perak', 47, 107),
    'Au': ('Emas', 79, 197), 'Mn': ('Mangan', 25, 55), 'Ni': ('Nikel', 28, 58),
    'Cr': ('Kromium', 24, 52), 'Co': ('Kobalt', 27, 59), 'Ti': ('Titanium', 22, 48),
}
GOL = {
    'alkali': ['Na', 'K', 'Li', 'Rb', 'Cs'],
    'alkaliTanah': ['Mg', 'Ca', 'Be', 'Sr', 'Ba'],
    'halogen': ['Cl', 'F', 'Br', 'I'],
    'gasMulia': ['Ne', 'Ar', 'Kr', 'Xe', 'He'],
    'transisi': ['Fe', 'Cu', 'Zn', 'Ag', 'Mn', 'Ni', 'Cr', 'Co', 'Ti', 'Au'],
}
ION = {  # muatan ion yang umum
    'alkali': [('Na', 1), ('K', 1), ('Li', 1), ('Rb', 1), ('Cs', 1)],
    'alkaliTanah': [('Mg', 2), ('Ca', 2), ('Sr', 2), ('Ba', 2), ('Be', 2)],
    'halogen': [('Cl', -1), ('F', -1), ('Br', -1), ('I', -1)],
    'transisi': [('Fe', 3), ('Cu', 2), ('Zn', 2), ('Fe', 2), ('Ag', 1), ('Ni', 2), ('Mn', 2), ('Cr', 3)],
}
GAS_MULIA_ELEKTRON = {2: 'He', 10: 'Ne', 18: 'Ar', 36: 'Kr', 54: 'Xe'}

SUP = str.maketrans('0123456789+-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻')
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')

def notasi(sim, A=None, Z=None):
    nama, z, a = U[sim]
    A = a if A is None else A
    Z = z if Z is None else Z
    return f'{str(A).translate(SUP)}{str(Z).translate(SUB)}{sim}'

def muatan(q):
    if q == 1: return '⁺'
    if q == -1: return '⁻'
    return (str(abs(q)) + ('+' if q > 0 else '-')).translate(SUP)

def ion(sim, q): return sim + muatan(q)

def sg(q): return f'+{q}' if q > 0 else f'−{abs(q)}'

def notasi_ion(sim, q): return notasi(sim) + muatan(q)

# ── Penampung soal ──
SOAL = []
counter = {'mudah': 0, 'sedang': 0, 'sulit': 0}
PREFIX = {'mudah': 'm', 'sedang': 's', 'sulit': 'x'}

def tambah(gol, tingkat, tp, pertanyaan, benar, salah, pembahasan, kunci):
    """benar: str; salah: list[str] (≥3, dipakai 3 pertama yang unik)."""
    pilihan = [benar]
    for s in salah:
        if s not in pilihan: pilihan.append(s)
        if len(pilihan) == 4: break
    assert len(pilihan) == 4, (pertanyaan, pilihan)
    rng.shuffle(pilihan)
    counter[tingkat] += 1
    sid = f'{PREFIX[tingkat]}{counter[tingkat]:02d}'
    SOAL.append(dict(id=sid, pertanyaan=pertanyaan, pilihan=pilihan, jawabanBenar=pilihan.index(benar),
                     golonganTerkait=gol, tingkatKesulitan=tingkat, tpTerkait=[tp], pembahasan=pembahasan,
                     _kunci=set(kunci)))

def angka_unik(benar, kandidat):
    out = []
    for k in kandidat:
        if k >= 0 and k != benar and k not in out: out.append(k)
    return [str(x) for x in out]

# ══════════════════ TP1 & TP2 — konsep (manual) ══════════════════
KONSEP = [
    # (golongan, tingkat, tp, kunci, pertanyaan, benar, salah[3], pembahasan)
    # ---- TP1 mudah ----
    ('alkali', 'mudah', 1, ['dalton'], 'Ilmuwan yang pertama kali menyatakan bahwa atom adalah partikel terkecil yang tidak dapat dibagi lagi adalah…',
     'John Dalton', ['J.J. Thomson', 'Ernest Rutherford', 'Niels Bohr'], 'Dalton (1803) menggambarkan atom sebagai bola pejal yang tidak dapat dibagi lagi.'),
    ('alkaliTanah', 'mudah', 1, ['thomson'], 'Model atom Thomson sering diibaratkan seperti…',
     'roti kismis', ['tata surya', 'bola biliar pejal', 'awan elektron'], 'Thomson: bola bermuatan positif dengan elektron tersebar di dalamnya, seperti kismis pada roti.'),
    ('halogen', 'mudah', 1, ['rutherford'], 'Percobaan penembakan sinar alfa pada lempeng emas tipis dilakukan oleh kelompok…',
     'Ernest Rutherford', ['John Dalton', 'J.J. Thomson', 'James Chadwick'], 'Percobaan hamburan sinar alfa (Geiger–Marsden) dirancang Rutherford dan melahirkan konsep inti atom.'),
    ('gasMulia', 'mudah', 1, ['bohr'], 'Menurut Bohr, elektron bergerak mengelilingi inti pada lintasan dengan energi tertentu yang disebut…',
     'kulit atau tingkat energi', ['inti atom', 'sinar katode', 'ruang hampa'], 'Bohr: elektron hanya menempati lintasan (kulit) dengan tingkat energi tertentu.'),
    ('transisi', 'mudah', 1, ['kuantum'], 'Model atom yang berlaku saat ini dan menggambarkan elektron sebagai "awan elektron" (orbital) adalah model atom…',
     'mekanika kuantum', ['Dalton', 'Thomson', 'Rutherford'], 'Model mekanika kuantum menyatakan elektron berada dalam orbital (daerah peluang terbesar).'),
    # ---- TP1 sedang ----
    ('alkali', 'sedang', 1, ['dalton-lemah'], 'Kelemahan model atom Dalton adalah…',
     'tidak dapat menjelaskan sifat listrik materi (adanya partikel bermuatan)',
     ['tidak dapat menjelaskan mengapa elektron tidak jatuh ke inti', 'hanya berlaku untuk atom hidrogen', 'menggambarkan atom seperti roti kismis'],
     'Dalton belum mengenal elektron dan proton, sehingga gejala listrik pada materi tidak terjelaskan.'),
    ('alkaliTanah', 'sedang', 1, ['alfa-tembus'], 'Pada percobaan Rutherford, sebagian besar sinar alfa diteruskan tanpa dibelokkan. Hal ini menunjukkan bahwa…',
     'sebagian besar atom berupa ruang kosong', ['atom bermuatan negatif', 'elektron tersebar merata', 'atom tidak memiliki inti'],
     'Sinar alfa menembus lurus karena sebagian besar volume atom adalah ruang kosong.'),
    ('halogen', 'sedang', 1, ['alfa-pantul'], 'Sebagian kecil sinar alfa dipantulkan kembali saat menumbuk lempeng emas. Rutherford menyimpulkan bahwa atom memiliki…',
     'inti yang sangat kecil, padat, dan bermuatan positif', ['elektron yang tersebar di seluruh atom', 'neutron di kulit terluar', 'muatan positif yang tersebar merata'],
     'Pantulan terjadi saat sinar alfa (positif) menumbuk inti kecil, padat, dan bermuatan positif.'),
    ('gasMulia', 'sedang', 1, ['rutherford-lemah'], 'Kelemahan model atom Rutherford adalah tidak dapat menjelaskan…',
     'mengapa elektron tidak jatuh ke inti', ['adanya inti atom', 'adanya ruang kosong dalam atom', 'muatan inti yang positif'],
     'Menurut fisika klasik elektron yang berputar kehilangan energi lalu jatuh ke inti; Rutherford tidak bisa menjelaskannya.'),
    ('transisi', 'sedang', 1, ['thomson-elektron'], 'Model atom Thomson diajukan setelah ditemukannya…',
     'elektron melalui percobaan sinar katode', ['neutron oleh Chadwick', 'inti atom oleh Rutherford', 'orbital oleh Schrödinger'],
     'Thomson (1897) menemukan elektron dari sinar katode, lalu memasukkannya ke dalam model atomnya.'),
    # ---- TP1 sulit ----
    ('alkali', 'sulit', 1, ['bohr-nyala'], 'Uji nyala natrium menghasilkan warna kuning karena elektron berpindah dari tingkat energi tinggi ke rendah sambil memancarkan cahaya. Model atom yang dapat menjelaskan gejala ini adalah…',
     'model atom Bohr', ['model atom Dalton', 'model atom Thomson', 'model atom Rutherford'], 'Bohr menjelaskan pemancaran cahaya (spektrum) dari perpindahan elektron antartingkat energi.'),
    ('alkaliTanah', 'sulit', 1, ['urutan'], 'Urutan perkembangan model atom yang benar adalah…',
     'Dalton → Thomson → Rutherford → Bohr → Mekanika kuantum',
     ['Thomson → Dalton → Bohr → Rutherford → Mekanika kuantum', 'Dalton → Rutherford → Thomson → Bohr → Mekanika kuantum', 'Dalton → Thomson → Bohr → Rutherford → Mekanika kuantum'],
     'Setiap model memperbaiki kelemahan model sebelumnya sesuai urutan waktu penemuannya.'),
    ('halogen', 'sulit', 1, ['bohr-lemah'], 'Kelemahan model atom Bohr adalah…',
     'hanya dapat menjelaskan spektrum atom berelektron tunggal seperti hidrogen',
     ['tidak mengenal adanya inti atom', 'menganggap atom tidak dapat dibagi', 'tidak mengenal adanya elektron'],
     'Bohr tepat untuk hidrogen tetapi gagal menjelaskan spektrum atom berelektron banyak.'),
    ('gasMulia', 'sulit', 1, ['thomson', 'rutherford'], 'Perbedaan utama model atom Thomson dan Rutherford terletak pada…',
     'letak muatan positif: tersebar merata (Thomson), terpusat di inti (Rutherford)',
     ['jumlah elektron: Thomson lebih banyak', 'Thomson mengenal neutron, Rutherford tidak', 'Rutherford menganggap atom tidak dapat dibagi'],
     'Thomson: muatan positif tersebar merata. Rutherford: muatan positif terpusat di inti yang kecil.'),
    ('transisi', 'sulit', 1, ['kuantum-posisi'], 'Menurut model atom mekanika kuantum, posisi elektron dalam atom…',
     'tidak dapat ditentukan pasti; yang dapat ditentukan adalah peluang keberadaannya (orbital)',
     ['berada pada lintasan berbentuk lingkaran yang pasti', 'tersebar merata di dalam bola positif', 'menempel di permukaan inti'],
     'Mekanika kuantum (Schrödinger, Heisenberg) hanya menentukan daerah peluang terbesar menemukan elektron.'),
    # ---- TP2 mudah ----
    ('alkali', 'mudah', 2, ['elektron'], 'Partikel penyusun atom yang bermuatan negatif adalah…',
     'elektron', ['proton', 'neutron', 'inti atom'], 'Elektron bermuatan −1 dan berada di kulit atom.'),
    ('alkaliTanah', 'mudah', 2, ['neutron'], 'Partikel penyusun atom yang tidak bermuatan (netral) adalah…',
     'neutron', ['proton', 'elektron', 'ion'], 'Neutron tidak bermuatan dan berada di inti bersama proton.'),
    ('halogen', 'mudah', 2, ['inti'], 'Proton dan neutron di dalam atom terletak di…',
     'inti atom', ['kulit atom', 'orbit terluar', 'ruang kosong di luar inti'], 'Proton dan neutron (nukleon) berada di inti; elektron di kulit.'),
    ('gasMulia', 'mudah', 2, ['thomson-elektron', 'sinar-katode'], 'Elektron ditemukan oleh…',
     'J.J. Thomson', ['James Chadwick', 'Eugen Goldstein', 'John Dalton'], 'Thomson menemukan elektron dari percobaan sinar katode (1897).'),
    ('transisi', 'mudah', 2, ['proton'], 'Partikel bermuatan positif yang terdapat di dalam inti atom adalah…',
     'proton', ['elektron', 'neutron', 'foton'], 'Proton bermuatan +1 dan berada di inti atom.'),
    # ---- TP2 sedang ----
    ('alkali', 'sedang', 2, ['chadwick'], 'Neutron ditemukan oleh…',
     'James Chadwick', ['J.J. Thomson', 'Ernest Rutherford', 'Niels Bohr'], 'Chadwick menemukan neutron pada tahun 1932.'),
    ('alkaliTanah', 'sedang', 2, ['massa-inti'], 'Massa atom dianggap terpusat pada inti karena…',
     'massa proton dan neutron jauh lebih besar daripada massa elektron',
     ['elektron tidak memiliki muatan', 'jumlah elektron selalu lebih sedikit dari proton', 'inti atom berukuran sangat besar'],
     'Massa elektron hanya ±1/1836 massa proton, sehingga massa atom hampir seluruhnya berasal dari inti.'),
    ('halogen', 'sedang', 2, ['massa-rasio'], 'Massa sebuah proton kira-kira … kali massa sebuah elektron.',
     '1836', ['18', '2', '1/1836'], 'Massa proton ≈ 1,67 × 10⁻²⁴ g, sekitar 1836 kali massa elektron.'),
    ('gasMulia', 'sedang', 2, ['netral'], 'Atom bersifat netral (tidak bermuatan) karena…',
     'jumlah proton sama dengan jumlah elektron', ['jumlah neutron sama dengan jumlah proton', 'tidak memiliki elektron', 'jumlah neutron sama dengan jumlah elektron'],
     'Muatan +1 setiap proton diimbangi muatan −1 setiap elektron.'),
    ('transisi', 'sedang', 2, ['nomor-atom'], 'Nomor atom (Z) suatu unsur menyatakan…',
     'jumlah proton dalam inti', ['jumlah neutron dalam inti', 'jumlah proton dan neutron', 'jumlah kulit elektron'],
     'Z = jumlah proton. Pada atom netral, jumlah elektron juga sama dengan Z.'),
    # ---- TP2 sulit ----
    ('alkali', 'sulit', 2, ['tabel-partikel'], 'Pernyataan yang benar tentang partikel penyusun atom adalah…',
     'elektron: muatan −1, massa sangat kecil, berada di kulit atom',
     ['proton: muatan 0, massa ±1 sma, berada di kulit atom', 'neutron: muatan +1, massa sangat kecil, berada di inti', 'elektron: muatan +1, massa ±1 sma, berada di inti'],
     'Proton (+1, ±1 sma, inti); neutron (0, ±1 sma, inti); elektron (−1, ±0 sma, kulit).'),
    ('alkaliTanah', 'sulit', 2, ['nomor-massa'], 'Nomor massa (A) suatu atom menyatakan…',
     'jumlah proton ditambah jumlah neutron', ['jumlah proton ditambah jumlah elektron', 'jumlah neutron saja', 'jumlah elektron dikurangi proton'],
     'A = p + n, sehingga jumlah neutron = A − Z.'),
    ('halogen', 'sulit', 2, ['sinar-katode'], 'Sinar katode dibelokkan ke arah kutub positif ketika melewati medan listrik. Hal ini membuktikan bahwa…',
     'sinar katode tersusun atas partikel bermuatan negatif', ['sinar katode bermuatan positif', 'sinar katode tidak bermuatan', 'sinar katode terdiri atas neutron'],
     'Partikel yang tertarik ke kutub positif pasti bermuatan negatif, yaitu elektron.'),
    ('gasMulia', 'sulit', 2, ['beda-unsur'], 'Dua atom dari unsur yang berbeda PASTI memiliki perbedaan dalam hal…',
     'jumlah proton', ['jumlah neutron', 'nomor massa', 'wujud zat'], 'Jumlah proton (nomor atom) adalah identitas unsur; neutron dan nomor massa bisa saja sama.'),
    ('transisi', 'sulit', 2, ['sinar-kanal'], 'Sinar kanal yang diamati Eugen Goldstein merupakan berkas partikel yang bermuatan…',
     'positif', ['negatif', 'netral', 'berubah-ubah'], 'Sinar kanal bergerak berlawanan arah sinar katode dan bermuatan positif — petunjuk awal adanya proton.'),
]
for gol, tk, tp, kunci, q, b, s, p in KONSEP:
    tambah(gol, tk, tp, q, b, s, p, kunci)

# ══════════════════ TP3 — atom netral (dihitung) ══════════════════
for gol, daftar in GOL.items():
    # pilih unsur yang aman (neutron ≠ proton untuk soal yang butuh beda angka)
    aman = [s for s in daftar if U[s][2] - U[s][1] != U[s][1]]
    d = aman
    # mudah
    s1, s2, s3 = d[0], d[1], d[2 % len(d)]
    nama, Z, A = U[s1]
    tambah(gol, 'mudah', 3, f'Atom {nama} ({s1}) memiliki nomor atom {Z} dan nomor massa {A}. Jumlah proton dalam atom {s1} adalah…',
           str(Z), angka_unik(Z, [A - Z, A, Z + 1, Z - 1]), f'Jumlah proton = nomor atom = {Z}.', ['tp3-proton', 'nomor-atom'])
    nama, Z, A = U[s2]
    tambah(gol, 'mudah', 3, f'Atom netral {nama} ({s2}) bernomor atom {Z} dan bernomor massa {A}. Jumlah elektronnya adalah…',
           str(Z), angka_unik(Z, [A - Z, A, Z + 2, Z - 2]), f'Pada atom netral, jumlah elektron = jumlah proton = nomor atom = {Z}.', ['tp3-elektron', 'netral'])
    nama, Z, A = U[s3]
    tambah(gol, 'mudah', 3, f'Kartu {nama} bertuliskan notasi {notasi(s3)}. Angka {Z} pada notasi tersebut menyatakan…',
           'nomor atom (jumlah proton)', ['nomor massa (jumlah proton + neutron)', 'jumlah neutron', 'nomor periode'],
           f'Pada notasi atom, angka atas = nomor massa dan angka bawah ({Z}) adalah nomor atom = jumlah proton.', ['tp3-arti-z', 'tp3-notasi'])
    # sedang
    s1, s2, s3 = d[1 % len(d)], d[2 % len(d)], d[3 % len(d)]
    nama, Z, A = U[s1]
    tambah(gol, 'sedang', 3, f'Perhatikan notasi atom {notasi(s1)}. Jumlah neutron dalam atom tersebut adalah…',
           str(A - Z), angka_unik(A - Z, [A, Z, A + Z, A - Z + 1]), f'Neutron = A − Z = {A} − {Z} = {A - Z}.', ['tp3-neutron', 'nomor-massa'])
    nama, Z, A = U[s2]
    tambah(gol, 'sedang', 3, f'Atom {nama} memiliki {Z} proton dan {A - Z} neutron. Nomor massa atom tersebut adalah…',
           str(A), angka_unik(A, [A - Z, Z, A - 1, A + Z]), f'Nomor massa = proton + neutron = {Z} + {A - Z} = {A}.', ['tp3-massa', 'nomor-massa'])
    nama, Z, A = U[s3]
    tambah(gol, 'sedang', 3, f'Jumlah elektron dan neutron atom netral {notasi(s3)} berturut-turut adalah…',
           f'{Z} dan {A - Z}', [f'{A - Z} dan {Z}', f'{A} dan {Z}', f'{Z} dan {A}', f'{A} dan {A - Z}'],
           f'Elektron = Z = {Z}; neutron = A − Z = {A - Z}.', ['tp3-neutron', 'tp3-elektron'])
    # sulit
    s1, s2 = d[2 % len(d)], d[0]
    nama, Z, A = U[s1]
    n = A - Z
    tambah(gol, 'sulit', 3, f'Atom netral {notasi(s1)} memiliki jumlah proton, elektron, dan neutron berturut-turut…',
           f'{Z}, {Z}, dan {n}', [f'{Z}, {n}, dan {Z}', f'{A}, {Z}, dan {n}', f'{Z}, {Z}, dan {A}', f'{n}, {n}, dan {Z}'],
           f'p = e = Z = {Z}; n = A − Z = {A} − {Z} = {n}.', ['tp3-triplet', 'tp3-notasi'])
    nama, Z, A = U[s2]
    n = A - Z
    benar = notasi(s2)
    salah = [notasi(s2, A=Z, Z=A), notasi(s2, A=n, Z=Z), notasi(s2, A=A, Z=n), notasi(s2, A=A + Z, Z=Z)]
    tambah(gol, 'sulit', 3, f'Suatu atom {nama} memiliki {Z} proton, {Z} elektron, dan {n} neutron. Notasi atom yang tepat adalah…',
           benar, salah, f'Z = proton = {Z} ditulis di bawah; A = {Z} + {n} = {A} ditulis di atas: {benar}.', ['tp3-notasi', 'tp3-massa'])
    a, b = d[0], d[1 % len(d)]
    na, nb = U[a][2] - U[a][1], U[b][2] - U[b][1]
    selisih = abs(na - nb)
    tambah(gol, 'sulit', 3, f'Selisih jumlah neutron antara atom {notasi(a)} dan {notasi(b)} adalah…',
           str(selisih), angka_unik(selisih, [abs(U[a][2] - U[b][2]), abs(U[a][1] - U[b][1]), selisih + 2, selisih + 1, selisih - 1]),
           f'Neutron {a} = {U[a][2]} − {U[a][1]} = {na}; neutron {b} = {U[b][2]} − {U[b][1]} = {nb}; selisih = {selisih}.', ['tp3-neutron'])

# ══════════════════ TP4 — ion (dihitung) ══════════════════
def jenis_ion(q): return 'kation (ion positif)' if q > 0 else 'anion (ion negatif)'

for gol, daftar in ION.items():
    # mudah
    sim, q = daftar[0]
    k = abs(q)
    aksi_b = f'melepas {k} elektron' if q > 0 else f'menerima {k} elektron'
    aksi_s = f'menerima {k} elektron' if q > 0 else f'melepas {k} elektron'
    tambah(gol, 'mudah', 4, f'Ion {ion(sim, q)} terbentuk ketika atom {sim}…',
           aksi_b, [aksi_s, f'melepas {k} proton', f'menerima {k} proton'],
           f'Muatan {"positif" if q > 0 else "negatif"} berarti atom {"kekurangan" if q > 0 else "kelebihan"} {k} elektron; proton tidak berubah.', ['tp4-terbentuk', 'kation' if q > 0 else 'anion'])
    sim, q = daftar[1]
    tambah(gol, 'mudah', 4, f'Ion {ion(sim, q)} termasuk jenis…',
           jenis_ion(q), [jenis_ion(-q), 'atom netral', 'isotop'],
           f'Ion bermuatan {"positif disebut kation" if q > 0 else "negatif disebut anion"}.', ['kation' if q > 0 else 'anion'])
    # sedang
    sim, q = daftar[2 % len(daftar)]
    nama, Z, A = U[sim]
    e = Z - q
    tambah(gol, 'sedang', 4, f'Atom {sim} bernomor atom {Z}. Jumlah elektron pada ion {ion(sim, q)} adalah…',
           str(e), angka_unik(e, [Z, Z + q, A - Z, e + 1, e - 1]),
           f'Elektron ion = Z − muatan = {Z} − ({sg(q)}) = {e}.', ['tp4-elektron'] + (['tp4-elektron-anion'] if q < 0 else []))
    sim, q = daftar[3 % len(daftar)]
    nama, Z, A = U[sim]
    tambah(gol, 'sedang', 4, f'Jumlah proton pada ion {ion(sim, q)} (nomor atom {sim} = {Z}) adalah…',
           str(Z), angka_unik(Z, [Z - q, Z + q, A - Z, Z + 2 * q]),
           f'Pembentukan ion hanya mengubah jumlah elektron; proton tetap {Z}.', ['tp4-proton'] + (['tp4-transisi'] if gol == 'transisi' else []))
    # sulit
    sim, q = daftar[4 % len(daftar)]
    nama, Z, A = U[sim]
    n, e = A - Z, Z - q
    tambah(gol, 'sulit', 4, f'Ion {notasi_ion(sim, q)} memiliki jumlah proton, neutron, dan elektron berturut-turut…',
           f'{Z}, {n}, dan {e}', [f'{Z}, {n}, dan {Z}', f'{e}, {n}, dan {Z}', f'{Z}, {A}, dan {e}', f'{Z}, {e}, dan {n}'],
           f'p = Z = {Z}; n = A − Z = {n}; e = Z − muatan = {Z} − ({sg(q)}) = {e}.', ['tp4-elektron', 'tp3-neutron'])
    sim, q = daftar[0]
    nama, Z, A = U[sim]
    n, e = A - Z, Z - q
    tambah(gol, 'sulit', 4, f'Ion {nama} bermuatan {sg(q)} memiliki {e} elektron dan {n} neutron. Nomor massa ion tersebut adalah…',
           str(A), angka_unik(A, [e + n, Z, e + n + 2 * q, A + 1, n]),
           f'Proton = elektron + muatan = {e} + ({sg(q)}) = {Z}; A = p + n = {Z} + {n} = {A}.', ['tp4-elektron', 'nomor-massa'])

# gas mulia × TP4 (isoelektronik & kestabilan)
tambah('gasMulia', 'mudah', 4, 'Atom gas mulia seperti neon sangat sukar membentuk ion karena…',
       'susunan elektronnya sudah stabil', ['tidak memiliki elektron', 'tidak memiliki proton', 'intinya bermuatan negatif'],
       'Kulit terluar gas mulia sudah penuh (2 untuk He, 8 untuk lainnya) sehingga tidak cenderung melepas/menerima elektron.', ['tp4-gm-stabil'])
tambah('gasMulia', 'mudah', 4, 'Saat atom membentuk ion, partikel yang dilepas atau diterima adalah…',
       'elektron', ['proton', 'neutron', 'inti atom'], 'Ion terbentuk karena pelepasan/penerimaan elektron; inti (proton dan neutron) tidak berubah.', ['tp4-terbentuk', 'tp4-proton'])
ISO = [('Na', 1), ('Cl', -1), ('Mg', 2), ('Br', -1), ('Ca', 2), ('I', -1)]
for i, (sim, q) in enumerate(ISO):
    Z = U[sim][1]
    e = Z - q
    gm = GAS_MULIA_ELEKTRON[e]
    lain = [g for g in ['Ne', 'Ar', 'Kr', 'Xe', 'He'] if g != gm]
    if i < 3:
        tambah('gasMulia', 'sedang', 4, f'Ion {ion(sim, q)} (nomor atom {sim} = {Z}) memiliki jumlah elektron yang sama dengan atom gas mulia…',
               f'{U[gm][0]} ({gm})', [f'{U[g][0]} ({g})' for g in lain],
               f'Elektron {ion(sim, q)} = {Z} − ({sg(q)}) = {e}, sama dengan {gm} (Z = {e}).', ['tp4-isoelek', 'tp4-elektron'])
    else:
        salah_gm = lain[0] if lain[0] != 'He' else lain[1]
        tambah('gasMulia', 'sulit', 4, f'Pasangan berikut yang memiliki jumlah elektron sama adalah… (Z: {sim} = {Z}, {gm} = {e}, {salah_gm} = {U[salah_gm][1]})',
               f'{ion(sim, q)} dan {gm}', [f'{sim} dan {gm}', f'{ion(sim, q)} dan {sim}', f'{ion(sim, q)} dan {salah_gm}'],
               f'{ion(sim, q)} memiliki {Z} − ({sg(q)}) = {e} elektron, sama dengan atom {gm}.', ['tp4-isoelek'])

# ══════════════════ Fun Fact ══════════════════
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

def ids_untuk(kunci):
    out = [q['id'] for q in SOAL if q['_kunci'] & set(kunci)]
    assert out, kunci
    return out

# ── Validasi ──
GOLS = ['alkali', 'alkaliTanah', 'halogen', 'gasMulia', 'transisi']
for g in GOLS:
    for t in ['mudah', 'sedang', 'sulit']:
        for tp in [1, 2, 3, 4]:
            assert any(q['golonganTerkait'] == g and q['tingkatKesulitan'] == t and tp in q['tpTerkait'] for q in SOAL), (g, t, tp)
assert len({q['id'] for q in SOAL}) == len(SOAL)
for q in SOAL:
    assert len(set(q['pilihan'])) == 4, q

# ── Tulis TypeScript ──
def ts_str(s): return json.dumps(s, ensure_ascii=False)

baris = ["import type { SoalKuis } from './types';", '',
         '/**',
         f' * Bank soal kuis UNO-Chem Edisi Struktur Atom — {len(SOAL)} soal untuk 4 TP:',
         ' *   TP1 perkembangan model atom · TP2 partikel penyusun atom ·',
         ' *   TP3 jumlah p/n/e atom netral dari notasi ᴬ_Z X · TP4 ion (kation & anion).',
         ' * DIBANGKITKAN oleh scripts/gen-soal-atom.py — jangan diedit manual;',
         ' * ubah generatornya lalu jalankan ulang. Soal TP3/TP4 dihitung dari data unsur.',
         ' * Dipakai QuizModal: draw2 -> `mudah`, wild4 -> `sedang`/`sulit`.',
         ' */',
         'export const BANK_SOAL: SoalKuis[] = [']
for t in ['mudah', 'sedang', 'sulit']:
    baris.append(f'  // ─────────────── {t.upper()} ───────────────')
    for q in [x for x in SOAL if x['tingkatKesulitan'] == t]:
        baris += ['  {',
                  f"    id: '{q['id']}',",
                  f"    pertanyaan: {ts_str(q['pertanyaan'])},",
                  f"    pilihan: [{', '.join(ts_str(p) for p in q['pilihan'])}],",
                  f"    jawabanBenar: {q['jawabanBenar']},",
                  f"    golonganTerkait: '{q['golonganTerkait']}',",
                  f"    tingkatKesulitan: '{q['tingkatKesulitan']}',",
                  f"    tpTerkait: {json.dumps(q['tpTerkait'])},",
                  f"    pembahasan: {ts_str(q['pembahasan'])},",
                  '  },']
baris.append('];\n')
(ROOT / 'src/data/kuis.ts').write_text('\n'.join(baris), encoding='utf-8')

fb = ["import type { FunFact } from './types';", '',
      '/**',
      f' * Bank Fun Fact UNO-Chem Edisi Struktur Atom — {len(FUNFACT)} fakta tentang model atom,',
      ' * partikel penyusun atom, notasi ᴬ_Z X, dan ion. `bantuSoal` menautkan ke soal',
      ' * di src/data/kuis.ts yang terbantu bila fakta ini disimak.',
      ' * DIBANGKITKAN oleh scripts/gen-soal-atom.py — jangan diedit manual.',
      ' */',
      'export const SEMUA_FUNFACT: FunFact[] = [']
for fid, teks, gol, ikon, kunci in FUNFACT:
    fb += ['  {', f"    id: '{fid}',", f'    teks: {ts_str(teks)},', f"    golongan: '{gol}',", f"    ikon: '{ikon}',",
           f"    bantuSoal: [{', '.join(repr(i) for i in ids_untuk(kunci))}],", '  },']
fb.append('];\n')
(ROOT / 'src/data/funfact.ts').write_text('\n'.join(fb), encoding='utf-8')

from collections import Counter
print('soal:', len(SOAL), Counter(q['tingkatKesulitan'] for q in SOAL), Counter(q['tpTerkait'][0] for q in SOAL))
print('funfact:', len(FUNFACT))
