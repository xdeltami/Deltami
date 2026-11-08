# Place 01 — DATARAN (Roblox)

Implementasi awal GDD **Place 01 — Dataran** (tugas blog "Tugas Places Dataran", 7 November 2026) sebagai game Roblox yang bisa langsung dibuka di Roblox Studio, disertai kode sumber lengkap. Aturan pemrograman mengikuti post **"Tugasmu" (5 November 2026)**.

## Isi repo

| File | Isi |
| --- | --- |
| `Dataran.rbxlx` | File place siap buka di Roblox Studio (File ▸ Open from File). Dunia sudah terbangun + semua script terpasang. |
| `src/*.luau` | Kode sumber semua script (identik dengan yang ter-embed di rbxlx, untuk dibaca/diff di GitHub). |
| `GDD_Place_01_Dataran.md` | Salinan penuh GDD acuan. |
| `README.md` | Dokumen ini. |

## Cara pakai

1. Buka Roblox Studio ▸ **File ▸ Open from File** ▸ pilih `Dataran.rbxlx`.
2. Tekan **Play**. Pemain muncul di Spawn padang tengah (dekat alun-alun); HUD Micda langsung tampil **di kiri atas, tepat di bawah tombol menu Roblox**, saldo sudah terisi `999,99 T` sejak masuk (bukan 0).
3. Dekati **Toko Benih** (barat alun-alun) ▸ proksimasi prompt **Buka Toko** pada kasir ▸ UI toko terbuka (30 benih, tab Toko/Tas, filter kategori).
4. Beli benih (1 Micda), lalu ke **Kebun Demonstrasi** (timur) ▸ prompt **Tanam** pada petak semai ▸ 1 detik tumbuh ▸ prompt **Panen**.
5. Data Micda + Tas tersimpan di DataStore `DataranData_v1` (aktif saat publish dengan Studio Access to API Services; di Studio tanpa akses API game tetap jalan dengan data sesi).

## Sistem yang diimplementasikan

- **Katalog 30 benih** persis GDD (Gandum s.d. Zaitun), kategori Serealia / Legum / Sayuran / Buah-buahan / Tanaman Lainnya, semua **harga 1 Micda** dan **waktu tumbuh 1 detik**.
- **Menu pembelian** sesuai GDD: ikon warna benih, nama, harga, waktu tumbuh, jumlah Micda, tombol BELI BENIH. UI ramah HP (layout scale, safe area, tidak menabrak tombol menu Roblox).
- **HUD Micda**: ikon koin emas bulat (huruf M) + jumlah format Indonesia pendek (`999,99 T`), tampil **di kiri atas, tepat di bawah tombol menu (FAB) Roblox** mengikuti `GuiService:GetTopbarInsets()` sehingga tidak menutupi apa pun; klik pil untuk melihat angka penuh (`999.990.000.000.000 Micda`).
- **Toko hanya menjual benih** — tidak ada block / material bangunan yang dijual.
- **Ekonomi Micda (arahan pemilik 7 Nov 2026)**: mata uang **Micda** berbentuk koin emas bulat. User baru **langsung terisi 999,99 Triliun Micda saat data dibuat** (`GameConfig.MicdaAwal`, bukan lewat jalur reward apa pun), **kapasitas maksimal 1000 Triliun** (`GameConfig.MicdaMaks`) di-clamp server di `UbahMicda` dan saat muat data.
- **Aturan reward**: bicara NPC **tidak memberi reward**. Jika kelak ada reward percakapan, jumlahnya wajib **di bawah 1000 Micda** — ditegakkan server oleh `DataService.HadiahBicara` (otomatis dipotong ke `GameConfig.HadiahBicaraMaks = 999`).
- **Tas**: 50 slot, maksimal 250 per slot (mengikuti aturan seri). Tas penuh → pembelian/panen ditolak dan pemain diberi tahu.
- **Kebun demonstrasi**: 30 bed contoh tanaman per kategori + 6 petak semai berfungsi (tanam → tumbuh 1 detik → panen 1–3 hasil).
- **Dunia (revisi 2 — 8 Nov 2026, GDD Bagian 8 + 9: masterplan)**: dibangun dengan **masterplan arsitektural + sistem okupansi** — setiap objek wajib lolos pemeriksaan tabrakan (lingkaran, kotak bangunan, segmen jalan, alur sungai), yang tidak lolos dilewati, sehingga **tidak ada objek tumpang tindih dan tidak ada papan tertutup**. Tanah, bukit, sungai berbasi batu, dan **tebing batu penutup tepi peta** = **Terrain asli Roblox** via script `TerrainDunia`. Komposisi: alun-alun cobble (air mancur + cincin bunga, 8 bangku, 4 lampu, papan informasi 16×7 berbingkai beratap dengan zona baca kosong), **totem penunjuk 4 arah di pelataran kedatangan** (pengganti papan kecil acak), Toko Benih + pelataran + bed bunga + etalase, **Dusun 6 rumah dua lantai** (plinth batu, jendela kaca+ambang, lis dinding, pilaster, cerobong, taman depan berpagar) menghadap jalan desa + gudang + sumur, Kebun Demonstrasi bergerbang kayu beratap, jalan berhierarki (**boulevard 24 = inti 16 + trotoar 4×2; sekunder 14; lokal 6–8**) dengan **allee pohon rapi di kedua sisi boulevard**, **sungai + promenade tepian (3 segmen + 5 pad, bangku menghadap sungai) + jembatan kayu boulevard selatan + dermaga**, gerombolan pohon di bukit, kincir angin di puncak bukit, 4 gerbang batu seragam.
- **Tempat luar = hamparan kosong (arahan pemilik 8 Nov 2026)**: Kampung/Sabana/Stepa/Perladangan **individual belum dijelaskan**, jadi isinya hanya spawn + satu gerbang kembali ke Dataran (jalur penghubung) + terrain lembut + tebing + kabut. Tanpa NPC/bangunan/papan — detail kawasan menunggu penjelasan pemilik dunia.
- **3 NPC di Dataran** (Bu Sari penjual, Pak Darsa, Mira) dengan bubble percakapan.
- **Pencahayaan**: siang tenang (ClockTime 14.5), ShadowMap, **Atmosphere tebal per place (Density 0,42–0,52 + Haze 2,0–2,6)** menutup tepi peta bersama tebing batu, lampu hangat + PointLight.

## Aturan yang diterapkan (dari post "Tugasmu")

- Kode **tanpa komentar**, tanpa nama/unsur game lain.
- Semua logika uang, tas, pembelian, tanam, panen ada di **ServerScriptService**; client hanya menampilkan dan mengirim permintaan.
- Semua RemoteEvent divalidasi server: **jarak**, **saldo/isi tas**, **kepemilikan petak**, dan **batas permintaan per detik** (5/detik, data 3/detik).
- Tidak ada `require` ID angka, `loadstring`, `getfenv`, `HttpService`; tidak ada model/script dari luar — semua objek dibuat dari Part.
- Data penting tidak disimpan di ReplicatedStorage (hanya server + DataStore).
- Skala wajib: dinding 20 stud, tebal 1 stud, bukaan pintu kosong 6×10, jendela dasar 3, ukuran kelipatan 2, posisi grid 4.
- Anti-lag: Part sederhana, tanpa script per plot, visual tanaman hanya saat ditanam, waktu tumbuh via `task.delay` (tanpa loop per plot), **StreamingEnabled**.

## Keputusan & catatan pengembang

- **Mata uang "Micda"** dipakai untuk seluruh game (katalog GDD menulis "1 koin" — 1 koin = 1 Micda). Nilai awal/kapasitas/reward mengikuti arahan pemilik 7 November 2026, yang berlaku di atas GDD.
- **Format angka Indonesia** di seluruh UI via `GameConfig.FormatMicda` (pendek: `999,99 T`, `2,50 Jt`) dan `GameConfig.FormatAngkaPenuh` (`999.990.000.000.000`); keduanya teruji 111 assertion (lihat `scripts/test_gameconfig.luau`).
- **Gerbang aktif teleport**: papan gerbang punya prompt **Masuk Gerbang** (TeleportService ke place Kampung/Sabana/Stepa/Perladangan; di tempat luar gerbangnya kembali ke Dataran). Papan dipasang di y 12,5 dan jarak prompt dinaikkan (16–18 stud) agar mudah dijangkau di HP.
- Fitur tanam-panen di petak semai adalah **tambahan minimal di luar GDD** agar benih yang dibeli punya fungsi di Place 01; hapus `KebunDemoService` jika tidak diinginkan.
- NPC statis dengan dialog; NPC berjalan + efek angin rumput ditunda ke Tahap 4 (butuh rig/animasi aset sendiri).
- Katalog benih, warna ikon, dan data zona ada di `ReplicatedStorage.GameConfig` — ubah di satu tempat.

## Struktur kode

```
ReplicatedStorage
├── GameConfig      (ModuleScript)  30 benih, kategori, aturan Micda/tas, format angka
└── Remotes         (ModuleScript)  PermintaanToko, AksiKebun, InfoDataran, AmbilData
ServerScriptService
├── RateLimit       (ModuleScript)  batas permintaan per detik
├── DataService     (ModuleScript)  Micda (awal langsung 999,99 T, maks 1000 T, guard reward NPC) + Tas, DataStore, autosave, BindToClose
├── TerrainDunia    (Script)        terrain asli per place: dasar, bukit/dune, sungai (Dataran), tebing tepi peta
├── TokoBenihService (Script)       pembelian benih (validasi penuh)
├── KebunDemoService (Script)       petak semai: tanam/tumbuh/panen
└── InteraksiDunia  (Script)        prompt toko, NPC, gerbang, papan informasi
StarterGui
└── DataranClient   (LocalScript)   HUD Micda (koin emas, kiri atas di bawah menu Roblox) + UI toko 30 benih, tas, picker benih, banner, bubble NPC
Workspace
└── Lanskap (jalan berhierarki + jembatan), AlunAlun, ZonaToko, KebunDemo, Permukiman, Alam (sungai/dermaga/pohon), Dekorasi, Gerbang, NPC, SpawnDataran
```
