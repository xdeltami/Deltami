#!/usr/bin/env python3
"""Ekstrak seksi UI trade dari UIController.luau menjadi modul baru
src/Client/TradeUI.luau (fungsi bangun(ctx)) agar chunk UIController tidak
melebihi batas 200 register. Seksi lama diganti satu baris pemanggilan."""
import pathlib
import re

ROOT = pathlib.Path("/home/z/my-project/download/dunia-akiomida")
UI = ROOT / "src/Client/UIController.luau"
TRADE = ROOT / "src/Client/TradeUI.luau"

text = UI.read_text()
lines = text.split("\n")

MULAI = "-- ===================== TRADE ANTAR PEMAIN ====================="
AKHIR = "-- ================== AKHIR TRADE ANTAR PEMAIN =================="

i_mulai = next(i for i, l in enumerate(lines) if l.strip() == MULAI)
i_akhir = next(i for i, l in enumerate(lines) if l.strip() == AKHIR)

seksi = lines[i_mulai + 1 : i_akhir]  # isi do-block (tanpa marker & end luar)
# buang baris 'do' pembuka blok lama dan indentasi tidak perlu diubah (tetap)

KEPALA = """local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")
local UserInputService = game:GetService("UserInputService")

local CropData = require(ReplicatedStorage.Shared.CropData)
local Net = require(ReplicatedStorage.Remotes)
local UIStyle = require(ReplicatedStorage.Shared.UIStyle)
local TasLogic = require(ReplicatedStorage.Shared.TasLogic)
local TradeLogic = require(ReplicatedStorage.Shared.TradeLogic)
local IkonKoin = require(ReplicatedStorage.Shared.IkonKoin)
local IkonTrade = require(ReplicatedStorage.Shared.IkonTrade)

-- TradeUI: seluruh UI trade antar pemain. Dibangun dengan konteks dari
-- UIController (helper mk/round/warna, panel system, state bersama).
local TradeUI = {}

function TradeUI.bangun(ctx: any)
        local mk = ctx.mk
        local round = ctx.round
        local warna = ctx.warna
        local toast = ctx.toast
        local fmt = ctx.fmt
        local ikonSlot = ctx.ikonSlot
        local makePanel = ctx.makePanel
        local openPanel = ctx.openPanel
        local closePanel = ctx.closePanel
        local panelAktif = ctx.panelAktif
        local state = ctx.state
        local tradeLanjutBtn = ctx.tradeLanjutBtn
        local gui = ctx.gui
        local playerGui = ctx.playerGui
        local player = ctx.player
        local camera = ctx.camera
        local FON = ctx.FON
        local FONTB = ctx.FONTB
"""

EKOR = """
end

return TradeUI
"""

badan = "\n".join(seksi)
# referensi currentPanel -> panelAktif()
badan = badan.replace("currentPanel == \"trade\"", "panelAktif() == \"trade\"")
badan = badan.replace("currentPanel ~= \"trade\"", "panelAktif() ~= \"trade\"")

modul = KEPALA + "\n" + badan + EKOR
TRADE.write_text(modul)

# ganti seksi di UIController dengan pemanggilan modul
pemanggil = """-- ===================== TRADE ANTAR PEMAIN =====================
-- Seluruh UI trade antar pemain kini tinggal di modul TradeUI (lihat
-- src/Client/TradeUI.luau): tap pemain lain -> kunci inggris -> konfirmasi ->
-- jendela trade dua kolom dengan sinkron server lewat TradeSync.
require(script.Parent.TradeUI).bangun({
        gui = gui,
        playerGui = playerGui,
        player = player,
        camera = camera,
        mk = mk,
        round = round,
        warna = warna,
        toast = toast,
        fmt = fmt,
        ikonSlot = ikonSlot,
        makePanel = makePanel,
        openPanel = openPanel,
        closePanel = closePanel,
        panelAktif = function()
                return currentPanel
        end,
        state = state,
        tradeLanjutBtn = tradeLanjutBtn,
        FON = FON,
        FONTB = FONTB,
})
-- ================== AKHIR TRADE ANTAR PEMAIN =================="""

baru = lines[:i_mulai] + pemanggil.split("\n") + lines[i_akhir + 2 :]
UI.write_text("\n".join(baru))
print("TradeUI.luau:", len(modul.split("\n")), "baris; UIController seksi diganti")
