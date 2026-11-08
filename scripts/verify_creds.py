#!/usr/bin/env python3
"""Verifikasi kredensial TANPA menampilkan rahasianya di output."""
import base64
import datetime
import json
import time
import urllib.error
import urllib.request

# --- Roblox API key ---
line = ""
for l in open("/home/z/my-project/.secrets/akiomida.env"):
    if l.startswith("ROBLOX_API_KEY="):
        line = l.strip()
key = line.split("=", 1)[1]

print("== ROBLOX API KEY ==")
print("panjang:", len(key), "karakter (isi tidak ditampilkan)")

# Struktur kunci: 48 karakter acak + base64url(JWT). Awal JWT terlihat sebagai 'ZXlK' (b64 dari 'eyJ').
start = 48 if len(key) > 48 and key[48:52] == "ZXlK" else key.find("ZXlK")
assert start > 0, "format key tidak dikenali"
jwt_b64 = key[start:]
jwt_text = base64.urlsafe_b64decode(jwt_b64 + "=" * (-len(jwt_b64) % 4)).decode("utf-8", "replace")
parts = jwt_text.split(".")
assert len(parts) >= 2, "JWT tidak lengkap"


def pad(x: str) -> str:
    return x + "=" * (-len(x) % 4)


payload = json.loads(base64.urlsafe_b64decode(pad(parts[1])).decode("utf-8", "replace"))


def fmt_ts(ts) -> str:
    return datetime.datetime.utcfromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M UTC")


for k, v in payload.items():
    if k in ("exp", "iat", "nbf") and str(v).isdigit():
        print(f"  {k}: {v}  ({fmt_ts(v)})")
    else:
        s = json.dumps(v, ensure_ascii=False)
        if len(s) > 200:
            s = s[:200] + " ..."
        print(f"  {k}: {s}")

exp = payload.get("exp")
if exp:
    status = "MASIH AKTIF" if int(exp) > time.time() else "SUDAH KEDALUWARSA"
    print("  status waktu:", status)

# --- probe API (key dikirim via header, tidak pernah dicetak) ---
req = urllib.request.Request(
    "https://apis.roblox.com/cloud/v2/universes/10774464946",
    headers={"x-api-key": key},
)
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        print("probe HTTP:", r.status)
        print("body:", r.read().decode()[:300])
except urllib.error.HTTPError as e:
    print("probe HTTP:", e.code, "(401=key tidak valid/kedaluwarsa; 403/404=key valid tapi izin read tidak diberikan)")
except Exception as e:
    print("probe gagal (jaringan):", e)
