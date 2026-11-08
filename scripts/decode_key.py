#!/usr/bin/env python3
"""decode_key.py — decode blob API key Open Cloud dari pemilik, simpan ke .secrets/akiomida.env.
Blob = base64 dari bytes acak + JWT. JWT ditemukan lewat penanda b'eyJhbGciOi'.
Kredensial tidak pernah dicetak utuh; hanya status kedaluwarsa yang ditampilkan."""
import base64, json, sys, time, pathlib

BLOB = """YmY0IxHct0KvNG9rGLjCKcEpywfF6kkfwaMMxIAKL04yJu85ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaeTB5TURJeExUQTNMVEV6VkRFNE9qVXhPalE1V2lJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpTYjJKc2IzaEpiblJsY201aGJDSXNJbWx6Y3lJNklrTnNiM1ZrUVhWMGFHVnVkR2xqWVhScGIyNVRaWEoyYVdObElpd2lZbUZ6WlVGd2FVdGxlU0k2SWxsdFdUQkplRWhqZERCTGRrNUhPWEpIVEdwRFMyTkZjSGwzWmtZMmEydG1kMkZOVFhoSlFVdE1NRFI1U25VNE5TSXNJbTkzYm1WeVNXUWlPaUl4TVRrek16VTNNREV5TmlJc0ltVjRjQ0k2TVRjNU5ERTBNemswTnl3aWFXRjBJam94TnprME1UUXdNelEzTENKdVltWWlPakUzT1RReE5EQXpORGQ5Lk9RQnd4dzM3Q2FfYTVvcUdxOGtlWDNTY1JTRXN6QUN4d3ZwU1dsRkRieEdDTlVQNUU2SU9hZjhPdUN0YWF4UnZqQzdDbkFiR2NyZTJLazlCTlRqODg5NzBQTW1iUXlTZmZ1OTFHWDRsdWc1ZnJFcVcxQk9qT1hCWXh0NDFUWEt5cC1WS0E3MjVScnA5RUU2aFZsQVdXNUlxbS1CbjJYc1ZKa1ZLYkFZWk84LWg3bW83Q1Flc3pELWRHZ2NXSWxXZWJ0ZzBFQnczNE92aUJSQUtwTmRuUFA1clRPSzc4SGFFM1p0d1hzdnR4c29XSWV0ZGhmYWhHRmt0cFA5ZWVZaWMxWkUyaDhkY0d5OEtfM0JyR1NtODBKU05heG04ZFNWUVV2dTFCSjkzOGZMenJtWVBYem12Z1d6aml0aVk1NUs4U2p1Q3hlM3BiLXV5c09uM0dHd1ZNUQ=="""

OUT = pathlib.Path("/home/z/my-project/.secrets/akiomida.env")

def main():
    raw = base64.b64decode(BLOB)  # blob = bytes acak di depan + JWT
    i = raw.find(b"eyJhbGciOi")
    if i < 0:
        print("GAGAL: penanda JWT tidak ditemukan dalam blob")
        return 1
    jwt = raw[i:].decode("ascii", "strict").strip()
    # JWT = header.payload.signature, potong sampai whitespace/padding aneh
    jwt = "".join(ch for ch in jwt if ch.isalnum() or ch in "._-")
    parts = jwt.split(".")
    if len(parts) < 2:
        print("GAGAL: JWT tidak punya payload")
        return 1
    # payload base64url
    pad = parts[1] + "=" * (-len(parts[1]) % 4)
    payload = json.loads(base64.urlsafe_b64decode(pad))
    exp, iat = payload.get("exp", 0), payload.get("iat", 0)
    now = int(time.time())
    print(f"iat = {iat} ({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(iat))} UTC)")
    print(f"exp = {exp} ({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(exp))} UTC)")
    print(f"now = {now} UTC | sisa = {exp - now} detik ({(exp-now)/60:.1f} menit)")
    if exp <= now:
        print("STATUS: KEDALUWARSA")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(f"ROBLOX_API_KEY={jwt}\n", encoding="utf-8")
    OUT.chmod(0o600)
    print(f"STATUS: VALID — disimpan ke {OUT} (mode 600), panjang key {len(jwt)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
