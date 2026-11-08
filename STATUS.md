# STATUS — Akiomida (Pemulihan & Backup)

> Diperbarui: 8 Nov 2026. Dokumen ini ada supaya **hasil kerja tidak pernah hilang lagi**:
> semua kode, dunia, dan dokumen ada di (a) folder lokal `download/Dataran-Roblox/`,
> (b) repo GitHub **xdeltami/Deltami**, dan (c) generator di `scripts-generasi/`.

## 1. Peta Aset

| Aset | Lokasi lokal | Lokasi GitHub |
| --- | --- | --- |
| 5 file place siap upload (`Dataran/Kampung/Sabana/Stepa/Perladangan` `.rbxl` + `.rbxlx`) | `download/Dataran-Roblox/` | repo `xdeltami/Deltami` |
| Generator dunia (Python: `rbxlx_lib`, `terrain_gen`, `world_dataran`, `world_luar`, `build_place`, `validate_rbxlx`) | `~/my-project/scripts/` + `download/Dataran-Roblox/scripts-generasi/` | repo `xdeltami/Deltami` → `scripts-generasi/` |
| Script Luau game (GameConfig, DataService, KebunDemoService, TokoBenihService, Remotes, RateLimit, InteraksiDunia, InteraksiTempat, TempatClient, DataranClient, GerbangTeleport) | `src/*.luau` | repo `xdeltami/Deltami` → `src/` |
| GDD + Masterplan (Bagian 1–9) | `GDD_Place_01_Dataran.md` | repo `xdeltami/Deltami` |
| README | `README.md` | repo `xdeltami/Deltami` |

## 2. Data Places (resmi dari pemilik dunia)

- Universe ID: **10774464946**
- Dataran (spawn utama): **77626159664192**
- Kampung: **104140882721739**
- Sabana: **114149183491762**
- Stepa: **121892136503729**
- Perladangan: **74900687715969**

## 3. Cara Membangun Ulang Dunia (tanpa internet)

```bash
python3 download/Dataran-Roblox/scripts-generasi/build_place.py
python3 download/Dataran-Roblox/scripts-generasi/validate_rbxlx.py
```

Hasil: 5 file `.rbxlx` + `.rbxl` (biner) diperbarui di `download/Dataran-Roblox/`.
Kondisi terakhir Dataran: **1.073 part** (target ≤1.100), 3 NPC, masterplan GDD Bagian 9 + 10 (Padang Civic).

## 4. Cara Publish ke Roblox

```bash
bash download/Dataran-Roblox/scripts-generasi/publish_roblox.sh
```

**PENTING — kunci API Roblox pemilik dunia hanya berlaku 1 JAM sejak dibuat**
(terbukti: kunci 8 Nov 2026 dibuat 07:23 UTC, kedaluwarsa 08:23 UTC; saat dicoba
07:55 UTC sudah ditolak `Invalid Grant`). Jadi: **buat kunci baru → segera jalankan
script di atas**. Kunci disimpan lokal di `~/my-project/.secrets/akiomida.env`
(di luar git, chmod 600). Kunci format: `baseApiKey(48 kar)+JWT` = ±736 karakter.

## 5. Riwayat Publish

- Dataran v68 + 4 kawasan luar v3 — 8 Nov 2026 (revisi "layak MMORPG", sebelum masterplan).
- Revisi **masterplan v2 arsitektural** (okupansi anti-tumpang tindih, bangunan
  berarsitektur, totem penunjuk, promenade sungai) — dibangun & tervalidasi.
- Revisi **masterplan v3 Padang Civic** (8 Nov 2026): padang persegi berkolonade,
  sumbu cobble, Menara Dataran, Paviliun Cahaya berusuk, rerouting 4 jalan diagonal
  dari tepi padang, perbaikan bug orientasi ukuran part (jalan/lantai), trim tumbuhan
  — part 1.073, 3 NPC, token bersih. **MENUNGGU kunci segar untuk publish**;
  kunci lama: console Active tetapi JWT dalam salinan kedaluwarsa (8 varian kunci
  diuji; body publish sudah benar octet-stream polos).
- Backup GitHub: commit `af240c3` (deliverable) + `0cf65bc` (generator) dan seterusnya.

## 6. Kredensial yang Diperlukan

| Kredensial | Dipakai untuk | Status |
| --- | --- | --- |
`ROBLOX_SECURITY` (kunci Open Cloud, umur 1 jam) | publish 5 place | **perlu kunci baru** |
| `GITHUB_TOKEN` (fine-grained PAT, user `xdeltami`) | push backup | **valid** |

Kredensial TIDAK PERNAH di-commit — `.gitignore` sudah menutup `.secrets/`.
