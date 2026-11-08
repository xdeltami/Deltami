"""Generator TerrainDunia.luau — terrain asli Roblox per place (dibangun runtime server).

Satu sumber data untuk dua kebutuhan:
  1. luau_source(nama_place) -> script Luau yang mengisi Terrain (bukit, sungai, dunes,
     tebing penutup tepi peta) saat server start via FillRegion/FillBall/FillBlock.
  2. tinggi_tanah(nama_place, x, z) -> tinggi permukaan dome bukit untuk menempatkan
     pohon/batu tidak melayang (permukaan dasar terrain = y 0).

Permukaan dasar terrain = y 0. Sungai: dasar batu di y -12..-8, air y -8..-4,
tepi (bank) di y 0. Voxels terrain 4x4x4 (resolusi 4).
"""
import math
import random

TEPI = {"jrk": 496, "tbl": 48, "tng": 90}
SUNGAI_INFO = {"lbr": 18, "pahat": 8.0}

SUNGAI_DATARAN = [
    (-470, 150), (-330, 122), (-180, 168), (-20, 196),
    (130, 150), (280, 186), (470, 150),
]

BUKIT_DATARAN = [
    (-320, -180, 85, 16), (280, -220, 80, 15), (-220, -60, 60, 12),
    (320, 100, 75, 14), (-340, 60, 70, 13), (200, 330, 80, 16),
    (-100, 350, 75, 15), (-380, 260, 70, 14), (60, -350, 70, 14),
    (-240, 400, 80, 16), (400, -80, 65, 12), (100, 230, 50, 10),
]

LINDUNGI_DATARAN = [
    ("plaza", "lingkaran", 0, 0, 44),
    ("spawn", "lingkaran", 16, 40, 16),
    ("jalan_barat_timur", "kotak", -240, -14, 240, 14),
    ("jalan_utara_selatan", "kotak", -14, -240, 14, 240),
    ("jalan_toko", "kotak", -70, -52, -20, -40),
    ("toko", "kotak", -108, -74, -58, -14),
    ("desa", "kotak", 30, -140, 170, -48),
    ("kebun", "kotak", 24, -64, 112, 6),
    ("jalan_kebun", "kotak", 20, -34, 44, -4),
    ("dermaga", "kotak", 100, 130, 165, 172),
    ("jembatan_selatan", "lingkaran", 0, 190, 32),
    ("jalan_sungai", "kotak", 24, 20, 130, 148),
    ("kincir", "lingkaran", -180, -170, 20),
    ("gerobak", "lingkaran", -52, -24, 12),
    ("sumur", "lingkaran", 18, 22, 12),
    ("gerbang_barat", "lingkaran", -220, 0, 20),
    ("gerbang_timur", "lingkaran", 220, 0, 20),
    ("gerbang_utara", "lingkaran", 0, -220, 20),
    ("gerbang_selatan", "lingkaran", 0, 220, 20),
]

SPESIFIKASI = {
    "Dataran": {
        "dasar": "Grass",
        "bukit": BUKIT_DATARAN,
        "tumpuk": [],
        "sungai": SUNGAI_DATARAN,
    },
    "Kampung": {"dasar": "Grass", "bukit": [], "tumpuk": [], "sungai": []},
    "Sabana": {"dasar": "Sand", "bukit": [], "tumpuk": [], "sungai": []},
    "Stepa": {"dasar": "Ground", "bukit": [], "tumpuk": [], "sungai": []},
    "Perladangan": {"dasar": "Grass", "bukit": [], "tumpuk": [], "sungai": []},
}

GUNUNGAN = {
    "Kampung": {"jml": 9, "r": (60, 105), "t": (4, 7), "mats": ("Grass", "Ground"), "patch": ("Ground",), "jml_patch": 10, "benih": 311},
    "Sabana": {"jml": 12, "r": (55, 95), "t": (5, 9), "mats": ("Sand",), "patch": ("Ground",), "jml_patch": 12, "benih": 411},
    "Stepa": {"jml": 8, "r": (90, 135), "t": (3, 6), "mats": ("Ground",), "patch": ("Rock",), "jml_patch": 8, "benih": 511},
    "Perladangan": {"jml": 10, "r": (60, 100), "t": (4, 7), "mats": ("Grass", "Ground"), "patch": ("Ground",), "jml_patch": 14, "benih": 611},
}

LINDUNGI_TEMPAT_LUAR = [
    ("spawn", "lingkaran", 0, 18, 18),
    ("koridor_gerbang", "kotak", -16, -95, 16, -38),
]


def dome_tinggi(bukit, x, z):
    h = 0.0
    for (hx, hz, r, t) in bukit:
        d = math.hypot(x - hx, z - hz)
        if d < r:
            hh = t - r + math.sqrt(r * r - d * d)
            if hh > h:
                h = hh
    return max(0.0, h)


def _kena_hindaran(hindar, x, z):
    for item in hindar:
        jenis = item[1]
        if jenis == "lingkaran":
            a, b, c = item[2], item[3], item[4]
            if (x - a) ** 2 + (z - b) ** 2 <= (c + 6) ** 2:
                return True
        else:
            a, b, c, d = item[2], item[3], item[4], item[5]
            if a - 8 <= x <= c + 8 and b - 8 <= z <= d + 8:
                return True
    return False


def _dekat_sungai(polyline, x, z, buffer):
    for i in range(len(polyline) - 1):
        x0, z0 = polyline[i]
        x1, z1 = polyline[i + 1]
        dx, dz = x1 - x0, z1 - z0
        panj2 = dx * dx + dz * dz
        if panj2 == 0:
            continue
        t = max(0.0, min(1.0, ((x - x0) * dx + (z - z0) * dz) / panj2))
        px, pz = x0 + t * dx, z0 + t * dz
        if math.hypot(x - px, z - pz) < buffer:
            return True
    return False


def _fmt(v):
    s = "%.2f" % float(v)
    s = s.rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def tinggi_tanah(nama_place, x, z):
    return dome_tinggi(SPEK(nama_place)["bukit"], x, z)


def SPEK(nama):
    return SPESIFIKASI[nama]


def bukit_tempat_luar(nama):
    g = GUNUNGAN[nama]
    rng = random.Random(g["benih"])
    hasil = []
    while len(hasil) < g["jml"]:
        x = rng.uniform(-430, 430)
        z = rng.uniform(-430, 430)
        r = rng.uniform(*g["r"])
        if _kena_hindaran(LINDUNGI_TEMPAT_LUAR, x, z):
            continue
        bentrok = False
        for (hx, hz, hr, _) in hasil:
            if math.hypot(x - hx, z - hz) < (r + hr) * 0.75:
                bentrok = True
                break
        if bentrok:
            continue
        hasil.append((round(x, 1), round(z, 1), round(r, 1), round(rng.uniform(*g["t"]), 1)))
    return hasil


def tumpuk_tempat_luar(nama):
    g = GUNUNGAN[nama]
    rng = random.Random(g["benih"] + 7)
    hasil = []
    while len(hasil) < g["jml_patch"]:
        x = rng.uniform(-420, 420)
        z = rng.uniform(-420, 420)
        if _kena_hindaran(LINDUNGI_TEMPAT_LUAR, x, z):
            continue
        sx = rng.uniform(24, 64)
        sz = rng.uniform(24, 64)
        hasil.append((round(x, 1), round(z, 1), round(sx, 1), round(sz, 1), g["patch"][0]))
    return hasil


def tumpuk_dataran():
    rng = random.Random(17)
    hasil = []
    mats = ("Ground", "Ground", "Sand")
    while len(hasil) < 26:
        x = rng.uniform(-430, 430)
        z = rng.uniform(-430, 430)
        if _kena_hindaran(LINDUNGI_DATARAN, x, z):
            continue
        if _dekat_sungai(SUNGAI_DATARAN, x, z, 30):
            continue
        sx = rng.uniform(20, 56)
        sz = rng.uniform(20, 56)
        hasil.append((round(x, 1), round(z, 1), round(sx, 1), round(sz, 1), mats[len(hasil) % len(mats)]))
    return hasil


def gigi_tebing(nama):
    rng = random.Random(hash(nama) % 9000 + 99)
    hasil = []
    jrk, tng = TEPI["jrk"], TEPI["tng"]
    per_sisi = 8
    for sisi in range(4):
        for i in range(per_sisi):
            u = -jrk + 40 + (2 * jrk - 80) * (i + rng.uniform(0.2, 0.8)) / per_sisi
            if sisi == 0:
                x, z = u, -jrk - rng.uniform(6, 26)
            elif sisi == 1:
                x, z = u, jrk + rng.uniform(6, 26)
            elif sisi == 2:
                x, z = -jrk - rng.uniform(6, 26), u
            else:
                x, z = jrk + rng.uniform(6, 26), u
            hasil.append((round(x, 1), round(z, 1), round(rng.uniform(9, 18), 1)))
    return hasil


def _tabel_bukit(bukit):
    baris = []
    for (x, z, r, t) in bukit:
        baris.append('{x=%s,z=%s,r=%s,t=%s,m="Grass"}' % (_fmt(x), _fmt(z), _fmt(r), _fmt(t)))
    return "{" + ", ".join(baris) + "}"


def _tabel_tumpuk(tumpuk):
    baris = []
    for (x, z, sx, sz, m) in tumpuk:
        baris.append('{x=%s,z=%s,sx=%s,sz=%s,m="%s"}' % (_fmt(x), _fmt(z), _fmt(sx), _fmt(sz), m))
    return "{" + ", ".join(baris) + "}"


def _tabel_sungai(polyline):
    baris = ["{x=%s,z=%s}" % (_fmt(x), _fmt(z)) for (x, z) in polyline]
    return "{" + ", ".join(baris) + "}"


def _tabel_gigi(gigi):
    baris = []
    for (x, z, d) in gigi:
        baris.append("{x=%s,z=%s,y=%s,d=%s}" % (_fmt(x), _fmt(z), _fmt(TEPI["tng"] + 2), _fmt(d)))
    return "{" + ", ".join(baris) + "}"


def luau_source(nama_place):
    s = SPEK(nama_place)
    bukit = s["bukit"]
    if nama_place != "Dataran":
        bukit = bukit_tempat_luar(nama_place)
    tumpuk = s["tumpuk"]
    if nama_place != "Dataran":
        tumpuk = tumpuk_tempat_luar(nama_place)
    sungai = s["sungai"]
    gigi = gigi_tebing(nama_place)
    script = """local Terrain = workspace:WaitForChild("Terrain")

local DASAR_M = "@@DASAR@@"
local BUKIT = @@BUKIT@@
local TUMPUK = @@TUMPUK@@
local SUNGAI = @@SUNGAI@@
local GIGI = @@GIGI@@
local TEPI = {jrk = @@JRK@@, tbl = @@TBL@@, tng = @@TNG@@}
local RIVER = {lbr = @@LBR@@, pahat = @@PAHAT@@}

local function bahan(nama)
	return Enum.Material[nama]
end

local dasar = Region3.new(Vector3.new(-512, -12, -512), Vector3.new(512, -0.001, 512))
Terrain:FillRegion(dasar, 4, bahan(DASAR_M))

for _, b in ipairs(BUKIT) do
	Terrain:FillBall(Vector3.new(b.x, b.t - b.r, b.z), b.r, bahan(b.m))
end

for _, p in ipairs(TUMPUK) do
	Terrain:FillBlock(CFrame.new(Vector3.new(p.x, -2, p.z)), Vector3.new(p.sx, 4, p.sz), bahan(p.m))
end

for i = 1, #SUNGAI - 1 do
	local a = SUNGAI[i]
	local b = SUNGAI[i + 1]
	local ax, az, bx, bz = a.x, a.z, b.x, b.z
	local panj = math.sqrt((bx - ax) ^ 2 + (bz - az) ^ 2)
	if panj > 1 then
		local mid = Vector3.new((ax + bx) / 2, -4, (az + bz) / 2)
		local cf = CFrame.lookAt(mid, Vector3.new(bx, -4, bz))
		Terrain:FillBlock(cf, Vector3.new(RIVER.lbr, 12, panj + 10), bahan("Air"))
		Terrain:FillBlock(cf, Vector3.new(RIVER.lbr, 4, panj + 10), bahan("Ground"))
		Terrain:FillBlock(cf, Vector3.new(RIVER.lbr - 2, 4, panj + 10), bahan("Water"))
	end
end

local j, tb, tg = TEPI.jrk, TEPI.tbl, TEPI.tng
local q = 2 * j + 2 * tb
Terrain:FillBlock(CFrame.new(Vector3.new(0, tg / 2 - 12, -j - tb / 2)), Vector3.new(q, tg + 12, tb), bahan("Rock"))
Terrain:FillBlock(CFrame.new(Vector3.new(0, tg / 2 - 12, j + tb / 2)), Vector3.new(q, tg + 12, tb), bahan("Rock"))
Terrain:FillBlock(CFrame.new(Vector3.new(-j - tb / 2, tg / 2 - 12, 0)), Vector3.new(tb, tg + 12, q), bahan("Rock"))
Terrain:FillBlock(CFrame.new(Vector3.new(j + tb / 2, tg / 2 - 12, 0)), Vector3.new(tb, tg + 12, q), bahan("Rock"))

for _, g in ipairs(GIGI) do
	Terrain:FillBall(Vector3.new(g.x, g.y, g.z), g.d, bahan("Rock"))
end
"""
    script = script.replace("@@DASAR@@", s["dasar"])
    script = script.replace("@@BUKIT@@", _tabel_bukit(bukit))
    script = script.replace("@@TUMPUK@@", _tabel_tumpuk(tumpuk))
    script = script.replace("@@SUNGAI@@", _tabel_sungai(sungai))
    script = script.replace("@@GIGI@@", _tabel_gigi(gigi))
    script = script.replace("@@JRK@@", str(TEPI["jrk"]))
    script = script.replace("@@TBL@@", str(TEPI["tbl"]))
    script = script.replace("@@TNG@@", str(TEPI["tng"]))
    script = script.replace("@@LBR@@", str(SUNGAI_INFO["lbr"]))
    script = script.replace("@@PAHAT@@", _fmt(SUNGAI_INFO["pahat"]))
    if "TODO" in script or "undefined" in script:
        raise SystemExit("token terlarang di TerrainDunia %s" % nama_place)
    return script


if __name__ == "__main__":
    # verifikasi lindungan: tak boleh ada bukit menutupi area terlindungi Dataran
    buruk = []
    for item in LINDUNGI_DATARAN:
        jenis = item[1]
        if jenis == "lingkaran":
            _, _, a, b, c = item
            for i in range(-int(c), int(c) + 1, 4):
                for k in range(-int(c), int(c) + 1, 4):
                    if i * i + k * k <= c * c and dome_tinggi(BUKIT_DATARAN, a + i, b + k) > 0.5:
                        buruk.append((a + i, b + k))
        else:
            _, _, a, b, c, d = item
            for i in range(int(a) - 8, int(c) + 9, 4):
                for k in range(int(b) - 8, int(d) + 9, 4):
                    if dome_tinggi(BUKIT_DATARAN, i, k) > 0.5:
                        buruk.append((i, k))
    for (x, z) in SUNGAI_DATARAN:
        pass
    # sungai tak boleh menabrak bukit (dome > 0 di jalur sungai)
    for i in range(len(SUNGAI_DATARAN) - 1):
        x0, z0 = SUNGAI_DATARAN[i]
        x1, z1 = SUNGAI_DATARAN[i + 1]
        for t in range(0, 101):
            px = x0 + (x1 - x0) * t / 100.0
            pz = z0 + (z1 - z0) * t / 100.0
            if dome_tinggi(BUKIT_DATARAN, px, pz) > 0.3:
                buruk.append(("sungai", px, pz))
    print("lindungan Dataran:", "AMAN" if not buruk else buruk[:20])
    for nama in ("Kampung", "Sabana", "Stepa", "Perladangan"):
        bk = bukit_tempat_luar(nama)
        tp = tumpuk_tempat_luar(nama)
        tabrak = [b for b in bk if dome_tinggi(bk, b[0], b[1]) and False]
        ok = all(not _kena_hindaran(LINDUNGI_TEMPAT_LUAR, hx, hz) for (hx, hz, _, _) in bk)
        print("%s: bukit=%d tumpuk=%d spawn-gerbang aman=%s" % (nama, len(bk), len(tp), ok))
        print("  sample:", bk[:3])
    src = luau_source("Dataran")
    print("luau Dataran:", len(src), "char |", len(src.splitlines()), "baris")
