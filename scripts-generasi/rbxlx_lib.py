import math
from xml.sax.saxutils import escape

_counter = {"n": 0}


def next_ref():
    _counter["n"] += 1
    return "RBX%d" % _counter["n"]


def fnum(v):
    s = "%.6f" % float(v)
    s = s.rstrip("0").rstrip(".")
    if s in ("", "-0"):
        s = "0"
    return s


def p_string(name, val):
    return '<string name="%s">%s</string>' % (name, escape(str(val)))


def p_bool(name, val):
    return '<bool name="%s">%s</bool>' % (name, "true" if val else "false")


def p_int(name, val):
    return '<int name="%s">%d</int>' % (name, int(val))


def p_float(name, val):
    return '<float name="%s">%s</float>' % (name, fnum(val))


def p_token(name, val):
    return '<token name="%s">%d</token>' % (name, int(val))


def p_vec3(name, v):
    return '<Vector3 name="%s"><X>%s</X><Y>%s</Y><Z>%s</Z></Vector3>' % (name, fnum(v[0]), fnum(v[1]), fnum(v[2]))


def p_vec2(name, v):
    return '<Vector2 name="%s"><X>%s</X><Y>%s</Y></Vector2>' % (name, fnum(v[0]), fnum(v[1]))


def p_udim2(name, xs, xo, ys, yo):
    return '<UDim2 name="%s"><XS>%s</XS><XO>%d</XO><YS>%s</YS><YO>%d</YO></UDim2>' % (name, fnum(xs), int(xo), fnum(ys), int(yo))


def p_color3(name, rgb):
    return '<Color3 name="%s"><R>%s</R><G>%s</G><B>%s</B></Color3>' % (name, fnum(rgb[0]), fnum(rgb[1]), fnum(rgb[2]))


def p_color3u8(name, rgb):
    packed = (0xFF << 24) | (int(rgb[0]) << 16) | (int(rgb[1]) << 8) | int(rgb[2])
    return '<Color3uint8 name="Color3uint8">%d</Color3uint8>' % packed


def p_cframe(name, pos, rot):
    lines = ['<CoordinateFrame name="%s">' % name]
    lines.append("<X>%s</X><Y>%s</Y><Z>%s</Z>" % (fnum(pos[0]), fnum(pos[1]), fnum(pos[2])))
    for r in range(3):
        for c in range(3):
            lines.append("<R%d%d>%s</R%d%d>" % (r, c, fnum(rot[r][c]), r, c))
    lines.append("</CoordinateFrame>")
    return "".join(lines)


def p_protected(name, text):
    return '<ProtectedString name="%s">%s</ProtectedString>' % (name, escape(text))


def rot_matrix(yaw=0.0, pitch=0.0, roll=0.0):
    def mat_mul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

    def ry(t):
        c, s = math.cos(t), math.sin(t)
        return [[c, 0, s], [0, 1, 0], [-s, 0, c]]

    def rx(t):
        c, s = math.cos(t), math.sin(t)
        return [[1, 0, 0], [0, c, -s], [0, s, c]]

    def rz(t):
        c, s = math.cos(t), math.sin(t)
        return [[c, -s, 0], [s, c, 0], [0, 0, 1]]

    r = ry(math.radians(yaw))
    if pitch:
        r = mat_mul(r, rx(math.radians(pitch)))
    if roll:
        r = mat_mul(r, rz(math.radians(roll)))
    return r


class Item:
    def __init__(self, cls, props=None):
        self.cls = cls
        self.props = props or []
        self.children = []

    def add(self, child):
        self.children.append(child)
        return child

    def render(self, indent=0):
        pad = " " * indent
        ref = next_ref()
        out = ['%s<Item class="%s" referent="%s">' % (pad, self.cls, ref)]
        if self.props:
            out.append("%s  <Properties>" % pad)
            for p in self.props:
                out.append("%s    %s" % (pad, p))
            out.append("%s  </Properties>" % pad)
        for child in self.children:
            out.append(child.render(indent + 2))
        out.append('%s</Item>' % pad)
        return "\n".join(out)


def part(name, pos, size, color, material="SmoothPlastic", shape="block", transparency=0.0,
         collide=True, yaw=0.0, pitch=0.0, roll=0.0, cls="Part"):
    shape_token = {"ball": 0, "block": 1, "cylinder": 2}[shape]
    props = [
        p_string("Name", name),
        p_bool("Anchored", True),
        p_bool("CanCollide", collide),
        p_float("Transparency", transparency),
        p_token("Material", material),
        p_token("shape", shape_token),
        p_color3u8("Color3uint8", color),
        p_vec3("size", size),
        p_cframe("CFrame", pos, rot_matrix(yaw, pitch, roll)),
    ]
    for face in ("TopSurface", "BottomSurface", "LeftSurface", "RightSurface", "FrontSurface", "BackSurface"):
        props.append(p_token(face, 0))
    return Item(cls, props)


def add_text_surface(part_item, face, text, text_color=(0.98, 0.96, 0.9)):
    gui = Item("SurfaceGui", [p_token("Face", face), p_bool("AlwaysOnTop", False)])
    label = Item("TextLabel", [
        p_string("Name", "Teks"),
        p_udim2("Size", 1, 0, 1, 0),
        p_udim2("Position", 0, 0, 0, 0),
        p_color3("BackgroundColor3", (1, 1, 1)),
        p_float("BackgroundTransparency", 1),
        p_color3("TextColor3", text_color),
        p_bool("TextScaled", True),
        p_bool("TextWrapped", True),
        p_token("Font", 4),
        p_string("Text", text),
    ])
    gui.add(label)
    part_item.add(gui)
    return part_item


def add_point_light(part_item, color=(1.0, 0.85, 0.6), brightness=1.2, rng=18):
    light = Item("PointLight", [
        p_string("Name", "Cahaya"),
        p_color3("Color", color),
        p_float("Brightness", brightness),
        p_float("Range", rng),
    ])
    part_item.add(light)
    return part_item


def add_billboard_tag(part_item, text, width=130, height=28, offset_y=1.8):
    gui = Item("BillboardGui", [
        p_string("Name", "NamaTag"),
        p_udim2("Size", 0, width, 0, height),
        p_vec3("StudsOffset", (0, offset_y, 0)),
        p_float("MaxDistance", 40),
        p_bool("AlwaysOnTop", False),
    ])
    label = Item("TextLabel", [
        p_string("Name", "Teks"),
        p_udim2("Size", 1, 0, 1, 0),
        p_color3("BackgroundColor3", (0.12, 0.14, 0.11)),
        p_float("BackgroundTransparency", 0.25),
        p_color3("TextColor3", (0.95, 0.93, 0.86)),
        p_bool("TextScaled", True),
        p_bool("TextWrapped", True),
        p_token("Font", 4),
        p_string("Text", text),
    ])
    gui.add(label)
    part_item.add(gui)
    return part_item


def add_proximity_prompt(part_item, action, objek, distance=12):
    prompt = Item("ProximityPrompt", [
        p_string("Name", "PromptStatis"),
        p_string("ActionText", action),
        p_string("ObjectText", objek),
        p_float("HoldDuration", 0.3),
        p_float("MaxActivationDistance", distance),
        p_bool("RequiresLineOfSight", False),
    ])
    part_item.add(prompt)
    return part_item


def script_item(cls, name, source, disabled=False):
    props = [p_string("Name", name), p_protected("Source", source)]
    if cls in ("Script", "LocalScript"):
        props.append(p_bool("Disabled", disabled))
    return Item(cls, props)


def folder(name, children=None):
    item = Item("Folder", [p_string("Name", name)])
    for child in children or []:
        item.add(child)
    return item


def model(name, children=None):
    item = Item("Model", [p_string("Name", name)])
    for child in children or []:
        item.add(child)
    return item
