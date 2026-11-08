"""Pulih kunci Roblox dari paste pemilik dunia (base64 -> baseApiKey + JWT).

Blob kunci TIDAK disimpan di dalam file ini (GitHub menolak push berisi secret).
Blob dibaca dari /home/z/my-project/.secrets/paste_key.b64 (chmod 600, di luar git).

Format paste: base64( base64decode(baseApiKey) || JWT ) — baseApiKey (48 karakter)
adalah klaim "baseApiKey" di dalam JWT; kunci penuh = baseApiKey + JWT.
"""
import base64
import json
import os

import sys

if len(sys.argv) > 1:
    jalur_blob = sys.argv[1]
else:
    jalur_blob = "/home/z/my-project/.secrets/paste_key.b64"

BLOB = open(jalur_blob).read().strip()

d = base64.b64decode(BLOB)
i = d.find(b"eyJhbGciOiJSUzI1NiIs")
assert i >= 0, "JWT tidak ditemukan"
jwt = d[i:].decode("ascii", "strict")
assert set(jwt) <= set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_."), "kunci mengandung karakter liar"
gugus = jwt.split(".")
assert len(gugus) == 3 and all(gugus), "kunci bukan JWT 3 gugus"

klm = json.loads(base64.urlsafe_b64decode(gugus[1] + "=" * (-len(gugus[1]) % 4)))
base = klm["baseApiKey"]
kunci_full = base + jwt

tujuan = "/home/z/my-project/.secrets/akiomida.env"
baris = {}
if os.path.exists(tujuan):
    for l in open(tujuan).read().splitlines():
        if "=" in l and not l.startswith("ROBLOX_SECURITY="):
            k, v = l.split("=", 1)
            baris[k] = v
baris["ROBLOX_SECURITY"] = kunci_full
urut = ["ROBLOX_SECURITY", "UNIVERSE_ID", "PLACE_DATARAN", "PLACE_KAMPUNG",
        "PLACE_SABANA", "PLACE_STEP", "PLACE_PERLADANGAN", "GITHUB_TOKEN", "GITHUB_USER"]
teks = "".join("%s=%s\n" % (k, baris[k]) for k in urut if k in baris)
open(tujuan, "w").write(teks)
os.chmod(tujuan, 0o600)

import datetime
exp = klm.get("exp")
print("kunci penuh dirakit:", len(kunci_full), "karakter")
print("exp  :", datetime.datetime.fromtimestamp(exp, datetime.UTC).isoformat(), "| sekarang:", datetime.datetime.now(datetime.UTC).isoformat())
print("BERLAKU" if exp and exp > datetime.datetime.now(datetime.UTC).timestamp() else "KADALUARSA — minta kunci baru")
