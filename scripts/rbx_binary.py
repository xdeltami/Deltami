"""Konverter rbxlx (XML) -> rbxl (biner) sesuai format Roblox.

Encoding diverifikasi dari sumber rbx-dom (rojo-rbx) dan file referensi:
- Header 32 byte: magic + version(0) + nclass + ninstance + 8 zero
- Chunk: name(4) + comp_len(u32) + uncomp_len(u32) + reserved(u32) + payload
  payload LZ4 block (store_size=False); comp_len=0 -> payload mentah
- PROP: classId(i32) + name(u32 str) + typeId(u8) + values
- INST: classId(i32) + className(u32 str) + is_service(u8) + count(i32)
        + referent array (delta + zigzag + interleaved BE) + (service byte 1x)
- PRNT: ver(u8=0) + count(i32) + child refs + parent refs
- END:  comp=0 uncomp=9 "</roblox>"
- Interleave: buffer[i + b*n] = bytes[b] (byte-plane transpose), nilai BE
- zigzag i32: (v << 1) ^ (v >> 31); f32: bits.rotate_left(1); token: u32 polos
"""
import struct
import xml.etree.ElementTree as ET

import lz4.block

MAGIC = b"<roblox!" + bytes([0x89, 0xFF, 0x0D, 0x0A, 0x1A, 0x0A]) + struct.pack("<H", 0)
FOOTER = b"</roblox>"

SERVICES = {
    "Workspace", "Lighting", "StarterGui", "ServerScriptService",
    "ReplicatedStorage", "SoundService", "Players", "Teams", "StarterPlayer",
}

# tag XML -> (typeId, label)
T_STRING, T_BOOL, T_I32, T_F32, T_F64 = 0x01, 0x02, 0x03, 0x04, 0x05
T_UDIM, T_UDIM2, T_COLOR3, T_VEC2, T_VEC3 = 0x06, 0x07, 0x0C, 0x0D, 0x0E
T_CFRAME, T_ENUM, T_REF, T_C3U8, T_I64 = 0x10, 0x12, 0x13, 0x1A, 0x1B

TAG2TYPE = {
    "string": T_STRING, "ProtectedString": T_STRING, "Content": T_STRING,
    "bool": T_BOOL, "int": T_I32, "float": T_F32, "double": T_F64,
    "token": T_ENUM, "Vector3": T_VEC3, "Vector2": T_VEC2, "UDim2": T_UDIM2,
    "Color3": T_COLOR3, "Color3uint8": T_C3U8, "CoordinateFrame": T_CFRAME,
}


def zigzag32(v):
    return ((v << 1) ^ (v >> 31)) & 0xFFFFFFFF


def f32bits(v):
    return struct.unpack("<I", struct.pack("<f", v))[0]


def rot1(v):
    return ((v << 1) | (v >> 31)) & 0xFFFFFFFF


def plane(blobs):
    """Transpose byte-planes: blobs = list of bytes (sama panjang)."""
    n, k = len(blobs), len(blobs[0])
    out = bytearray(n * k)
    for i, b in enumerate(blobs):
        out[i::n] = b
    return bytes(out)


def i32_plane(vals):
    return plane([zigzag32(v).to_bytes(4, "big") for v in vals])


def u32_plane(vals):
    return plane([v.to_bytes(4, "big") for v in vals])


def f32_plane(vals):
    return plane([rot1(f32bits(v)).to_bytes(4, "big") for v in vals])


def ref_plane(vals):
    out, last = [], 0
    for v in vals:
        out.append(v - last)
        last = v
    return i32_plane(out)


def i64_plane(vals):
    def zz64(v):
        return ((v << 1) ^ (v >> 63)) & 0xFFFFFFFFFFFFFFFF
    return plane([zz64(v).to_bytes(8, "big") for v in vals])


class Inst:
    __slots__ = ("cls", "props", "children", "ref", "parent")

    def __init__(self, cls):
        self.cls = cls
        self.props = {}     # nama -> (typeId, value)
        self.children = []
        self.ref = 0
        self.parent = -1


def parse_xml(path):
    root = ET.parse(path).getroot()
    tops = []
    for el in root:
        if el.tag == "Item":
            tops.append(_parse_item(el))
    return tops


def _parse_item(el):
    inst = Inst(el.get("class"))
    pel = el.find("Properties")
    if pel is not None:
        for p in pel:
            t = TAG2TYPE.get(p.tag)
            if t is None:
                continue
            inst.props[p.get("name")] = (t, _parse_value(t, p))
    for child in el:
        if child.tag == "Item":
            inst.children.append(_parse_item(child))
    return inst


def _txt(el):
    return el.text if el.text is not None else ""


def _parse_value(t, p):
    if t == T_STRING:
        return _txt(p).encode("utf-8")
    if t == T_BOOL:
        return _txt(p).strip() == "true"
    if t in (T_I32, T_ENUM):
        return int(_txt(p).strip() or 0)
    if t == T_F32:
        return float(_txt(p).strip() or 0.0)
    if t == T_F64:
        return float(_txt(p).strip() or 0.0)
    if t == T_C3U8:
        v = int(_txt(p).strip() or 0) & 0xFFFFFFFF
        return ((v >> 16) & 255, (v >> 8) & 255, v & 255)
    if t == T_VEC3:
        return (float(_txt(p.find("X"))), float(_txt(p.find("Y"))), float(_txt(p.find("Z"))))
    if t == T_VEC2:
        return (float(_txt(p.find("X"))), float(_txt(p.find("Y"))))
    if t == T_UDIM2:
        return (float(_txt(p.find("XS"))), int(_txt(p.find("XO"))),
                float(_txt(p.find("YS"))), int(_txt(p.find("YO"))))
    if t == T_COLOR3:
        return (float(_txt(p.find("R"))), float(_txt(p.find("G"))), float(_txt(p.find("B"))))
    if t == T_CFRAME:
        pos = (float(_txt(p.find("X"))), float(_txt(p.find("Y"))), float(_txt(p.find("Z"))))
        rot = [[float(_txt(p.find("R%d%d" % (r, c)))) for c in range(3)] for r in range(3)]
        return (pos, rot)
    raise ValueError("tipe tak didukung: %s" % t)


def flatten(tops):
    flat, stack = [], list(reversed(tops))
    while stack:
        inst = stack.pop()
        inst.ref = len(flat)
        flat.append(inst)
        for c in reversed(inst.children):
            c.parent = inst.ref
            stack.append(c)
    for inst in flat:
        for c in inst.children:
            pass
    return flat


DEFAULTS = {
    T_STRING: b"", T_BOOL: False, T_I32: 0, T_F32: 0.0, T_F64: 0.0,
    T_ENUM: 0, T_VEC2: (0.0, 0.0), T_VEC3: (0.0, 0.0, 0.0),
    T_UDIM2: (0.0, 0, 0.0, 0), T_COLOR3: (0.0, 0.0, 0.0),
    T_C3U8: (163, 162, 165), T_CFRAME: ((0.0, 0.0, 0.0), [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
}


def chunk(name, payload, compress=True):
    if compress:
        cp = lz4.block.compress(payload, store_size=False)
        head = struct.pack("<4sIII", name, len(cp), len(payload), 0)
        return head + cp
    head = struct.pack("<4sIII", name, 0, len(payload), 0)
    return head + payload


def write_prop_values(typeid, values):
    if typeid == T_STRING:
        out = bytearray()
        for v in values:
            out += struct.pack("<I", len(v)) + v
        return bytes(out)
    if typeid == T_BOOL:
        return bytes(1 if v else 0 for v in values)
    if typeid == T_I32:
        return i32_plane(values)
    if typeid == T_F32:
        return f32_plane(values)
    if typeid == T_F64:
        return b"".join(struct.pack("<d", v) for v in values)
    if typeid == T_ENUM:
        return u32_plane(values)
    if typeid == T_I64:
        return i64_plane(values)
    if typeid == T_VEC3:
        return f32_plane([v[0] for v in values]) + f32_plane([v[1] for v in values]) \
            + f32_plane([v[2] for v in values])
    if typeid == T_VEC2:
        return f32_plane([v[0] for v in values]) + f32_plane([v[1] for v in values])
    if typeid == T_COLOR3:
        return f32_plane([v[0] for v in values]) + f32_plane([v[1] for v in values]) \
            + f32_plane([v[2] for v in values])
    if typeid == T_UDIM2:
        return f32_plane([v[0] for v in values]) + f32_plane([v[2] for v in values]) \
            + i32_plane([v[1] for v in values]) + i32_plane([v[3] for v in values])
    if typeid == T_C3U8:
        return bytes(b for v in values for b in (v[0], v[1], v[2]))
    if typeid == T_CFRAME:
        rots = bytearray()
        for v in values:
            rots.append(0x00)
            for r in range(3):
                for c in range(3):
                    rots += struct.pack("<f", float(v[1][r][c]))
        return (bytes(rots)
                + f32_plane([v[0][0] for v in values])
                + f32_plane([v[0][1] for v in values])
                + f32_plane([v[0][2] for v in values]))
    raise ValueError("tipe nilai tak didukung: %#x" % typeid)


def build_rbxl(tops, compress=True):
    flat = flatten(tops)
    classes = {}
    for inst in flat:
        classes.setdefault(inst.cls, []).append(inst)

    out = bytearray(MAGIC)
    out += struct.pack("<II", len(classes), len(flat))
    out += b"\x00" * 8

    meta = struct.pack("<I", 1)
    k = b"ExplicitAutoJoints"
    meta += struct.pack("<I", len(k)) + k + struct.pack("<I", 4) + b"true"
    out += chunk(b"META", meta, compress)

    for cid, (cls, insts) in enumerate(classes.items()):
        c = struct.pack("<i", cid)
        nb = cls.encode("utf-8")
        c += struct.pack("<I", len(nb)) + nb
        svc = 1 if cls in SERVICES else 0
        c += bytes([svc])
        c += struct.pack("<i", len(insts))
        c += ref_plane([i.ref for i in insts])
        if svc:
            c += b"\x01" * len(insts)
        out += chunk(b"INST", c, compress)

    for cid, (cls, insts) in enumerate(classes.items()):
        propnames = []
        for i in insts:
            for nm in i.props:
                if nm not in propnames:
                    propnames.append(nm)
        for nm in propnames:
            typeid = None
            vals = []
            for i in insts:
                if nm in i.props:
                    t, v = i.props[nm]
                    if typeid is None:
                        typeid = t
                    vals.append(v)
                else:
                    vals.append(DEFAULTS[typeid if typeid is not None else T_STRING])
            p = struct.pack("<i", cid)
            nb = nm.encode("utf-8")
            p += struct.pack("<I", len(nb)) + nb + bytes([typeid])
            p += write_prop_values(typeid, vals)
            out += chunk(b"PROP", p, compress)

    prnt = bytes([0]) + struct.pack("<I", len(flat))
    prnt += ref_plane([i.ref for i in flat])
    prnt += ref_plane([i.parent for i in flat])
    out += chunk(b"PRNT", prnt, compress)

    out += chunk(b"END\x00", FOOTER, compress=False)
    return bytes(out)


# ---------- pembaca (validasi roundtrip) ----------

def read_chunks(data):
    assert data[:16] == MAGIC, "magic salah"
    nclass, ninst = struct.unpack("<II", data[16:24])
    off = 32
    chunks = []
    while off < len(data):
        name = data[off:off + 4]
        clen, ulen, res = struct.unpack("<III", data[off + 4:off + 16])
        if clen:
            payload = lz4.block.decompress(data[off + 16:off + 16 + clen],
                                           uncompressed_size=ulen)
            off += 16 + clen
        else:
            payload = data[off + 16:off + 16 + ulen]
            off += 16 + ulen
        chunks.append((name, payload))
    return nclass, ninst, chunks


def _unzz32(v):
    v &= 0xFFFFFFFF
    return (v >> 1) ^ -(v & 1)


def _unplane(buf, n, k):
    return [buf[i::n] for i in range(n)] if False else None


def deplane(buf, n, k):
    vals = []
    for i in range(n):
        vals.append(bytes(buf[i + b * n] for b in range(k)))
    return vals


def de_i32(buf, n):
    return [_unzz32(int.from_bytes(b, "big")) for b in deplane(buf, n, 4)]


def de_u32(buf, n):
    return [int.from_bytes(b, "big") for b in deplane(buf, n, 4)]


def de_f32(buf, n):
    out = []
    for b in deplane(buf, n, 4):
        bits = int.from_bytes(b, "big")
        bits = ((bits >> 1) | (bits << 31)) & 0xFFFFFFFF
        out.append(struct.unpack("<f", struct.pack("<I", bits))[0])
    return out


def de_ref(buf, n):
    out, last = [], 0
    for d in de_i32(buf, n):
        last += d
        out.append(last)
    return out


def read_rbxl(data, verbose=False):
    nclass, ninst, chunks = read_chunks(data)
    insts = {}       # ref -> dict(cls, props)
    class_order = []
    props_by_class = {}
    parents = None
    for name, raw in chunks:
        if name == b"INST":
            cid = struct.unpack("<i", raw[0:4])[0]
            nlen = struct.unpack("<I", raw[4:8])[0]
            cls = raw[8:8 + nlen].decode()
            p = 8 + nlen
            svc = raw[p]
            p += 1
            cnt = struct.unpack("<i", raw[p:p + 4])[0]
            p += 4
            refs = de_ref(raw[p:p + 4 * cnt], cnt)
            for r in refs:
                insts[r] = {"cls": cls, "props": {}}
            if cls not in props_by_class:
                props_by_class[cls] = {}
                class_order.append(cls)
        elif name == b"PROP":
            cid = struct.unpack("<i", raw[0:4])[0]
            nlen = struct.unpack("<I", raw[4:8])[0]
            pname = raw[8:8 + nlen].decode()
            p = 8 + nlen
            tid = raw[p]
            p += 1
            props_by_class[class_order[cid]][pname] = (tid, raw[p:])
        elif name == b"PRNT":
            cnt = struct.unpack("<I", raw[1:5])[0]
            kids = de_ref(raw[5:5 + 4 * cnt], cnt)
            pars = de_ref(raw[5 + 4 * cnt:5 + 8 * cnt], cnt)
            parents = dict(zip(kids, pars))
    # terapkan properti per instance
    for cls, props in props_by_class.items():
        members = [r for r, i in insts.items() if i["cls"] == cls]
        members.sort()
        for pname, (tid, blob) in props.items():
            vals = decode_values(tid, blob, len(members))
            for r, v in zip(members, vals):
                insts[r]["props"][pname] = v
    if verbose:
        print("read_rbxl: kelas=%d instance=%d chunks=%d" % (len(class_order), len(insts), len(chunks)))
    return class_order, insts, parents


def decode_values(tid, blob, n):
    if tid == T_STRING:
        out, off = [], 0
        for _ in range(n):
            ln = struct.unpack("<I", blob[off:off + 4])[0]
            off += 4
            out.append(blob[off:off + ln])
            off += ln
        return out
    if tid == T_BOOL:
        return [blob[i] == 1 for i in range(n)]
    if tid == T_I32:
        return de_i32(blob, n)
    if tid == T_F32:
        return de_f32(blob, n)
    if tid == T_F64:
        return list(struct.unpack("<%dd" % n, blob[:8 * n]))
    if tid == T_UDIM2:
        sx = de_f32(blob[0:4 * n], n)
        sy = de_f32(blob[4 * n:8 * n], n)
        ox = de_i32(blob[8 * n:12 * n], n)
        oy = de_i32(blob[12 * n:16 * n], n)
        return list(zip(sx, ox, sy, oy))
    if tid == T_VEC2:
        x = de_f32(blob[:4 * n], n)
        y = de_f32(blob[4 * n:8 * n], n)
        return list(zip(x, y))
    if tid == T_COLOR3:
        r = de_f32(blob[:4 * n], n)
        g = de_f32(blob[4 * n:8 * n], n)
        b = de_f32(blob[8 * n:12 * n], n)
        return list(zip(r, g, b))
    if tid == T_ENUM:
        return de_u32(blob, n)
    if tid == T_VEC3:
        x = de_f32(blob[:4 * n], n)
        y = de_f32(blob[4 * n:8 * n], n)
        z = de_f32(blob[8 * n:12 * n], n)
        return list(zip(x, y, z))
    if tid == T_C3U8:
        return [(blob[3 * i], blob[3 * i + 1], blob[3 * i + 2]) for i in range(n)]
    if tid == T_CFRAME:
        rots, off = [], 0
        for _ in range(n):
            rid = blob[off]
            off += 1
            if rid == 0x00:
                m = [[struct.unpack("<f", blob[off + 4 * (3 * r + c):off + 4 * (3 * r + c) + 4])[0]
                      for c in range(3)] for r in range(3)]
                off += 36
            else:
                m = None
            rots.append(m)
        x = de_f32(blob[off:off + 4 * n], n)
        y = de_f32(blob[off + 4 * n:off + 8 * n], n)
        z = de_f32(blob[off + 8 * n:off + 12 * n], n)
        return [(pos, rot) for pos, rot in zip(zip(x, y, z), rots)]
    raise ValueError("decode: tipe tak didukung %#x" % tid)


def convert(path_in, path_out):
    tops = parse_xml(path_in)
    data = build_rbxl(tops)
    with open(path_out, "wb") as f:
        f.write(data)
    return data, tops


if __name__ == "__main__":
    import sys
    src = sys.argv[1]
    dst = sys.argv[2]
    data, tops = convert(src, dst)
    print("rbxl ditulis: %s (%d bytes)" % (dst, len(data)))
    # roundtrip
    order, insts, parents = read_rbxl(data, verbose=True)
    flat = flatten(tops)
    ok = len(insts) == len(flat)
    mismatch = 0
    for inst in flat:
        got = insts.get(inst.ref)
        if not got or got["cls"] != inst.cls:
            mismatch += 1
            continue
        nm = inst.props.get("Name")
        if nm and got["props"].get("Name") != nm[1]:
            mismatch += 1
    cfm = sum(1 for i in flat if "CFrame" in i.props)
    print("roundtrip: total=%d mismatch=%d cframe=%d -> %s"
          % (len(flat), mismatch, cfm, "OK" if ok and mismatch == 0 else "GAGAL"))
