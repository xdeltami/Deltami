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
import terrain_gen
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
    "Kampung": {},
    "Sabana": {},
    "Stepa": {},
    "Perladangan": {},
}

PESAN_KAWASAN = {
    "Dataran": "Selamat datang di Dataran! Toko Benih di barat, kebun demonstrasi di timur, empat gerbang di utara, timur, selatan, dan barat. Kawasan baru: Pasar Dusun dan Kebun Buah di timur, Taman Mandala di barat laut, Danau Tenang di barat daya, Panggung Dataran di tenggara.",
    "Kampung": "KAMPUNG AKIOMIDA - hamparan awal kawasan; detailnya belum ditentukan. Gerbang di utara kembali ke Dataran.",
    "Sabana": "SABANA AKIOMIDA - hamparan awal kawasan; detailnya belum ditentukan. Gerbang di utara kembali ke Dataran.",
    "Stepa": "STEPA AKIOMIDA - hamparan awal kawasan; detailnya belum ditentukan. Gerbang di utara kembali ke Dataran.",
    "Perladangan": "PERLADANGAN AKIOMIDA - hamparan awal kawasan; detailnya belum ditentukan. Gerbang di utara kembali ke Dataran.",
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
    sss.add(script_item("Script", "TerrainDunia", terrain_gen.luau_source(nama_place)))
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
