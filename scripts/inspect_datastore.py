#!/usr/bin/env python3
"""Baca DataStore AKM_T1 via Open Cloud untuk memverifikasi data tersimpan pemain.
Tidak pernah mencetak kunci API. Hanya ringkasan saldo/jumlah item."""
import json
import os
import sys
import urllib.request
import urllib.error

SECRETS = "/tmp/my-project/.secrets/akiomida.env"


def load_secrets():
    vals = {}
    with open(SECRETS) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                vals[k] = v
    return vals


def req(url, key):
    r = urllib.request.Request(url, headers={"x-api-key": key})
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


def main():
    s = load_secrets()
    key = s.get("ROBLOX_API_KEY", "")
    uni = s.get("UNIVERSE_ID", "10774464946")
    base = f"https://apis.roblox.com/datastores/v1/universes/{uni}/standard-datastore/datastore/AKM_T1"

    # 1) daftar entri u_ (data pemain)
    st, body = req(f"{base}/entries?prefix=u_&limit=100&AllScopes=true", key)
    print(f"[entries u_] status={st}")
    if st != 200:
        print(body)
        sys.exit(1)
    keys = [e.get("key") for e in body.get("data", [])]
    print(f"entri data pemain: {keys}")
    cur = body.get("nextPageCursor")
    while cur:
        st, body = req(f"{base}/entries?prefix=u_&limit=100&AllScopes=true&cursor={cur}", key)
        if st != 200:
            break
        keys += [e.get("key") for e in body.get("data", [])]
        cur = body.get("nextPageCursor")

    # 2) isi tiap entri
    for k in keys:
        st, val = req(f"{base}/entries/{k}", key)
        if st != 200:
            print(f"{k}: HTTP {st} {val[:120]}")
            continue
        u = val.get("u") or {}
        saldo = u.get("m", u.get("saldo", "?"))
        tas = u.get("t", [])
        print(f"{k}: saldo={saldo} jenis_tas={len(tas) if isinstance(tas, list) else '?'} "
              f"isi={[ (i.get('i'), i.get('n')) for i in tas[:6] ] if isinstance(tas, list) else tas}")

    # 3) entri dunia d_
    st, body = req(f"{base}/entries?prefix=d_&limit=100&AllScopes=true", key)
    print(f"[entries d_] status={st}")
    if st == 200:
        print(f"entri dunia: {[e.get('key') for e in body.get('data', [])]}")


if __name__ == "__main__":
    main()
