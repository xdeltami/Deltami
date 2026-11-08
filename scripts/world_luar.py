"""Pembangun dunia untuk 4 kawasan luar: Kampung, Sabana, Stepa, Perladangan.

Pemakaian: build_<nama>() -> Item Workspace (struktur sama dengan Dataran):
Lanskap, SpawnLocation, folder Gerbang (GerbangDataran), folder NPC, PapanKawasan.
Prompt bicara/teleport ditambahkan runtime oleh InteraksiTempat/GerbangTeleport.
"""
import math
import random

import rbxlx_lib
from rbxlx_lib import (Item, add_billboard_tag, add_text_surface, folder, model,
                       p_bool, p_color3, p_cframe, p_float, p_string, p_token,
                       part, rot_matrix)
from world_dataran import Frame, M, FACE, spawn_location


def lighting_custom(nama_atmos, jam, kecerahan, ambient, outdoor, warna_atmos,
                    decay_atmos, haze, densitas=0.3):
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
        p_float("Offset", 0.4),
        p_color3("Color", warna_atmos),
        p_color3("Decay", decay_atmos),
        p_float("Glare", 0),
        p_float("Haze", haze),
    ])
    lighting.add(atmosphere)
    return lighting


def lanskap_dasar(warna_dasar, mat_dasar, palet_variasi, variasi, zona, benih=21):
    items = [part("TanahKawasan", (0, -0.5, 0), (1024, 1, 1024), warna_dasar, mat_dasar)]
    rng = random.Random(benih)
    for i, (x, z) in enumerate(variasi):
        s = rng.uniform(30, 60)
        warna = palet_variasi[i % len(palet_variasi)]
        items.append(part("VariasiTanah%d" % i, (x, 0.05, z), (s, 0.4, s * rng.uniform(0.7, 1.2)),
                          warna, mat_dasar))
    for i, ((x0, z0, x1, z1), warna, mat) in enumerate(zona):
        items.append(part("ZonaJauh%d" % i, ((x0 + x1) / 2.0, 0.1, (z0 + z1) / 2.0),
                          (x1 - x0, 0.4, z1 - z0), warna, mat))
    return items


def jalan_tanah(items, nama, x0, z0, x1, z1, lebar, warna, mat):
    panjang = math.hypot(x1 - x0, z1 - z0)
    sudut = math.degrees(math.atan2(x1 - x0, z1 - z0))
    cx, cz = (x0 + x1) / 2.0, (z0 + z1) / 2.0
    jalan = part(nama, (cx, 0.12, cz), (lebar, 0.4, panjang), warna, mat)
    jalan.props[8] = p_cframe("CFrame", (cx, 0.12, cz), rot_matrix(sudut))
    items.append(jalan)


def gerbang(nama, gx, gz, axis, teks):
    """Gerbang fungsional kembali ke Dataran (axis 0 = timur-barat, 1 = utara-selatan)."""
    g = model(nama)
    g.add(part("PilarGerbang1", (gx + (6.5 if axis == 0 else 0) * 1, 10, gz + (6.5 if axis == 1 else 0) * 1),
               (3, 20, 3), (140, 138, 132), M["slate"]))
    g.add(part("PilarGerbang2", (gx - (6.5 if axis == 0 else 0), 10, gz - (6.5 if axis == 1 else 0)),
               (3, 20, 3), (140, 138, 132), M["slate"]))
    g.add(part("BalokGerbang", (gx, 21.2, gz),
               (17, 2.4, 3) if axis == 0 else (3, 2.4, 17), (120, 118, 112), M["slate"]))
    sign_size = (12, 4, 0.6) if axis == 0 else (0.6, 4, 12)
    sign = part("PapanGerbang", (gx, 16.5, gz), sign_size, (110, 78, 46), M["planks"])
    face_in = FACE["front"] if axis == 1 else FACE["right"]
    face_out = FACE["back"] if axis == 1 else FACE["left"]
    add_text_surface(sign, face_in, teks, (0.96, 0.92, 0.8))
    add_text_surface(sign, face_out, teks, (0.96, 0.92, 0.8))
    g.add(sign)
    barrier = part("PenghalangGerbang", (gx, 13, gz),
                   (2, 26, 22) if axis == 0 else (22, 26, 2), (255, 255, 255), M["smooth"], "block", 1, True)
    g.add(barrier)
    return g


def papan_kawasan(x, z, yaw, teks):
    fr = Frame(x, z, yaw)
    tiang1 = fr.part("TiangPapan1", (-2.2, 2, 0), (0.8, 4, 0.8), (120, 88, 52), M["wood"])
    tiang2 = fr.part("TiangPapan2", (2.2, 2, 0), (0.8, 4, 0.8), (120, 88, 52), M["wood"])
    papan = fr.part("PapanKawasan", (0, 4.4, 0), (7, 3, 0.5), (146, 110, 70), M["planks"])
    add_text_surface(papan, FACE["front"], teks, (0.98, 0.94, 0.82))
    add_text_surface(papan, FACE["back"], teks, (0.98, 0.94, 0.82))
    grp = model("PapanInfoGrp")
    grp.add(tiang1)
    grp.add(tiang2)
    grp.add(papan)
    return grp


def buat_npc(npcs):
    folder_npc = folder("NPC")
    for name, (x, z), yaw, skin, shirt, pants, hat in npcs:
        fr = Frame(x, z, yaw)
        npc = model(name)
        for sx in (-1, 1):
            npc.add(fr.part("Kaki", (sx * 0.65, 1.0, 0), (1.1, 2, 1.1), pants, M["smooth"]))
        npc.add(fr.part("Torso", (0, 3.1, 0), (2.6, 2.2, 1.3), shirt, M["smooth"]))
        for sx in (-1, 1):
            npc.add(fr.part("Lengan", (sx * 1.75, 3.1, 0), (0.9, 2, 0.9), skin, M["smooth"]))
        kepala = fr.part("Kepala", (0, 4.95, 0), (1.5, 1.5, 1.5), skin, M["smooth"], "ball")
        add_billboard_tag(kepala, name.replace("NPC_", ""))
        npc.add(kepala)
        npc.add(fr.part("TopiBrim", (0, 5.55, 0), (0.4, 2.4, 2.4), hat, M["smooth"], "cylinder", 0, False, 0, 0, 90))
        npc.add(fr.part("TopiTop", (0, 6.0, 0), (0.7, 1.1, 1.1), hat, M["smooth"], "cylinder", 0, False, 0, 0, 90))
        folder_npc.add(npc)
    return folder_npc


def pohon_kelapa(x, z, rng, tinggi=None):
    grp = model("Pohon")
    t = tinggi or rng.uniform(14, 20)
    grp.add(part("Batang", (x, t / 2.0, z), (1.4, t, 1.4), (110, 84, 56), M["wood"]))
    for i in range(6):
        a = i * 60 + rng.uniform(-8, 8)
        daun = part("Daun%d" % i, (x + math.cos(math.radians(a)) * 3.2, t + 1.2, z + math.sin(math.radians(a)) * 3.2),
                    (7, 0.5, 2.4), (52, 130, 62), M["grass"])
        daun.props[8] = p_cframe("CFrame",
                                                         (x + math.cos(math.radians(a)) * 3.2, t + 1.2, z + math.sin(math.radians(a)) * 3.2),
                                                         rot_matrix(a, 18))
        grp.add(daun)
    grp.add(part("Kelapa", (x, t - 0.6, z), (1.6, 1.6, 1.6), (110, 78, 44), M["smooth"], "ball"))
    return grp


def rumah_panggung(x, z, yaw, dinding, atap):
    fr = Frame(x, z, yaw)
    grp = model("Rumah")
    grp.add(fr.part("Lantai", (0, 4.2, 0), (18, 0.6, 14), (150, 112, 68), M["planks"]))
    for sx in (-1, 1):
        for sz in (-1, 1):
            grp.add(fr.part("Tiang", (sx * 7.6, 2.1, sz * 5.6), (1.2, 4.2, 1.2), (122, 92, 56), M["wood"]))
    for sz in (-1, 1):
        grp.add(fr.part("DindingDepan", (0, 6.4, sz * 6.8), (18, 4, 0.6), dinding, M["planks"]))
    grp.add(fr.part("DindingKiri", (-8.7, 6.4, 0), (0.6, 4, 13), dinding, M["planks"]))
    grp.add(fr.part("DindingKanan", (8.7, 6.4, 0), (0.6, 4, 13), dinding, M["planks"]))
    grp.add(fr.part("AtapBawah", (0, 9.2, 0), (20, 0.8, 16), atap, M["planks"]))
    grp.add(fr.part("AtapAtas", (0, 10.4, 0), (22, 1.2, 18), atap, M["planks"], "block", 0, True, 0, 6))
    grp.add(fr.part("Tangga", (0, 1.8, 9.2), (5, 0.5, 6), (140, 104, 62), M["planks"], "block", 0, True, 0, 14))
    jendela = fr.part("Jendela", (0, 6.6, 6.9), (6, 2.4, 0.3), (150, 190, 210), M["glass"], "block", 0.35)
    grp.add(jendela)
    return grp


def sumur(x, z):
    grp = model("Sumur")
    grp.add(part("BibirSumur", (x, 1.4, z), (5, 2.8, 5), (128, 126, 120), M["cobble"], "cylinder"))
    grp.add(part("AirSumur", (x, 1.2, z), (4.4, 0.4, 4.4), (70, 130, 170), M["water"], "cylinder"))
    grp.add(part("TiangSumur1", (x - 2.2, 3.4, z), (0.7, 4, 0.7), (130, 96, 58), M["wood"]))
    grp.add(part("TiangSumur2", (x + 2.2, 3.4, z), (0.7, 4, 0.7), (130, 96, 58), M["wood"]))
    grp.add(part("AtapSumur", (x, 5.8, z), (6.4, 0.6, 4.2), (150, 92, 60), M["planks"], "block", 0, True, 0, 8))
    return grp


# ============================ KAMPUNG ============================

def build_kampung():
    rng = random.Random(101)
    workspace = Item("Workspace", [p_string("Name", "Workspace"), p_bool("StreamingEnabled", True)])

    lanskap = folder("Lanskap")
    items = lanskap_dasar((96, 132, 62), M["grass"],
                          [(86, 124, 58), (108, 146, 68), (92, 138, 60), (102, 142, 64)],
                          [(-70, 80), (80, 70), (-110, -30), (130, -50), (-50, -120), (170, 120), (-190, 90), (60, 170)],
                          [((-320, -90, -240, 90), (88, 126, 58), M["grass"]),
                           ((-90, -330, 90, -240), (128, 102, 62), M["ground"]),
                           ((240, -90, 330, 90), (90, 128, 60), M["grass"]),
                           ((-90, 240, 90, 330), (94, 130, 64), M["grass"])], benih=31)
    sawah = folder("Sawah")
    for r in range(3):
        for c in range(4):
            x, z = -150 + c * 26, 150 + r * 22
            petak = part("PetakSawah%d%d" % (r, c), (x, 0.3, z), (22, 0.5, 17), (116, 158, 74), M["grass"])
            sawah.add(petak)
            sawah.add(part("AirSawah%d%d" % (r, c), (x, 0.42, z), (21, 0.3, 16), (96, 150, 170), M["water"], "block", 0.4))
            for k in range(4):
                sawah.add(part("Padi%d%d%d" % (r, c, k), (x - 7 + k * 4.6, 1.3, z), (0.9, 2.2, 0.9), (196, 188, 96), M["grass"], "block", 0, True, rng.uniform(-8, 8)))
    for i in items:
        lanskap.add(i)
    workspace.add(lanskap)
    workspace.add(sawah)

    permukiman = folder("Permukiman")
    for i, (x, z, yaw, d, a) in enumerate([
            (-52, -60, 30, (176, 128, 84), (196, 92, 64)),
            (56, -64, -25, (168, 120, 78), (188, 84, 58)),
            (-64, 40, 115, (182, 136, 90), (204, 100, 70)),
            (62, 44, -110, (172, 124, 82), (192, 88, 62)),
            (10, -110, 180, (178, 132, 88), (200, 96, 66))]):
        permukiman.add(rumah_panggung(x, z, yaw, d, a))
    for i in range(8):
        x = rng.uniform(-190, 190)
        z = rng.uniform(-190, 190)
        if abs(x) < 40 and abs(z) < 40:
            continue
        permukiman.add(pohon_kelapa(x, z, rng))
    workspace.add(permukiman)

    alun = folder("PusatKampung")
    alun.add(part("AlunKampung", (0, 0.2, -10), (44, 0.5, 40), (176, 148, 104), M["ground"]))
    alun.add(sumur(0, -10))
    for a in (0, 90, 180, 270):
        bangku = part("Bangku%d" % a, (math.cos(math.radians(a)) * 14, 0.9, -10 + math.sin(math.radians(a)) * 14),
                      (3.4, 0.5, 1.2), (138, 102, 60), M["wood"])
        bangku.props[8] = p_cframe("CFrame", (math.cos(math.radians(a)) * 14, 0.9, -10 + math.sin(math.radians(a)) * 14), rot_matrix(a))
        alun.add(bangku)
    workspace.add(alun)

    jalan = []
    jalan_tanah(jalan, "JalanUtama", 0, -220, 0, 40, 12, (150, 120, 80), M["ground"])
    jalan_tanah(jalan, "JalanSawah", 0, 40, -120, 150, 8, (150, 120, 80), M["ground"])
    for i in jalan:
        lanskap.add(i)

    workspace.add(spawn_location("SpawnKampung", (6, 0.6, -2), (14, 1.2, 14), (120, 150, 76)))
    workspace.add(papan_kawasan(-8, 12, 15, "KAMPUNG AKIOMIDA"))
    workspace.add(gerbang("GerbangDataran", 0, -210, 1, "GERBANG DATARAN"))
    workspace.add(buat_npc([
        ("NPC_PakUmar", (-10, -28), 20, (232, 190, 152), (84, 116, 168), (62, 58, 54), (128, 96, 58)),
        ("NPC_BuRatna", (14, -30), -20, (236, 196, 158), (196, 84, 96), (70, 74, 96), (172, 128, 74)),
        ("NPC_Dedi", (-14, 56), 140, (226, 186, 148), (110, 138, 84), (58, 54, 50), (142, 108, 64)),
    ]))
    return workspace


def lighting_kampung():
    return lighting_custom("AtmosferKampung", 9.5, 2.3, (0.60, 0.60, 0.52), (0.52, 0.52, 0.44),
                           (0.82, 0.80, 0.62), (0.40, 0.38, 0.30), 1.0)


# ============================ SABANA ============================

def build_sabana():
    rng = random.Random(202)
    workspace = Item("Workspace", [p_string("Name", "Workspace"), p_bool("StreamingEnabled", True)])

    lanskap = folder("Lanskap")
    items = lanskap_dasar((198, 176, 118), M["sand"],
                          [(192, 170, 112), (206, 184, 126), (184, 164, 108)],
                          [(-80, 60), (90, 80), (-120, -60), (140, -40), (-60, -150), (180, 140), (-180, 20), (40, 180)],
                          [((-320, -90, -240, 90), (188, 168, 112), M["sand"]),
                           ((-90, -330, 90, -240), (206, 188, 140), M["sand"]),
                           ((240, -90, 330, 90), (182, 162, 108), M["sand"]),
                           ((-90, 240, 90, 330), (192, 172, 120), M["sand"])], benih=41)
    for i in items:
        lanskap.add(i)
    workspace.add(lanskap)

    geni = folder("AlamSabana")
    for i in range(9):
        a = i * 40 + rng.uniform(-12, 12)
        r = rng.uniform(60, 220)
        x, z = math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r
        t = rng.uniform(10, 15)
        geni.add(part("BatangAkasia%d" % i, (x, t / 2.0, z), (1.6, t, 1.6), (98, 74, 48), M["wood"], "block", 0, True, rng.uniform(-6, 6)))
        geni.add(part("TajukAkasia%d" % i, (x, t + 1.6, z), (rng.uniform(12, 17), 1.4, rng.uniform(12, 17)), (88, 118, 52), M["grass"]))
    for i in range(14):
        a = rng.uniform(0, 360)
        r = rng.uniform(30, 250)
        x, z = math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r
        s = rng.uniform(3, 7)
        geni.add(part("BatuSabana%d" % i, (x, s * 0.35, z), (s, s * 0.7, s * rng.uniform(0.8, 1.3)),
                     (150, 140, 122), M["slate"], "ball", 0, True, rng.uniform(0, 180)))
    for i in range(22):
        a = rng.uniform(0, 360)
        r = rng.uniform(24, 240)
        x, z = math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r
        geni.add(part("RumputKering%d" % i, (x, 0.7, z), (2.4, 1.4, 2.4), (168, 150, 84), M["ground"], "ball"))
    workspace.add(geni)

    pusat = folder("PusatSabana")
    pusat.add(part("AlunSabana", (0, 0.2, -8), (40, 0.5, 36), (186, 170, 126), M["ground"]))
    pusat.add(part("MataAir", (26, 0.25, 22), (22, 0.5, 18), (74, 136, 160), M["water"], "block", 0.25))
    pusat.add(part("LumpurMataAir", (26, 0.15, 22), (26, 0.4, 22), (140, 118, 82), M["ground"]))
    menara = Frame(-20, -20, 0)
    pusat.add(menara.part("KakiMenara", (0, 5, 0), (5, 10, 5), (140, 104, 62), M["wood"]))
    pusat.add(menara.part("DekMenara", (0, 10.6, 0), (8, 0.8, 8), (150, 112, 68), M["planks"]))
    pusat.add(menara.part("AtapMenara", (0, 14.4, 0), (9, 1, 9), (176, 84, 58), M["planks"], "block", 0, True, 0, 10))
    workspace.add(pusat)

    jalan = []
    jalan_tanah(jalan, "JalanSafari", 0, 210, 0, -30, 11, (172, 152, 108), M["ground"])
    jalan_tanah(jalan, "JalanMataAir", 0, -30, 26, 22, 7, (172, 152, 108), M["ground"])
    for i in jalan:
        lanskap.add(i)

    workspace.add(spawn_location("SpawnSabana", (5, 0.6, -4), (14, 1.2, 14), (206, 186, 134)))
    workspace.add(papan_kawasan(-9, 10, 12, "SABANA AKIOMIDA"))
    workspace.add(gerbang("GerbangDataran", 0, 210, 1, "GERBANG DATARAN"))
    workspace.add(buat_npc([
        ("NPC_PanduSaka", (-11, -26), 15, (214, 168, 122), (146, 92, 54), (70, 56, 42), (120, 88, 54)),
        ("NPC_BuLesa", (15, -28), -18, (222, 176, 130), (188, 106, 74), (78, 62, 48), (150, 112, 66)),
        ("NPC_Rio", (-13, 44), 150, (218, 172, 126), (96, 118, 140), (66, 54, 44), (132, 98, 58)),
    ]))
    return workspace


def lighting_sabana():
    return lighting_custom("AtmosferSabana", 16.8, 2.6, (0.66, 0.58, 0.44), (0.58, 0.50, 0.38),
                           (0.88, 0.72, 0.48), (0.52, 0.36, 0.22), 2.2, densitas=0.34)


# ============================ STEPA ============================

def build_stepa():
    rng = random.Random(303)
    workspace = Item("Workspace", [p_string("Name", "Workspace"), p_bool("StreamingEnabled", True)])

    lanskap = folder("Lanskap")
    items = lanskap_dasar((154, 160, 104), M["ground"],
                          [(148, 154, 102), (160, 166, 110), (142, 150, 98)],
                          [(-70, 80), (90, 70), (-120, -40), (130, -50), (-50, -140), (170, 130), (-180, 60), (50, 170)],
                          [((-320, -90, -240, 90), (146, 152, 100), M["ground"]),
                           ((-90, -330, 90, -240), (162, 166, 112), M["ground"]),
                           ((240, -90, 330, 90), (140, 148, 98), M["ground"]),
                           ((-90, 240, 90, 330), (158, 162, 108), M["ground"])], benih=51)
    for i in items:
        lanskap.add(i)
    workspace.add(lanskap)

    gundukan = folder("BukitStepa")
    for i, (x, z, s, pitch) in enumerate([(-190, -160, 26, 9), (170, -180, 30, -7), (220, 120, 24, 8),
                                          (-220, 100, 28, -6), (80, 230, 30, 6), (-90, 220, 26, -8),
                                          (-250, -40, 24, 10), (250, -20, 22, -9)]):
        gundukan.add(part("Bukit%d" % i, (x, 1.4, z), (s, 2.8, s * 0.8), (148, 154, 102), M["ground"], "block", 0, True, rng.uniform(-10, 10), pitch))
    for i in range(12):
        a = rng.uniform(0, 360)
        r = rng.uniform(40, 250)
        x, z = math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r
        s = rng.uniform(2.5, 6)
        gundukan.add(part("BatuStepa%d" % i, (x, s * 0.3, z), (s, s * 0.6, s), (136, 134, 128), M["slate"], "ball", 0, True, rng.uniform(0, 180)))
    workspace.add(gundukan)

    pusat = folder("PusatStepa")
    pusat.add(part("AlunStepa", (0, 0.2, -8), (40, 0.5, 36), (170, 172, 118), M["ground"]))
    kincir = Frame(-24, -18, 0)
    pusat.add(kincir.part("MenaraKincir", (0, 9, 0), (6, 18, 6), (222, 216, 204), M["smooth"]))
    pusat.add(kincir.part("AtapKincir", (0, 19.4, 0), (8, 2, 8), (120, 72, 52), M["planks"], "block", 0, True, 0, 12))
    for b in range(4):
        sudut = b * 90
        blade = kincir.part("Baling%d" % b, (0, 16.5, 4.2), (1.4, 9, 0.4), (238, 234, 224), M["planks"])
        blade.props[8] = p_cframe("CFrame", (0 - 24, 16.5, -18 + 4.2), rot_matrix(sudut, 78))
        pusat.add(blade)
    for i in range(7):
        x = rng.uniform(-160, 160)
        z = rng.uniform(-160, 160)
        if abs(x) < 30 and abs(z) < 30:
            continue
        pusat.add(part("BaleJerami%d" % i, (x, 2.4, z), (6, 4.8, 6), (204, 178, 92), M["grass"], "cylinder", 0, True, rng.uniform(0, 180), 90))
    menara = Frame(20, -20, 0)
    pusat.add(menara.part("KakiMenaraStepa", (0, 6, 0), (4.4, 12, 4.4), (128, 94, 56), M["wood"]))
    pusat.add(menara.part("DekMenaraStepa", (0, 12.6, 0), (7, 0.8, 7), (146, 110, 68), M["planks"]))
    pusat.add(menara.part("AtapMenaraStepa", (0, 15.8, 0), (8, 1, 8), (108, 82, 56), M["planks"], "block", 0, True, 0, 10))
    workspace.add(pusat)

    jalan = []
    jalan_tanah(jalan, "JalanStepa", 210, 0, 30, 0, 11, (158, 154, 106), M["ground"])
    for i in jalan:
        lanskap.add(i)

    workspace.add(spawn_location("SpawnStepa", (5, 0.6, 6), (14, 1.2, 14), (168, 172, 118)))
    workspace.add(papan_kawasan(-9, -12, -10, "STEPA AKIOMIDA"))
    workspace.add(gerbang("GerbangDataran", 210, 0, 0, "GERBANG DATARAN"))
    workspace.add(buat_npc([
        ("NPC_Jaro", (-11, -24), 18, (222, 182, 142), (92, 104, 128), (56, 54, 50), (126, 94, 58)),
        ("NPC_Altai", (14, -26), -15, (230, 190, 150), (150, 84, 60), (60, 56, 52), (138, 102, 60)),
        ("NPC_Marek", (-13, 40), 145, (218, 178, 140), (104, 128, 92), (58, 54, 50), (132, 98, 60)),
    ]))
    return workspace


def lighting_stepa():
    return lighting_custom("AtmosferStepa", 11.0, 2.1, (0.58, 0.60, 0.56), (0.50, 0.52, 0.48),
                           (0.78, 0.80, 0.72), (0.38, 0.40, 0.36), 1.3)


# ============================ PERLADANGAN ============================

def build_perladangan():
    rng = random.Random(404)
    workspace = Item("Workspace", [p_string("Name", "Workspace"), p_bool("StreamingEnabled", True)])

    lanskap = folder("Lanskap")
    items = lanskap_dasar((118, 142, 70), M["ground"],
                          [(110, 136, 66), (122, 146, 72), (102, 130, 62)],
                          [(-70, 80), (90, 70), (-120, -40), (130, -50), (-60, -140), (170, 120), (-180, 70), (60, 170)],
                          [((-320, -90, -240, 90), (108, 134, 66), M["ground"]),
                           ((-90, -330, 90, -240), (112, 138, 68), M["ground"]),
                           ((240, -90, 330, 90), (104, 130, 64), M["ground"]),
                           ((-90, 240, 90, 330), (116, 140, 72), M["ground"])], benih=61)
    for i in items:
        lanskap.add(i)
    workspace.add(lanskap)

    kebun = folder("TerasKebun")
    warna_teh = [(64, 118, 58), (72, 128, 62), (58, 110, 54)]
    for baris in range(5):
        z = -120 + baris * 24
        for kolom in range(10):
            x = -170 + kolom * 34
            warna = warna_teh[(baris + kolom) % 3]
            kebun.add(part("Teh%d%d" % (baris, kolom), (x, 1.4, z), (14, 2.8, 6), warna, M["grass"], "block", 0, True, 0, rng.uniform(-2, 2)))
    for baris in range(4):
        x = 120 + (baris % 2) * 26
        z = -110 + baris * 26
        kebun.add(part("SalakBaris%d" % baris, (x, 2.6, z), (3, 5.2, 34), (86, 132, 60), M["grass"], "block", 0, True, rng.uniform(-4, 4)))
    teras = folder("TerasTanah")
    for i, (x, z, w, d, pitch) in enumerate([(-140, -60, 180, 12, 7), (-140, 10, 180, 12, -6), (150, -40, 14, 160, 8), (60, 130, 170, 12, -7)]):
        teras.add(part("Teras%d" % i, (x, 0.6, z), (w, 1.2, d), (124, 96, 62), M["ground"], "block", 0, True, 0, pitch))
    workspace.add(kebun)
    workspace.add(teras)

    pusat = folder("PusatPerladangan")
    pusat.add(part("AlunKebun", (0, 0.2, -8), (42, 0.5, 38), (148, 120, 82), M["ground"]))
    lumbung = Frame(-30, -34, 12)
    pusat.add(lumbung.part("LantaiLumbung", (0, 0.5, 0), (20, 1, 15), (128, 100, 64), M["planks"]))
    for sx in (-1, 1):
        pusat.add(lumbung.part("DindingLumbung%d" % sx, (sx * 9.4, 4.6, 0), (1.2, 8.2, 15), (188, 96, 62), M["planks"]))
    pusat.add(lumbung.part("DindingLumbungD", (0, 4.6, -7.4), (20, 8.2, 1.2), (176, 88, 58), M["planks"]))
    pusat.add(lumbung.part("AtapLumbung", (0, 10.2, 0), (23, 1, 18), (94, 66, 44), M["planks"], "block", 0, True, 0, 10))
    pusat.add(lumbung.part("PintuLumbung", (0, 3.4, 7.5), (6, 6, 0.5), (120, 84, 52), M["wood"]))
    kanal = Frame(34, 30, 0)
    pusat.add(kanal.part("KanalIrigasi", (0, 0.15, 0), (10, 0.5, 90), (86, 140, 166), M["water"], "block", 0.3))
    pusat.add(kanal.part("TepiKanal1", (-5.6, 0.3, 0), (1.4, 0.8, 90), (138, 108, 70), M["ground"]))
    pusat.add(kanal.part("TepiKanal2", (5.6, 0.3, 0), (1.4, 0.8, 90), (138, 108, 70), M["ground"]))
    workspace.add(pusat)

    jalan = []
    jalan_tanah(jalan, "JalanKebun", -210, 0, 30, 0, 12, (144, 116, 78), M["ground"])
    for i in jalan:
        lanskap.add(i)

    workspace.add(spawn_location("SpawnPerladangan", (6, 0.6, 4), (14, 1.2, 14), (126, 150, 78)))
    workspace.add(papan_kawasan(-9, -14, -12, "PERLADANGAN AKIOMIDA"))
    workspace.add(gerbang("GerbangDataran", -210, 0, 0, "GERBANG DATARAN"))
    workspace.add(buat_npc([
        ("NPC_PakTani", (-11, -24), 18, (228, 188, 150), (98, 130, 84), (60, 56, 50), (140, 106, 62)),
        ("NPC_BuLastri", (14, -26), -15, (234, 194, 156), (198, 96, 88), (72, 70, 66), (160, 120, 70)),
        ("NPC_Mulyo", (-13, 44), 145, (222, 182, 144), (108, 96, 148), (58, 54, 50), (130, 98, 58)),
    ]))
    return workspace


def lighting_perladangan():
    return lighting_custom("AtmosferPerladangan", 8.5, 2.3, (0.62, 0.60, 0.50), (0.54, 0.52, 0.42),
                           (0.84, 0.78, 0.58), (0.44, 0.38, 0.26), 1.6)
