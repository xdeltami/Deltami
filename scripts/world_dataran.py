import math
import random

from rbxlx_lib import (Item, add_billboard_tag, add_point_light, add_text_surface, folder, model,
                       p_bool, p_color3, p_color3u8, p_cframe, p_float, p_int, p_string, p_token,
                       p_vec3, part, rot_matrix, script_item)

M = {
    "grass": 1280, "ground": 1360, "sand": 1296, "slate": 800, "concrete": 816,
    "cobble": 880, "brick": 848, "wood": 512, "planks": 528, "smooth": 272,
    "neon": 288, "metal": 1088, "water": 2048, "pebble": 864, "glass": 1568,
}
FACE = {"right": 0, "top": 1, "back": 2, "left": 3, "bottom": 4, "front": 5}

TAN30 = math.tan(math.radians(30))


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def ry(t):
    c, s = math.cos(math.radians(t)), math.sin(math.radians(t))
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]


class Frame:
    def __init__(self, cx, cz, yaw):
        self.cx, self.cz, self.yaw = cx, cz, yaw
        self.r = ry(yaw)

    def pos(self, lx, ly, lz):
        x = self.cx + self.r[0][0] * lx + self.r[0][2] * lz
        z = self.cz + self.r[2][0] * lx + self.r[2][2] * lz
        return (x, ly, z)

    def rot(self, lyaw=0.0, lpitch=0.0, lroll=0.0):
        local = rot_matrix(lyaw, lpitch, lroll)
        return mat_mul(self.r, local)

    def part(self, name, lpos, size, color, material=M["smooth"], shape="block",
             transparency=0.0, collide=True, lyaw=0.0, lpitch=0.0, lroll=0.0, cls="Part"):
        wpos = self.pos(*lpos)
        item = part(name, wpos, size, color, material, shape, transparency, collide)
        item.props[8] = p_cframe("CFrame", wpos, self.rot(lyaw, lpitch, lroll))
        return item


def spawn_location(name, pos, size, color):
    props = [
        p_string("Name", name),
        p_bool("Anchored", True),
        p_bool("CanCollide", True),
        p_bool("Neutral", True),
        p_token("Material", M["grass"]),
        p_token("shape", 1),
        p_color3u8("Color3uint8", color),
        p_vec3("size", size),
        p_cframe("CFrame", pos, rot_matrix()),
    ]
    for face in ("TopSurface", "BottomSurface", "LeftSurface", "RightSurface", "FrontSurface", "BackSurface"):
        props.append(p_token(face, 0))
    return Item("SpawnLocation", props)


def wall_piece(frame, name, along, fixed, a, b, y0, y1, color, material):
    length = b - a
    height = y1 - y0
    mid = (a + b) / 2.0
    if along == "z":
        return frame.part(name, (fixed, (y0 + y1) / 2.0, mid), (1, height, length), color, material)
    return frame.part(name, (mid, (y0 + y1) / 2.0, fixed), (length, height, 1), color, material)


def wall_with_holes(frame, name, along, fixed, start, length, base, top, holes, color, material):
    items = []
    edges = sorted([(s, s + w, y0, y1) for (s, w, y0, y1) in holes])
    cursor = start
    for (hs, he, y0, y1) in edges:
        if hs > cursor:
            items.append(wall_piece(frame, name, along, fixed, cursor, hs, base, top, color, material))
        if y0 > base:
            items.append(wall_piece(frame, name, along, fixed, hs, he, base, y0, color, material))
        if y1 < top:
            items.append(wall_piece(frame, name, along, fixed, hs, he, y1, top, color, material))
        cursor = he
    if cursor < start + length:
        items.append(wall_piece(frame, name, along, fixed, cursor, start + length, base, top, color, material))
    return items


def building(frame, width_z, depth_x, wall_rgb, roof_rgb, wood_rgb, floor_rgb,
             holes_front, holes_side=None, name_plate=None, window_panes=False):
    items = []
    items.append(frame.part("Pondasi", (0, 0.5, 0), (depth_x + 2, 1, width_z + 2), (130, 128, 124), M["slate"]))
    items.append(frame.part("Lantai", (0, 1.2, 0), (depth_x - 2, 0.4, width_z - 2), floor_rgb, M["planks"]))
    front_x = depth_x / 2.0 - 0.5
    back_x = -depth_x / 2.0 + 0.5
    items += wall_with_holes(frame, "DindingDepan", "z", front_x, -width_z / 2.0, width_z, 1, 21, holes_front, wall_rgb, M["smooth"])
    items.append(frame.part("DindingBelakang", (back_x, 11, 0), (1, 20, width_z), wall_rgb, M["smooth"]))
    if holes_side is None:
        items.append(frame.part("DindingKiri", (0, 11, width_z / 2.0 - 0.5), (depth_x, 20, 1), wall_rgb, M["smooth"]))
        items.append(frame.part("DindingKanan", (0, 11, -width_z / 2.0 + 0.5), (depth_x, 20, 1), wall_rgb, M["smooth"]))
    else:
        items += wall_with_holes(frame, "DindingSamping", "x", width_z / 2.0 - 0.5, -depth_x / 2.0, depth_x, 1, 21, holes_side, wall_rgb, M["smooth"])
        items += wall_with_holes(frame, "DindingSamping", "x", -width_z / 2.0 + 0.5, -depth_x / 2.0, depth_x, 1, 21, holes_side, wall_rgb, M["smooth"])
    for sx in (-1, 1):
        for sz in (-1, 1):
            items.append(frame.part("TiangSudut", (sx * (depth_x / 2.0 - 1), 11, sz * (width_z / 2.0 - 1)),
                                    (2, 20, 2), wood_rgb, M["wood"]))
    if window_panes:
        for (off, w, y0, y1) in holes_front:
            if y0 > 1:
                items.append(frame.part("KacaJendela", (depth_x / 2.0 - 0.5, (y0 + y1) / 2.0, -width_z / 2.0 + off + w / 2.0),
                                        (0.2, y1 - y0 - 0.4, w - 0.4), (168, 200, 210), M["glass"], transparency=0.45))
    run = depth_x / 2.0 + 3
    rise = run * TAN30
    ridge_y = 21 + rise
    slab_len = 2 * math.ceil(math.sqrt(run * run + rise * rise) / 2)
    slab_w = width_z + 6
    for sx in (-1, 1):
        cx_local = sx * (run / 2.0 - 0.25)
        cy_local = (21 + ridge_y) / 2.0 - 0.433
        items.append(frame.part("Atap", (cx_local, cy_local, 0), (slab_len, 1, slab_w), roof_rgb, M["brick"],
                                lroll=-30 * sx))
    rise_w = (depth_x / 2.0) * TAN30
    for sx in (-1, 1):
        for sz in (-1, 1):
            items.append(frame.part("Bubungan", (sx * depth_x / 4.0, 21 + rise_w / 2.0, sz * (width_z / 2.0 - 0.5)),
                                    (1, rise_w, depth_x / 2.0), wall_rgb, M["smooth"], lyaw=-90 * sx))
    if name_plate:
        plate = frame.part("PapanNama", (depth_x / 2.0 + 0.25, 14, 0), (0.5, 4, 16), wood_rgb, M["planks"])
        add_text_surface(plate, FACE["right"], name_plate, (0.98, 0.94, 0.82))
        items.append(plate)
        items.append(frame.part("Kanopi", (depth_x / 2.0 + 2, 16.4, 0), (4, 0.8, width_z + 4), roof_rgb, M["brick"]))
        for sz in (-1, 1):
            items.append(frame.part("TiangKanopi", (depth_x / 2.0 + 3, 8, sz * (width_z / 2.0 - 6)), (2, 16, 2), wood_rgb, M["wood"]))
    return items


def tree_at(x, z, rng):
    items = []
    h = rng.uniform(7, 11)
    d = rng.uniform(1.8, 2.4)
    items.append(part("BatangPohon", (x, h / 2.0, z), (h, d, d), (110, 84, 58), M["wood"], "cylinder", 0, True, 0, 0, 90))
    greens = [(64, 124, 58), (84, 146, 70), (56, 110, 52), (96, 152, 74)]
    g = greens[rng.randrange(len(greens))]
    d1 = rng.uniform(5.5, 8)
    items.append(part("Dedaunan", (x, h + d1 * 0.22, z), (d1, d1 * 0.95, d1), g, M["grass"], "ball"))
    if rng.random() < 0.65:
        d2 = rng.uniform(4, 6)
        ox = rng.uniform(-1.6, 1.6)
        oz = rng.uniform(-1.6, 1.6)
        items.append(part("DedaunanAtas", (x + ox, h + d1 * 0.22 + d2 * 0.4, z + oz), (d2, d2 * 0.9, d2),
                          (min(255, g[0] + 12), g[1], g[2]), M["grass"], "ball"))
    return items


def build_ground():
    items = []
    items.append(part("TanahDataran", (0, -0.5, 0), (1024, 1, 1024), (98, 138, 66), M["grass"]))
    rng = random.Random(21)
    greens = [(86, 124, 58), (112, 150, 70), (92, 144, 62), (104, 142, 60)]
    spots = [(-60, 90), (90, 60), (-120, 40), (140, -40), (-40, -140), (190, 140),
             (-200, 60), (60, 180), (-160, -240), (220, -200), (-220, 220), (240, 240)]
    for i, (x, z) in enumerate(spots):
        s = rng.uniform(34, 66)
        items.append(part("VariasiRumput%d" % i, (x, 0.05, z), (s, 0.4, s * rng.uniform(0.7, 1.2)),
                          greens[i % len(greens)], M["grass"]))
    zona = [
        ((-330, -90, -240, 90), (92, 132, 60), M["grass"]),
        ((-90, -330, 90, -240), (206, 186, 142), M["sand"]),
        ((240, -90, 330, 90), (150, 156, 100), M["grass"]),
        ((-90, 240, 90, 330), (122, 94, 64), M["ground"]),
    ]
    for i, ((x0, z0, x1, z1), warna, mat) in enumerate(zona):
        items.append(part("ZonaJauh%d" % i, ((x0 + x1) / 2.0, 0.1, (z0 + z1) / 2.0), (x1 - x0, 0.4, z1 - z0), warna, mat))
    return items


def build_paths():
    items = []
    c = (178, 171, 160)
    items.append(part("JalurBarat", (-122, 0.15, 0), (196, 0.5, 8), c, M["concrete"]))
    items.append(part("JalurTimur", (122, 0.15, 0), (196, 0.5, 8), c, M["concrete"]))
    items.append(part("JalurUtara", (0, 0.15, -122), (8, 0.5, 196), c, M["concrete"]))
    items.append(part("JalurSelatan", (0, 0.15, 122), (8, 0.5, 196), c, M["concrete"]))
    items.append(part("JalurToko", (-47, 0.15, -48), (46, 0.5, 6), c, M["concrete"]))
    items.append(part("JalurDesa", (57, 0.15, -64), (106, 0.5, 6), c, M["concrete"]))
    items.append(part("JalurDesa2", (104, 0.15, -114), (6, 0.5, 104), c, M["concrete"]))
    items.append(part("JalurKolam", (56, 0.2, 96), (100, 0.4, 4), (120, 96, 66), M["ground"]))
    return items


def bench(angle):
    items = []
    fr = Frame(19 * math.cos(math.radians(angle)), 19 * math.sin(math.radians(angle)), 90 - angle)
    items.append(fr.part("DudukanBangku", (0, 2.4, 0), (4, 0.8, 2), (140, 100, 60), M["planks"]))
    items.append(fr.part("SandaranBangku", (0, 3.3, 1.05), (4, 1.8, 0.6), (140, 100, 60), M["planks"]))
    for sx in (-1, 1):
        items.append(fr.part("KakiBangku", (sx * 1.4, 1.4, 0), (0.8, 1.2, 1.6), (90, 66, 40), M["wood"]))
    return items


def lamp(angle):
    items = []
    x = 23 * math.cos(math.radians(angle))
    z = 23 * math.sin(math.radians(angle))
    items.append(part("TiangLampu", (x, 5.3, z), (9, 0.9, 0.9), (60, 62, 66), M["metal"], "cylinder", 0, True, 0, 0, 90))
    head = part("KepalaLampu", (x, 10.3, z), (1.8, 1.8, 1.8), (255, 216, 150), M["neon"], "ball")
    add_point_light(head, (1.0, 0.85, 0.6), 1.3, 20)
    items.append(head)
    return items


def build_plaza():
    items = []
    items.append(part("LantaiAlunAlun", (0, 0.4, 0), (0.8, 48, 48), (172, 166, 152), M["cobble"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("MancurBak", (0, 2.0, 0), (2.4, 18, 18), (150, 148, 142), M["slate"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("MancurAir", (0, 2.2, 0), (1.8, 14, 14), (96, 150, 196), M["water"], "cylinder", 0.25, False, 0, 0, 90))
    items.append(part("MancurTiang", (0, 5.4, 0), (4.4, 2.2, 2.2), (150, 148, 142), M["slate"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("MancurMangkuk", (0, 7.8, 0), (0.8, 5, 5), (150, 148, 142), M["slate"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("MancurBola", (0, 9.3, 0), (2, 2, 2), (150, 210, 240), M["neon"], "ball"))
    for angle in (22, 67, 112, 157, 202, 247, 292, 337):
        items += bench(angle)
    for angle in (45, 135, 225, 315):
        items += lamp(angle)
    papan_fr = Frame(-16, -16, 225)
    for off in (-4, 4):
        items.append(papan_fr.part("TiangPapan", (off, 4.8, 0), (0.8, 8, 0.8), (110, 78, 46), M["wood"]))
    papan = papan_fr.part("PapanInfo", (0, 6.4, 0), (12, 6, 0.6), (110, 78, 46), M["planks"])
    add_text_surface(papan, FACE["front"],
                     "PAPAN INFORMASI DATARAN\nSelamat datang di Dataran!\nToko Benih: barat - Kebun Demonstrasi: timur\nGerbang: Kampung (barat) - Sabana (utara)\nStepa (timur) - Perladangan (selatan)",
                     (0.96, 0.92, 0.8))
    items.append(papan)
    signs = [
        ("PenunjukKampung", (-30, 7), "KAMPUNG", FACE["right"]),
        ("PenunjukStepa", (30, -7), "STEPA", FACE["left"]),
        ("PenunjukSabana", (7, -30), "SABANA", FACE["back"]),
        ("PenunjukPerladangan", (-7, 30), "PERLADANGAN", FACE["front"]),
    ]
    for name, (x, z), text, face in signs:
        items.append(part(name + "Tiang", (x, 3.5, z), (0.8, 7, 0.8), (120, 88, 52), M["wood"]))
        board = part(name, (x, 5.6, z), (6, 3, 0.5), (146, 110, 70), M["planks"])
        add_text_surface(board, face, text, (0.16, 0.13, 0.1))
        items.append(board)
    return items


def shelf_unit(fr, wall_coord, center, facing):
    items = []
    bag_colors = [(198, 168, 88), (164, 44, 96), (108, 180, 78), (196, 52, 48), (124, 64, 152), (238, 232, 214)]
    levels = (3.0, 5.4, 7.8)
    if facing == "x":
        items.append(fr.part("RakBelakang", (wall_coord + 0.3, 5.4, center), (0.6, 8, 8), (94, 68, 44), M["wood"]))
        for idx, level in enumerate(levels):
            items.append(fr.part("RakPapan", (wall_coord + 1.3, level, center), (2, 0.6, 8), (146, 108, 64), M["planks"]))
            items.append(fr.part("KarungBenih", (wall_coord + 1.3, level + 1.2, center - 2 + idx * 2),
                                 (1.4, 1.8, 1.4), bag_colors[idx], M["smooth"]))
        for sz in (-1, 1):
            items.append(fr.part("RakSisi", (wall_coord + 1.3, 5.4, center + sz * 3.7), (2, 8, 0.6), (94, 68, 44), M["wood"]))
    else:
        items.append(fr.part("RakBelakang", (center, 5.4, wall_coord - 0.3), (8, 8, 0.6), (94, 68, 44), M["wood"]))
        for idx, level in enumerate(levels):
            items.append(fr.part("RakPapan", (center, level, wall_coord - 1.3), (8, 0.6, 2), (146, 108, 64), M["planks"]))
            items.append(fr.part("KarungBenih", (center - 2 + idx * 2, level + 1.2, wall_coord - 1.3),
                                 (1.4, 1.8, 1.4), bag_colors[idx + 3], M["smooth"]))
        for sx in (-1, 1):
            items.append(fr.part("RakSisi", (center + sx * 3.7, 5.4, wall_coord - 1.3), (0.6, 8, 2), (94, 68, 44), M["wood"]))
    return items


def build_toko():
    fr = Frame(-84, -48, 0)
    wall_rgb = (226, 212, 180)
    roof_rgb = (162, 84, 68)
    wood_rgb = (78, 56, 40)
    floor_rgb = (150, 112, 70)
    holes = [(2, 10, 4, 12), (17, 6, 1, 11), (28, 10, 4, 12)]
    items = building(fr, 40, 30, wall_rgb, roof_rgb, wood_rgb, floor_rgb, holes,
                     name_plate="TOKO BENIH", window_panes=True)
    for zc in (-10, 10):
        items += shelf_unit(fr, -14.0, zc, "x")
    for xc in (-8, 8):
        items += shelf_unit(fr, xc, 19.0, "-z")
    items.append(fr.part("MejaEtalase", (0, 4.2, 2), (4, 0.8, 6), (150, 112, 70), M["planks"]))
    for sz in (-1, 1):
        items.append(fr.part("KakiMeja", (0, 2.6, 2 + sz * 2), (0.8, 2.4, 0.8), (78, 56, 40), M["wood"]))
    for (lx, lz) in ((-8, 0), (8, 0), (0, -10)):
        items.append(fr.part("TaliLampu", (lx, 24.3, lz), (0.3, 2.6, 0.3), (40, 40, 40), M["metal"]))
        bulb = fr.part("LampuGantung", (lx, 22.4, lz), (1.2, 1.2, 1.2), (255, 224, 160), M["neon"], "ball")
        add_point_light(bulb, (1.0, 0.88, 0.66), 0.9, 14)
        items.append(bulb)
    zona = folder("ZonaToko")
    toko_model = model("TokoBenih")
    for item in items:
        toko_model.add(item)
    zona.add(toko_model)
    zona.add(fr.part("CounterToko", (-4, 2.9, -12), (2, 3, 12), (146, 104, 62), M["planks"]))
    return zona


def fence_yard(cx, cz, yaw):
    items = []
    for sz in (-1, 1):
        base_x = cx + (10 if yaw == 0 else -10)
        z0 = cz + sz * 5
        items.append(part("PagarTiang", (base_x, 1.8, z0), (1.2, 3.6, 1.2), (130, 96, 58), M["wood"]))
        items.append(part("PagarTiang", (base_x, 1.8, z0 + sz * 6), (1.2, 3.6, 1.2), (130, 96, 58), M["wood"]))
        for y in (1.2, 2.6):
            items.append(part("PagarRel", (base_x, y, z0 + sz * 3), (0.5, 0.7, 6), (140, 104, 62), M["planks"]))
    return items


def build_village():
    items_all = []
    rng = random.Random(5)
    cottages = [
        (56, -76, 0, (222, 200, 168), (150, 88, 72)),
        (96, -68, 180, (210, 190, 158), (140, 96, 70)),
        (56, -120, 0, (230, 208, 176), (156, 92, 66)),
        (100, -124, 180, (218, 196, 162), (146, 90, 74)),
        (140, -76, 180, (224, 202, 170), (152, 86, 68)),
        (140, -120, 180, (214, 194, 160), (144, 94, 72)),
    ]
    for i, (cx, cz, yaw, wall_rgb, roof_rgb) in enumerate(cottages):
        fr = Frame(cx, cz, yaw)
        holes = [(7, 6, 1, 11)]
        holes_side = [(5, 6, 4, 12)]
        items = building(fr, 20, 16, wall_rgb, roof_rgb, (84, 60, 42), (150, 112, 70), holes, holes_side)
        rumah = model("Rumah%d" % (i + 1))
        for item in items:
            rumah.add(item)
        items_all.append(rumah)
        items_all += fence_yard(cx, cz, yaw)
        items_all += tree_at(cx + (14 if yaw == 0 else -14), cz + rng.uniform(-4, 4), rng)
    gudang_fr = Frame(120, -150, 180)
    holes = [(11, 6, 1, 11), (3, 6, 4, 12)]
    gudang = building(gudang_fr, 28, 24, (146, 104, 62), (108, 110, 114), (84, 60, 42), (140, 106, 64), holes)
    gd = model("Gudang")
    for item in gudang:
        gd.add(item)
    items_all.append(gd)
    return items_all


SEEDS = [
    (1, "Gandum", (198, 168, 88), "Serealia"), (2, "Jelai", (176, 150, 80), "Serealia"),
    (3, "Oat", (210, 186, 120), "Serealia"), (4, "Rye", (146, 124, 88), "Serealia"),
    (5, "Sorgum", (168, 96, 60), "Serealia"), (6, "Jewawut", (204, 178, 98), "Serealia"),
    (7, "Buckwheat", (120, 96, 72), "Serealia"), (8, "Kacang polong", (108, 180, 78), "Legum"),
    (9, "Kacang lentil", (198, 132, 64), "Legum"), (10, "Kacang arab", (214, 190, 140), "Legum"),
    (11, "Kacang hitam", (70, 62, 56), "Legum"), (12, "Kacang merah", (168, 64, 52), "Legum"),
    (13, "Bit", (164, 44, 96), "Sayuran"), (14, "Asparagus", (96, 150, 70), "Sayuran"),
    (15, "Seledri", (140, 190, 96), "Sayuran"), (16, "Selada", (116, 178, 84), "Sayuran"),
    (17, "Brokoli", (72, 124, 58), "Sayuran"), (18, "Kembang kol", (238, 232, 214), "Sayuran"),
    (19, "Kubis", (128, 168, 96), "Sayuran"), (20, "Paprika", (196, 44, 44), "Sayuran"),
    (21, "Mentimun", (78, 148, 72), "Sayuran"), (22, "Apel", (196, 52, 48), "Buah-buahan"),
    (23, "Pir", (188, 196, 96), "Buah-buahan"), (24, "Anggur", (124, 64, 152), "Buah-buahan"),
    (25, "Plum", (110, 54, 128), "Buah-buahan"), (26, "Aprikot", (232, 140, 72), "Buah-buahan"),
    (27, "Persik", (238, 150, 130), "Buah-buahan"), (28, "Nektarin", (212, 88, 56), "Buah-buahan"),
    (29, "Ceri", (140, 28, 36), "Buah-buahan"), (30, "Zaitun", (118, 132, 66), "Tanaman Lainnya"),
]


def display_plant(x, z, sid, warna, kategori):
    items = []
    top = 0.8
    if kategori == "Serealia":
        for ox, oz in ((-0.9, -0.4), (0.9, 0.3), (0, 0.9)):
            items.append(part("Tanaman%d" % sid, (x + ox, top + 1.6, z + oz), (0.5, 3.2, 0.5), warna, M["smooth"], "cylinder", 0, False, 0, 0, 90))
        items.append(part("Tangkai%d" % sid, (x, top + 3.5, z), (1.0, 1.0, 1.0), warna, M["smooth"], "ball", 0, False))
    elif kategori == "Legum":
        items.append(part("Tanaman%d" % sid, (x, top + 1.2, z), (0.7, 2.4, 0.7), (96, 140, 60), M["smooth"], "cylinder", 0, False, 0, 0, 90))
        for sx in (-1, 1):
            items.append(part("Polong%d" % sid, (x + sx * 1.1, top + 1.6, z), (1.0, 1.0, 1.0), warna, M["smooth"], "ball", 0, False))
    elif kategori == "Sayuran":
        items.append(part("Tanaman%d" % sid, (x, top + 0.9, z), (2.4, 2.4, 2.4), warna, M["smooth"], "ball", 0, False))
        items.append(part("Tangkai%d" % sid, (x, top + 2.3, z), (0.4, 0.9, 0.4), (96, 140, 60), M["smooth"], "cylinder", 0, False, 0, 0, 90))
    elif kategori == "Buah-buahan":
        items.append(part("Batang%d" % sid, (x, top + 1.6, z), (3.2, 0.8, 0.8), (110, 84, 58), M["wood"], "cylinder", 0, False, 0, 0, 90))
        items.append(part("Dedaunan%d" % sid, (x, top + 3.6, z), (2.8, 2.8, 2.8), (86, 140, 64), M["grass"], "ball", 0, False))
        items.append(part("Buah%d" % sid, (x + 0.9, top + 3.4, z + 0.5), (1.3, 1.3, 1.3), warna, M["smooth"], "ball", 0, False))
    else:
        items.append(part("Batang%d" % sid, (x, top + 1.3, z), (2.6, 0.7, 0.7), (110, 84, 58), M["wood"], "cylinder", 0, False, 0, 0, 90))
        for sx in (-1, 1):
            items.append(part("Buah%d" % sid, (x + sx * 0.8, top + 2.6, z), (0.9, 0.9, 0.9), warna, M["smooth"], "ball", 0, False))
    return items


def build_kebun():
    kebun = folder("KebunDemo")
    for i in range(6):
        kebun.add(part("PetakSemai%d" % (i + 1), (44, 0.45, -8 - 8 * i), (6, 0.6, 6), (88, 64, 44), M["ground"]))
    kebun.add(part("TiangPetak", (36, 3.5, -6.5), (0.8, 7, 0.8), (120, 88, 52), M["wood"]))
    board = part("PapanPetak", (36, 5.6, -6.5), (4.4, 3, 0.5), (146, 110, 70), M["planks"])
    add_text_surface(board, FACE["back"], "PETAK SEMAI", (0.16, 0.13, 0.1))
    kebun.add(board)
    rows = [(56, "Serealia"), (66, "Legum"), (76, "Sayuran"), (86, "Buah-buahan"), (96, "Tanaman Lainnya")]
    for row_x, kategori in rows:
        kebun.add(part("TiangKategori", (row_x, 3.5, -6.5), (0.8, 7, 0.8), (120, 88, 52), M["wood"]))
        board = part("PapanKategori", (row_x, 5.6, -6.5), (8, 3.4, 0.5), (146, 110, 70), M["planks"])
        add_text_surface(board, FACE["back"], kategori.upper(), (0.16, 0.13, 0.1))
        kebun.add(board)
        benih_kategori = [s for s in SEEDS if s[3] == kategori]
        for j, (sid, nama, warna, _) in enumerate(benih_kategori):
            z = -10 - 8 * j
            kebun.add(part("Bed%d" % sid, (row_x, 0.4, z), (4, 0.8, 4), (96, 72, 50), M["ground"]))
            for item in display_plant(row_x, z, sid, warna, kategori):
                kebun.add(item)
            plate = part("Plate%d" % sid, (row_x, 1.9, z + 2.15), (2.6, 1.4, 0.3), (150, 118, 74), M["planks"])
            add_text_surface(plate, FACE["back"], nama, (0.16, 0.13, 0.1))
            kebun.add(plate)
    return kebun


def build_pond():
    items = []
    items.append(part("KolamAir", (128, -0.1, 96), (36, 0.8, 26), (92, 148, 196), M["water"], "block", 0.2, False))
    items.append(part("TepiKolam1", (128, 0.15, 82.5), (40, 0.5, 3), (150, 148, 142), M["pebble"]))
    items.append(part("TepiKolam2", (128, 0.15, 109.5), (40, 0.5, 3), (150, 148, 142), M["pebble"]))
    items.append(part("TepiKolam3", (108.5, 0.15, 96), (3, 0.5, 30), (150, 148, 142), M["pebble"]))
    items.append(part("TepiKolam4", (147.5, 0.15, 96), (3, 0.5, 30), (150, 148, 142), M["pebble"]))
    items.append(part("DekatJembatan", (112, 1.4, 96), (14, 0.7, 6), (150, 112, 70), M["planks"]))
    for sz in (-1, 1):
        items.append(part("RelJembatan", (112, 2.5, 96 + sz * 3.2), (14, 1.6, 0.5), (130, 96, 58), M["wood"]))
        for sx in (-1, 1):
            items.append(part("TiangJembatan", (112 + sx * 6, 2.2, 96 + sz * 3.2), (0.6, 1.8, 0.6), (130, 96, 58), M["wood"]))
    return items


ANIMASI_KINCIR = """local pusat = script.Parent:WaitForChild("PusatBaling")
local sudut = 0
while true do
	task.wait(0.06)
	sudut += 0.04
	for i = 1, 4 do
		local baling = script.Parent:FindFirstChild("Baling" .. i)
		if baling then
			baling.CFrame = pusat.CFrame * CFrame.Angles(0, 0, sudut + (i - 1) * math.pi / 2) * CFrame.new(0, 6, 0)
		end
	end
end
"""


def build_dekorasi():
    dekor = folder("Dekorasi")
    kincir = model("KincirAngin")
    kincir.add(part("MenaraBawah", (-180, 26, -170), (14, 10, 10), (226, 212, 180), M["smooth"], "cylinder", 0, True, 0, 0, 90))
    kincir.add(part("MenaraAtas", (-180, 38, -170), (10, 7, 7), (226, 212, 180), M["smooth"], "cylinder", 0, True, 0, 0, 90))
    kincir.add(part("Kubah", (-180, 44, -170), (8, 8, 8), (162, 84, 68), M["brick"], "ball"))
    kincir.add(part("PusatBaling", (-180, 41, -165.8), (0.4, 0.4, 0.4), (255, 255, 255), M["smooth"], "block", 1, False))
    for i, phi in enumerate((0, 90, 180, 270)):
        rad = math.radians(phi)
        bx = -180 - 6 * math.sin(rad)
        by = 41 + 6 * math.cos(rad)
        kincir.add(part("Baling%d" % (i + 1), (bx, by, -165.8), (1.6, 11, 0.4), (110, 84, 58), M["wood"], "block", 0, False, 0, 0, phi))
    kincir.add(script_item("Script", "AnimasiKincir", ANIMASI_KINCIR))
    dekor.add(kincir)
    items = []
    items.append(part("BodiGerobak", (-52, 3.5, -24), (6, 2.6, 4), (140, 100, 60), M["planks"]))
    for sz in (-1, 1):
        items.append(part("RodaGerobak", (-52, 1.5, -24 + sz * 1.6), (0.8, 3, 3), (90, 66, 40), M["wood"], "cylinder", 0, True, 90))
    for sz in (-1, 1):
        items.append(part("PeganganGerobak", (-48.6, 3.2, -24 + sz), (2.4, 0.6, 0.6), (90, 66, 40), M["wood"]))
    for k, (ox, oz) in enumerate(((-1.2, -1), (1.2, 0.8), (0, 1.2))):
        items.append(part("KarungGerobak%d" % k, (-52 + ox, 5.6, -24 + oz), (2, 2, 2), (206, 180, 130), M["smooth"], "ball"))
    for item in items:
        dekor.add(item)
    items = []
    items.append(part("BadanSumur", (18, 1.5, 22), (3, 7, 7), (132, 130, 124), M["cobble"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("AirSumur", (18, 2.7, 22), (0.6, 5, 5), (92, 148, 196), M["water"], "cylinder", 0.2, False, 0, 0, 90))
    for sz in (-1, 1):
        items.append(part("TiangSumur", (18, 6.5, 22 + sz * 2.6), (0.8, 7, 0.8), (130, 96, 58), M["wood"]))
    items.append(part("AtapSumur1", (19.2, 10.5, 22), (7, 0.7, 7), (162, 84, 68), M["brick"], "block", 0, True, 0, 0, -25))
    items.append(part("AtapSumur2", (16.8, 10.5, 22), (7, 0.7, 7), (162, 84, 68), M["brick"], "block", 0, True, 0, 0, 25))
    for item in items:
        dekor.add(item)
    return dekor


def build_gates():
    gerbang_folder = folder("Gerbang")
    gates = [
        ("GerbangKampung", (-220, 0), 0, "GERBANG KAMPUNG", FACE["right"], FACE["left"], "kampung"),
        ("GerbangSabana", (0, -220), 1, "GERBANG SABANA", FACE["back"], FACE["front"], "sabana"),
        ("GerbangStepa", (220, 0), 0, "GERBANG STEPA", FACE["left"], FACE["right"], "stepa"),
        ("GerbangPerladangan", (0, 220), 1, "GERBANG PERLADANGAN", FACE["front"], FACE["back"], "perladangan"),
    ]
    for name, (gx, gz), axis, text, face_in, face_out, gaya in gates:
        parts = []
        away_x = 1 if gx > 0 else (-1 if gx < 0 else 0)
        away_z = 1 if gz > 0 else (-1 if gz < 0 else 0)
        for s in (-1, 1):
            px = gx + (s * 6.5 if axis == 0 else 0)
            pz = gz + (s * 6.5 if axis == 1 else 0)
            parts.append(part("PilarGerbang", (px, 10, pz), (3, 20, 3), (140, 138, 132), M["slate"]))
        beam_size = (17, 2.4, 3) if axis == 0 else (3, 2.4, 17)
        parts.append(part("BalokGerbang", (gx, 21.2, gz), beam_size, (120, 118, 112), M["slate"]))
        sign_size = (12, 4, 0.6) if axis == 0 else (0.6, 4, 12)
        sign = part("PapanGerbang", (gx, 16.5, gz), sign_size, (110, 78, 46), M["planks"])
        add_text_surface(sign, face_in, text, (0.96, 0.92, 0.8))
        add_text_surface(sign, face_out, text, (0.96, 0.92, 0.8))
        parts.append(sign)
        barrier_size = (2, 26, 22) if axis == 0 else (22, 26, 2)
        parts.append(part("PenghalangGerbang", (gx + away_x * 14, 13, gz + away_z * 14), barrier_size,
                          (255, 255, 255), M["smooth"], "block", 1, True))
        board_size = (6, 3, 0.5) if axis == 0 else (0.5, 3, 6)
        board = part("PapanBuka", (gx + away_x * 20, 4.2, gz + away_z * 20), board_size, (146, 110, 70), M["planks"])
        add_text_surface(board, face_in, "GERBANG AKTIF - MASUK UNTUK TELEPORT", (0.2, 0.16, 0.12))
        parts.append(board)
        for s in (-1, 1):
            if axis == 0:
                parts.append(part("TiangSegera", (gx + away_x * 20, 1.5, gz + s * 2), (0.8, 3, 0.8), (130, 96, 58), M["wood"]))
            else:
                parts.append(part("TiangSegera", (gx + s * 2, 1.5, gz + away_z * 20), (0.8, 3, 0.8), (130, 96, 58), M["wood"]))
        if gaya == "kampung":
            for s in (-1, 1):
                for k in (9.5, 15.5):
                    if axis == 0:
                        parts.append(part("PagarGerbang", (gx, 1.8, gz + s * k), (1.2, 3.6, 1.2), (130, 96, 58), M["wood"]))
                    else:
                        parts.append(part("PagarGerbang", (gx + s * k, 1.8, gz), (1.2, 3.6, 1.2), (130, 96, 58), M["wood"]))
                for y in (1.2, 2.6):
                    if axis == 0:
                        parts.append(part("RelGerbang", (gx, y, gz + s * 12.5), (0.5, 0.7, 6), (140, 104, 62), M["planks"]))
                    else:
                        parts.append(part("RelGerbang", (gx + s * 12.5, y, gz), (6, 0.7, 0.5), (140, 104, 62), M["planks"]))
        elif gaya == "sabana":
            for s in (-1, 1):
                if axis == 0:
                    parts.append(part("PasirGerbang", (gx, 0.2, gz + s * 16), (14, 0.4, 14), (214, 192, 146), M["sand"]))
                else:
                    parts.append(part("PasirGerbang", (gx + s * 16, 0.2, gz), (14, 0.4, 14), (214, 192, 146), M["sand"]))
            parts.append(part("RumputKeringGerbang", (gx + (12 if axis == 0 else 0), 0.2, gz - away_z * 12),
                              (14, 0.4, 10), (150, 144, 84), M["ground"]))
        elif gaya == "stepa":
            parts.append(part("BatuGerbang1", (gx + away_x * 8, 1.6, gz + (14 if axis == 0 else 0)),
                              (4, 3, 4), (128, 126, 120), M["slate"], "ball"))
            parts.append(part("BatuGerbang2", (gx + away_x * 8, 1.4, gz - (14 if axis == 0 else 0)) if axis == 0
                              else (gx + 14, 1.4, gz + away_z * 8), (3, 2.5, 3), (128, 126, 120), M["slate"], "ball"))
            parts.append(part("RumputJarangGerbang", (gx + (16 if axis == 0 else 0), 0.2, gz - away_z * 16 if axis == 1 else gz),
                              (12, 0.4, 10), (150, 156, 100), M["ground"]))
        else:
            for s in (-1, 1):
                if axis == 0:
                    parts.append(part("BaleGerbang", (gx + s * 14, 2, gz - away_z * 4), (6, 4, 4), (204, 178, 92), M["grass"]))
                else:
                    parts.append(part("BaleGerbang", (gx - away_x * 4, 2, gz + s * 14), (4, 4, 6), (204, 178, 92), M["grass"]))
            parts.append(part("BaleAtasGerbang", (gx + (-14 if axis == 0 else 0), 6, gz + (-4 if axis == 0 else -14)),
                              (4, 4, 4), (204, 178, 92), M["grass"]))
            parts.append(part("TanahGaruGerbang", (gx + (16 if axis == 0 else 0), 0.2, gz - away_z * 16),
                              (24, 0.4, 14), (98, 72, 48), M["ground"]))
        gerbang = model(name)
        for item in parts:
            gerbang.add(item)
        gerbang_folder.add(gerbang)
    return gerbang_folder


def build_npc():
    folder_npc = folder("NPC")
    npcs = [
        ("NPC_BuSari", (-64, -40), -90, (232, 190, 152), (188, 92, 96), (70, 74, 96), (150, 120, 80)),
        ("NPC_PakDarsa", (80, -104), 135, (226, 186, 148), (96, 120, 88), (60, 58, 54), (120, 90, 60)),
        ("NPC_Mira", (36, -16), -45, (238, 198, 160), (220, 170, 90), (90, 110, 140), (200, 150, 60)),
    ]
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


def build_lighting():
    lighting = Item("Lighting", [
        p_string("Name", "Lighting"),
        p_color3("Ambient", (0.62, 0.60, 0.52)),
        p_color3("OutdoorAmbient", (0.52, 0.50, 0.44)),
        p_float("Brightness", 2.4),
        p_float("ClockTime", 14.5),
        p_float("GeographicLatitude", 12),
        p_bool("GlobalShadows", True),
        p_token("Technology", 3),
    ])
    atmosphere = Item("Atmosphere", [
        p_string("Name", "AtmosferDataran"),
        p_float("Density", 0.3),
        p_float("Offset", 0.4),
        p_color3("Color", (0.84, 0.78, 0.62)),
        p_color3("Decay", (0.42, 0.38, 0.30)),
        p_float("Glare", 0),
        p_float("Haze", 1.4),
    ])
    lighting.add(atmosphere)
    return lighting


def build_nature():
    alam = folder("Alam")
    hills = [
        (-180, 10, -170, (140, 22, 130), 12, -10),
        (130, 7, -210, (120, 16, 100), 10, 0),
        (230, 7, -110, (100, 16, 120), 0, -12),
        (270, 6, 80, (110, 14, 110), 0, -8),
        (210, 8, 190, (120, 18, 110), 10, -8),
        (-70, 6, 245, (110, 14, 100), 10, 0),
        (-200, 9, 150, (130, 20, 130), 12, 8),
        (-255, 6, -80, (110, 14, 120), 0, 8),
    ]
    for i, (x, y, z, size, pitch, roll) in enumerate(hills):
        alam.add(part("Bukit%d" % (i + 1), (x, y, z), size, (96 + i * 3, 134 + i * 2, 62), M["grass"], "block", 0, True, 0, pitch, roll))
    rng = random.Random(7)
    excl = [
        (-10, -240, 10, 240), (-240, -10, 240, 10), (-80, -54, -16, -42),
        (0, -70, 120, -58), (98, -175, 110, -52), (-112, -80, -56, -16),
        (32, -60, 108, 2), (42, -170, 155, -58), (94, 78, 162, 120),
        (-205, -195, -155, -145), (-240, -16, -200, 16), (-16, -240, 16, -200),
        (200, -16, 240, 16), (-16, 200, 16, 240), (4, 28, 30, 52),
    ]
    for (x, y, z, size, _, _) in hills:
        excl.append((x - size[0] * 0.35, z - size[2] * 0.35, x + size[0] * 0.35, z + size[2] * 0.35))

    def bebas(x, z):
        if x * x + z * z < 34 * 34:
            return False
        for (x0, z0, x1, z1) in excl:
            if x0 <= x <= x1 and z0 <= z <= z1:
                return False
        return True

    count = 0
    while count < 48:
        x = rng.uniform(-270, 270)
        z = rng.uniform(-270, 270)
        if bebas(x, z):
            for item in tree_at(x, z, rng):
                alam.add(item)
            count += 1
    for i in range(22):
        while True:
            x = rng.uniform(-250, 250)
            z = rng.uniform(-250, 250)
            if bebas(x, z):
                break
        d = rng.uniform(2.4, 4)
        alam.add(part("Semak%d" % i, (x, d * 0.4, z), (d, d * 0.8, d), (74, 128, 60), M["grass"], "ball"))
    flower_colors = [(255, 120, 150), (255, 210, 90), (240, 240, 230), (200, 90, 200), (255, 150, 80), (150, 200, 255)]
    for i in range(60):
        while True:
            x = rng.uniform(-240, 240)
            z = rng.uniform(-240, 240)
            if bebas(x, z):
                break
        c = flower_colors[i % len(flower_colors)]
        alam.add(part("Bunga%d" % i, (x, 0.55, z), (0.9, 0.9, 0.9), c, M["smooth"], "ball", 0, False))
    rocks = [(-236, 1.6, 24, 4), (-206, 2, -30, 5), (238, 2, 30, 5), (206, 1.5, -22, 4),
             (16, 1.8, -238, 4.5), (-20, 2, 236, 4), (-150, 24, -160, 7), (-120, 23, -180, 6),
             (150, 20, -190, 6), (240, 18, 170, 7), (-180, 22, 130, 6), (110, 2, 112, 4),
             (146, 2, 84, 3.5), (60, 1.5, 130, 3.5)]
    for i, (x, y, z, d) in enumerate(rocks):
        alam.add(part("Batu%d" % (i + 1), (x, y, z), (d, d * 0.7, d), (128, 126, 120), M["slate"], "ball"))
    for item in build_pond():
        alam.add(item)
    return alam


def build_world():
    workspace = Item("Workspace", [p_string("Name", "Workspace"), p_bool("StreamingEnabled", True)])
    lanskap = folder("Lanskap")
    for item in build_ground() + build_paths():
        lanskap.add(item)
    workspace.add(lanskap)
    alun = folder("AlunAlun")
    for item in build_plaza():
        alun.add(item)
    workspace.add(alun)
    workspace.add(spawn_location("SpawnDataran", (16, 0.6, 40), (14, 1.2, 14), (108, 146, 72)))
    workspace.add(build_toko())
    permukiman = folder("Permukiman")
    for item in build_village():
        permukiman.add(item)
    workspace.add(permukiman)
    workspace.add(build_kebun())
    workspace.add(build_nature())
    workspace.add(build_dekorasi())
    workspace.add(build_gates())
    workspace.add(build_npc())
    return workspace
