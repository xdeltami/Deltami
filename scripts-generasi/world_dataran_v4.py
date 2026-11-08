"""Pengayaan Dataran v4 "Dataran Hidup" (arahan pemilik 8 Nov 2026):
mengisi lahan kosong dengan kawasan kehidupan yang menenangkan —
taman mandala, pasar dusun, danau tenang, panggung selatan, kebun buah,
jalur pohon antar-gerbang, dan detail kenyamanan.
Semua lolos sistem okupansi world_dataran; satu palet dan satu gaya.
"""
import math
import random

from terrain_gen import tinggi_tanah
from rbxlx_lib import add_point_light, add_text_surface, model, part, p_cframe, rot_matrix
from world_dataran import (FACE, Frame, M, PAL, RECTS, bench_at, bunga_at, jalan, lampu_at,
                           papan_tanda, pohon, tempat, warna_varian, bebas, pilih, pilih_di_jalan)

BUNGA_TAMAN = [(206, 194, 160), (196, 182, 148), (178, 182, 198), (188, 170, 130),
               (204, 196, 168), (182, 176, 142)]
BUNTING = [(196, 120, 96), (206, 178, 110), (128, 152, 116), (122, 138, 168), (198, 160, 140)]


def bed_bunga(items, cx, cz, r, tinggi=0.5):
    items.append(part("BedMandala", (cx, tinggi / 2.0, cz), (tinggi, r * 2, r * 2),
                      (104, 82, 58), M["ground"], "cylinder", 0, True, 0, 0, 90))
    RECTS.append((cx - r, cz - r, cx + r, cz + r))
    for k in range(8):
        a = math.radians(k * 45 + 22.5)
        fx, fz = cx + (r - 1.6) * math.cos(a), cz + (r - 1.6) * math.sin(a)
        if bebas(fx, fz, 0.8, di_jalan=True):
            items.append(bunga_at(fx, fz, BUNGA_TAMAN[(k + int(cx)) % 6]))


def build_taman_mandala():
    """Taman geometris barat-laut: titik pusat matahari, empat bed kelopak,
    cincin pagar hidup bergerbang, bangku diagonal, lampu kebun."""
    taman = model("TamanMandala")
    cx, cz = -140, -120
    items = []
    jalan(items, "JalanTaman", -96, 0, -134, -100, 8, PAL["tanah"], M["ground"])
    items.append(part("RingTaman", (cx, 0.06, cz), (0.3, 42, 42), PAL["tanah_muda"], M["ground"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("TiangeInti", (cx, 3.5, cz), (1.6, 7, 1.6), PAL["batu"], M["slate"]))
    gnomon = part("Gnomon", (cx + 1.1, 6.4, cz), (3.6, 0.5, 0.9), PAL["kayu"], M["wood"], "block", 0, False, 0, 0, -32)
    items.append(gnomon)
    tempat(cx, cz, 4.5)
    for (bx, bz) in ((cx - 11, cz), (cx + 11, cz), (cx, cz - 11), (cx, cz + 11)):
        bed_bunga(items, bx, bz, 4.6)
        tempat(bx, bz, 4.8)
    for k in range(12):
        if k % 3 == 0:
            continue
        a = math.radians(k * 30)
        hx, hz = cx + 17.5 * math.cos(a), cz + 17.5 * math.sin(a)
        items.append(part("PagarHidupMandala", (hx, 1.0, hz), (1.3, 2.0, 5.6), PAL["daun_tua"], M["grass"], "block", 0, True, math.degrees(a) + 90))
        tempat(hx, hz, 2.6)
    for (ax, az, yaw) in ((cx, cz + 22.5, 0), (cx, cz - 22.5, 180)):
        items.append(part("TiangGerbangTaman", (ax - 3.2, 3.5, az), (1.0, 7, 1.0), PAL["kayu"], M["wood"], "cylinder", 0, True, 0, 0, 90))
        items.append(part("TiangGerbangTaman", (ax + 3.2, 3.5, az), (1.0, 7, 1.0), PAL["kayu"], M["wood"], "cylinder", 0, True, 0, 0, 90))
        items.append(part("BalokGerbangTaman", (ax, 7.4, az), (8.2, 1.0, 1.4), PAL["kayu_muda"], M["planks"]))
        tempat(ax, az, 3.4)
    for k in range(4):
        a = math.radians(45 + k * 90)
        bx, bz = cx + 21.5 * math.cos(a), cz + 21.5 * math.sin(a)
        if tempat(bx, bz, 2.5):
            items += bench_at(bx, bz, 90 - (45 + k * 90))
    for k in range(2):
        a = math.radians(15 + k * 150)
        lx, lz = cx + 19 * math.cos(a), cz + 19 * math.sin(a)
        if tempat(lx, lz, 1.5):
            items += lampu_at(lx, lz)
    for item in items:
        taman.add(item)
    return taman


def _stall(fr, name, warna_awning):
    s = []
    for sx in (-1, 1):
        for sz in (-1, 1):
            s.append(fr.part(name + "Tiang", (sx * 4.6, 3.5, sz * 2.6), (0.8, 7, 0.8), PAL["kayu"], M["wood"]))
    s.append(fr.part(name + "Counter", (0, 2.3, 1.6), (10, 2.6, 2), PAL["kayu_muda"], M["planks"]))
    s.append(fr.part(name + "MejaBawah", (0, 1.0, 1.6), (9.4, 1, 1.6), PAL["kayu"], M["wood"]))
    s.append(fr.part(name + "Awning", (0, 8.1, 0.2), (11, 0.6, 7.4), warna_awning, M["brick"], "block", 0, True, 0, -18))
    s.append(fr.part(name + "AwningLis", (0, 7.3, 3.6), (11, 0.5, 0.7), PAL["plester"], M["smooth"]))
    s.append(fr.part(name + "RakBelakang", (0, 5.4, -2.3), (9, 6.8, 0.7), PAL["kayu"], M["wood"]))
    for k in range(3):
        s.append(fr.part(name + "Karung%d" % k, (-3 + k * 3, 9.4, -2.2), (1.8, 2.2, 1.8), PAL["karung"], M["smooth"], "ball"))
    lentera = fr.part(name + "Lentera", (0, 6.6, 0.4), (1.1, 1.1, 1.1), PAL["aksen"], M["neon"], "ball")
    add_point_light(lentera, (1.0, 0.86, 0.62), 0.9, 14)
    s.append(lentera)
    return s


def build_pasar():
    """Pasar Dusun timur: dua deret kios beratap mengapit jalan desa,
    gapura masuk, peti dagangan antar kios."""
    pasar = model("PasarDusun")
    jalan_items = []
    jalan(jalan_items, "JalanPasar", 112, -62, 188, -62, 14, PAL["tanah"], M["ground"])
    for item in jalan_items:
        pasar.add(item)
    warna = [(150, 108, 88), (108, 128, 108), (128, 120, 148), (150, 108, 88), (108, 128, 108), (128, 120, 148)]
    posisi = [(186, -76), (212, -76), (238, -76), (186, -48), (212, -48), (238, -48)]
    for i, (sx, sz) in enumerate(posisi):
        fr = Frame(sx, sz, 180 if sz < -60 else 0)
        stall = model("Kios%d" % (i + 1))
        for item in _stall(fr, "Kios", warna[i]):
            stall.add(item)
        pasar.add(stall)
        RECTS.append((sx - 6, sz - 4, sx + 6, sz + 4))
        tempat(sx, sz, 6)
    for (px, pz) in ((199, -76), (225, -76), (199, -48), (225, -48)):
        if bebas(px, pz, 1.2):
            pasar.add(part("PetiDagangan", (px, 1.4, pz), (2.6, 2, 2.6), PAL["kayu_muda"], M["planks"]))
            pasar.add(part("TutupPeti", (px, 2.6, pz), (2.8, 0.4, 2.8), PAL["kayu"], M["wood"]))
            tempat(px, pz, 1.8)
    gapura = []
    for sz in (-70, -54):
        gapura.append(part("TiangGapuraPasar", (166, 4.5, sz), (1.2, 9, 1.2), PAL["kayu"], M["wood"]))
        tempat(166, sz, 1.6)
    gapura.append(part("BalokGapuraPasar", (166, 9.6, -62), (1.6, 1.2, 18), PAL["kayu_muda"], M["planks"]))
    papan = part("PapanGapuraPasar", (166, 8.2, -62), (0.5, 2.6, 13), PAL["papan"], M["planks"])
    add_text_surface(papan, FACE["left"], "PASAR DUSUN", PAL["teks_gelap"])
    gapura.append(papan)
    for item in gapura:
        pasar.add(item)
    for (lx, lz) in ((199, -56), (225, -68)):
        if tempat(lx, lz, 1.5):
            for item in lampu_at(lx, lz):
                pasar.add(item)
    papan2 = []
    papan_tanda(papan2, 199, -34, 0, "PASAR DUSUN\nKios petani dan pengrajin Dusun Dataran.\nBuka sepanjang hari.", lebar=10, tinggi=4.2, nama="PapanPasar")
    for item in papan2:
        pasar.add(item)
    tempat(199, -34, 4.5)
    return pasar


def build_danau():
    """Danau Tenang barat-daya: bak batu besar, dermaga papan kecil, wadah teratai,
    pergola tepi danau, bangku menghadap air."""
    danau = model("DanauTenang")
    items = []
    jalan(items, "JalanTepiBaratDaya", 10, 216, -168, 200, 8, PAL["tanah"], M["ground"])
    jalan(items, "JalanDanau", -172, 202, -198, 246, 8, PAL["tanah"], M["ground"])
    cx, cz = -200, 262
    items.append(part("BakDanau", (cx, 0.8, cz), (1.6, 27, 27), PAL["batu"], M["slate"], "cylinder", 0, True, 0, 0, 90))
    items.append(part("AirDanau", (cx, 1.1, cz), (1.1, 23.6, 23.6), PAL["air"], M["water"], "cylinder", 0.18, False, 0, 0, 90))
    for item in items:
        danau.add(item)
    items = []
    for k, (ox, oz) in enumerate(((-5, -3), (4, 5), (6, -4), (-3, 6))):
        items.append(part("Teratai%d" % k, (cx + ox, 1.75, cz + oz), (0.3, 2.6, 2.6), (96, 148, 92), M["grass"], "cylinder", 0, False, 0, 0, 90))
        items.append(part("BungaTeratai%d" % k, (cx + ox, 2.0, cz + oz), (0.7, 0.7, 0.7), (232, 220, 214), M["smooth"], "ball", 0, False))
    tempat(cx, cz, 14)
    for k in range(5):
        a = math.radians(95 + k * 43)
        rx, rz = cx + 16.2 * math.cos(a), cz + 16.2 * math.sin(a)
        h = rng_danau().uniform(2.4, 3.8)
        items.append(part("RumputTepi%d" % k, (rx, h / 2.0, rz), (h, 0.4, 0.4), (88, 118, 70), M["smooth"], "cylinder", 0, False, 0, 0, 90))
    for item in items:
        danau.add(item)
    items = []
    dek = []
    dek.append(part("DekDanau", (cx + 20, 0.55, cz - 8), (10, 1.1, 14), PAL["kayu_muda"], M["planks"]))
    RECTS.append((cx + 15, cz - 15, cx + 25, cz - 1))
    tempat(cx + 20, cz - 8, 7)
    for sz in (-13.5, -2.5):
        dek.append(part("TiangDekDanau", (cx + 24.4, 1.4, cz + sz), (0.8, 1.6, 0.8), PAL["kayu"], M["wood"]))
    dek.append(part("RelDekDanau", (cx + 24.4, 2.2, cz - 8), (0.5, 0.5, 14), PAL["kayu"], M["wood"]))
    for item in dek:
        danau.add(item)
    gazebo = model("PergolaDanau")
    gx, gz = cx + 20, cz + 14
    for sx in (-1, 1):
        for sz in (-1, 1):
            gazebo.add(part("TiangPergola", (gx + sx * 3.2, 3.6, gz + sz * 3.2), (0.9, 7.2, 0.9), PAL["kayu"], M["wood"]))
    gazebo.add(part("BingkaiPergola", (gx, 7.4, gz), (8.4, 0.7, 8.4), PAL["kayu_muda"], M["planks"]))
    for k in range(5):
        gazebo.add(part("KasauPergola%d" % k, (gx, 7.9, gz - 3.2 + k * 1.6), (9, 0.4, 0.7), PAL["kayu"], M["wood"]))
    daun = warna_varian(PAL["daun"], rng_danau(), 5)
    gazebo.add(part("MerambatPergola", (gx - 3.2, 6.6, gz + 3.2), (2.2, 2.2, 2.2), daun, M["grass"], "ball", 0, False))
    for item in gazebo.children:
        danau.add(item)
    RECTS.append((gx - 5, gz - 5, gx + 5, gz + 5))
    tempat(gx, gz, 5.5)
    for (bx, bz, yaw) in ((cx - 18, cz - 4, -90), (cx + 4, cz + 19, 12)):
        if tempat(bx, bz, 2.5):
            for item in bench_at(bx, bz, yaw):
                danau.add(item)
    if tempat(cx - 2, cz - 22, 1.5):
        for item in lampu_at(cx - 2, cz - 22):
            danau.add(item)
    papan3 = []
    papan_tanda(papan3, cx - 14, cz - 26, 20, "DANAU TENANG\nTempat duduk, rebahan, dan memandang air.\nSunyi dipelihara di sini.", lebar=10, tinggi=4.2, nama="PapanDanau")
    for item in papan3:
        danau.add(item)
    tempat(cx - 14, cz - 26, 4.5)
    return danau


_rng_danau = random.Random(9)


def rng_danau():
    return _rng_danau


def build_panggung():
    """Panggung Selatan: pelataran bundar batu, panggung kayu berkanopi,
    busur bangku penonton, tiang umbul, lampu pelataran."""
    panggung = model("PanggungDataran")
    items = []
    jalan(items, "JalanPanggung", 14, 230, 220, 236, 10, PAL["tanah"], M["ground"])
    cx, cz = 248, 236
    items.append(part("PelataranPanggung", (cx, 0.3, cz), (0.6, 30, 30), PAL["cobble"], M["cobble"], "cylinder", 0, True, 0, 0, 90))
    for item in items:
        panggung.add(item)
    items = []
    stage = model("Pentas")
    sx, sz = cx, cz - 9
    stage.add(part("DekPanggung", (sx, 1.5, sz), (18, 1.6, 8), PAL["kayu_muda"], M["planks"]))
    stage.add(part("DindingBelakangPanggung", (sx, 5.2, sz - 3.6), (18, 6.4, 0.9), PAL["plester_tua"], M["smooth"]))
    for sxx in (-1, 1):
        stage.add(part("TiangKanopiPanggung", (sx + sxx * 8.2, 5.4, sz + 3), (0.9, 8, 0.9), PAL["kayu"], M["wood"]))
    stage.add(part("KanopiPanggung", (sx, 9.8, sz), (20, 0.7, 10), PAL["atap"], M["brick"], "block", 0, True, 0, -14))
    for sxx in (-1, 1):
        stage.add(part("TanggaPanggung", (sx + sxx * 10.4, 0.7, sz), (2.4, 1.4, 6), PAL["batu"], M["slate"]))
    panggung.add(stage)
    RECTS.append((sx - 11, sz - 5, sx + 11, sz + 5))
    tempat(sx, sz, 11)
    for k in range(6):
        a = math.radians(40 + k * 52)
        bx, bz = cx + 20.5 * math.cos(a), cz + 20.5 * math.sin(a)
        if tempat(bx, bz, 2.5):
            yaw = math.degrees(math.atan2(bx - cx, bz - cz))
            for item in bench_at(bx, bz, yaw):
                panggung.add(item)
    for k in range(4):
        a = math.radians(30 + k * 100)
        px, pz = cx + 16.5 * math.cos(a), cz + 16.5 * math.sin(a)
        if tempat(px, pz, 1.2):
            panggung.add(part("TiangUmbulPanggung%d" % k, (px, 4.5, pz), (9, 0.8, 0.8), PAL["kayu"], M["wood"], "cylinder", 0, True, 0, 0, 90))
            for f in range(4):
                fx = px - 3 + f * 2
                panggung.add(part("Umbul%d" % f, (fx, 7.6 + (f % 2) * 0.3, pz), (0.5, 1.0, 0.12), BUNTING[(k + f) % 5], M["smooth"], "block", 0, False))
    for k in range(2):
        a = math.radians(120 + k * 120)
        lx, lz = cx + 23 * math.cos(a), cz + 23 * math.sin(a)
        if tempat(lx, lz, 1.5):
            for item in lampu_at(lx, lz):
                panggung.add(item)
    papan4 = []
    papan_tanda(papan4, cx - 20, cz + 8, 160, "PANGGUNG DATARAN\nPentas seni, pengumuman dusun,\ndan malam bercerita.", lebar=10, tinggi=4.2, nama="PapanPanggung")
    for item in papan4:
        panggung.add(item)
    tempat(cx - 20, cz + 8, 4.5)
    return panggung


def build_kebun_buah():
    """Kebun Buah timur-laut: barisan pohon berbuah berpagar batu rendah,
    gubuk penjaga, peti panen, papan nama."""
    kebun = model("KebunBuah")
    items = []
    rng = random.Random(23)
    jalan(items, "JalanKebunBuah", 214, -72, 202, -128, 8, PAL["tanah"], M["ground"])
    ox, oz = 214, -172
    for (wx0, wz0, wx1, wz1) in ((ox - 34, oz - 32, ox + 34, oz - 32), (ox - 34, oz + 32, ox + 34, oz + 32)):
        panj = wx1 - wx0
        items.append(part("PagarBatuKebunBuah", ((wx0 + wx1) / 2.0, 0.9, wz0), (panj, 1.8, 1.2), PAL["batu"], M["slate"]))
    for (wx, wz, panj) in ((ox - 34, oz - 20, 24), (ox - 34, oz + 20, 24), (ox + 34, oz, 64)):
        if wx == ox - 34:
            items.append(part("PagarBatuKebunBuah", (wx, 0.9, wz - 12), (1.2, 1.8, panj), PAL["batu"], M["slate"]))
            items.append(part("PagarBatuKebunBuah", (wx, 0.9, wz + 12), (1.2, 1.8, panj), PAL["batu"], M["slate"]))
        else:
            items.append(part("PagarBatuKebunBuah", (wx, 0.9, wz), (1.2, 1.8, panj), PAL["batu"], M["slate"]))
    RECTS.append((ox - 36, oz - 34, ox + 36, oz + 34))
    tempat(ox, oz - 24, 5)
    n = 0
    for rx in (ox - 24, ox, ox + 24):
        for rz in (oz - 20, oz + 2, oz + 20):
            n += 1
            if n % 4 == 0:
                continue
            if bebas(rx, rz, 3.2):
                items += pohon(rx, rz, rng)
                if bebas(rx + 2.2, rz + 2.2, 0.8, di_jalan=True):
                    items.append(bunga_at(rx + 2.2, rz + 2.2, BUNGA_TAMAN[n % 6]))
    gubuk = model("GubukKebun")
    gx, gz = ox + 26, oz - 26
    gubuk.add(part("LantaiGubuk", (gx, 0.4, gz), (8, 0.8, 8), (140, 122, 96), M["planks"]))
    gubuk.add(part("DindingGubukB", (gx, 3.4, gz - 3.8), (8, 6, 0.8), PAL["plester_tua"], M["smooth"]))
    for sxx in (-1, 1):
        gubuk.add(part("DindingGubukS", (gx + sxx * 3.8, 3.4, gz), (0.8, 6, 8), PAL["plester_tua"], M["smooth"]))
    gubuk.add(part("DindingGubukD1", (gx - 2.6, 3.4, gz + 3.8), (2.8, 6, 0.8), PAL["plester_tua"], M["smooth"]))
    gubuk.add(part("DindingGubukD2", (gx + 2.6, 3.4, gz + 3.8), (2.8, 6, 0.8), PAL["plester_tua"], M["smooth"]))
    gubuk.add(part("DindingGubukD3", (gx, 5.9, gz + 3.8), (2.4, 1, 0.8), PAL["plester_tua"], M["smooth"]))
    rise = 4.4 * math.tan(math.radians(30))
    for sxx in (-1, 1):
        gubuk.add(part("AtapGubuk", (gx + sxx * 2.3, 7.4 + rise / 2.0 - 0.4, gz), (5.2, 0.6, 9.6), PAL["atap"], M["brick"], "block", 0, True, 0, 0, -30 * sxx))
    gubuk.add(part("PuncakGubuk", (gx, 7.4 + rise, gz), (0.9, 0.7, 9.8), PAL["atap_tua"], M["brick"]))
    for item in gubuk.children:
        kebun.add(item)
    RECTS.append((gx - 5, gz - 5, gx + 5, gz + 5))
    tempat(gx, gz, 5.5)
    for (px, pz) in ((gx - 7, gz + 4), (gx - 9, gz + 7)):
        if bebas(px, pz, 1.4):
            kebun.add(part("PetiPanen", (px, 1.3, pz), (2.4, 1.8, 2.4), PAL["kayu_muda"], M["planks"]))
            kebun.add(part("IsiPeti", (px, 2.4, pz), (1.6, 0.7, 1.6), (196, 120, 84), M["smooth"], "ball"))
            tempat(px, pz, 1.6)
    papan5 = []
    papan_tanda(papan5, ox - 30, oz - 40, 15, "KEBUN BUAH\nBarisan apel, pir, dan plum dusun.\nPeti panen disiapkan tiap pagi.", lebar=11, tinggi=4.2, nama="PapanKebunBuah")
    for item in papan5:
        kebun.add(item)
    tempat(ox - 30, oz - 40, 4.5)
    for item in items:
        kebun.add(item)
    return kebun


def build_jalur_gerbang():
    """Jalur perjalanan antar-gerbang: pohon penembang dan batu penanda
    di sepanjang lanjutan tiap boulevard, agar dunia terasa berlanjut."""
    alam = model("JalurGerbang")
    rng = random.Random(31)
    items = []
    for axis in range(4):
        for i in range(5, 11):
            u = i * 40
            off = 22 if i % 2 == 0 else -22
            kandidat = []
            if axis == 0:
                kandidat = [(u, off), (u + 8, -off)]
            elif axis == 1:
                kandidat = [(-u, off), (-u - 8, -off)]
            elif axis == 2:
                kandidat = [(off, -u), (-off, -u - 8)]
            else:
                kandidat = [(off, u), (-off, u + 8)]
            for (x, z) in kandidat:
                if abs(x) > 462 or abs(z) > 462:
                    continue
                if bebas(x, z, 3.2):
                    items += pohon(x, z, rng)
    batu_lokasi = [(-260, -40), (-300, 120), (260, 120), (340, -140), (-140, 300), (120, 320),
                   (-360, -300), (360, 300), (-90, -280), (90, -300)]
    for (bx, bz) in batu_lokasi:
        if bebas(bx, bz, 4):
            r = rng.uniform(2.6, 4.2)
            items.append(part("BatuBesar", (bx, r * 0.42, bz), (r * 2, r * 1.3, r * 2), PAL["batu"], M["granite"], "ball"))
            tempat(bx, bz, r + 1)
    for item in items:
        alam.add(item)
    return alam


def build_kenyamanan():
    """Detail kenyamanan: pot bunga di pelataran kedatangan & promenade,
    bangku tambahan dekat totem, lampu taman kecil."""
    nyaman = model("SentuhKenyamanan")
    items = []
    pot_lokasi = [(6, 31), (26, 31), (6, 49), (26, 49), (-172, 146), (135, 130),
                  (-60, -30), (46, 4), (-40, 8)]
    for i, (px, pz) in enumerate(pot_lokasi):
        if not tempat(px, pz, 1.1):
            continue
        base = tinggi_tanah("Dataran", px, pz)
        items.append(part("PotBunga%d" % i, (px, base + 0.75, pz), (1.5, 1.5, 1.5), (128, 100, 74), M["ground"], "cylinder", 0, True, 0, 0, 90))
        items.append(part("IsiPot%d" % i, (px, base + 1.6, pz), (1.1, 0.4, 1.1), (104, 82, 58), M["ground"], "cylinder", 0, False, 0, 0, 90))
        items.append(bunga_at(px, pz, BUNGA_TAMAN[i % 6]))
    for (bx, bz, yaw) in ((4, 26, 180), (28, 26, 180)):
        if tempat(bx, bz, 2.5):
            for item in bench_at(bx, bz, yaw):
                nyaman.add(item)
    for item in items:
        nyaman.add(item)
    return nyaman


def build_semua_tambahan():
    tambahan = []
    tambahan.append(build_taman_mandala())
    tambahan.append(build_pasar())
    tambahan.append(build_danau())
    tambahan.append(build_panggung())
    tambahan.append(build_kebun_buah())
    tambahan.append(build_jalur_gerbang())
    tambahan.append(build_kenyamanan())
    return tambahan
