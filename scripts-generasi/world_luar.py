"""Pembangun dunia untuk 4 kawasan luar: Kampung, Sabana, Stepa, Perladangan.

Aturan pemilik dunia (8 Nov 2026): kawasan ini individual belum dijelaskan, jadi
hanya berupa HAMPARAN KOSONG + satu gerbang kembali ke Dataran sebagai jalur
penghubung. Tanpa NPC, tanpa bangunan, tanpa papan, tanpa isi lain. Tanah, bukit
lembut, dan tebing tepi peta dibangun runtime oleh script TerrainDunia.

Pemakaian: build_<nama>() -> Item Workspace; lighting_<nama>() -> Item Lighting.
Prompt teleport ditambahkan runtime oleh GerbangTeleport (menempel di PapanGerbang).
"""
from rbxlx_lib import (Item, add_text_surface, folder, model, p_bool, p_color3,
                       p_float, p_string, p_token, part)
from world_dataran import FACE, PAL, M, spawn_location


def gerbang_dataran(nama):
    """Gerbang batu-kayu seragam, papan di y 12.5 agar prompt mudah dijangkau."""
    g = model(nama)
    gx, gz = 0, -64
    for s in (-1, 1):
        g.add(part("PilarGerbang", (gx + s * 6.5, 10, gz), (3, 20, 3), PAL["batu"], M["slate"]))
    g.add(part("BalokGerbang", (gx, 21.2, gz), (17, 2.4, 3), PAL["batu_gelap"], M["slate"]))
    sign = part("PapanGerbang", (gx, 12.5, gz), (12, 4, 0.6), PAL["papan"], M["planks"])
    add_text_surface(sign, FACE["front"], "GERBANG DATARAN", PAL["teks_papan"])
    add_text_surface(sign, FACE["back"], "GERBANG DATARAN", PAL["teks_papan"])
    g.add(sign)
    g.add(part("PenghalangGerbang", (gx, 13, gz), (22, 26, 2), (255, 255, 255), M["smooth"], "block", 1, True))
    folder_gerbang = folder("Gerbang")
    folder_gerbang.add(g)
    return folder_gerbang


def workspace_kosong(nama_spawn):
    ws = Item("Workspace", [p_string("Name", "Workspace"), p_bool("StreamingEnabled", True)])
    ws.add(spawn_location(nama_spawn, (0, 0.6, 18), (12, 1.2, 12), (128, 140, 108)))
    ws.add(gerbang_dataran("GerbangDataran"))
    return ws


def lighting_custom(nama_atmos, jam, kecerahan, ambient, outdoor, warna_atmos,
                    decay_atmos, haze, densitas=0.5):
    lighting = Item("Lighting", [
        p_string("Name", "Lighting"),
        p_color3("Ambient", ambient),
        p_color3("OutdoorAmbient", outdoor),
        p_float("Brightness", kecerahan),
        p_float("ClockTime", jam),
        p_float("GeographicLatitude", 12),
        p_bool("GlobalShadows", True),
        p_token("Technology", 3),
    ])
    atmosphere = Item("Atmosphere", [
        p_string("Name", nama_atmos),
        p_float("Density", densitas),
        p_float("Offset", 0.25),
        p_color3("Color", warna_atmos),
        p_color3("Decay", decay_atmos),
        p_float("Glare", 0.03),
        p_float("Haze", haze),
    ])
    lighting.add(atmosphere)
    return lighting


# ============================ KAMPUNG ============================

def build_kampung():
    return workspace_kosong("SpawnKampung")


def lighting_kampung():
    return lighting_custom("AtmosferKampung", 9.5, 2.2, (0.58, 0.58, 0.52), (0.50, 0.50, 0.44),
                           (0.80, 0.78, 0.68), (0.40, 0.38, 0.30), 2.4, densitas=0.5)


# ============================ SABANA ============================

def build_sabana():
    return workspace_kosong("SpawnSabana")


def lighting_sabana():
    return lighting_custom("AtmosferSabana", 16.8, 2.4, (0.64, 0.57, 0.45), (0.56, 0.50, 0.40),
                           (0.86, 0.72, 0.52), (0.50, 0.38, 0.26), 2.6, densitas=0.52)


# ============================ STEPA ============================

def build_stepa():
    return workspace_kosong("SpawnStepa")


def lighting_stepa():
    return lighting_custom("AtmosferStepa", 11.0, 2.0, (0.56, 0.58, 0.56), (0.48, 0.50, 0.48),
                           (0.76, 0.78, 0.74), (0.36, 0.38, 0.36), 2.2, densitas=0.48)


# ============================ PERLADANGAN ============================

def build_perladangan():
    return workspace_kosong("SpawnPerladangan")


def lighting_perladangan():
    return lighting_custom("AtmosferPerladangan", 8.5, 2.2, (0.60, 0.58, 0.50), (0.52, 0.51, 0.44),
                           (0.82, 0.77, 0.62), (0.42, 0.38, 0.28), 2.4, densitas=0.5)
