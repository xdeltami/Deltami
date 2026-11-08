#!/usr/bin/env python3
"""Perbaiki seksi uji UI trade playtest: pakai pemain segar TD (3001), bukan
P2 yang ternyata sudah di-shadow oleh variabel lokal 'tamu' di atasnya."""
import pathlib

P = pathlib.Path("/home/z/my-project/scripts/playtest.luau")
text = P.read_text()
lines = text.split("\n")

MULAI = 'section("UI trade: alur nyata server -> jendela trade di klien")'
AKHIR = 'section("Simpan data saat keluar")'

i_mulai = next(i for i, l in enumerate(lines) if l.strip() == MULAI)
i_akhir = next(i for i, l in enumerate(lines) if l.strip() == AKHIR)

BARU = r'''section("UI trade: alur nyata server -> jendela trade di klien")
if MOD_RateLimit and MOD_RateLimit.clear then
        MOD_RateLimit.clear(1001)
        MOD_RateLimit.clear(3001)
end
profStore.__data["u_3001"] = { m = 9000, t = { { kind = "hasil", id = "labu_maxima", count = 4 } }, dev = false }
local TD = Stub.addPlayer(3001, "trader4")
Stub.giveCharacter(TD, 0, 6, 44)
Players.PlayerAdded:Fire(TD)
Stub.Scheduler.advance(0.5)
do
        local rP1 = P1.Character and (P1.Character.PrimaryPart or P1.Character:FindFirstChild("HumanoidRootPart"))
        if rP1 then
                Stub.giveCharacter(TD, rP1.Position.X + 2, rP1.Position.Y, rP1.Position.Z)
        end
end
local okAjakKlien, msgAjakKlien = serverCall("TradeAct", P1, "ajukan", 3001)
check("Ajakan trade P1 -> trader4 lolos server (jarak dekat)", okAjakKlien == true, tostring(msgAjakKlien))
Stub.Scheduler.advance(0.1)
local dimTrade = gui:FindFirstChild("DimLayar")
check("Jendela trade terbuka otomatis di klien P1 (TradeSync nyata)", dimTrade ~= nil and dimTrade.Visible == true, dimTrade and tostring(dimTrade.Visible) or "hilang")
local teksLawan = false
local teksJudul = false
local tombolSiapAda = false
local tombolBatalAda = false
if dimTrade then
        for _, d in ipairs(dimTrade:GetDescendants()) do
                if (d:IsA("TextLabel") or d:IsA("TextButton")) and type(d.Text) == "string" then
                        if string.find(d.Text, "Trade dengan trader4", 1, true) then
                                teksLawan = true
                        end
                        if d.Text == "Trade" then
                                teksJudul = true
                        end
                        if d.Text == "Tawaran Siap" then
                                tombolSiapAda = true
                        end
                        if d.Text == "Batal Trade" then
                                tombolBatalAda = true
                        end
                end
        end
end
check("Judul panel menjadi 'Trade'", teksJudul, "-")
check("Jendela memuat nama lawan (trader4)", teksLawan, "-")
check("Tombol 'Tawaran Siap' tersedia", tombolSiapAda, "-")
check("Tombol 'Batal Trade' tersedia", tombolBatalAda, "-")
local lanjutBtn = gui:FindFirstChild("LanjutTrade", true)
check("Tombol Lanjutkan Trade muncul di HUD", lanjutBtn ~= nil and lanjutBtn.Visible == true, lanjutBtn and tostring(lanjutBtn.Visible) or "hilang")
local okTawarKlien, msgTawarKlien = serverCall("TradeAct", TD, "ubah", { items = { { kind = "hasil", id = "labu_maxima", count = 2 } }, micda = 0 })
check("Tawaran trader4 (2 labu) diterima server", okTawarKlien == true, tostring(msgTawarKlien))
Stub.Scheduler.advance(0.1)
local teksTawaran = false
if dimTrade then
        for _, d in ipairs(dimTrade:GetDescendants()) do
                if (d:IsA("TextLabel") or d:IsA("TextButton")) and type(d.Text) == "string" then
                        if string.find(d.Text, "x2", 1, true) then
                                teksTawaran = true
                        end
                end
        end
end
check("Tawaran lawan tampil langsung di jendela (x2)", teksTawaran, "-")
local okBatalKlien, msgBatalKlien = serverCall("TradeAct", P1, "batal")
check("Batal dari klien diterima server", okBatalKlien == true, tostring(msgBatalKlien))
Stub.Scheduler.advance(0.1)
local dimSetelah = gui:FindFirstChild("DimLayar")
check("Jendela trade menutup sendiri saat penutup batal", dimSetelah ~= nil and dimSetelah.Visible == false, dimSetelah and tostring(dimSetelah.Visible) or "hilang")
local lanjutSetelah = gui:FindFirstChild("LanjutTrade", true)
check("Tombol Lanjutkan Trade hilang setelah sesi tuntas", lanjutSetelah == nil or lanjutSetelah.Visible == false, "-")
local stTD = serverCall("GetState", TD)
check("Setelah batal: 4 labu trader4 utuh (tidak ada item pindah)", stTD ~= nil and (function()
        local n = 0
        for _, s in ipairs(stTD.tas) do
                if s.kind == "hasil" and s.id == "labu_maxima" then
                        n += s.count
                end
        end
        return n
end)() == 4, stTD and tostring(stTD.micda) or "hilang")
Players.PlayerRemoving:Fire(TD)
Stub.Scheduler.advance(0.3)

'''

out = lines[:i_mulai] + BARU.split("\n") + lines[i_akhir:]
P.write_text("\n".join(out))
print("seksi UI trade diperbarui (TD 3001)")
