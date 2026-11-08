"""Pembangun dunia Place 01 Dataran — dengan MASTERPLAN arsitektural.

Prinsip (arahan pemilik dunia, 8 Nov 2026 — "bangun sungguhan, bukan taman kanak-kanak"):
1. Penempatan terarah: poros civic timur-barat lewat alun-alun, distrik menghadap jalan
   dengan mundur seragam, tanda arah satu titik (totem), promenade tepi sungai.
2. Tidak ada objek tumpang tindih: semua penempatan melewati pemeriksaan okupansi
   (lingkaran, kotak bangunan, segmen jalan, alur sungai) sebelum part dibuat.
3. Tumbuhan terkomposisi: jajaran pohon boulevard (allee), gerombolan di bukit,
   pagar hidup, bunga di bed geometris — tanpa sebar acak.
4. Bangunan berarsitektur: plinth batu, dinding berjendela berbingkai + ambang,
   lis dinding (cornice), atap pelana + bubungan, cerobong, tangga pintu — dua lantai
   untuk rumah.
5. Papan dirancang: bingkai + atap kecil + batu pijakan, zona baca bebas.

Tanah/bukit/sungai/tebing tetap dari script runtime TerrainDunia (terrain_gen.py).
"""
import math
import random

from terrain_gen import tinggi_tanah
from rbxlx_lib import (Item, add_billboard_tag, add_point_light, add_text_surface, folder, model,
                       p_bool, p_color3, p_color3u8, p_cframe, p_float, p_int, p_string, p_token,
                       p_vec3, part, rot_matrix, script_item)

M = {
    "grass": 1280, "ground": 1360, "sand": 1296, "slate": 800, "concrete": 816,
    "cobble": 880, "brick": 848, "wood": 512, "planks": 528, "smooth": 272,
    "neon": 288, "metal": 1088, "water": 2048, "pebble": 864, "glass": 1568,
    "asphalt": 1400, "rock": 896, "granite": 832,
}
FACE = {"right": 0, "top": 1, "back": 2, "left": 3, "bottom": 4, "front": 5}

PAL = {
    "rumput": (88, 106, 62),
    "tanah": (122, 100, 72),
    "tanah_muda": (134, 112, 82),
    "pasir": (182, 168, 138),
    "batu": (122, 120, 114),
    "batu_gelap": (104, 102, 98),
    "cobble": (150, 148, 140),
    "cobble_gelap": (130, 128, 122),
    "jalan": (108, 106, 102),
    "trotoar": (146, 140, 128),
    "plester": (196, 186, 168),
    "plester_tua": (186, 174, 154),
    "atap": (118, 88, 70),
    "atap_tua": (108, 80, 64),
    "kayu": (92, 70, 50),
    "kayu_muda": (122, 98, 68),
    "papan": (134, 108, 74),
    "karung": (172, 156, 124),
    "daun": (58, 84, 48),
    "daun_muda": (70, 96, 54),
    "daun_tua": (48, 72, 42),
    "batang": (94, 74, 54),
    "air": (86, 118, 132),
    "aksen": (255, 214, 150),
    "teks_papan": (0.96, 0.93, 0.85),
    "teks_gelap": (0.18, 0.15, 0.12),
}

TAN30 = math.tan(math.radians(30))

SUNGAI = [(-470, 150), (-330, 122), (-180, 168), (-20, 196), (130, 150), (280, 186), (470, 150)]

# ---------- sistem okupansi: larang objek tumpang tindih ----------

OKUP = []   # lingkaran terpakai (x, z, r)
RECTS = []  # kotak terpakai (x0, z0, x1, z1)
ROADS = []  # segmen jalan (x0, z0, x1, z1, setengah_lebar)


def tempat(x, z, r):
    """Cadangkan lingkaran; False jika bertabrakan dengan yang sudah terpakai."""
    for (ox, oz, orr) in OKUP:
        if (x - ox) ** 2 + (z - oz) ** 2 < (r + orr) ** 2:
            return False
    OKUP.append((x, z, r))
    return True


def kena_rect(x, z, r, margin=0.0):
    for (x0, z0, x1, z1) in RECTS:
        dx = max(x0 - margin - x, 0, x - (x1 + margin))
        dz = max(z0 - margin - z, 0, z - (z1 + margin))
        if dx * dx + dz * dz < r * r:
            return True
    return False


def kena_jalan(x, z, r):
    for (x0, z0, x1, z1, half) in ROADS:
        dx, dz = x1 - x0, z1 - z0
        panj2 = dx * dx + dz * dz
        if panj2 == 0:
            continue
        t = max(0.0, min(1.0, ((x - x0) * dx + (z - z0) * dz) / panj2))
        if math.hypot(x - (x0 + t * dx), z - (z0 + t * dz)) < half + r:
            return True
    return False


def kena_sungai(x, z, r):
    for i in range(len(SUNGAI) - 1):
        x0, z0 = SUNGAI[i]
        x1, z1 = SUNGAI[i + 1]
        dx, dz = x1 - x0, z1 - z0
        panj2 = dx * dx + dz * dz
        t = max(0.0, min(1.0, ((x - x0) * dx + (z - z0) * dz) / panj2))
        if math.hypot(x - (x0 + t * dx), z - (z0 + t * dz)) < 14 + r:
            return True
    return False


def bebas(x, z, r, di_jalan=False):
    """Lolos semua larangan: padang, jalan, sungai, bangunan, objek terpakai.
    di_jalan=True untuk furnitur yang memang sengaja berdiri di atas pelataran/jalan."""
    if abs(x) > 470 or abs(z) > 470:
        return False
    if not di_jalan and (kena_jalan(x, z, r) or kena_sungai(x, z, r)):
        return False
    if kena_rect(x, z, r):
        return False
    return tempat(x, z, r)


def pilih(candidates, r):
    """Ambil kandidat pertama yang lolos; None jika semua bentrok."""
    for (x, z) in candidates:
        if bebas(x, z, r):
            return (x, z)
    return None


def pilih_di_jalan(candidates, r):
    """Sama dengan pilih, tapi untuk furnitur yang memang berdiri di pelataran/jalan."""
    for (x, z) in candidates:
        if bebas(x, z, r, di_jalan=True):
            return (x, z)
    return None


# ---------- primitif ----------

def warna_varian(rgb, rng, amplitudo=6):
    return tuple(max(0, min(255, v + rng.randint(-amplitudo, amplitudo))) for v in rgb)


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


def jalan(items, nama, x0, z0, x1, z1, lebar, warna, mat, tebal=0.5, y=0.0):
    """Jalan lurus dua titik (bisa diagonal); sekalian dicatat ke sistem okupansi."""
    panj = math.hypot(x1 - x0, z1 - z0)
    if panj < 1:
        return
    yaw = math.degrees(math.atan2(x1 - x0, z1 - z0))
    cx, cz = (x0 + x1) / 2.0, (z0 + z1) / 2.0
    p = part(nama, (cx, y, cz), (lebar, tebal, panj), warna, mat)
    p.props[8] = p_cframe("CFrame", (cx, y, cz), rot_matrix(yaw))
    items.append(p)
    ROADS.append((x0, z0, x1, z1, lebar / 2.0))


def boulevard(items, arah):
    """Boulevard 24: jalan inti 16 (cobble) + trotoar 4x2 (konkrit) tepi gerbang."""
    u0, u1 = 24, 238
    if arah == "barat":
        jalan(items, "BoulevardBarat", -u0, 0, -u1, 0, 16, PAL["jalan"], M["cobble"])
        jalan(items, "TrotoarBaratU", -u0, 10, -u1, 10, 4, PAL["trotoar"], M["concrete"], 0.7)
        jalan(items, "TrotoarBaratD", -u0, -10, -u1, -10, 4, PAL["trotoar"], M["concrete"], 0.7)
    elif arah == "timur":
        jalan(items, "BoulevardTimur", u0, 0, u1, 0, 16, PAL["jalan"], M["cobble"])
        jalan(items, "TrotoarTimurU", u0, 10, u1, 10, 4, PAL["trotoar"], M["concrete"], 0.7)
        jalan(items, "TrotoarTimurD", u0, -10, u1, -10, 4, PAL["trotoar"], M["concrete"], 0.7)
    elif arah == "utara":
        jalan(items, "BoulevardUtara", 0, -u0, 0, -u1, 16, PAL["jalan"], M["cobble"])
        jalan(items, "TrotoarUtaraT", 10, -u0, 10, -u1, 4, PAL["trotoar"], M["concrete"], 0.7)
        jalan(items, "TrotoarUtaraB", -10, -u0, -10, -u1, 4, PAL["trotoar"], M["concrete"], 0.7)
    else:
        jalan(items, "BoulevardSelatanA", 0, u0, 0, 172, 16, PAL["jalan"], M["cobble"])
        jalan(items, "TrotoarSelatanAT", 10, u0, 10, 172, 4, PAL["trotoar"], M["concrete"], 0.7)
        jalan(items, "TrotoarSelatanAB", -10, u0, -10, 172, 4, PAL["trotoar"], M["concrete"], 0.7)
        jalan(items, "BoulevardSelatanB", 0, 208, 0, u1, 16, PAL["jalan"], M["cobble"])
        jalan(items, "TrotoarSelatanBT", 10, 208, 10, u1, 4, PAL["trotoar"], M["concrete"], 0.7)
        jalan(items, "TrotoarSelatanBB", -10, 208, -10, u1, 4, PAL["trotoar"], M["concrete"], 0.7)


def build_jalan():
    items = []
    for arah in ("barat", "timur", "utara", "selatan"):
        boulevard(items, arah)
    jalan(items, "SumbuBarat", -24, 0, -9, 0, 16, PAL["cobble"], M["cobble"])
    jalan(items, "SumbuTimur", 9, 0, 24, 0, 16, PAL["cobble"], M["cobble"])
    jalan(items, "JalanToko", -30, -18, -58, -46, 8, PAL["tanah"], M["ground"])
    jalan(items, "JalanKebun", 30, -10, 52, -6, 8, PAL["tanah"], M["ground"])
    jalan(items, "JalanDesaA", 21, -22, 52, -62, 10, PAL["tanah"], M["ground"])
    jalan(items, "JalanDesaB", 52, -62, 112, -62, 14, PAL["tanah"], M["ground"])
    jalan(items, "JalanSungai", 18.4, 22, 57, 155, 14, PAL["tanah"], M["ground"])
    jalan(items, "LokalGudang", 112, -62, 138, -50, 6, PAL["tanah_muda"], M["ground"])
    return items


def build_jembatan():
    items = []
    items.append(part("DekJembatan", (0, 0.9, 190), (24, 1.2, 36), PAL["kayu_muda"], M["planks"]))
    for sx in (-1, 1):
        items.append(part("RelJembatan", (sx * 11.4, 2.7, 190), (1.6, 0.8, 36), PAL["kayu"], M["wood"]))
        for sz in (174, 190, 206):
            items.append(part("TiangRelJembatan", (sx * 11.4, 1.6, sz), (0.9, 2.2, 0.9), PAL["kayu"], M["wood"]))
    for sx in (-1, 1):
        for sz in (177, 203):
            items.append(part("PilarJembatan", (sx * 9, -1, sz), (2.4, 12, 2.4), PAL["batu_gelap"], M["slate"]))
    tempat(0, 190, 17)
    return items


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


def _pos_bukaan(along, fixed, off, y, luar=0.0):
    if along == "z":
        return (fixed + luar, y, off)
    return (off, y, fixed - luar)


def _ukur_bukaan(along, w, h):
    if along == "z":
        return (0.3, h, w)
    return (w, h, 0.3)


def _isi_bukaan(frame, along, fixed, start, holes):
    """Pintu (daun + pijakan batu) dan jendela (kaca + ambang + sekat kayu) per bukaan."""
    items = []
    for (s, w, y0, y1) in holes:
        off = start + s + w / 2.0
        if y0 <= 1.5:
            items.append(frame.part("DaunPintu", _pos_bukaan(along, fixed, off, (y0 + y1) / 2.0),
                                    _ukur_bukaan(along, w - 0.7, y1 - y0 - 0.4), PAL["kayu"], M["planks"]))
            items.append(frame.part("Pijakan", _pos_bukaan(along, fixed, off, 0.45, luar=1.4),
                                    _ukur_bukaan(along, w + 1.2, 0.9), PAL["batu"], M["slate"]))
        else:
            items.append(frame.part("KacaJendela", _pos_bukaan(along, fixed, off, (y0 + y1) / 2.0),
                                    _ukur_bukaan(along, w - 0.5, y1 - y0 - 0.5), (150, 170, 178), M["glass"], "block", 0, False))
            items.append(frame.part("AmbangJendela", _pos_bukaan(along, fixed, off, y0 - 0.25, luar=0.75),
                                    _ukur_bukaan(along, w + 0.6, 0.5), PAL["plester_tua"], M["smooth"]))
    return items


def building(frame, width_z, depth_x, dinding, atap, kayu, lantai_rgb,
             holes_front, holes_side=None, name_plate=None,
             dua_lantai=False, cerobong=False, etalase=False):
    """Bangunan berarsitektur: plinth batu, dinding berbukaan berkaca, lis dinding,
    atap pelana 30 derajat + bubungan, pintu berdaun + pijakan, cerobong."""
    items = []
    items.append(frame.part("Plinth", (0, 0.75, 0), (depth_x + 0.6, 1.5, width_z + 0.6), PAL["batu"], M["slate"]))
    items.append(frame.part("Lantai", (0, 1.75, 0), (depth_x - 2, 0.4, width_z - 2), lantai_rgb, M["planks"]))
    if dua_lantai:
        items.append(frame.part("LantaiDua", (0, 10.6, 0), (depth_x - 2, 0.5, width_z - 2), lantai_rgb, M["planks"]))
    front_x = depth_x / 2.0 - 0.5
    back_x = -depth_x / 2.0 + 0.5
    items += wall_with_holes(frame, "DindingDepan", "z", front_x, -width_z / 2.0, width_z, 1, 21, holes_front, dinding, M["smooth"])
    items += _isi_bukaan(frame, "z", front_x, -width_z / 2.0, holes_front)
    items.append(frame.part("DindingBelakang", (back_x, 11, 0), (1, 20, width_z), dinding, M["smooth"]))
    if holes_side is None:
        items.append(frame.part("DindingKiri", (0, 11, width_z / 2.0 - 0.5), (depth_x, 20, 1), dinding, M["smooth"]))
        items.append(frame.part("DindingKanan", (0, 11, -width_z / 2.0 + 0.5), (depth_x, 20, 1), dinding, M["smooth"]))
    else:
        items += wall_with_holes(frame, "DindingSamping", "x", width_z / 2.0 - 0.5, -depth_x / 2.0, depth_x, 1, 21, holes_side, dinding, M["smooth"])
        items += _isi_bukaan(frame, "x", width_z / 2.0 - 0.5, -depth_x / 2.0, holes_side)
        items += wall_with_holes(frame, "DindingSamping", "x", -width_z / 2.0 + 0.5, -depth_x / 2.0, depth_x, 1, 21, holes_side, dinding, M["smooth"])
        items += _isi_bukaan(frame, "x", -width_z / 2.0 + 0.5, -depth_x / 2.0, holes_side)
    for sx in (-1, 1):
        for sz in (-1, 1):
            items.append(frame.part("PilasterSudut", (sx * (depth_x / 2.0 - 1), 11, sz * (width_z / 2.0 - 1)),
                                    (2, 20, 2), kayu, M["wood"]))
    for (cx_local, cz_local, sx_len, sz_len) in (
            (0, width_z / 2.0 - 0.1, depth_x + 0.8, 1.0),
            (0, -width_z / 2.0 + 0.1, depth_x + 0.8, 1.0),
            (depth_x / 2.0 - 0.1, 0, 1.0, width_z + 0.8),
            (-depth_x / 2.0 + 0.1, 0, 1.0, width_z + 0.8)):
        items.append(frame.part("LisDinding", (cx_local, 20.4, cz_local), (sx_len, 0.8, sz_len), PAL["plester_tua"], M["smooth"]))
    run = depth_x / 2.0 + 3
    rise = run * TAN30
    ridge_y = 21 + rise
    slab_len = 2 * math.ceil(math.sqrt(run * run + rise * rise) / 2)
    slab_w = width_z + 6
    for sx in (-1, 1):
        cx_local = sx * (run / 2.0 - 0.25)
        cy_local = (21 + ridge_y) / 2.0 - 0.433
        items.append(frame.part("Atap", (cx_local, cy_local, 0), (slab_len, 1, slab_w), atap, M["brick"], lroll=-30 * sx))
    rise_w = (depth_x / 2.0) * TAN30
    for sx in (-1, 1):
        for sz in (-1, 1):
            items.append(frame.part("Bubungan", (sx * depth_x / 4.0, 21 + rise_w / 2.0, sz * (width_z / 2.0 - 0.5)),
                                    (1, rise_w, depth_x / 2.0), dinding, M["smooth"], lyaw=-90 * sx))
    items.append(frame.part("PuncakAtap", (0, ridge_y + 0.35, 0), (1.2, 0.9, width_z + 2), PAL["atap_tua"], M["brick"]))
    if cerobong:
        items.append(frame.part("Cerobong", (-depth_x / 4.0, 24.5, -width_z / 4.0), (2.4, 7, 2.4), PAL["atap"], M["brick"]))
        items.append(frame.part("TopiCerobong", (-depth_x / 4.0, 28.4, -width_z / 4.0), (3.2, 0.7, 3.2), PAL["batu"], M["slate"]))
    if name_plate:
        plate = frame.part("PapanNama", (depth_x / 2.0 + 0.35, 14, 0), (0.5, 4, 16), kayu, M["planks"])
        add_text_surface(plate, FACE["right"], name_plate, PAL["teks_papan"])
        items.append(plate)
        items.append(frame.part("Kanopi", (depth_x / 2.0 + 2, 16.4, 0), (4, 0.8, width_z + 4), atap, M["brick"]))
        for sz in (-1, 1):
            items.append(frame.part("TiangKanopi", (depth_x / 2.0 + 3, 8, sz * (width_z / 2.0 - 6)), (2, 16, 2), kayu, M["wood"]))
    if etalase:
        items.append(frame.part("MejaEtalase", (0, 4.4, 2), (4, 0.8, 6), PAL["kayu_muda"], M["planks"]))
        for sz in (-1, 1):
            items.append(frame.part("KakiMeja", (0, 2.6, 2 + sz * 2), (0.8, 2.4, 0.8), kayu, M["wood"]))
    return items


def pohon(x, z, rng):
    """Satu gaya pohon: batang silinder + tajuk dua bola hijau redup, di atas terrain."""
    items = []
    tinggi = tinggi_tanah("Dataran", x, z)
    h = rng.uniform(7, 11)
    d = rng.uniform(1.6, 2.2)
    items.append(part("BatangPohon", (x, tinggi + h / 2.0, z), (h, d, d), PAL["batang"], M["wood"], "cylinder", 0, True, 0, 0, 90))
    greens = [PAL["daun"], PAL["daun_muda"], PAL["daun_tua"]]
    g = greens[rng.randrange(len(greens))]
    d1 = rng.uniform(5, 7.4)
    items.append(part("Dedaunan", (x, tinggi + h + d1 * 0.18, z), (d1, d1 * 0.85, d1), g, M["grass"], "ball"))
    if rng.random() < 0.6:
        d2 = rng.uniform(3.6, 5)
        items.append(part("DedaunanAtas", (x + rng.uniform(-1.4, 1.4), tinggi + h + d1 * 0.18 + d2 * 0.36, z + rng.uniform(-1.4, 1.4)),
                          (d2, d2 * 0.85, d2), warna_varian(g, rng, 4), M["grass"], "ball"))
    return items


# ---------- tanda/sistem papan dirancang ----------

def papan_tanda(items, x, z, yaw, teks, lebar=9, tinggi=4.2, face=FACE["front"], nama="PapanTanda"):
    """Papan dirancang: dua tiang di belakang, balok caping, atap dua bidang, pijakan batu."""
    fr = Frame(x, z, yaw)
    for sx in (-1, 1):
        px = sx * (lebar / 2.0 - 0.6)
        items.append(fr.part(nama + "Tiang", (px, tinggi / 2.0 + 1.5, -0.8), (0.9, tinggi + 4, 0.9), PAL["kayu"], M["wood"]))
        items.append(fr.part(nama + "Pijakan", (px, 0.6, -0.8), (1.7, 1.2, 1.7), PAL["batu"], M["slate"]))
    items.append(fr.part(nama + "Caping", (0, tinggi + tinggi / 2.0 + 0.9, -0.8), (lebar + 1.6, 0.8, 1.0), PAL["kayu_muda"], M["planks"]))
    for s in (-1, 1):
        items.append(fr.part(nama + "Atap", (0, tinggi + tinggi / 2.0 + 1.9, -0.8 + s * 0.55),
                             (0.7, lebar + 2.2, 2.0), PAL["atap"], M["brick"], lroll=-24 * s))
    board = fr.part(nama, (0, tinggi, 0), (lebar, tinggi, 0.6), PAL["papan"], M["planks"])
    add_text_surface(board, face, teks, PAL["teks_gelap"])
    items.append(board)


def bench_at(x, z, yaw):
    fr = Frame(x, z, yaw)
    items = []
    items.append(fr.part("DudukanBangku", (0, 1.9, 0), (4, 0.8, 2), PAL["kayu_muda"], M["planks"]))
    items.append(fr.part("SandaranBangku", (0, 2.8, 1.05), (4, 1.8, 0.6), PAL["kayu_muda"], M["planks"]))
    for sx in (-1, 1):
        items.append(fr.part("KakiBangku", (sx * 1.4, 0.9, 0), (0.8, 1.2, 1.6), PAL["kayu"], M["wood"]))
    return items


def lampu_at(x, z):
    items = []
    items.append(part("TiangLampu", (x, 5.0, z), (10, 0.9, 0.9), (66, 64, 62), M["metal"], "cylinder", 0, True, 0, 0, 90))
    head = part("KepalaLampu", (x, 10.3, z), (1.8, 1.8, 1.8), PAL["aksen"], M["neon"], "ball")
    add_point_light(head, (1.0, 0.85, 0.6), 1.3, 20)
    items.append(head)
    return items


def bunga_at(x, z, warna):
    return part("Bunga", (x, tinggi_tanah("Dataran", x, z) + 0.35, z), (0.8, 0.8, 0.8), warna, M["smooth"], "ball", 0, False)


def arah_ke_sungai(px, pz):
    terbaik = None
    for i in range(len(SUNGAI) - 1):
        x0, z0 = SUNGAI[i]
        x1, z1 = SUNGAI[i + 1]
        dx, dz = x1 - x0, z1 - z0
        panj2 = dx * dx + dz * dz
        t = max(0.0, min(1.0, ((px - x0) * dx + (pz - z0) * dz) / panj2))
        qx, qz = x0 + t * dx, z0 + t * dz
        d = math.hypot(px - qx, pz - qz)
        if terbaik is None or d < terbaik[0]:
            terbaik = (d, qx, qz)
    if terbaik is None:
        return 0.0
    _, qx, qz = terbaik
    dx, dz = qx - px, qz - pz
    panj = math.hypot(dx, dz) or 1.0
    return math.degrees(math.atan2(-dx / panj, -dz / panj))


# ---------- alun-alun ----------

def build_padang():
    """Padang civic formal — prinsip dari dataran-dataran kota dunia (padang hijau
    persegi dikepung tepi terbangun, satu sumbu, landmark menara di tepi, ritme
    struktur berulang yang menembus cahaya). Bentuk 100% original, tanpa bendera
    dan tanpa simbol negara apa pun."""
    items = []
    RECTS.append((-30, -22, 30, 22))
    items.append(part("PadangBaratS", (-21, 0.0, -15), (18, 0.6, 14), PAL["rumput"], M["grass"]))
    items.append(part("PadangBaratU", (-21, 0.0, 15), (18, 0.6, 14), PAL["rumput"], M["grass"]))
    items.append(part("PadangTimurS", (21, 0.0, -15), (18, 0.6, 14), PAL["rumput"], M["grass"]))
    items.append(part("PadangTimurU", (21, 0.0, 15), (18, 0.6, 14), PAL["rumput"], M["grass"]))
    items.append(part("PadangTengahS", (0, 0.0, -15), (24, 0.6, 14), PAL["rumput"], M["grass"]))
    items.append(part("PadangTengahU", (0, 0.0, 15), (24, 0.6, 14), PAL["rumput"], M["grass"]))
    kolom = [(-30, -12), (-30, 12), (-30, 16.75), (-30, 21.5),
             (30, -21.5), (30, -17), (30, 12), (30, 16.75), (30, 21.5)]
    for (kx, kz) in kolom:
        if tempat(kx, kz, 1.2):
            items.append(part("KolomPadang", (kx, 3.4, kz), (1.2, 6.8, 1.2), PAL["batu"], M["slate"]))
    for (lx, lz, ll) in ((-30, 16.75, 10.5), (30, 16.75, 10.5), (30, -19.25, 5.5)):
        items.append(part("LintelPadang", (lx, 7.4, lz), (0.9, 1.2, ll + 1), PAL["kayu_muda"], M["planks"]))
    items.append(part("PagarHidupUtara", (0, 1.1, -22), (60, 2.2, 1.2), PAL["daun_tua"], M["grass"]))
    items.append(part("PagarHidupSelatan", (-9.5, 1.1, 22), (41, 2.2, 1.2), PAL["daun_tua"], M["grass"]))
    RECTS.append((-30, -22.6, 30, -21.4))
    RECTS.append((-30, 21.4, 11, 22.6))
    items.append(part("MancurBak", (0, 1.9, 0), (2.6, 18, 18), PAL["batu"], M["slate"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("MancurAir", (0, 2.0, 0), (2.0, 14.6, 14.6), PAL["air"], M["water"], "cylinder", 0.25, False, 0, 0, 90))
    items.append(part("MancurTiang", (0, 5.2, 0), (4.4, 2.2, 2.2), PAL["batu"], M["slate"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("MancurMangkuk", (0, 7.6, 0), (0.9, 5.2, 5.2), PAL["batu"], M["slate"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("MancurBola", (0, 8.8, 0), (1.8, 1.8, 1.8), PAL["batu"], M["granite"], "ball"))
    tempat(0, 0, 10)
    putih = (230, 228, 222)
    for i in (45, 90, 135, 225, 270, 315):
        rad = math.radians(i)
        rx, rz = 14 * math.cos(rad), 14 * math.sin(rad)
        if tempat(rx, rz, 1.3):
            items.append(part("RusukPaviliun", (rx, 6.5, rz), (1.1, 13, 0.9), putih, M["smooth"], "block", 0, True, i))
    for i in (67.5, 112.5, 157.5, 202.5, 247.5, 292.5):
        rad = math.radians(i)
        rx, rz = 14 * math.cos(rad), 14 * math.sin(rad)
        if tempat(rx, rz, 1.2):
            items.append(part("CincinPaviliun", (rx, 13.6, rz), (12, 0.6, 0.9), putih, M["smooth"], "block", 0, True, i + 90))
    fr = Frame(-20, -30, 180)
    items.append(fr.part("PijakanMenara", (0, 0.6, 0), (6, 1.2, 6), PAL["batu"], M["slate"]))
    items.append(fr.part("DasarMenara", (0, 3.5, 0), (4.5, 5, 4.5), PAL["batu_gelap"], M["slate"]))
    items.append(fr.part("BatangMenara", (0, 15, 0), (3, 18, 3), PAL["plester"], M["smooth"]))
    jam = fr.part("KotakJam", (0, 20, 0), (3.8, 3.2, 3.8), PAL["batu_gelap"], M["slate"])
    add_text_surface(jam, FACE["front"], "MENARA\nDATARAN", PAL["teks_papan"])
    add_text_surface(jam, FACE["back"], "PADANG\nCIVIC", PAL["teks_papan"])
    items.append(jam)
    items.append(fr.part("LisMenara", (0, 24.4, 0), (3.6, 0.8, 3.6), PAL["plester_tua"], M["smooth"]))
    items.append(fr.part("AtapMenara1", (0, 25.9, 0), (5.4, 1, 4.2), PAL["atap"], M["brick"], "block", 0, True, 0, 30))
    items.append(fr.part("AtapMenara2", (0, 25.9, 0), (4.2, 1, 5.4), PAL["atap"], M["brick"], "block", 0, True, 90, 30))
    items.append(fr.part("PuncakMenara", (0, 28.6, 0), (1.4, 1.4, 1.4), PAL["batu"], M["granite"], "ball"))
    tempat(-20, -30, 5)
    papan = []
    papan_tanda(papan, -24, -14, 270,
                "PAPAN INFORMASI PADANG DATARAN\nPadang civic terbuka di pusat Dataran.\nToko Benih lewat gerbang barat - Kebun Demonstrasi lewat gerbang timur.\nDusun di timur laut; pasar dusun, kebun buah, dan panggung di timur.\nTaman Mandala di barat laut; Danau Tenang di barat daya.\nGerbang kawasan: Kampung, Sabana, Stepa, Perladangan.",
                lebar=14, tinggi=4.5, nama="PapanInfo")
    for item in papan:
        items.append(item)
    tempat(-24, -14, 4)
    for a in (35, 75, 105, 145, 215, 325):
        rad = math.radians(a)
        bx, bz = 19 * math.cos(rad), 19 * math.sin(rad)
        if tempat(bx, bz, 2.5):
            items += bench_at(bx, bz, 90 - a)
    for a in (30, 150, 210, 330):
        rad = math.radians(a)
        lx, lz = 21 * math.cos(rad), 21 * math.sin(rad)
        if tempat(lx, lz, 1.5):
            items += lampu_at(lx, lz)
    bunga_k = [(206, 194, 160), (196, 182, 148), (178, 182, 198), (188, 170, 130)]
    nomor = 0
    for (cx, cz) in ((-26, -18), (26, -18), (-26, 18), (26, 18)):
        for (ox, oz) in ((1.5, 0), (-1.5, 0), (0, -1.5)):
            fx, fz = cx + ox, cz + oz
            if tempat(fx, fz, 0.8):
                items.append(bunga_at(fx, fz, bunga_k[nomor % 4]))
            nomor += 1
    return items


def build_totem():
    """Totem penunjuk: satu tiang, empat papan arah menghadap gerbangnya."""
    items = []
    tx, tz = 2, 34
    items.append(part("TotemTiang", (tx, 4.5, tz), (9, 1.0, 1.0), PAL["kayu"], M["wood"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("TotemPijakan", (tx, 0.6, tz), (2.6, 2.0, 2.6), PAL["batu"], M["slate"]))
    targets = [("KAMPUNG", -220, 0), ("SABANA", 0, -220), ("STEPA", 220, 0), ("PERLADANGAN", 0, 220)]
    dx_r, dz_r = 1, 1
    for i, (teks, gx, gz) in enumerate(targets):
        ddx, ddz = gx - tx, gz - tz
        panj = math.hypot(ddx, ddz)
        yaw = math.degrees(math.atan2(-ddz / panj, ddx / panj))
        yaw_rad = math.radians(yaw)
        nx, nz = math.sin(yaw_rad), math.cos(yaw_rad)
        dot = nx * dx_r + nz * dz_r
        face = FACE["front"] if dot < 0 else FACE["back"]
        y = 4.6 + i * 1.6
        board = part("TotemArah" + teks, (tx, y, tz), (8, 1.6, 0.4), PAL["papan"], M["planks"], "block", 0, False, yaw)
        add_text_surface(board, face, teks + "  >>" if face == FACE["back"] else "<<  " + teks, PAL["teks_gelap"])
        items.append(board)
    items.append(part("TotemMahkota", (tx, 10.3, tz), (2.0, 2.0, 2.0), PAL["batu"], M["granite"], "ball"))
    tempat(tx, tz, 4.5)
    return items


# ---------- toko benih + halaman depan ----------

def shelf_unit(fr, wall_coord, center, facing):
    items = []
    bag_colors = [PAL["karung"], (158, 142, 112), (148, 132, 104)]
    levels = (3.0, 5.4, 7.8)
    if facing == "x":
        items.append(fr.part("RakBelakang", (wall_coord + 0.3, 5.4, center), (0.6, 8, 8), PAL["kayu"], M["wood"]))
        for idx, level in enumerate(levels):
            items.append(fr.part("RakPapan", (wall_coord + 1.3, level, center), (2, 0.6, 8), PAL["kayu_muda"], M["planks"]))
            items.append(fr.part("KarungBenih", (wall_coord + 1.3, level + 1.2, center - 2 + idx * 2),
                                 (1.4, 1.8, 1.4), bag_colors[idx], M["smooth"]))
        for sz in (-1, 1):
            items.append(fr.part("RakSisi", (wall_coord + 1.3, 5.4, center + sz * 3.7), (2, 8, 0.6), PAL["kayu"], M["wood"]))
    else:
        items.append(fr.part("RakBelakang", (center, 5.4, wall_coord - 0.3), (8, 8, 0.6), PAL["kayu"], M["wood"]))
        for idx, level in enumerate(levels):
            items.append(fr.part("RakPapan", (center, level, wall_coord - 1.3), (8, 0.6, 2), PAL["kayu_muda"], M["planks"]))
            items.append(fr.part("KarungBenih", (center - 2 + idx * 2, level + 1.2, wall_coord - 1.3),
                                 (1.4, 1.8, 1.4), bag_colors[(idx + 1) % 3], M["smooth"]))
        for sx in (-1, 1):
            items.append(fr.part("RakSisi", (center + sx * 3.7, 5.4, wall_coord - 1.3), (0.6, 8, 2), PAL["kayu"], M["wood"]))
    return items


def build_toko():
    fr = Frame(-84, -48, 0)
    items = building(fr, 40, 30, PAL["plester"], PAL["atap"], PAL["kayu"], (150, 132, 104),
                     [(2, 12, 2, 9), (17, 6, 1, 11), (28, 12, 2, 9)], [(5, 6, 4, 12)],
                     name_plate="TOKO BENIH", cerobong=True, etalase=True)
    for zc in (-10, 10):
        items += shelf_unit(fr, -14.0, zc, "x")
    for xc in (-8, 8):
        items += shelf_unit(fr, xc, 19.0, "-z")
    for (lx, lz) in ((-8, 0), (8, 0), (0, -10)):
        items.append(fr.part("TaliLampu", (lx, 24.3, lz), (0.3, 2.6, 0.3), (50, 48, 46), M["metal"]))
        bulb = fr.part("LampuGantung", (lx, 22.4, lz), (1.2, 1.2, 1.2), PAL["aksen"], M["neon"], "ball")
        add_point_light(bulb, (1.0, 0.88, 0.66), 0.9, 14)
        items.append(bulb)
    zona = folder("ZonaToko")
    toko_model = model("TokoBenih")
    for item in items:
        toko_model.add(item)
    zona.add(toko_model)
    zona.add(fr.part("CounterToko", (-4, 2.9, -12), (2, 3, 12), PAL["kayu_muda"], M["planks"]))

    halaman = []
    halaman.append(part("PelataranToko", (-61, 0.0, -48), (18, 0.6, 16), PAL["cobble"], M["cobble"]))
    RECTS.append((-70, -56, -52, -40))
    for bz in (-55.5, -40.5):
        halaman.append(part("BedBungaToko", (-61, 0.3, bz), (10, 0.5, 3), (104, 82, 58), M["ground"]))
        RECTS.append((-66, bz - 1.5, -56, bz + 1.5))
        bunga_k = [(206, 194, 160), (196, 182, 148), (178, 182, 198), (188, 170, 130)]
        for i, fx in enumerate((-65, -62.3, -59.6, -57)):
            if tempat(fx, bz, 0.8):
                halaman.append(bunga_at(fx, bz, bunga_k[i % 4]))
    for (lx, lz) in ((-53, -54), (-67, -42)):
        if tempat(lx, lz, 1.5):
            halaman += lampu_at(lx, lz)
    if tempat(-63, -53, 2.5):
        halaman += bench_at(-63, -53, 0)
    for item in halaman:
        zona.add(item)
    return zona


# ---------- dusun (permukiman) ----------

RUMAH_HOLES_DEPAN = [(1.5, 4.5, 4, 10), (7, 6, 1, 10), (14, 4.5, 4, 10),
                     (3, 4.5, 13, 19), (12.5, 4.5, 13, 19)]
RUMAH_HOLES_SAMPING = [(5.5, 5, 4, 10)]


def pagar_taman(items, hx, zf, pintu_x):
    """Pagar taman depan dengan celah gerbang di depan pintu rumah."""
    for px in (hx - 9, hx - 6, hx + 6, hx + 9):
        items.append(part("PagarTiang", (px, 1.8, zf), (1.0, 3.6, 1.0), PAL["kayu"], M["wood"]))
        tempat(px, zf, 1.0)
    for (a, b) in ((hx - 9, hx - 3.5), (hx + 3.5, hx + 9)):
        panj = b - a
        cx = (a + b) / 2.0
        for y in (1.2, 2.6):
            items.append(part("PagarRel", (cx, y, zf), (panj, 0.6, 0.5), PAL["kayu_muda"], M["planks"]))


def build_village():
    rng = random.Random(5)
    items_all = []
    rumah_utara = [66, 94, 122]
    rumah_selatan = [80, 108, 136]
    for hx in rumah_utara:
        fr = Frame(hx, -82, 270)
        dinding = warna_varian(PAL["plester"], rng, 7)
        atap = warna_varian(PAL["atap"], rng, 6)
        rumah = model("Rumah%d" % hx)
        for item in building(fr, 20, 16, dinding, atap, PAL["kayu"], (150, 132, 104),
                             RUMAH_HOLES_DEPAN, RUMAH_HOLES_SAMPING, dua_lantai=True, cerobong=True):
            rumah.add(item)
        items_all.append(rumah)
        RECTS.append((hx - 10, -90, hx + 10, -74))
        pagar_taman(items_all, hx, -71, hx)
        bunga_k = [(206, 194, 160), (196, 182, 148), (178, 182, 198), (188, 170, 130)]
        for i, fx in enumerate((hx - 3, hx + 3)):
            if tempat(fx, -72.5, 0.8):
                items_all.append(bunga_at(fx, -72.5, bunga_k[i % 4]))
        lokasi = pilih([(hx, -96), (hx + 4, -98), (hx - 4, -98)], 3.2)
        if lokasi:
            items_all += pohon(lokasi[0], lokasi[1], rng)
    for hx in rumah_selatan:
        fr = Frame(hx, -38, 90)
        dinding = warna_varian(PAL["plester_tua"], rng, 7)
        atap = warna_varian(PAL["atap_tua"], rng, 6)
        rumah = model("Rumah%d" % hx)
        for item in building(fr, 20, 16, dinding, atap, PAL["kayu"], (150, 132, 104),
                             RUMAH_HOLES_DEPAN, RUMAH_HOLES_SAMPING, dua_lantai=True, cerobong=True):
            rumah.add(item)
        items_all.append(rumah)
        RECTS.append((hx - 10, -46, hx + 10, -30))
        pagar_taman(items_all, hx, -53, hx)
        bunga_k = [(206, 194, 160), (196, 182, 148), (178, 182, 198), (188, 170, 130)]
        for i, fx in enumerate((hx - 3, hx + 3)):
            if tempat(fx, -49.5, 0.8):
                items_all.append(bunga_at(fx, -49.5, bunga_k[i % 4]))
        lokasi = pilih([(hx, -22), (hx - 4, -20), (hx + 4, -20)], 3.2)
        if lokasi:
            items_all += pohon(lokasi[0], lokasi[1], rng)
    gudang_fr = Frame(140, -38, 90)
    holes = [(3, 6, 4, 12), (11, 7, 1, 12), (22, 6, 4, 12)]
    gd = model("Gudang")
    for item in building(gudang_fr, 28, 24, (150, 128, 98), PAL["atap_tua"], PAL["kayu"], (140, 122, 96),
                         holes, cerobong=True):
        gd.add(item)
    items_all.append(gd)
    RECTS.append((126, -52, 154, -24))
    pagar_taman(items_all, 140, -53, 140)
    if tempat(120, -46, 5):
        items_all.append(part("BadanSumur", (120, 1.5, -46), (3, 7, 7), PAL["cobble_gelap"], M["cobble"], "cylinder", 0, True, 0, 0, 90))
        items_all.append(part("AirSumur", (120, 2.7, -46), (0.6, 5, 5), PAL["air"], M["water"], "cylinder", 0.2, False, 0, 0, 90))
        for sz in (-1, 1):
            items_all.append(part("TiangSumur", (120, 6.5, -46 + sz * 2.6), (0.8, 7, 0.8), PAL["kayu"], M["wood"]))
        items_all.append(part("AtapSumur1", (121.2, 10.5, -46), (7, 0.7, 7), PAL["atap"], M["brick"], "block", 0, True, 0, 0, -25))
        items_all.append(part("AtapSumur2", (118.8, 10.5, -46), (7, 0.7, 7), PAL["atap"], M["brick"], "block", 0, True, 0, 0, 25))
    return items_all


# ---------- kebun demonstrasi ----------

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
        items.append(part("Batang%d" % sid, (x, top + 1.6, z), (3.2, 0.8, 0.8), PAL["batang"], M["wood"], "cylinder", 0, False, 0, 0, 90))
        items.append(part("Dedaunan%d" % sid, (x, top + 3.6, z), (2.8, 2.8, 2.8), PAL["daun"], M["grass"], "ball", 0, False))
        items.append(part("Buah%d" % sid, (x + 0.9, top + 3.4, z + 0.5), (1.3, 1.3, 1.3), warna, M["smooth"], "ball", 0, False))
    else:
        items.append(part("Batang%d" % sid, (x, top + 1.3, z), (2.6, 0.7, 0.7), PAL["batang"], M["wood"], "cylinder", 0, False, 0, 0, 90))
        for sx in (-1, 1):
            items.append(part("Buah%d" % sid, (x + sx * 0.8, top + 2.6, z), (0.9, 0.9, 0.9), warna, M["smooth"], "ball", 0, False))
    return items


def build_kebun():
    kebun = folder("KebunDemo")
    for i in range(6):
        kebun.add(part("PetakSemai%d" % (i + 1), (106, 0.45, -18 - 7 * i), (6, 0.6, 6), (96, 74, 52), M["ground"]))
        tempat(106, -18 - 7 * i, 3.5)
    rows = [(60, "Serealia"), (70, "Legum"), (80, "Sayuran"), (90, "Buah-buahan"), (100, "Tanaman Lainnya")]
    for row_x, kategori in rows:
        kebun.add(part("TiangKategori", (row_x, 3.5, -6.5), (0.8, 7, 0.8), PAL["kayu"], M["wood"]))
        board = part("PapanKategori", (row_x, 5.6, -6.5), (8, 3.4, 0.5), PAL["papan"], M["planks"])
        add_text_surface(board, FACE["back"], kategori.upper(), PAL["teks_gelap"])
        kebun.add(board)
        tempat(row_x, -6.5, 1.2)
        benih_kategori = [s for s in SEEDS if s[3] == kategori]
        for j, (sid, nama, warna, _) in enumerate(benih_kategori):
            z = -10 - 8 * j
            kebun.add(part("Bed%d" % sid, (row_x, 0.4, z), (4, 0.8, 4), (104, 82, 58), M["ground"]))
            tempat(row_x, z, 2.5)
            for item in display_plant(row_x, z, sid, warna, kategori):
                kebun.add(item)
            plate = part("Plate%d" % sid, (row_x, 1.9, z + 2.15), (2.6, 1.4, 0.3), PAL["papan"], M["planks"])
            add_text_surface(plate, FACE["back"], nama, PAL["teks_gelap"])
            kebun.add(plate)
    gerbang_kebun = []
    for pz in (3.5, -14.5):
        gerbang_kebun.append(part("TiangGerbangKebun", (52, 4.5, pz), (0.9, 9, 0.9), PAL["kayu"], M["wood"], "cylinder", 0, True, 0, 0, 90))
        gerbang_kebun.append(part("KakiGerbangKebun", (52, 0.6, pz), (1.8, 1.2, 1.8), PAL["batu"], M["slate"]))
        tempat(52, pz, 1.2)
    gerbang_kebun.append(part("BalokGerbangKebun", (52, 8.6, -5.5), (1.2, 1.0, 19), PAL["kayu_muda"], M["planks"]))
    for s in (-1, 1):
        gerbang_kebun.append(part("AtapGerbangKebun", (52 - s * 0.5, 9.6, -5.5), (1.6, 0.6, 20), PAL["atap"], M["brick"], "block", 0, True, 0, 0, 22 * s))
    papan = part("PapanGerbangKebun", (52, 6.6, -5.5), (0.6, 2.6, 13), PAL["papan"], M["planks"])
    add_text_surface(papan, FACE["left"], "KEBUN DEMONSTRASI", PAL["teks_gelap"])
    gerbang_kebun.append(papan)
    for item in gerbang_kebun:
        kebun.add(item)
    papan_petak = []
    papan_tanda(papan_petak, 36, 6, 180, "PETAK SEMAI\nTanam benih di petak, tunggu sebentar,\nlalu panen hasilnya.", lebar=9, tinggi=4.2, nama="PapanPetak")
    for item in papan_petak:
        kebun.add(item)
    tempat(36, 6, 5)
    return kebun


# ---------- promenade tepi sungai ----------

PROMENADE = [
    (-177.2, 152.2, -17.2, 180.2),
    (14, 168.85, 125.3, 134.72),
    (133.7, 134.45, 283.7, 170.4),
]
PAD_PROMENADE = [(-177.2, 152.2), (-17.2, 180.2), (129.5, 134.6), (283.7, 170.4), (57, 155.4)]


def build_riverside():
    items = []
    for i, (x0, z0, x1, z1) in enumerate(PROMENADE):
        jalan(items, "Promenade%d" % (i + 1), x0, z0, x1, z1, 6, PAL["tanah_muda"], M["ground"])
    for i, (px, pz) in enumerate(PAD_PROMENADE):
        items.append(part("PadPromenade%d" % (i + 1), (px, 0.25, pz), (0.6, 6, 6), PAL["tanah_muda"], M["ground"], "cylinder", 0, True, 0, 0, 90))
    for i in (1, 2, 3):
        px, pz = PAD_PROMENADE[i]
        yaw = arah_ke_sungai(px, pz)
        lokasi = pilih_di_jalan([(px, pz), (px + 1.5, pz - 1.5), (px - 1.5, pz + 1.5)], 2.5)
        if lokasi:
            items += bench_at(lokasi[0], lokasi[1], yaw)
    for i in (0, 2, 4):
        px, pz = PAD_PROMENADE[i]
        lokasi = pilih_di_jalan([(px, pz), (px + 1.5, pz + 1.5), (px - 1.5, pz - 1.5)], 1.5)
        if lokasi:
            items += lampu_at(lokasi[0], lokasi[1])
    bunga_k = [(206, 194, 160), (196, 182, 148), (178, 182, 198), (188, 170, 130), (204, 196, 168), (182, 176, 142)]
    for i in (0, 3):
        px, pz = PAD_PROMENADE[i]
        for k in range(4):
            a = math.radians(k * 60 + 30)
            fx, fz = px + 4.6 * math.cos(a), pz + 4.6 * math.sin(a)
            if bebas(fx, fz, 0.8, di_jalan=True):
                items.append(bunga_at(fx, fz, bunga_k[k % 6]))
    rng = random.Random(11)
    kandidat_pohon = [
        PAD_PROMENADE[0], PAD_PROMENADE[1], PAD_PROMENADE[2], PAD_PROMENADE[3], PAD_PROMENADE[4],
        (-130, 165), (-80, 172), (40, 160), (90, 148), (180, 146), (240, 158),
    ]
    for (cx, cz) in kandidat_pohon:
        lokasi = pilih([(cx + 5, cz + 5), (cx - 5, cz - 5), (cx + 5, cz - 5), (cx, cz + 6), (cx, cz)], 3.2)
        if lokasi:
            items += pohon(lokasi[0], lokasi[1], rng)
    return items


def build_dermaga():
    items = []
    yaw = math.degrees(math.atan2(0.292, 0.953))
    cx, cz = 59.4, 169.6
    deck = part("DekDermaga", (cx, 0.8, cz), (6, 0.8, 14), PAL["kayu_muda"], M["planks"])
    deck.props[8] = p_cframe("CFrame", (cx, 0.8, cz), rot_matrix(yaw))
    items.append(deck)
    for sx in (-1, 1):
        rx = cx + math.cos(math.radians(yaw)) * sx * 2.7
        rz = cz - math.sin(math.radians(yaw)) * sx * 2.7
        rel = part("RelDermaga", (rx, 2.0, rz), (1.2, 0.6, 14), PAL["kayu"], M["wood"])
        rel.props[8] = p_cframe("CFrame", (rx, 2.0, rz), rot_matrix(yaw))
        items.append(rel)
    for (dx, dz) in ((-2.4, -5.5), (2.4, -5.5), (-2.4, 5.5), (2.4, 5.5)):
        px = cx + math.sin(math.radians(yaw)) * dx + math.cos(math.radians(yaw)) * dz
        pz = cz + math.cos(math.radians(yaw)) * dx - math.sin(math.radians(yaw)) * dz
        items.append(part("TiangDermaga", (px, -1.5, pz), (1.0, 8, 1.0), PAL["kayu"], M["wood"]))
    tempat(cx, cz, 9)
    return items


# ---------- tata hijau terarah: allee boulevard + gerombolan bukit ----------

GEROMBOLAN = [(280, -220, 80), (320, 100, 75), (-340, 60, 70), (200, 330, 80)]


def build_tata_hijau():
    items = []
    rng = random.Random(7)
    for arah in ("barat", "timur", "utara", "selatan"):
        for u in range(30, 214, 44):
            if arah == "barat":
                kandidat = [(-u, 16), (-u, -16)]
            elif arah == "timur":
                kandidat = [(u, 16), (u, -16)]
            elif arah == "utara":
                kandidat = [(16, -u), (-16, -u)]
            else:
                kandidat = [(16, u), (-16, u)]
            for (x, z) in kandidat:
                if bebas(x, z, 3.2):
                    items += pohon(x, z, rng)
    for (gx, gz, gr) in GEROMBOLAN:
        for k in range(3):
            a = math.radians(k * 90 + 45)
            radius = min(gr * 0.5, 30)
            x, z = gx + radius * math.cos(a), gz + radius * math.sin(a)
            if bebas(x, z, 3.2):
                items += pohon(x, z, rng)
    return items


# ---------- dekorasi ----------

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
    wx, wz = -320, -180
    basis = tinggi_tanah("Dataran", wx, wz)
    kincir.add(part("MenaraBawah", (wx, basis + 26, wz), (14, 10, 10), PAL["plester"], M["smooth"], "cylinder", 0, True, 0, 0, 90))
    kincir.add(part("MenaraAtas", (wx, basis + 38, wz), (10, 7, 7), PAL["plester_tua"], M["smooth"], "cylinder", 0, True, 0, 0, 90))
    kincir.add(part("Kubah", (wx, basis + 44, wz), (8, 8, 8), PAL["atap"], M["brick"], "ball"))
    kincir.add(part("PusatBaling", (wx, basis + 41, wz - 4.2), (0.4, 0.4, 0.4), (255, 255, 255), M["smooth"], "block", 1, False))
    for i, phi in enumerate((0, 90, 180, 270)):
        rad = math.radians(phi)
        bx = wx - 6 * math.sin(rad)
        by = basis + 41 + 6 * math.cos(rad)
        kincir.add(part("Baling%d" % (i + 1), (bx, by, wz - 4.2), (1.6, 11, 0.4), PAL["kayu"], M["wood"], "block", 0, False, 0, 0, phi))
    kincir.add(script_item("Script", "AnimasiKincir", ANIMASI_KINCIR))
    dekor.add(kincir)
    tempat(wx, wz, 14)
    if tempat(-56, -30, 4):
        dekor.add(part("BodiGerobak", (-56, 3.5, -30), (6, 2.6, 4), PAL["kayu_muda"], M["planks"]))
        for sz in (-1, 1):
            dekor.add(part("RodaGerobak", (-56, 1.5, -30 + sz * 1.6), (0.8, 3, 3), PAL["kayu"], M["wood"], "cylinder", 0, True, 90))
        for sz in (-1, 1):
            dekor.add(part("PeganganGerobak", (-52.6, 3.2, -30 + sz), (2.4, 0.6, 0.6), PAL["kayu"], M["wood"]))
        for k, (ox, oz) in enumerate(((-1.2, -1), (1.2, 0.8), (0, 1.2))):
            dekor.add(part("KarungGerobak%d" % k, (-56 + ox, 5.6, -30 + oz), (2, 2, 2), PAL["karung"], M["smooth"], "ball"))
    return dekor


# ---------- gerbang seragam ----------

def build_gates():
    gerbang_folder = folder("Gerbang")
    gates = [
        ("GerbangKampung", (-220, 0), 0, "GERBANG KAMPUNG", FACE["right"], FACE["left"]),
        ("GerbangSabana", (0, -220), 1, "GERBANG SABANA", FACE["back"], FACE["front"]),
        ("GerbangStepa", (220, 0), 0, "GERBANG STEPA", FACE["left"], FACE["right"]),
        ("GerbangPerladangan", (0, 220), 1, "GERBANG PERLADANGAN", FACE["front"], FACE["back"]),
    ]
    for name, (gx, gz), axis, text, face_in, face_out in gates:
        parts = []
        for s in (-1, 1):
            px = gx + (s * 6.5 if axis == 0 else 0)
            pz = gz + (s * 6.5 if axis == 1 else 0)
            parts.append(part("PilarGerbang", (px, 10, pz), (3, 20, 3), PAL["batu"], M["slate"]))
        beam_size = (17, 2.4, 3) if axis == 0 else (3, 2.4, 17)
        parts.append(part("BalokGerbang", (gx, 21.2, gz), beam_size, PAL["batu_gelap"], M["slate"]))
        sign_size = (12, 4, 0.6) if axis == 0 else (0.6, 4, 12)
        sign = part("PapanGerbang", (gx, 12.5, gz), sign_size, PAL["papan"], M["planks"])
        add_text_surface(sign, face_in, text, PAL["teks_papan"])
        add_text_surface(sign, face_out, text, PAL["teks_papan"])
        parts.append(sign)
        barrier_size = (2, 26, 22) if axis == 0 else (22, 26, 2)
        parts.append(part("PenghalangGerbang", (gx, 13, gz), barrier_size,
                          (255, 255, 255), M["smooth"], "block", 1, True))
        gerbang = model(name)
        for item in parts:
            gerbang.add(item)
        gerbang_folder.add(gerbang)
        tempat(gx, gz, 15)
    return gerbang_folder


# ---------- NPC ----------

def build_npc():
    folder_npc = folder("NPC")
    npcs = [
        ("NPC_BuSari", [(-46, -50), (-50, -46), (-42, -54)], -90, (226, 190, 156), (110, 118, 96), (70, 68, 62), (150, 120, 80)),
        ("NPC_PakDarsa", [(70, -62), (60, -62), (78, -62)], 135, (220, 186, 152), (96, 116, 88), (60, 58, 54), (120, 90, 60)),
        ("NPC_Mira", [(40, -8), (44, -7), (36, -9)], -45, (232, 198, 164), (178, 148, 92), (90, 100, 124), (188, 150, 66)),
    ]
    for name, kandidat, yaw, skin, shirt, pants, hat in npcs:
        lokasi = pilih_di_jalan(kandidat, 4)
        if not lokasi:
            continue
        x, z = lokasi
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


# ---------- pencahayaan & kedatangan ----------

def build_lighting():
    lighting = Item("Lighting", [
        p_string("Name", "Lighting"),
        p_color3("Ambient", (0.56, 0.55, 0.50)),
        p_color3("OutdoorAmbient", (0.50, 0.49, 0.45)),
        p_float("Brightness", 2.2),
        p_float("ClockTime", 14.5),
        p_float("GeographicLatitude", 12),
        p_bool("GlobalShadows", True),
        p_token("Technology", 3),
    ])
    atmosphere = Item("Atmosphere", [
        p_string("Name", "AtmosferDataran"),
        p_float("Density", 0.42),
        p_float("Offset", 0.25),
        p_color3("Color", (0.82, 0.78, 0.70)),
        p_color3("Decay", (0.42, 0.40, 0.36)),
        p_float("Glare", 0.03),
        p_float("Haze", 2.0),
    ])
    lighting.add(atmosphere)
    return lighting


def build_spawn(items_lanskap):
    items_lanskap.append(part("PelataranDatang", (16, 0.0, 40), (18, 0.6, 18), PAL["cobble"], M["cobble"]))
    RECTS.append((7, 31, 25, 49))
    for (lx, lz) in ((10, 34), (12, 46)):
        if tempat(lx, lz, 1.5):
            items_lanskap += lampu_at(lx, lz)


def build_world():
    workspace = Item("Workspace", [p_string("Name", "Workspace"), p_bool("StreamingEnabled", True)])
    lanskap_items = []
    lanskap_items += build_jalan()
    lanskap_items += build_jembatan()
    build_spawn(lanskap_items)
    for item in build_riverside():
        lanskap_items.append(item)
    lanskap = folder("Lanskap")
    for item in lanskap_items:
        lanskap.add(item)
    workspace.add(lanskap)
    alun = folder("PadangDataran")
    for item in build_padang():
        alun.add(item)
    workspace.add(alun)
    workspace.add(spawn_location("SpawnDataran", (16, 0.3, 40), (14, 0.6, 14), (128, 146, 104)))
    for item in build_totem():
        workspace.add(item)
    workspace.add(build_toko())
    permukiman = folder("Permukiman")
    for item in build_village():
        permukiman.add(item)
    workspace.add(permukiman)
    workspace.add(build_kebun())
    gerbang = build_gates()
    alam = folder("Alam")
    for item in build_dermaga() + build_tata_hijau():
        alam.add(item)
    workspace.add(alam)
    workspace.add(build_dekorasi())
    from world_dataran_v4 import build_semua_tambahan
    pengayaan = folder("PengayaanV4")
    for m in build_semua_tambahan():
        pengayaan.add(m)
    workspace.add(pengayaan)
    workspace.add(gerbang)
    workspace.add(build_npc())
    return workspace


