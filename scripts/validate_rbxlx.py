import re
import sys
import xml.etree.ElementTree as ET

SRC = "/home/z/my-project/download/Dataran-Roblox/src"
RBXLX = "/home/z/my-project/download/Dataran-Roblox/Dataran.rbxlx"

galat = []

tree = ET.parse(RBXLX)
root = tree.getroot()
print("XML well-formed: OK, root =", root.tag, "version =", root.get("version"))

semua_sumber = {}
for script in root.iter("ProtectedString"):
    if script.get("name") == "Source":
        semua_sumber[script.text or ""] = True

import os
for nama in sorted(os.listdir(SRC)):
    with open(os.path.join(SRC, nama), encoding="utf-8") as f:
        isi = f.read()
    if semua_sumber.get(isi):
        print(f"embed identik: {nama} ({len(isi)} chars)")
    else:
        galat.append(f"embed TIDAK ditemukan/berbeda: {nama}")

teks_file = open(RBXLX, encoding="utf-8").read()

wajib_ada = [
    "MicdaAwal = 999990000000000",
    "MicdaMaks = 1000000000000000",
    "HadiahBicaraMaks = 999",
    'MataUang = "Micda"',
    "function GameConfig.FormatMicda",
    "function GameConfig.FormatAngkaPenuh",
    "function DataService.HadiahBicara",
    "function DataService.UbahMicda",
    'Name = "MicdaHud"',
    "GetTopbarInsets",
]
for teks in wajib_ada:
    if teks in teks_file:
        print(f"ada: {teks!r}")
    else:
        galat.append(f"HILANG: {teks!r}")

dilarang = ["KoinAwal", "Koin tidak cukup", "UbahKoin", '"Koin"', "1 koin", "Belanda"]
for teks in dilarang:
    if teks in teks_file:
        galat.append(f"MASIH ADA (dilarang): {teks!r}")

jumlah_part = sum(1 for _ in root.iter("Item") if _.get("class") == "Part")
jumlah_spawn = sum(1 for _ in root.iter("Item") if _.get("class") == "SpawnLocation")
print(f"Part: {jumlah_part}, SpawnLocation: {jumlah_spawn}")
if jumlah_spawn != 1:
    galat.append("SpawnLocation harus tepat 1")

if galat:
    print("\nGAGAL:")
    for g in galat:
        print(" -", g)
    sys.exit(1)
print("\nVALIDASI RBXLX: SEMUA LOLOS")
