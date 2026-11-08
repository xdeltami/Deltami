# GAME DESIGN DOCUMENT (GDD) — PLACE 01: DATARAN

Sumber: https://yuyanaka.blogspot.com/2026/11/tugas-places-dataran.html (7 Nov 2026)
Salinan resmi proyek Dunia Akiomida. Acuan wajib pembangunan Dataran.

## 1. IDENTITAS DAN KONSEP DATARAN

Dataran merupakan Place utama sekaligus titik awal pemain memasuki dunia
permainan. Kawasan ini memiliki lanskap alami berupa padang rumput luas,
perbukitan rendah, pepohonan, dan permukiman kecil.

Fungsi utama Dataran:
- Tempat pertama pemain muncul (spawn).
- Pusat aktivitas dan interaksi pemain.
- Lokasi toko benih utama.
- Kawasan pengenalan sumber daya pertanian.
- Penghubung menuju empat kawasan lain: Kampung, Sabana, Stepa, Perladangan.

Identitas visual: alam terbuka, pedesaan, subur, hangat, dan penuh kehidupan.

## 2. TATA LETAK DAN PEMBAGIAN ZONA

A. Padang Spawn — titik awal pemain; padang rumput terbuka di bagian tengah;
   bunga liar, pepohonan, jalur setapak.
B. Alun-alun Dataran — pusat aktivitas dan orientasi; air mancur, bangku,
   lampu, papan informasi, penunjuk arah; titik temu jalur.
C. Kawasan Permukiman — rumah-rumah kecil bergaya pedesaan; pagar, halaman,
   jalan setapak, dekorasi; NPC penduduk.
D. Toko Benih — hanya menjual benih; TIDAK menjual block maupun material
   bangunan.
E. Kebun Demonstrasi — contoh berbagai jenis tanaman agar pemain mengenali
   bentuknya sebelum membeli benih.
F. Perbukitan dan Area Alam — bukit rendah, bebatuan, pepohonan, semak,
   pemandangan terbuka.
G. Empat Jalur dan Gerbang Keluar:
   - Barat: Kampung.
   - Utara: Sabana.
   - Timur: Stepa.
   - Selatan: Perladangan.

Skema arah kawasan:

```
        UTARA
       SABANA
         |
BARAT -- ALUN-ALUN (DATARAN) -- TIMUR
KAMPUNG                        STEPA
         |
      PERLADANGAN
       SELATAN
```

Pemain dapat menjelajahi Dataran terlebih dahulu sebelum menemukan dan
menggunakan gerbang-gerbang tersebut.

Data place kawasan (dari pemilik):
- Dataran (Spawn Utama): place 77626159664192
- Kampung: place 104140882721739
- Sabana: place 114149183491762
- Stepa: place 121892136503729
- Perladangan: place 74900687715969

Arahan pemilik: fokus garap Dataran; bila place lain menjadi tempat gerbang,
cukup buatkan gerbang untuk kembali ke place yang digarap.

## 3. TOKO BENIH DATARAN

Ketentuan toko:
- Hanya menjual benih; tidak menjual block; tidak menjual material bangunan.
- Setiap benih harga 1 koin; waktu tumbuh 1 detik.

Katalog 30 benih (harga 1 koin, tumbuh 1 detik semua):

| No | Benih | No | Benih |
|----|-------|----|-------|
| 1 | Gandum | 16 | Selada |
| 2 | Jelai | 17 | Brokoli |
| 3 | Oat | 18 | Kembang kol |
| 4 | Rye | 19 | Kubis |
| 5 | Sorgum | 20 | Paprika |
| 6 | Jewawut | 21 | Mentimun |
| 7 | Buckwheat | 22 | Apel |
| 8 | Kacang polong | 23 | Pir |
| 9 | Kacang lentil | 24 | Anggur (buah saja) |
| 10 | Kacang arab | 25 | Plum |
| 11 | Kacang hitam | 26 | Aprikot |
| 12 | Kacang merah | 27 | Persik |
| 13 | Bit | 28 | Nektarin |
| 14 | Asparagus | 29 | Ceri |
| 15 | Seledri | 30 | Zaitun |

Kategori tampilan katalog:
1. Serealia — Gandum, Jelai, Oat, Rye, Sorgum, Jewawut, Buckwheat.
2. Legum — Kacang polong, Kacang lentil, Kacang arab, Kacang hitam, Kacang merah.
3. Sayuran — Bit, Asparagus, Seledri, Selada, Brokoli, Kembang kol, Kubis, Paprika, Mentimun.
4. Buah-buahan — Apel, Pir, Anggur (buah saja), Plum, Aprikot, Persik, Nektarin, Ceri.
5. Tanaman lainnya — Zaitun.

Menu pembelian menampilkan: ikon/gambar benih, nama, harga, waktu tumbuh,
jumlah koin pemain, tombol beli.

## 4. ARAHAN DESAIN VISUAL

A. Vegetasi: rumput bervariasi warna/tinggi, bunga liar, semak, pohon
   beragam bentuk.
B. Lanskap: perbukitan rendah, bebatuan alami, sungai kecil/kolam, jembatan
   kayu di jalur yang melintasi air.
C. Arsitektur: rumah pedesaan, toko benih mudah dikenali, gudang pendukung,
   pagar kayu, jalan setapak.
D. Dekorasi: kincir angin di perbukitan, gerobak, sumur, bangku taman,
   lampu jalan, papan petunjuk arah.
E. Pencahayaan dan atmosfer: cahaya alami nyaman, bayangan pohon, lampu
   lingkungan malam, efek angin pada rumput/dedaunan, animasi air.
F. Aktivitas lingkungan: NPC penduduk berjalan/beraktivitas, NPC penjaga
   atau penjual di sekitar toko, animasi lingkungan sederhana.

## 5. NAVIGASI DAN PETUNJUK PEMAIN

Tiap jalur keluar punya penanda jelas dan identitas visual berbeda:
- Gerbang Barat (Kampung): nuansa pedesaan.
- Gerbang Utara (Sabana): vegetasi dan warna lebih kering.
- Gerbang Timur (Stepa): lanskap terbuka, vegetasi jarang.
- Gerbang Selatan (Perladangan): dekorasi pertanian.
Papan penunjuk arah di persimpangan utama; nama kawasan terbaca dari
jarak wajar.

## 6. PRIORITAS PEMBANGUNAN

- Tahap 1 — Struktur dasar: terrain, titik spawn, alun-alun, 4 jalur + gerbang.
- Tahap 2 — Fasilitas utama: bangunan Toko Benih, antarmuka toko, katalog
  30 benih, harga 1 koin, tumbuh 1 detik.
- Tahap 3 — Lingkungan: permukiman, kebun demonstrasi, pohon, bukit, sungai,
  dekorasi.
- Tahap 4 — Kehidupan kawasan: NPC, animasi lingkungan, pencahayaan,
  pengujian navigasi dan kenyamanan.

## 7. IDENTITAS AKHIR & PRINSIP

Dataran adalah pusat pengenalan dunia: tempat mulai, mengenal lingkungan,
membeli benih, dan menemukan akses kawasan lain. Harus mudah dikenali,
hidup, dan tata letaknya jelas; tetap berguna walau kawasan lain terbuka.

Prinsip yang harus dipertahankan:
- Dataran adalah Place utama; spawn di padang terbuka tengah.
- Alun-alun pusat aktivitas.
- Barat Kampung, Utara Sabana, Timur Stepa, Selatan Perladangan.
- Toko Dataran hanya menjual 30 benih tercantum; semua 1 koin; tumbuh 1 detik.
- Toko tidak menjual block.
