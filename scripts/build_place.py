"""Rakit rbxlx + rbxl untuk kelima place AKIOMIDA.

Pemakaian:
  python build_place.py            -> rakit & konversi semua 5 place
  python build_place.py Kampung    -> hanya satu place
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rbxlx_lib
from rbxlx_lib import Item, p_bool, p_string, script_item
import rbx_binary
import world_dataran
import world_luar

SRC = "/home/z/my-project/download/Dataran-Roblox/src"
OUT_DIR = "/home/z/my-project/download/Dataran-Roblox"

PLACE_IDS = {
    "Dataran": 77626159664192,
    "Kampung": 104140882721739,
    "Sabana": 114149183491762,
    "Stepa": 121892136503729,
    "Perladangan": 74900687715969,
}

NPCTEKS = {
    "Dataran": {},
    "Kampung": {
        "NPC_PakUmar": [
            "Selamat datang di Kampung, pemuda! Aku Pak Umar, kepala desa di sini.",
            "Kampung adalah kampung halaman kami: sawah, sumur, dan rumah panggung.",
            "Lewati gerbang besar di utara kalau ingin kembali ke Dataran.",
        ],
        "NPC_BuRatna": [
            "Halo nak, aku Bu Ratna! Sembako dari sawah kampung selalu cukup.",
            "Kalau lapang, main ke alun-alun; sumurnya airnya jernih.",
            "Micdamu banyak ya? Simpan baik-baik, di Kampung semua serba sederhana.",
        ],
        "NPC_Dedi": [
            "Aku Dedi, petani sawah di kampung ini.",
            "Padi kami tumbuh pelan tapi pasti, seperti cerita kawasan ini.",
            "Mau jalan-jalan? Gerbang utara langsung menuju Dataran.",
        ],
    },
    "Sabana": {
        "NPC_PanduSaka": [
            "Selamat datang di Sabana! Aku Saka, pemandu safari kawasan ini.",
            "Jaga jarak dengan batu besar; di baliknya kadang ada angin kencang.",
            "Gerbang di selatan mengembalikanmu ke Dataran kapan saja.",
        ],
        "NPC_BuLesa": [
            "Aku Bu Lesa, penjaga mata air Sabana.",
            "Air di sini berharga; semua hewan sabana datang ke tepian itu.",
            "Matahari sore di Sabana paling indah, lihat ke arah barat nanti.",
        ],
        "NPC_Rio": [
            "Namaku Rio, penjelajah muda!",
            "Stepa di timur katanya dingin dan berangin, aku belum berani kesana.",
            "Kalau ketemu kawanan hewan, jangan berlari; berjalan saja pelan.",
        ],
    },
    "Stepa": {
        "NPC_Jaro": [
            "Aku Jaro, penjaga menara Stepa.",
            "Dari atas menara bisa lihat kincir angin tua peninggalan pendiri kawasan.",
            "Gerbang timur membawamu pulang ke Dataran.",
        ],
        "NPC_Altai": [
            "Nama ku Altai. Udara Stepa sejuk sepanjang tahun.",
            "Bale jerami di ladang itu simpanan pakan ternak musim dingin.",
            "Cerita lama bilang dataran ini dulu lautan rumput, makanya kami jaga baik-baik.",
        ],
        "NPC_Marek": [
            "Aku Marek, tukang reparasi kincir.",
            "Baling kincir itu masih berputar; suaranya bagus saat senja.",
            "Nanti kalau ke Perladangan, sapa Pak Tani; dia sahabat lamaku.",
        ],
    },
    "Perladangan": {
        "NPC_PakTani": [
            "Selamat datang di Perladangan! Aku Pak Tani, mandor kebun di sini.",
            "Teh di teras itu dipetik tiap pagi; warnanya paling bagus sebelum siang.",
            "Gerbang barat di tepi kebun langsung menuju Dataran.",
        ],
        "NPC_BuLastri": [
            "Aku Bu Lastri, pengurus gudang lumbung.",
            "Hasil panen ditimbang di lumbung merah itu sebelum dikirim ke Kampung.",
            "Kanal irigasi selalu mengalir; jangan main air di tepinya ya.",
        ],
        "NPC_Mulyo": [
            "Namaku Mulyo, penyuluh pertanian.",
            "Perladangan ini hasil kerja keras tiga generasi keluarga akiomida.",
            "Cerita kawasan masih panjang; banyak gerbang menanti di Dataran.",
        ],
    },
}

PESAN_KAWASAN = {
    "Dataran": "Selamat datang di Dataran! Toko Benih di barat, kebun demonstrasi di timur, empat gerbang di utara, timur, selatan, dan barat.",
    "Kampung": "KAMPUNG AKIOMIDA - Desa pertama di dataran ini. Sawah di selatan, alun-alun dan sumur di tengah, gerbang ke Dataran di utara. Bicara dengan penduduk untuk mengenal cerita kawasan.",
    "Sabana": "SABANA AKIOMIDA - Padang emas dengan akasia dan mata air. Gerbang ke Dataran di selatan. Jelajahi sabana dan sapa para penjaga kawasan.",
    "Stepa": "STEPA AKIOMIDA - Dataran luas berangin dengan kincir tua dan menara jaga. Gerbang ke Dataran di timur.",
    "Perladangan": "PERLADANGAN AKIOMIDA - Kebun teh berteras, lumbung merah, dan kanal irigasi. Gerbang ke Dataran di barat.",
}


def read_source(name):
    with open(os.path.join(SRC, name), "r", encoding="utf-8") as f:
        return f.read()


def lua_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def lua_npc_table(nama_place):
    teks = NPCTEKS.get(nama_place, {})
    if not teks:
        return "{}"
    parts = []
    for npc, daftar in teks.items():
        baris = ", ".join(lua_str(t) for t in daftar)
        parts.append("%s = {%s}" % (npc, baris))
    return "{" + ", ".join(parts) + "}"


def siapkan_source(nama_place):
    hasil = {}
    for f in os.listdir(SRC):
        if f.endswith(".luau"):
            src = read_source(f)
            src = src.replace("@@TEMPAT@@", nama_place)
            src = src.replace("@@PESAN_KAWASAN@@", PESAN_KAWASAN[nama_place])
            src = src.replace("@@NPCTEKS@@", lua_npc_table(nama_place))
            hasil[f] = src
    return hasil


def rakit(nama_place):
    s = siapkan_source(nama_place)
    workspace = Item("Workspace", [p_string("Name", "Workspace"), p_bool("StreamingEnabled", True)])

    if nama_place == "Dataran":
        workspace = world_dataran.build_world()
        lighting = world_dataran.build_lighting()
    elif nama_place == "Kampung":
        workspace = world_luar.build_kampung()
        lighting = world_luar.lighting_kampung()
    elif nama_place == "Sabana":
        workspace = world_luar.build_sabana()
        lighting = world_luar.lighting_sabana()
    elif nama_place == "Stepa":
        workspace = world_luar.build_stepa()
        lighting = world_luar.lighting_stepa()
    elif nama_place == "Perladangan":
        workspace = world_luar.build_perladangan()
        lighting = world_luar.lighting_perladangan()
    else:
        raise ValueError("place tidak dikenal: %s" % nama_place)

    replicated = Item("ReplicatedStorage", [p_string("Name", "ReplicatedStorage")])
    replicated.add(script_item("ModuleScript", "GameConfig", s["GameConfig.luau"]))
    replicated.add(script_item("ModuleScript", "Remotes", s["Remotes.luau"]))

    sss = Item("ServerScriptService", [p_string("Name", "ServerScriptService")])
    sss.add(script_item("ModuleScript", "RateLimit", s["RateLimit.luau"]))
    sss.add(script_item("ModuleScript", "DataService", s["DataService.luau"]))
    sss.add(script_item("Script", "GerbangTeleport", s["GerbangTeleport.luau"]))
    if nama_place == "Dataran":
        sss.add(script_item("Script", "TokoBenihService", s["TokoBenihService.luau"]))
        sss.add(script_item("Script", "KebunDemoService", s["KebunDemoService.luau"]))
        sss.add(script_item("Script", "InteraksiDunia", s["InteraksiDunia.luau"]))
        client = script_item("LocalScript", "DataranClient", s["DataranClient.luau"])
    else:
        sss.add(script_item("Script", "InteraksiTempat", s["InteraksiTempat.luau"]))
        client = script_item("LocalScript", "TempatClient", s["TempatClient.luau"])

    starter_gui = Item("StarterGui", [p_string("Name", "StarterGui")])
    starter_gui.add(client)

    root = rbxlx_lib.Item("roblox", [])
    root.cls = None
    header = ('<?xml version="1.0" encoding="utf-8"?>\n'
              '<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" '
              'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
              'xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">\n')
    body = "\n".join([
        workspace.render(2),
        lighting.render(2),
        replicated.render(2),
        sss.render(2),
        starter_gui.render(2),
    ])
    xml_text = header + body + "\n</roblox>\n"

    for marker in ("@@TEMPAT@@", "@@PESAN_KAWASAN@@", "@@NPCTEKS@@"):
        if marker in xml_text:
            raise SystemExit("marker tersisa: %s di %s" % (marker, nama_place))
    if "TODO" in xml_text or "undefined" in xml_text:
        raise SystemExit("token terlarang ada di XML %s" % nama_place)

    xlx_path = os.path.join(OUT_DIR, "%s.rbxlx" % nama_place)
    with open(xlx_path, "w", encoding="utf-8") as f:
        f.write(xml_text)

    rbx_path = os.path.join(OUT_DIR, "%s.rbxl" % nama_place)
    data, tops = rbx_binary.convert(xlx_path, rbx_path)

    # roundtrip + cek penting
    order, insts, parents = rbx_binary.read_rbxl(data)
    assert len(insts) == len(rbx_binary.flatten(tops)), "roundtrip beda jumlah instance %s" % nama_place
    gerbang_ok = any(i["cls"] == "Model" and i["props"].get("Name") == b"GerbangDataran"
                     for i in insts.values()) if nama_place != "Dataran" else True
    npc_ok = sum(1 for i in insts.values() if i["props"].get("Name", b"").startswith(b"NPC_"))
    print("[%s] rbxlx=%d B | rbxl=%d B | instance=%d | NPC=%d | gerbangDataran=%s"
          % (nama_place, os.path.getsize(xlx_path), len(data), len(insts), npc_ok, gerbang_ok))
    return xlx_path, rbx_path


if __name__ == "__main__":
    daftar = sys.argv[1:] or list(PLACE_IDS)
    for nama in daftar:
        rakit(nama)
