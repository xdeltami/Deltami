#!/usr/bin/env python3
"""Cek ketersediaan endpoint Open Cloud dengan kunci yang ada (tanpa mencetak kunci)."""
import json
import urllib.request
import urllib.error

s = {}
with open("/tmp/my-project/.secrets/akiomida.env") as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            s[k] = v

key = s.get("ROBLOX_API_KEY", "")
uni = s.get("UNIVERSE_ID", "")

tests = [
    ("datastore-list", f"https://apis.roblox.com/datastores/v1/universes/{uni}/standard-datastore/datastores"),
    ("datastore-entries-singular", f"https://apis.roblox.com/datastores/v1/universes/{uni}/standard-datastore/datastore/entries?prefix=u_&AllScopes=true"),
    ("datastore-entries-plural", f"https://apis.roblox.com/datastores/v1/universes/{uni}/standard-datastore/datastores/AKM_T1/entries?prefix=u_&AllScopes=true"),
]
for name, url in tests:
    r = urllib.request.Request(url, headers={"x-api-key": key})
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            body = resp.read().decode()[:400]
            print(f"{name}: HTTP {resp.status} {body}")
    except urllib.error.HTTPError as e:
        print(f"{name}: HTTP {e.code} {e.read().decode()[:200]}")
