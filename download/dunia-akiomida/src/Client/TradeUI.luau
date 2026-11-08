local Players = game:GetService("Players")
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

-- Alur: ketuk karakter pemain lain -> ikon kunci inggris muncul di atas
-- kepalanya -> ketuk ikon -> konfirmasi "Trade dengan (nama)?" -> server
-- membuat sesi -> jendela trade terbuka di kedua klien (tanpa dialog lagi).
-- Semua data tawaran datang dari server lewat TradeSync; klien hanya layar.
-- Kode dipecah beberapa do-block supaya register chunk tetap aman.
local hapusTargetTrade: (() -> ())? = nil
local bukaPemilihTrade: ((number) -> ())? = nil
local bukaMicdaTrade: (() -> ())? = nil
local refreshTrade: (() -> ())? = nil

do
        local tradeTarget: Player? = nil
        local billboardTrade: BillboardGui? = nil

        function hapusTargetTrade()
                if billboardTrade then
                        billboardTrade:Destroy()
                        billboardTrade = nil
                end
                tradeTarget = nil
        end

        Players.PlayerRemoving:Connect(function(p)
                if tradeTarget == p then
                        hapusTargetTrade()
                end
        end)

        -- ---------- modal konfirmasi ajakan ----------
        local ajakDim = mk("Frame", { Name = "ModalTradeAjak", Size = UDim2.new(1, 0, 1, 0), BackgroundColor3 = Color3.new(0, 0, 0), BackgroundTransparency = 0.5, Visible = false, Active = true, ZIndex = 5 }, gui)
        local ajakBox = mk("Frame", { AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.new(0.5, 0, 0.5, 0), Size = UDim2.new(0.86, 0, 0, 190), BackgroundColor3 = warna(UIStyle.Latar), Active = true, ZIndex = 6 }, ajakDim)
        round(ajakBox, 12)
        mk("UISizeConstraint", { MinSize = Vector2.new(280, 180), MaxSize = Vector2.new(420, 240) }, ajakBox)
        mk("TextLabel", { Size = UDim2.new(1, -24, 0, 30), Position = UDim2.new(0, 12, 0, 12), BackgroundTransparency = 1, Text = "Ajak Trade", TextSize = UIStyle.UkuranJudul, Font = FONTB, TextColor3 = warna(UIStyle.Teks), TextXAlignment = Enum.TextXAlignment.Left, ZIndex = 6 }, ajakBox)
        local ajakIsi = mk("TextLabel", { Size = UDim2.new(1, -24, 0, 44), Position = UDim2.new(0, 12, 0, 46), BackgroundTransparency = 1, Text = "", TextSize = UIStyle.UkuranIsi, Font = FON, TextColor3 = warna(UIStyle.Abu), TextXAlignment = Enum.TextXAlignment.Left, TextWrapped = true, ZIndex = 6 }, ajakBox)
        local ajakYa = mk("TextButton", { Size = UDim2.new(0.5, -9, 0, 44), Position = UDim2.new(0, 12, 1, -56), BackgroundColor3 = warna(UIStyle.Hijau), Text = "Ya, Ajak Trade", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = Color3.new(1, 1, 1), ZIndex = 6 }, ajakBox)
        round(ajakYa, UIStyle.SudutKecil)
        local ajakBatal = mk("TextButton", { Size = UDim2.new(0.5, -9, 0, 44), Position = UDim2.new(0.5, 9, 1, -56), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "Batal", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = warna(UIStyle.Teks), ZIndex = 6 }, ajakBox)
        round(ajakBatal, UIStyle.SudutKecil)
        ajakBatal.Activated:Connect(function()
                ajakDim.Visible = false
        end)
        ajakYa.Activated:Connect(function()
                local p = tradeTarget
                ajakDim.Visible = false
                if not p then
                        return
                end
                task.spawn(function()
                        local ok, msg = Net.get("TradeAct"):InvokeServer("ajukan", p.UserId)
                        if not ok then
                                toast("Trade", tostring(msg))
                        end
                end)
        end)

        -- ---------- billboard kunci inggris di atas kepala target ----------
        local function bukaKonfirmasiTrade(p: Player)
                tradeTarget = p
                ajakIsi.Text = "Trade dengan " .. UIStyle.potong((p.DisplayName and p.DisplayName ~= "" and p.DisplayName) or p.Name) .. "?"
                ajakDim.Visible = true
        end

        local function tunjukTarget(p: Player)
                hapusTargetTrade()
                local char = p.Character
                local kepala = char and (char:FindFirstChild("Head") or char.PrimaryPart)
                if not kepala then
                        return
                end
                tradeTarget = p
                local bb = mk("BillboardGui", {
                        Name = "TawarkanTrade",
                        Adornee = kepala,
                        Size = UDim2.fromOffset(120, 52),
                        StudsOffset = Vector3.new(0, 3, 0),
                        AlwaysOnTop = true,
                        MaxDistance = 90,
                }, playerGui)
                local tombol = mk("TextButton", { Size = UDim2.fromScale(1, 1), BackgroundColor3 = warna(UIStyle.Latar), BackgroundTransparency = 0.06, Text = "", AutoButtonColor = true }, bb)
                round(tombol, UIStyle.SudutKecil)
                IkonTrade.buat(tombol, 30, warna(UIStyle.Latar))
                mk("TextLabel", { AnchorPoint = Vector2.new(0.5, 1), Position = UDim2.new(0.5, 0, 1, -2), Size = UDim2.new(1, -8, 0, 14), BackgroundTransparency = 1, Text = "TRADE", TextSize = UIStyle.UkuranKecil, Font = FONTB, TextColor3 = warna(UIStyle.Teks) }, tombol)
                tombol.Activated:Connect(function()
                        if tradeTarget == p then
                                bukaKonfirmasiTrade(p)
                        end
                end)
                billboardTrade = bb
                task.delay(10, function()
                        if billboardTrade == bb then
                                hapusTargetTrade()
                        end
                end)
        end

        -- Ketukan (touch/klik) di dunia: cari karakter pemain lain di bawah jari.
        UserInputService.InputBegan:Connect(function(input, processed)
                if processed then
                        return
                end
                local t = input.UserInputType
                if t ~= Enum.UserInputType.Touch and t ~= Enum.UserInputType.MouseButton1 then
                        return
                end
                if panelAktif() == "trade" or state.trade or ajakDim.Visible then
                        return
                end
                local ok, target = pcall(function()
                        local pos = input.Position
                        local unit = camera:ViewportPointToRay(pos.X, pos.Y)
                        local char = player.Character
                        local params = RaycastParams.new()
                        params.FilterType = Enum.RaycastFilterType.Exclude
                        params.FilterDescendantsInstances = char and { char } or {}
                        local hit = Workspace:Raycast(unit.Origin, unit.Direction * 320, params)
                        if not hit or not hit.Instance then
                                return nil
                        end
                        local node = hit.Instance.Parent
                        while node do
                                if node:FindFirstChildOfClass("Humanoid") then
                                        return Players:GetPlayerFromCharacter(node)
                                end
                                node = node.Parent
                        end
                        return nil
                end)
                if ok and target and target ~= player then
                        tunjukTarget(target)
                end
        end)
end

do
        -- ---------- panel trade ----------
        local tradePanel = makePanel("trade")

        local tradeLawanLabel = mk("TextLabel", { Size = UDim2.new(1, 0, 0, 28), BackgroundTransparency = 1, Text = "Trade dengan ...", TextSize = UIStyle.UkuranJudul, Font = FONTB, TextColor3 = warna(UIStyle.Teks), TextXAlignment = Enum.TextXAlignment.Left }, tradePanel)
        local tradeFaseLabel = mk("TextLabel", { Size = UDim2.new(1, 0, 0, 22), BackgroundTransparency = 1, Text = "", TextSize = UIStyle.UkuranKecil, Font = FON, TextColor3 = warna(UIStyle.Abu), TextXAlignment = Enum.TextXAlignment.Left }, tradePanel)

        local function kolomTrade(parent: Frame, judul: string): any
                local kolom = mk("Frame", { BackgroundTransparency = 1 }, parent)
                mk("TextLabel", { Size = UDim2.new(1, 0, 0, 22), BackgroundTransparency = 1, Text = judul, TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = warna(UIStyle.Aksen), TextXAlignment = Enum.TextXAlignment.Left }, kolom)
                local grid = mk("Frame", { Size = UDim2.new(1, 0, 0, 148), Position = UDim2.new(0, 0, 0, 24), BackgroundTransparency = 1 }, kolom)
                mk("UIGridLayout", { CellSize = UDim2.new(0.5, -5, 0, 70), CellPadding = UDim2.new(0, 8, 0, 8), SortOrder = Enum.SortOrder.LayoutOrder }, grid)
                local slots = {}
                for i = 1, 4 do
                        local cell = mk("TextButton", { BackgroundColor3 = warna(UIStyle.Permukaan), Text = "", LayoutOrder = i }, grid)
                        round(cell, UIStyle.SudutKecil)
                        slots[i] = cell
                end
                local micdaSlot = mk("TextButton", { Size = UDim2.new(1, 0, 0, 44), Position = UDim2.new(0, 0, 0, 182), BackgroundColor3 = warna(UIStyle.Permukaan), Text = "" }, kolom)
                round(micdaSlot, UIStyle.SudutKecil)
                IkonKoin.buat(micdaSlot, 22).Position = UDim2.new(0, 8, 0.5, -11)
                local micdaL = mk("TextLabel", { Size = UDim2.new(1, -44, 1, 0), Position = UDim2.new(0, 40, 0, 0), BackgroundTransparency = 1, Text = "Micda: -", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = warna(UIStyle.Teks), TextXAlignment = Enum.TextXAlignment.Left, TextTruncate = Enum.TextTruncate.AtEnd }, micdaSlot)
                local statusL = mk("TextLabel", { Size = UDim2.new(1, 0, 0, 20), Position = UDim2.new(0, 0, 0, 232), BackgroundTransparency = 1, Text = "Belum siap", TextSize = UIStyle.UkuranKecil, Font = FONTB, TextColor3 = warna(UIStyle.Abu), TextXAlignment = Enum.TextXAlignment.Left }, kolom)
                return { kolom = kolom, slots = slots, micdaSlot = micdaSlot, micdaL = micdaL, statusL = statusL }
        end

        local tradeKolom = mk("Frame", { Size = UDim2.new(1, 0, 1, -118), Position = UDim2.new(0, 0, 0, 52), BackgroundTransparency = 1 }, tradePanel)
        local kolomKu = kolomTrade(tradeKolom, "Kamu")
        kolomKu.kolom.Size = UDim2.new(0.5, -6, 1, 0)
        local kolomLawan = kolomTrade(tradeKolom, "Lawan")
        kolomLawan.kolom.Position = UDim2.new(0.5, 6, 0, 0)
        kolomLawan.kolom.Size = UDim2.new(0.5, -6, 1, 0)

        local tradeSiapBtn = mk("TextButton", { AnchorPoint = Vector2.new(0, 1), Position = UDim2.new(0, 0, 1, -34), Size = UDim2.new(0.62, -6, 0, 46), BackgroundColor3 = warna(UIStyle.Hijau), Text = "Tawaran Siap", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = Color3.new(1, 1, 1) }, tradePanel)
        round(tradeSiapBtn, UIStyle.SudutKecil)
        local tradeKonfirmBtn = mk("TextButton", { AnchorPoint = Vector2.new(0, 1), Position = UDim2.new(0, 0, 1, -34), Size = UDim2.new(0.62, -6, 0, 46), BackgroundColor3 = warna(UIStyle.Kuning), Text = "Konfirmasi Trade", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = warna(UIStyle.Latar), Visible = false }, tradePanel)
        round(tradeKonfirmBtn, UIStyle.SudutKecil)
        local tradeBatalBtn = mk("TextButton", { AnchorPoint = Vector2.new(1, 1), Position = UDim2.new(1, 0, 1, -34), Size = UDim2.new(0.38, -6, 0, 46), BackgroundColor3 = warna(UIStyle.Merah), Text = "Batal Trade", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = Color3.new(1, 1, 1) }, tradePanel)
        round(tradeBatalBtn, UIStyle.SudutKecil)

        local function tawaranSaya(): any
                if state.trade and type(state.trade.ku) == "table" then
                        return state.trade.ku
                end
                return { items = {}, micda = 0 }
        end

        local function isiSlot(cell: TextButton, e: any?, kosongTeks: string)
                for _, c in ipairs(cell:GetChildren()) do
                        if c:IsA("Frame") or c:IsA("TextLabel") then
                                c:Destroy()
                        end
                end
                if not e then
                        mk("TextLabel", { Size = UDim2.new(1, -8, 1, -8), Position = UDim2.new(0, 4, 0, 4), BackgroundTransparency = 1, Text = kosongTeks, TextSize = UIStyle.UkuranKecil, Font = FON, TextColor3 = warna(UIStyle.AbuGelap), TextWrapped = true }, cell)
                        return
                end
                ikonSlot(cell :: any, { kind = e.kind, id = e.id, count = e.count })
                local info = CropData.byId[e.id]
                local nama = e.kind == "benih" and CropData.namaBenih(e.id) or (info and info.nama or e.id)
                mk("TextLabel", { Size = UDim2.new(1, -40, 0, 30), Position = UDim2.new(0, 36, 0, 4), BackgroundTransparency = 1, Text = UIStyle.potong(nama, 14), TextSize = UIStyle.UkuranKecil, Font = FONTB, TextColor3 = warna(UIStyle.Teks), TextXAlignment = Enum.TextXAlignment.Left, TextWrapped = true }, cell)
                mk("TextLabel", { Size = UDim2.new(1, -8, 0, 16), Position = UDim2.new(0, 4, 1, -20), BackgroundTransparency = 1, Text = "x" .. tostring(e.count), TextSize = UIStyle.UkuranKecil, Font = FONTB, TextColor3 = warna(UIStyle.Aksen), TextXAlignment = Enum.TextXAlignment.Left }, cell)
        end

        refreshTrade = function()
                local p = state.trade
                if not p then
                        return
                end
                local judul = "Trade dengan " .. UIStyle.potong(tostring(p.lawan), 22)
                tradeFaseLabel.Text = p.fase == "konfirm" and "Tahap konfirmasi: tawaran dikunci. Sisa " .. tostring(p.sisa) .. " dtk." or "Atur tawaranmu. Sisa " .. tostring(p.sisa) .. " dtk."
                local ku = tawaranSaya()
                local lawan = (type(p.lawanTawar) == "table") and p.lawanTawar or { items = {}, micda = 0 }
                local terkunci = p.fase == "konfirm"
                for i = 1, 4 do
                        local e = ku.items[i]
                        isiSlot(kolomKu.slots[i], e, terkunci and "Kosong" or "+ Isi")
                        kolomKu.slots[i].AutoButtonColor = not terkunci
                end
                kolomKu.micdaL.Text = ku.micda > 0 and ("Micda: " .. fmt(ku.micda)) or "Micda: -"
                kolomKu.statusL.Text = (p.setujuKu and "Siap") or "Belum siap"
                kolomKu.statusL.TextColor3 = warna(p.setujuKu and UIStyle.Hijau or UIStyle.Abu)
                for i = 1, 4 do
                        local e = lawan.items[i]
                        isiSlot(kolomLawan.slots[i], e, "Kosong")
                        kolomLawan.slots[i].AutoButtonColor = false
                end
                kolomLawan.micdaL.Text = lawan.micda > 0 and ("Micda: " .. fmt(lawan.micda)) or "Micda: -"
                kolomLawan.statusL.Text = (p.setujuLawan and "Siap") or "Belum siap"
                kolomLawan.statusL.TextColor3 = warna(p.setujuLawan and UIStyle.Hijau or UIStyle.Abu)
                tradeSiapBtn.Visible = not terkunci
                tradeSiapBtn.Text = p.setujuKu and "Batal Siap" or "Tawaran Siap"
                tradeKonfirmBtn.Visible = terkunci
                tradeKonfirmBtn.Text = (p.konfirmKu and "Menunggu lawan...") or "Konfirmasi Trade"
                tradeKonfirmBtn.BackgroundColor3 = warna(p.konfirmKu and UIStyle.PermukaanAktif or UIStyle.Kuning)
                tradeLawanLabel.Text = judul .. (p.konfirmLawan and "  (lawan sudah konfirmasi)" or "")
        end

        tradeLanjutBtn.Activated:Connect(function()
                if state.trade then
                        openPanel("trade")
                        if refreshTrade then
                                refreshTrade()
                        end
                end
        end)

        tradeBatalBtn.Activated:Connect(function()
                task.spawn(function()
                        local ok, msg = Net.get("TradeAct"):InvokeServer("batal")
                        if not ok and msg ~= "Tidak ada trade yang berjalan." then
                                toast("Trade", tostring(msg))
                        end
                end)
        end)

        tradeSiapBtn.Activated:Connect(function()
                task.spawn(function()
                        local ok, msg = Net.get("TradeAct"):InvokeServer("setuju")
                        if not ok then
                                toast("Trade", tostring(msg))
                        end
                end)
        end)

        tradeKonfirmBtn.Activated:Connect(function()
                local p = state.trade
                if not p or p.konfirmKu then
                        return
                end
                task.spawn(function()
                        local ok, msg = Net.get("TradeAct"):InvokeServer("konfirm")
                        if not ok then
                                toast("Trade", tostring(msg))
                        end
                end)
        end)

        -- ketuk slotku: kosong = pilih item; terisi = tarik tawaran itu
        for i = 1, 4 do
                kolomKu.slots[i].Activated:Connect(function()
                        local p = state.trade
                        if not p or p.fase ~= "tawar" then
                                return
                        end
                        local ku = tawaranSaya()
                        if ku.items[i] then
                                local sisa = {}
                                for j, e in ipairs(ku.items) do
                                        if j ~= i then
                                                table.insert(sisa, { kind = e.kind, id = e.id, count = e.count })
                                        end
                                end
                                task.spawn(function()
                                        Net.get("TradeAct"):InvokeServer("ubah", { items = sisa, micda = ku.micda })
                                end)
                        else
                                if bukaPemilihTrade then
                                        bukaPemilihTrade(i)
                                end
                        end
                end)
        end

        kolomKu.micdaSlot.Activated:Connect(function()
                local p = state.trade
                if p and p.fase == "tawar" then
                        if bukaMicdaTrade then
                                bukaMicdaTrade()
                        end
                end
        end)
end

do
        -- ---------- modal pilih item + jumlah ----------
        local pilihDim = mk("Frame", { Name = "ModalTradePilih", Size = UDim2.new(1, 0, 1, 0), BackgroundColor3 = Color3.new(0, 0, 0), BackgroundTransparency = 0.5, Visible = false, Active = true, ZIndex = 5 }, gui)
        local pilihBox = mk("Frame", { AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.new(0.5, 0, 0.5, 0), Size = UDim2.new(0.88, 0, 0, 380), BackgroundColor3 = warna(UIStyle.Latar), Active = true, ZIndex = 6 }, pilihDim)
        round(pilihBox, 12)
        mk("UISizeConstraint", { MinSize = Vector2.new(300, 340), MaxSize = Vector2.new(440, 520) }, pilihBox)
        local pilihJudul = mk("TextLabel", { Size = UDim2.new(1, -24, 0, 30), Position = UDim2.new(0, 12, 0, 10), BackgroundTransparency = 1, Text = "Pilih Item untuk Trade", TextSize = UIStyle.UkuranJudul, Font = FONTB, TextColor3 = warna(UIStyle.Teks), TextXAlignment = Enum.TextXAlignment.Left, ZIndex = 6 }, pilihBox)
        local pilihDaftar = mk("ScrollingFrame", { Size = UDim2.new(1, -24, 1, -160), Position = UDim2.new(0, 12, 0, 44), BackgroundTransparency = 1, ScrollBarThickness = 6, AutomaticCanvasSize = Enum.AutomaticSize.Y, CanvasSize = UDim2.new(0, 0, 0, 0), ZIndex = 6 }, pilihBox)
        mk("UIListLayout", { Padding = UDim.new(0, 6), SortOrder = Enum.SortOrder.LayoutOrder }, pilihDaftar)
        local pilihQty = mk("TextBox", { Size = UDim2.new(1, -24, 0, 44), Position = UDim2.new(0, 12, 1, -104), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "1", PlaceholderText = "1", TextSize = UIStyle.UkuranJudul, Font = FONTB, TextColor3 = warna(UIStyle.Teks), ClearTextOnFocus = false, Visible = false, ZIndex = 6 }, pilihBox)
        local pilihKurang = mk("TextButton", { Size = UDim2.new(0.25, -6, 0, 40), Position = UDim2.new(0, 12, 1, -150), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "-", TextSize = UIStyle.UkuranJudul, Font = FONTB, TextColor3 = warna(UIStyle.Teks), Visible = false, ZIndex = 6 }, pilihBox)
        round(pilihKurang, UIStyle.SudutKecil)
        local pilihTambah = mk("TextButton", { Size = UDim2.new(0.25, -6, 0, 40), Position = UDim2.new(0.25, 6, 1, -150), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "+", TextSize = UIStyle.UkuranJudul, Font = FONTB, TextColor3 = warna(UIStyle.Teks), Visible = false, ZIndex = 6 }, pilihBox)
        round(pilihTambah, UIStyle.SudutKecil)
        local pilihMaks = mk("TextButton", { Size = UDim2.new(0.25, -6, 0, 40), Position = UDim2.new(0.5, 6, 1, -150), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "Maks", TextSize = UIStyle.UkuranKecil, Font = FONTB, TextColor3 = warna(UIStyle.Teks), Visible = false, ZIndex = 6 }, pilihBox)
        round(pilihMaks, UIStyle.SudutKecil)
        local pilihHapus = mk("TextButton", { Size = UDim2.new(0.25, -6, 0, 40), Position = UDim2.new(0.75, 6, 1, -150), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "Hapus", TextSize = UIStyle.UkuranKecil, Font = FONTB, TextColor3 = warna(UIStyle.Teks), Visible = false, ZIndex = 6 }, pilihBox)
        round(pilihHapus, UIStyle.SudutKecil)
        local pilihPasang = mk("TextButton", { Size = UDim2.new(0.5, -9, 0, 44), Position = UDim2.new(0, 12, 1, -56), BackgroundColor3 = warna(UIStyle.Hijau), Text = "Pasang", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = Color3.new(1, 1, 1), Visible = false, ZIndex = 6 }, pilihBox)
        round(pilihPasang, UIStyle.SudutKecil)
        local pilihKembali = mk("TextButton", { Size = UDim2.new(0.5, -9, 0, 44), Position = UDim2.new(0.5, 9, 1, -56), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "Kembali", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = warna(UIStyle.Teks), Visible = false, ZIndex = 6 }, pilihBox)
        round(pilihKembali, UIStyle.SudutKecil)

        local pilihSlot: number? = nil
        local pilihEntri: any? = nil
        local modeJumlahItem: (() -> ())? = nil

        local function daftarTasTrade(): { any }
                local tawar = state.trade and type(state.trade.ku) == "table" and state.trade.ku or { items = {}, micda = 0 }
                local kunci = TradeLogic.kunciOf(tawar)
                local out = {}
                for _, kind in ipairs({ "benih", "hasil" }) do
                        for _, r in ipairs(TasLogic.ringkas(state.tas, kind)) do
                                local bebas = r.count - (kunci[kind .. ":" .. r.id] or 0)
                                if bebas > 0 then
                                        table.insert(out, { kind = kind, id = r.id, count = bebas })
                                end
                        end
                end
                return out
        end

        local function modePilihItem()
                pilihJudul.Text = "Pilih Item untuk Trade"
                pilihDaftar.Visible = true
                pilihQty.Visible = false
                pilihKurang.Visible = false
                pilihTambah.Visible = false
                pilihMaks.Visible = false
                pilihHapus.Visible = false
                pilihPasang.Visible = false
                pilihKembali.Visible = false
                for _, c in ipairs(pilihDaftar:GetChildren()) do
                        if c:IsA("TextButton") then
                                c:Destroy()
                        end
                end
                local daftar = daftarTasTrade()
                if #daftar == 0 then
                        mk("TextLabel", { Size = UDim2.new(1, 0, 0, 40), BackgroundTransparency = 1, Text = "Tasmu kosong untuk ditawarkan.", TextSize = UIStyle.UkuranIsi, Font = FON, TextColor3 = warna(UIStyle.Abu), ZIndex = 6 }, pilihDaftar)
                        return
                end
                for i, e in ipairs(daftar) do
                        local baris = mk("TextButton", { Size = UDim2.new(1, -8, 0, 40), BackgroundColor3 = warna(UIStyle.Permukaan), Text = "", LayoutOrder = i, ZIndex = 6 }, pilihDaftar)
                        round(baris, UIStyle.SudutKecil)
                        ikonSlot(baris :: any, e)
                        local info = CropData.byId[e.id]
                        local nama = e.kind == "benih" and CropData.namaBenih(e.id) or (info and info.nama or e.id)
                        mk("TextLabel", { Size = UDim2.new(1, -90, 1, 0), Position = UDim2.new(0, 40, 0, 0), BackgroundTransparency = 1, Text = UIStyle.potong(nama), TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = warna(UIStyle.Teks), TextXAlignment = Enum.TextXAlignment.Left, ZIndex = 6 }, baris)
                        mk("TextLabel", { Size = UDim2.new(0, 44, 1, 0), Position = UDim2.new(1, -48, 0, 0), BackgroundTransparency = 1, Text = "x" .. tostring(e.count), TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = warna(UIStyle.Aksen), TextXAlignment = Enum.TextXAlignment.Right, ZIndex = 6 }, baris)
                        baris.Activated:Connect(function()
                                pilihEntri = e
                                pilihQty.Text = "1"
                                if modeJumlahItem then
                                        modeJumlahItem()
                                end
                        end)
                end
        end

        modeJumlahItem = function()
                pilihJudul.Text = "Atur Jumlah Tawaran"
                pilihDaftar.Visible = false
                pilihQty.Visible = true
                pilihKurang.Visible = true
                pilihTambah.Visible = true
                pilihMaks.Visible = true
                pilihHapus.Visible = true
                pilihPasang.Visible = true
                pilihKembali.Visible = true
        end

        local function qtySekarang(maks: number): number
                local v = tonumber(pilihQty.Text)
                if not v or v ~= v or v < 1 then
                        return 1
                end
                v = math.floor(v)
                if v > maks then
                        return maks
                end
                return v
        end

        pilihKurang.Activated:Connect(function()
                local maks = pilihEntri and pilihEntri.count or 1
                pilihQty.Text = tostring(math.max(1, qtySekarang(maks) - 1))
        end)
        pilihTambah.Activated:Connect(function()
                local maks = pilihEntri and pilihEntri.count or 1
                pilihQty.Text = tostring(math.min(maks, qtySekarang(maks) + 1))
        end)
        pilihMaks.Activated:Connect(function()
                if pilihEntri then
                        pilihQty.Text = tostring(pilihEntri.count)
                end
        end)
        pilihHapus.Activated:Connect(function()
                pilihQty.Text = "1"
        end)
        pilihKembali.Activated:Connect(function()
                modePilihItem()
        end)
        pilihPasang.Activated:Connect(function()
                local slot = pilihSlot
                local e = pilihEntri
                if not slot or not e then
                        return
                end
                local n = qtySekarang(e.count)
                local tawar = state.trade and type(state.trade.ku) == "table" and state.trade.ku or { items = {}, micda = 0 }
                local sisa = {}
                for j, lama in ipairs(tawar.items) do
                        if j ~= slot and not (lama.kind == e.kind and lama.id == e.id) then
                                table.insert(sisa, { kind = lama.kind, id = lama.id, count = lama.count })
                        end
                end
                table.insert(sisa, { kind = e.kind, id = e.id, count = n })
                pilihDim.Visible = false
                pilihSlot = nil
                pilihEntri = nil
                task.spawn(function()
                        local ok, msg = Net.get("TradeAct"):InvokeServer("ubah", { items = sisa, micda = tawar.micda })
                        if not ok then
                                toast("Trade", tostring(msg))
                        end
                end)
        end)

        bukaPemilihTrade = function(slot: number)
                local p = state.trade
                if not p or p.fase ~= "tawar" then
                        return
                end
                pilihSlot = slot
                pilihEntri = nil
                modePilihItem()
                pilihDim.Visible = true
        end
end

do
        -- ---------- modal micda ----------
        local micdaDim = mk("Frame", { Name = "ModalTradeMicda", Size = UDim2.new(1, 0, 1, 0), BackgroundColor3 = Color3.new(0, 0, 0), BackgroundTransparency = 0.5, Visible = false, Active = true, ZIndex = 5 }, gui)
        local micdaBox = mk("Frame", { AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.new(0.5, 0, 0.5, 0), Size = UDim2.new(0.86, 0, 0, 300), BackgroundColor3 = warna(UIStyle.Latar), Active = true, ZIndex = 6 }, micdaDim)
        round(micdaBox, 12)
        mk("UISizeConstraint", { MinSize = Vector2.new(300, 280), MaxSize = Vector2.new(440, 360) }, micdaBox)
        local micdaStok = mk("TextLabel", { Size = UDim2.new(1, -24, 0, 20), Position = UDim2.new(0, 12, 0, 42), BackgroundTransparency = 1, Text = "", TextSize = UIStyle.UkuranKecil, Font = FON, TextColor3 = warna(UIStyle.Abu), TextXAlignment = Enum.TextXAlignment.Left, ZIndex = 6 }, micdaBox)
        local micdaQty = mk("TextBox", { Size = UDim2.new(1, -24, 0, 44), Position = UDim2.new(0, 12, 0, 66), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "0", PlaceholderText = "0", TextSize = UIStyle.UkuranJudul, Font = FONTB, TextColor3 = warna(UIStyle.Teks), ClearTextOnFocus = false, ZIndex = 6 }, micdaBox)
        local function tombolMicda(teks: string, urut: number): TextButton
                local b = mk("TextButton", { Size = UDim2.new(0.25, -6, 0, 38), Position = UDim2.new((urut - 1) % 4 * 0.25, 12, 0, 118), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = teks, TextSize = UIStyle.UkuranKecil, Font = FONTB, TextColor3 = warna(UIStyle.Teks), ZIndex = 6 }, micdaBox)
                round(b, UIStyle.SudutKecil)
                return b
        end
        local micdaM1 = tombolMicda("-1 Rb", 1)
        local micdaP1 = tombolMicda("+1 Rb", 2)
        local micdaM10 = tombolMicda("-10 Rb", 3)
        local micdaP10 = tombolMicda("+10 Rb", 4)
        local micdaMaks = tombolMicda("Maks", 5)
        micdaMaks.Position = UDim2.new(0, 12, 0, 160)
        local micdaHapus = tombolMicda("Hapus", 6)
        micdaHapus.Position = UDim2.new(0.25, 6, 0, 160)
        local micdaPasang = mk("TextButton", { Size = UDim2.new(0.5, -9, 0, 44), Position = UDim2.new(0, 12, 1, -56), BackgroundColor3 = warna(UIStyle.Hijau), Text = "Pasang", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = Color3.new(1, 1, 1), ZIndex = 6 }, micdaBox)
        round(micdaPasang, UIStyle.SudutKecil)
        local micdaBatal = mk("TextButton", { Size = UDim2.new(0.5, -9, 0, 44), Position = UDim2.new(0.5, 9, 1, -56), BackgroundColor3 = warna(UIStyle.PermukaanAktif), Text = "Batal", TextSize = UIStyle.UkuranIsi, Font = FONTB, TextColor3 = warna(UIStyle.Teks), ZIndex = 6 }, micdaBox)
        round(micdaBatal, UIStyle.SudutKecil)
        micdaBatal.Activated:Connect(function()
                micdaDim.Visible = false
        end)

        local function micdaSekarang(): number
                local v = tonumber(micdaQty.Text)
                if not v or v ~= v or v < 0 then
                        return 0
                end
                return math.floor(v)
        end

        local function langkahMicda(delta: number)
                local maks = state.micda or 0
                local v = micdaSekarang() + delta
                if v < 0 then
                        v = 0
                end
                if v > maks then
                        v = maks
                end
                micdaQty.Text = tostring(v)
        end

        micdaM1.Activated:Connect(function()
                langkahMicda(-1000)
        end)
        micdaP1.Activated:Connect(function()
                langkahMicda(1000)
        end)
        micdaM10.Activated:Connect(function()
                langkahMicda(-10000)
        end)
        micdaP10.Activated:Connect(function()
                langkahMicda(10000)
        end)
        micdaMaks.Activated:Connect(function()
                micdaQty.Text = tostring(math.max(0, state.micda or 0))
        end)
        micdaHapus.Activated:Connect(function()
                micdaQty.Text = "0"
        end)
        micdaPasang.Activated:Connect(function()
                local tawar = state.trade and type(state.trade.ku) == "table" and state.trade.ku or { items = {}, micda = 0 }
                local v = micdaSekarang()
                micdaDim.Visible = false
                task.spawn(function()
                        local ok, msg = Net.get("TradeAct"):InvokeServer("ubah", { items = tawar.items, micda = v })
                        if not ok then
                                toast("Trade", tostring(msg))
                        end
                end)
        end)

        bukaMicdaTrade = function()
                local p = state.trade
                if not p or p.fase ~= "tawar" then
                        return
                end
                micdaStok.Text = "Saldo kamu: " .. fmt(state.micda or 0) .. " Micda"
                local tawar = state.trade and type(state.trade.ku) == "table" and state.trade.ku or { items = {}, micda = 0 }
                micdaQty.Text = tostring(tawar.micda or 0)
                micdaDim.Visible = true
        end
end

-- ---------- sinkron dari server ----------
Net.get("TradeSync").OnClientEvent:Connect(function(p)
        state.trade = p
        if type(p) == "table" and p.penutup then
                toast(p.penutup == "sukses" and "Trade Berhasil" or "Trade", tostring(p.pesan or ""))
                state.trade = nil
                if hapusTargetTrade then
                        hapusTargetTrade()
                end
                tradeLanjutBtn.Visible = false
                if panelAktif() == "trade" then
                        closePanel()
                end
                return
        end
        if type(p) ~= "table" then
                return
        end
        tradeLanjutBtn.Visible = true
        if panelAktif() ~= "trade" then
                openPanel("trade")
        end
        if refreshTrade then
                refreshTrade()
        end
end)

end

return TradeUI
