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
2. Tekan **Play**. Pemain muncul di Spawn padang tengah (dekat alun-alun).
3. Dekati **Toko Benih** (barat alun-alun) ▸ proksimasi prompt **Buka Toko** pada kasir ▸ UI toko terbuka (30 benih, tab Toko/Tas, filter kategori).
4. Beli benih (1 koin), lalu ke **Kebun Demonstrasi** (timur) ▸ prompt **Tanam** pada petak semai ▸ 1 detik tumbuh ▸ prompt **Panen**.
5. Data Koin + Tas tersimpan di DataStore `DataranData_v1` (aktif saat publish dengan Studio Access to API Services; di Studio tanpa akses API game tetap jalan dengan data sesi).

## Sistem yang diimplementasikan

- **Katalog 30 benih** persis GDD (Gandum s.d. Zaitun), kategori Serealia / Legum / Sayuran / Buah-buahan / Tanaman Lainnya, semua **harga 1 koin** dan **waktu tumbuh 1 detik**.
- **Menu pembelian** sesuai GDD: ikon warna benih, nama, harga, waktu tumbuh, jumlah koin, tombol BELI BENIH. UI ramah HP (layout scale, safe area, tidak menabrak tombol menu Roblox).
- **Toko hanya menjual benih** — tidak ada block / material bangunan yang dijual.
- **Koin awal 50** (pilihan sendiri, GDD tidak menentukan), disimpan DataStore agar terbawa.
- **Tas**: 50 slot, maksimal 250 per slot (mengikuti aturan seri). Tas penuh → pembelian/panen ditolak dan pemain diberi tahu.
- **Kebun demonstrasi**: 30 bed contoh tanaman per kategori + 6 petak semai berfungsi (tanam → tumbuh 1 detik → panen 1–3 hasil).
- **Dunia**: Padang Spawn, Alun-alun (air mancur, 8 bangku, 4 lampu, papan informasi, 4 penunjuk arah), Permukiman (6 rumah + gudang + pagar), Toko Benih resep 40×30 (pondasi batu, dinding krem, tiang kayu gelap, atap pelana 30° merah bata, kanopi, papan nama, kasir, 4 rak, meja etalase, 3 lampu gantung), Perbukitan + alam (8 bukit, 48 pohon, semak, 60 bunga, batu, kolam + jembatan kayu), dekorasi (kincir angin berputar, gerobak, sumur), **4 gerbang** dengan identitas visual berbeda (Barat Kampung: pagar kayu; Utara Sabana: pasir; Timur Stepa: batu/rumput jarang; Selatan Perladangan: bale jerami + tanah garu).
- **3 NPC** (Bu Sari penjual, Pak Darsa, Mira) dengan bubble percakapan.
- **Pencahayaan**: siang hangat (ClockTime 14.5), ShadowMap, atmosfer, bayangan pohon, lampu neon + PointLight.

## Aturan yang diterapkan (dari post "Tugasmu")

- Kode **tanpa komentar**, tanpa nama/unsur game lain.
- Semua logika uang, tas, pembelian, tanam, panen ada di **ServerScriptService**; client hanya menampilkan dan mengirim permintaan.
- Semua RemoteEvent divalidasi server: **jarak**, **saldo/isi tas**, **kepemilikan petak**, dan **batas permintaan per detik** (5/detik, data 3/detik).
- Tidak ada `require` ID angka, `loadstring`, `getfenv`, `HttpService`; tidak ada model/script dari luar — semua objek dibuat dari Part.
- Data penting tidak disimpan di ReplicatedStorage (hanya server + DataStore).
- Skala wajib: dinding 20 stud, tebal 1 stud, bukaan pintu kosong 6×10, jendela dasar 3, ukuran kelipatan 2, posisi grid 4.
- Anti-lag: Part sederhana, tanpa script per plot, visual tanaman hanya saat ditanam, waktu tumbuh via `task.delay` (tanpa loop per plot), **StreamingEnabled**.

## Keputusan & catatan pengembang

- **Mata uang "Koin"** dipakai sesuai GDD Dataran (post "Tugasmu" memakai "Micda" untuk place lahan; keduanya sengaja terpisah, bisa disatukan nanti).
- **Gerbang belum teleport**: menuju Kampung/Sabana/Stepa/Perladangan butuh Place ID tujuan (TeleportService). Papan "SEGERA DIBUKA" + penghalang dipasang; tinggal isi ID place saat place lain jadi.
- Fitur tanam-panen di petak semai adalah **tambahan minimal di luar GDD** agar benih yang dibeli punya fungsi di Place 01; hapus `KebunDemoService` jika tidak diinginkan.
- NPC statis dengan dialog; NPC berjalan + efek angin rumput ditunda ke Tahap 4 (butuh rig/animasi aset sendiri).
- Katalog benih, warna ikon, dan data zona ada di `ReplicatedStorage.GameConfig` — ubah di satu tempat.

## Struktur kode

```
ReplicatedStorage
├── GameConfig      (ModuleScript)  30 benih, kategori, aturan tas/koin
└── Remotes         (ModuleScript)  PermintaanToko, AksiKebun, InfoDataran, AmbilData
ServerScriptService
├── RateLimit       (ModuleScript)  batas permintaan per detik
├── DataService     (ModuleScript)  Koin + Tas, DataStore, autosave, BindToClose
├── TokoBenihService (Script)       pembelian benih (validasi penuh)
├── KebunDemoService (Script)       petak semai: tanam/tumbuh/panen
└── InteraksiDunia  (Script)        prompt toko, NPC, gerbang, papan informasi
StarterGui
└── DataranClient   (LocalScript)   UI toko 30 benih, tas, picker benih, banner, bubble NPC
Workspace
└── Lanskap, AlunAlun, ZonaToko, KebunDemo, Permukiman, Alam, Dekorasi, Gerbang, NPC, SpawnDataran
```
