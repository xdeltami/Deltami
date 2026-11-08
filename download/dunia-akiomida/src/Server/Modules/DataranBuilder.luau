local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local BuildingKit = require(script.Parent.BuildingKit)
local CropData = require(ReplicatedStorage.Shared.CropData)

local DataranBuilder = {}

-- Palet Dataran
local RUMPUT = Color3.fromRGB(106, 168, 79)
local RUMPUT_TUA = Color3.fromRGB(88, 142, 66)
local TANAH = Color3.fromRGB(134, 100, 62)
local JALAN = Color3.fromRGB(178, 168, 150)
local ASPAL = Color3.fromRGB(56, 58, 62)
local MARKA = Color3.fromRGB(236, 233, 224)
local TROTOAR = Color3.fromRGB(192, 187, 176)
local SEPEDA = Color3.fromRGB(174, 62, 48)
local KAYU = Color3.fromRGB(160, 110, 60)
local KAYU_TUA = Color3.fromRGB(112, 76, 42)
local DINDING = Color3.fromRGB(222, 206, 178)
local ATAP = Color3.fromRGB(168, 78, 58)
local BATU = Color3.fromRGB(142, 140, 134)
local AIR = Color3.fromRGB(96, 168, 220)
local KERING = Color3.fromRGB(196, 178, 108)
local PUTIH = Color3.fromRGB(238, 234, 224)
local BENDERA = {
        Color3.fromRGB(216, 84, 66),
        Color3.fromRGB(240, 196, 84),
        Color3.fromRGB(110, 168, 92),
        Color3.fromRGB(96, 148, 200),
}
local BUNGA_LIAR = {
        Color3.fromRGB(232, 96, 84),
        Color3.fromRGB(240, 196, 84),
        Color3.fromRGB(240, 240, 240),
        Color3.fromRGB(196, 130, 208),
        Color3.fromRGB(140, 190, 240),
}

local GT = 0

local function part(parent: Instance, size: Vector3, cf: CFrame, color: Color3, material: Enum.Material?, transparency: number?): Part
        return BuildingKit.part(parent, size, cf, color, material, transparency)
end

local function teksPapan(papan: Part, face: Enum.NormalId, teks: string)
        local gui = Instance.new("SurfaceGui")
        gui.Face = face
        gui.CanvasSize = Vector2.new(700, 220)
        gui.Parent = papan
        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(1, 0, 1, 0)
        label.BackgroundTransparency = 1
        label.Text = teks
        label.TextScaled = true
        label.Font = Enum.Font.GothamBold
        label.TextColor3 = Color3.fromRGB(42, 28, 14)
        label.Parent = gui
end

local function papanTeks(parent: Instance, x: number, z: number, teks: string, yaw: number, tinggi: number)
        part(parent, Vector3.new(0.5, tinggi, 0.5), CFrame.new(x, GT + tinggi / 2, z), KAYU_TUA, Enum.Material.Wood)
        local papan = part(parent, Vector3.new(7, 2.2, 0.3), CFrame.new(x, GT + tinggi + 0.4, z) * CFrame.Angles(0, yaw, 0), KAYU, Enum.Material.Wood)
        teksPapan(papan, Enum.NormalId.Front, teks)
        teksPapan(papan, Enum.NormalId.Back, teks)
        return papan
end

-- y0 = ketinggian lantai tempat bangku berdiri (plaza alun-alun lebih
-- tinggi dari tanah, jadi perabotnya harus ikut naik agar tidak terkubur).
local function bangku(parent: Instance, x: number, z: number, yaw: number, y0: number?)
        local y = y0 or GT
        local m = Instance.new("Model")
        m.Name = "BangkuTaman"
        m.Parent = parent
        local dudukan = part(m, Vector3.new(3.2, 0.3, 1.1), CFrame.new(x, y + 0.85, z) * CFrame.Angles(0, yaw, 0), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(3.2, 1.1, 0.25), CFrame.new(x, y + 1.5, z) * CFrame.Angles(0, yaw, 0) * CFrame.new(0, 0, -0.45), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(0.3, 0.85, 1), CFrame.new(x, y + 0.43, z) * CFrame.Angles(0, yaw, 0) * CFrame.new(-1.3, 0, 0), KAYU_TUA, Enum.Material.Wood)
        part(m, Vector3.new(0.3, 0.85, 1), CFrame.new(x, y + 0.43, z) * CFrame.Angles(0, yaw, 0) * CFrame.new(1.3, 0, 0), KAYU_TUA, Enum.Material.Wood)
        return dudukan
end

local function lampuTaman(parent: Instance, x: number, z: number, y0: number?)
        local y = y0 or GT
        local m = Instance.new("Model")
        m.Name = "LampuTaman"
        m.Parent = parent
        part(m, Vector3.new(0.4, 3.6, 0.4), CFrame.new(x, y + 1.8, z), KAYU_TUA, Enum.Material.Metal)
        local bola = part(m, Vector3.new(1, 1, 1), CFrame.new(x, y + 3.9, z), PUTIH, Enum.Material.Neon)
        bola.Shape = Enum.PartType.Ball
        local cahaya = Instance.new("PointLight")
        cahaya.Range = 14
        cahaya.Brightness = 1.1
        cahaya.Color = Color3.fromRGB(255, 226, 160)
        cahaya.Parent = bola
end

local function pohonAlam(parent: Instance, x: number, z: number, skala: number?)
        local s = skala or 1
        local m = Instance.new("Model")
        m.Name = "PohonAlam"
        m.Parent = parent
        local tinggi = 4.5 * s
        part(m, Vector3.new(0.9 * s, tinggi, 0.9 * s), CFrame.new(x, GT + tinggi / 2, z), KAYU_TUA, Enum.Material.Wood)
        local daun1 = part(m, Vector3.new(4.4 * s, 3.6 * s, 4.4 * s), CFrame.new(x, GT + tinggi + 1.2, z), RUMPUT_TUA, Enum.Material.Grass)
        daun1.Shape = Enum.PartType.Ball
        local daun2 = part(m, Vector3.new(2.8 * s, 2.4 * s, 2.8 * s), CFrame.new(x + 1.1 * s, GT + tinggi + 1.9 * s, z - 0.7 * s), Color3.fromRGB(98, 156, 72), Enum.Material.Grass)
        daun2.Shape = Enum.PartType.Ball
end

local function batuAlam(parent: Instance, x: number, z: number, dia: number)
        local b = part(parent, Vector3.new(dia, dia * 0.8, dia), CFrame.new(x, GT + dia * 0.25, z), BATU, Enum.Material.Slate)
        b.Shape = Enum.PartType.Ball
end

local function bukit(parent: Instance, x: number, z: number, dia: number, tinggi: number)
        local b = part(parent, Vector3.new(dia, dia, dia), CFrame.new(x, GT - dia / 2 + tinggi, z), RUMPUT, Enum.Material.Grass)
        b.Shape = Enum.PartType.Ball
end

local function tanamanDemo(parent: Instance, x: number, z: number, cropId: string)
        local b = CropData.Bentuk[cropId]
        if not b then
                return
        end
        local w = Color3.fromRGB(b.warna[1], b.warna[2], b.warna[3])
        local tinggi = math.min(b.t, 2.6)
        if b.jenis == "pohon" then
                part(parent, Vector3.new(0.5, tinggi * 0.55, 0.5), CFrame.new(x, GT + tinggi * 0.28, z), KAYU_TUA, Enum.Material.Wood)
                local d = part(parent, Vector3.new(2.1, 2.1, 2.1), CFrame.new(x, GT + tinggi * 0.55 + 0.9, z), w, Enum.Material.Grass)
                d.Shape = Enum.PartType.Ball
        elseif b.jenis == "bulat" or b.jenis == "kacang" then
                local dia = math.min(b.w, 2)
                local d = part(parent, Vector3.new(dia, dia, dia), CFrame.new(x, GT + dia / 2, z), w, Enum.Material.Grass)
                d.Shape = Enum.PartType.Ball
        else
                part(parent, Vector3.new(math.max(b.w * 0.5, 0.5), tinggi, math.max(b.w * 0.5, 0.5)), CFrame.new(x, GT + tinggi / 2, z), w, Enum.Material.Grass)
        end
end

local function airMancur(parent: Instance, x: number, z: number)
        local m = Instance.new("Model")
        m.Name = "AirMancur"
        m.Parent = parent
        part(m, Vector3.new(15, 1, 15), CFrame.new(x, GT + 0.5, z), BATU, Enum.Material.Cobblestone)
        local bak = part(m, Vector3.new(1.4, 12.4, 12.4), CFrame.new(x, GT + 1.9, z) * CFrame.Angles(0, 0, math.rad(90)), BATU, Enum.Material.Cobblestone)
        bak.Shape = Enum.PartType.Cylinder
        local air = part(m, Vector3.new(0.6, 10.8, 10.8), CFrame.new(x, GT + 2.4, z) * CFrame.Angles(0, 0, math.rad(90)), AIR, Enum.Material.Glass, 0.35)
        air.Shape = Enum.PartType.Cylinder
        air.CanCollide = false
        part(m, Vector3.new(1.3, 3, 1.3), CFrame.new(x, GT + 3.4, z), BATU, Enum.Material.Cobblestone)
        local mangkuk = part(m, Vector3.new(0.9, 5.2, 5.2), CFrame.new(x, GT + 5.4, z) * CFrame.Angles(0, 0, math.rad(90)), BATU, Enum.Material.Cobblestone)
        mangkuk.Shape = Enum.PartType.Cylinder
        local semburan = part(m, Vector3.new(0.55, 2.6, 0.55), CFrame.new(x, GT + 7.2, z), AIR, Enum.Material.Glass, 0.45)
        semburan.CanCollide = false
        local pucuk = part(m, Vector3.new(0.9, 0.9, 0.9), CFrame.new(x, GT + 8.6, z), AIR, Enum.Material.Neon, 0.3)
        pucuk.Shape = Enum.PartType.Ball
        pucuk.CanCollide = false
end

local function gerbangKawasan(parent: Instance, x: number, z: number, yaw: number, nama: string, kode: string, warnaPilar: Color3, hooks)
        local m = Instance.new("Model")
        m.Name = "Gerbang" .. nama
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(2.2, 9, 2.2), cf * CFrame.new(-5.2, 4.5, 0), warnaPilar, Enum.Material.Wood)
        part(m, Vector3.new(2.2, 9, 2.2), cf * CFrame.new(5.2, 4.5, 0), warnaPilar, Enum.Material.Wood)
        local balok = part(m, Vector3.new(13.4, 1.7, 2.4), cf * CFrame.new(0, 9.5, 0), warnaPilar, Enum.Material.Wood)
        local papan = part(m, Vector3.new(9, 2.3, 0.4), cf * CFrame.new(0, 11.2, 0), KAYU, Enum.Material.Wood)
        teksPapan(papan, Enum.NormalId.Front, nama)
        teksPapan(papan, Enum.NormalId.Back, nama)
        local prompt = Instance.new("ProximityPrompt")
        prompt.ActionText = "Menuju " .. nama
        prompt.ObjectText = "Gerbang " .. nama
        prompt.HoldDuration = 0.5
        prompt.MaxActivationDistance = 12
        prompt.RequiresLineOfSight = false
        prompt.Parent = balok
        prompt.Triggered:Connect(function(player: Player)
                if hooks and hooks.onGerbangKawasan then
                        hooks.onGerbangKawasan(player, kode)
                end
        end)
end

-- ====================================================================
-- PERBAIKAN TENGGELAM: semua model yang dibangun di koordinat lokal
-- WAJIB menyetel WorldPivot ke titik tanah (0,0,0) sebelum PivotTo,
-- kalau tidak pivot model memakai tengah bounding box dan separuh
-- bangunan terkubur di tanah.
-- ====================================================================

local function rumahDesa(parent: Instance, x: number, z: number, menghadapTimur: boolean)
        local m = Instance.new("Model")
        m.Name = "RumahDesa"
        m.Parent = parent
        local yaw = menghadapTimur and math.rad(90) or math.rad(-90)
        part(m, Vector3.new(11, 0.5, 9), CFrame.new(0, 0.25, 0), KAYU, Enum.Material.WoodPlanks)
        part(m, Vector3.new(11, 5, 0.5), CFrame.new(0, 3, -4.25), DINDING, Enum.Material.WoodPlanks)
        part(m, Vector3.new(0.5, 5, 9), CFrame.new(-5.25, 3, 0), DINDING, Enum.Material.WoodPlanks)
        part(m, Vector3.new(0.5, 5, 9), CFrame.new(5.25, 3, 0), DINDING, Enum.Material.WoodPlanks)
        part(m, Vector3.new(4, 5, 0.5), CFrame.new(-3.5, 3, 4.25), DINDING, Enum.Material.WoodPlanks)
        part(m, Vector3.new(4, 5, 0.5), CFrame.new(3.5, 3, 4.25), DINDING, Enum.Material.WoodPlanks)
        part(m, Vector3.new(3, 0.8, 0.5), CFrame.new(0, 5.4, 4.25), DINDING, Enum.Material.WoodPlanks)
        local jendela = part(m, Vector3.new(0.3, 1.7, 2.2), CFrame.new(-5.3, 3.45, -1.5), AIR, Enum.Material.Glass, 0.45)
        jendela.CanCollide = false
        local jendela2 = part(m, Vector3.new(0.3, 1.7, 2.2), CFrame.new(5.3, 3.45, 1), AIR, Enum.Material.Glass, 0.45)
        jendela2.CanCollide = false
        -- tangga depan kecil agar pintu tidak menggantung
        part(m, Vector3.new(3, 0.4, 1.6), CFrame.new(0, 0.2, 5.05), BATU, Enum.Material.Concrete)
        BuildingKit.gableRoof(m, 12, 10, 2.6, 5.6, ATAP)
        m.WorldPivot = CFrame.new(0, 0, 0)
        m:PivotTo(CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0))
end

-- y0 = lantai pijakan NPC (plaza alun-alun 0.28 stud di atas tanah).
local function npc(parent: Instance, x: number, z: number, yaw: number, nama: string, warnaBaju: Color3, y0: number?)
        local m = Instance.new("Model")
        m.Name = "NPC " .. nama
        m.Parent = parent
        local cf = CFrame.new(x, y0 or GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(1.5, 1.7, 0.85), cf * CFrame.new(0, 0.85, 0), Color3.fromRGB(70, 76, 112), Enum.Material.Fabric)
        part(m, Vector3.new(2.1, 2, 1.05), cf * CFrame.new(0, 2.7, 0), warnaBaju, Enum.Material.Fabric)
        local kepala = part(m, Vector3.new(1.5, 1.5, 1.5), cf * CFrame.new(0, 4.4, 0), Color3.fromRGB(234, 190, 156), Enum.Material.SmoothPlastic)
        kepala.Shape = Enum.PartType.Ball
        part(m, Vector3.new(1.9, 0.45, 1.9), cf * CFrame.new(0, 5.25, 0), KAYU_TUA, Enum.Material.Wood)
        local gui = Instance.new("BillboardGui")
        gui.Size = UDim2.new(0, 120, 0, 30)
        gui.StudsOffset = Vector3.new(0, 3.4, 0)
        gui.AlwaysOnTop = true
        gui.Parent = kepala
        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(1, 0, 1, 0)
        label.BackgroundTransparency = 1
        label.Text = nama
        label.Font = Enum.Font.GothamBold
        label.TextSize = 16
        label.TextColor3 = Color3.new(1, 1, 1)
        label.TextStrokeTransparency = 0.4
        label.Parent = gui
        -- PERBAIKAN TENGGELAM NPC: bob animasi memakai pivot awal model
        -- (pivot bbox memusat di perut karakter, bukan di kaki).
        local pivot0 = m:GetPivot()
        task.spawn(function()
                local t = 0
                while m.Parent do
                        local dt = RunService.Heartbeat:Wait()
                        t += dt
                        m:PivotTo(pivot0 * CFrame.new(0, math.abs(math.sin(t * 2)) * 0.16, 0))
                end
        end)
end

local function kincirAngin(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "KincirAngin"
        m.Parent = parent
        local dasar = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(9, 1.2, 9), CFrame.new(0, 0.6, 0), BATU, Enum.Material.Slate)
        part(m, Vector3.new(6.4, 6, 6.4), CFrame.new(0, 4.2, 0), PUTIH, Enum.Material.WoodPlanks)
        part(m, Vector3.new(4.6, 5.4, 4.6), CFrame.new(0, 9.9, 0), PUTIH, Enum.Material.WoodPlanks)
        BuildingKit.gableRoof(m, 6, 6, 2.2, 12.6, ATAP)
        part(m, Vector3.new(1, 1, 1), CFrame.new(0, 10.4, -2.9), KAYU_TUA, Enum.Material.Wood)
        local bilah = {}
        for i = 1, 4 do
                bilah[i] = part(m, Vector3.new(0.7, 8, 0.28), CFrame.new(0, 10.4, -2.9), KAYU, Enum.Material.Wood)
        end
        m.WorldPivot = CFrame.new(0, 0, 0)
        m:PivotTo(dasar)
        task.spawn(function()
                local sudut = 0
                while m.Parent do
                        local dt = RunService.Heartbeat:Wait()
                        sudut += dt * 1.3
                        for i, b in ipairs(bilah) do
                                if b.Parent then
                                        b.CFrame = dasar * CFrame.new(0, 10.4, -2.9) * CFrame.Angles(0, 0, sudut + math.pi * (i - 1) / 2) * CFrame.new(0, 3.9, 0)
                                end
                        end
                end
        end)
end

local function sumur(parent: Instance, x: number, z: number)
        local m = Instance.new("Model")
        m.Name = "Sumur"
        m.Parent = parent
        local badan = part(m, Vector3.new(1.8, 3, 3), CFrame.new(0, 1.5, 0) * CFrame.Angles(0, 0, math.rad(90)), BATU, Enum.Material.Cobblestone)
        badan.Shape = Enum.PartType.Cylinder
        local air = part(m, Vector3.new(0.4, 2.4, 2.4), CFrame.new(0, 2.3, 0) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromRGB(40, 70, 110), Enum.Material.Glass, 0.2)
        air.Shape = Enum.PartType.Cylinder
        air.CanCollide = false
        part(m, Vector3.new(0.4, 3.4, 0.4), CFrame.new(-1.4, 1.7, 0), KAYU_TUA, Enum.Material.Wood)
        part(m, Vector3.new(0.4, 3.4, 0.4), CFrame.new(1.4, 1.7, 0), KAYU_TUA, Enum.Material.Wood)
        BuildingKit.gableRoof(m, 3.6, 3.4, 1.2, 3.4, ATAP)
        local ember = part(m, Vector3.new(0.8, 0.7, 0.8), CFrame.new(0, 2.4, 0), KAYU, Enum.Material.Wood)
        ember.CanCollide = false
        m.WorldPivot = CFrame.new(0, 0, 0)
        m:PivotTo(CFrame.new(x, GT, z))
end

local function gerobak(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "Gerobak"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(3.6, 1.3, 2.1), cf * CFrame.new(0, 1.25, 0), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(3.7, 0.35, 2.2), cf * CFrame.new(0, 2, 0), KAYU_TUA, Enum.Material.Wood)
        local roda1 = part(m, Vector3.new(0.35, 1.5, 1.5), cf * CFrame.new(-1.4, 0.75, 0) * CFrame.Angles(0, math.rad(90), 0), KAYU_TUA, Enum.Material.Wood)
        roda1.Shape = Enum.PartType.Cylinder
        local roda2 = part(m, Vector3.new(0.35, 1.5, 1.5), cf * CFrame.new(1.4, 0.75, 0) * CFrame.Angles(0, math.rad(90), 0), KAYU_TUA, Enum.Material.Wood)
        roda2.Shape = Enum.PartType.Cylinder
        local pegangan = part(m, Vector3.new(1.8, 0.3, 0.3), cf * CFrame.new(2.5, 1.5, 0) * CFrame.Angles(0, 0, math.rad(-24)), KAYU_TUA, Enum.Material.Wood)
        pegangan.CanCollide = false
        part(m, Vector3.new(1, 0.8, 1), cf * CFrame.new(-0.7, 2.35, 0), TANAH, Enum.Material.Ground)
        part(m, Vector3.new(0.9, 0.7, 0.9), cf * CFrame.new(0.5, 2.3, 0.2), RUMPUT_TUA, Enum.Material.Grass)
end

-- ====================================================================
-- MASTERPLAN JALAN: aspal + marka + trotoar + jalur sepeda
-- ====================================================================

local function dalamSkip(skips, v: number): boolean
        if not skips then
                return false
        end
        for _, r in ipairs(skips) do
                if v >= r[1] and v <= r[2] then
                        return true
                end
        end
        return false
end

-- Jalan aspal dua arah: slab aspal + marka putus-putus + trotoar timbul
-- dua sisi + jalur sepeda merah dua sisi. Sumbu jalan mengikuti sisi
-- terpanjang dari (ax,az)->(bx,bz).
local function jalanAspal(parent: Instance, ax: number, az: number, bx: number, bz: number, o)
        o = o or {}
        local lebar = o.lebar or 12
        local tebal = o.tebal or 0.2
        local horizontal = math.abs(bx - ax) >= math.abs(bz - az)
        local len = horizontal and (bx - ax) or (bz - az)
        local abslen = math.abs(len)
        local cx, cz = (ax + bx) / 2, (az + bz) / 2
        local m = Instance.new("Model")
        m.Name = "Jalan_" .. (o.nama or "Aspal")
        m.Parent = parent
        local rot = horizontal and 0 or math.rad(90)
        local cf0 = CFrame.new(cx, GT, cz) * CFrame.Angles(0, rot, 0)
        local aspal = part(m, Vector3.new(abslen, tebal, lebar), cf0 * CFrame.new(0, tebal / 2, 0), ASPAL, Enum.Material.Asphalt)
        aspal.Name = "JalanAspal"
        local nDash = math.floor((abslen - 6) / 7)
        for i = 0, nDash - 1 do
                local along = -abslen / 2 + 6 + i * 7
                if math.abs(along) < abslen / 2 - 2 then
                        local dash = part(m, Vector3.new(2.6, 0.06, 0.45), cf0 * CFrame.new(along, tebal + 0.07, 0), MARKA, Enum.Material.SmoothPlastic)
                        dash.Name = "MarkaPutih"
                        dash.CanCollide = false
                end
        end
        for _, s in ipairs({ -1, 1 }) do
                local trotoar = part(m, Vector3.new(abslen, 0.35, 2.4), cf0 * CFrame.new(0, 0.175, s * (lebar / 2 + 0.8)), TROTOAR, Enum.Material.Concrete)
                trotoar.Name = "Trotoar"
                local jalur = part(m, Vector3.new(abslen, 0.08, 2), cf0 * CFrame.new(0, tebal + 0.05, s * (lebar / 2 - 1.5)), SEPEDA, Enum.Material.SmoothPlastic)
                jalur.Name = "JalurSepeda"
                jalur.CanCollide = false
        end
        return m, horizontal, cx, cz, abslen
end

-- Lampu jalan + pohon pinggir jalan, bolak-balik sisi, dengan daftar
-- rentang koordinat yang dilewati (persimpangan/zebra/gerbang).
local function hiasJalan(parent: Instance, horizontal: boolean, cx: number, cz: number, abslen: number, lebar: number, skips)
        local s = -abslen / 2 + 14
        local k = 0
        while s <= abslen / 2 - 14 do
                local pusatSum = horizontal and cx or cz
                if not dalamSkip(skips, pusatSum + s) then
                        local side = (k % 2 == 0) and -1 or 1
                        local lx, lz
                        if horizontal then
                                lx, lz = cx + s, cz + side * (lebar / 2 + 1.2)
                        else
                                lx, lz = cx + side * (lebar / 2 + 1.2), cz + s
                        end
                        lampuTaman(parent, lx, lz)
                        local ta = s + 15
                        if not dalamSkip(skips, pusatSum + ta) then
                                local tx, tz
                                if horizontal then
                                        tx, tz = cx + ta, cz - side * (lebar / 2 + 2.8)
                                else
                                        tx, tz = cx - side * (lebar / 2 + 2.8), cz + ta
                                end
                                pohonAlam(parent, tx, tz, 0.72)
                        end
                end
                s += 30
                k += 1
        end
end

-- Zebra cross: batang putih memanjang searah jalan, berulang melintang
-- lebar jalan (gaya piano).
local function zebraCross(parent: Instance, cx: number, cz: number, horizontal: boolean)
        for i = 0, 9 do
                local off = -4.5 + i * 1
                local p
                if horizontal then
                        p = part(parent, Vector3.new(2.6, 0.06, 0.55), CFrame.new(cx, GT + 0.275, cz + off), MARKA, Enum.Material.SmoothPlastic)
                else
                        p = part(parent, Vector3.new(0.55, 0.06, 2.6), CFrame.new(cx + off, GT + 0.275, cz), MARKA, Enum.Material.SmoothPlastic)
                end
                p.Name = "ZebraCross"
                p.CanCollide = false
        end
end

local function benderaHias(parent: Instance, x1: number, z1: number, x2: number, z2: number, y0: number?)
        local y = y0 or GT
        local m = Instance.new("Model")
        m.Name = "BenderaHias"
        m.Parent = parent
        local tinggi = 5.5
        part(m, Vector3.new(0.3, tinggi, 0.3), CFrame.new(x1, y + tinggi / 2, z1), KAYU_TUA, Enum.Material.Wood)
        part(m, Vector3.new(0.3, tinggi, 0.3), CFrame.new(x2, y + tinggi / 2, z2), KAYU_TUA, Enum.Material.Wood)
        local panjang = math.sqrt((x2 - x1) ^ 2 + (z2 - z1) ^ 2)
        local yaw = math.atan2(z2 - z1, x2 - x1)
        local cfTali = CFrame.new((x1 + x2) / 2, y + tinggi - 0.6, (z1 + z2) / 2) * CFrame.Angles(0, -yaw, 0)
        local tali = part(m, Vector3.new(panjang, 0.07, 0.07), cfTali, KAYU_TUA, Enum.Material.Wood)
        tali.CanCollide = false
        local n = 8
        for i = 1, n - 1 do
                local t = i / n
                local px = x1 + (x2 - x1) * t
                local pz = z1 + (z2 - z1) * t
                local kendur = math.sin(t * math.pi) * 0.5
                local bendera = part(m, Vector3.new(0.55, 0.85, 0.06), CFrame.new(px, y + tinggi - 1.05 - kendur, pz) * CFrame.Angles(0, -yaw, 0), BENDERA[(i - 1) % #BENDERA + 1], Enum.Material.SmoothPlastic)
                bendera.CanCollide = false
        end
end

local function sepeda(parent: Instance, x: number, z: number, yaw: number, warna: Color3)
        local m = Instance.new("Model")
        m.Name = "Sepeda"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        local rodaTua = Color3.fromRGB(50, 50, 54)
        local r1 = part(m, Vector3.new(0.22, 1.5, 1.5), cf * CFrame.new(-0.95, 0.75, 0) * CFrame.Angles(0, math.rad(90), 0), rodaTua, Enum.Material.SmoothPlastic)
        r1.Shape = Enum.PartType.Cylinder
        r1.CanCollide = false
        local r2 = part(m, Vector3.new(0.22, 1.5, 1.5), cf * CFrame.new(0.95, 0.75, 0) * CFrame.Angles(0, math.rad(90), 0), rodaTua, Enum.Material.SmoothPlastic)
        r2.Shape = Enum.PartType.Cylinder
        r2.CanCollide = false
        local rangka = part(m, Vector3.new(2.3, 0.16, 0.16), cf * CFrame.new(0, 1.05, 0), warna, Enum.Material.SmoothPlastic)
        rangka.CanCollide = false
        local sadel = part(m, Vector3.new(0.75, 0.18, 0.45), cf * CFrame.new(-0.45, 1.5, 0), KAYU_TUA, Enum.Material.Wood)
        sadel.CanCollide = false
        local tiang = part(m, Vector3.new(0.14, 0.8, 0.14), cf * CFrame.new(1.0, 1.3, 0), warna, Enum.Material.SmoothPlastic)
        tiang.CanCollide = false
        local setang = part(m, Vector3.new(0.14, 0.14, 1.15), cf * CFrame.new(1.0, 1.72, 0), KAYU_TUA, Enum.Material.Wood)
        setang.CanCollide = false
end

local function rakSepeda(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "RakSepeda"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(7, 0.25, 0.3), cf * CFrame.new(0, 0.55, 1.05), KAYU_TUA, Enum.Material.Metal)
        part(m, Vector3.new(0.3, 0.55, 0.3), cf * CFrame.new(-3.2, 0.28, 1.05), KAYU_TUA, Enum.Material.Metal)
        part(m, Vector3.new(0.3, 0.55, 0.3), cf * CFrame.new(3.2, 0.28, 1.05), KAYU_TUA, Enum.Material.Metal)
        local warna = { Color3.fromRGB(196, 60, 50), Color3.fromRGB(70, 110, 180), Color3.fromRGB(80, 150, 80) }
        for i = -1, 1 do
                local sx = cf * CFrame.new(i * 2.3, 0, -0.35)
                local pos = sx.Position
                sepeda(m, pos.X, pos.Z, yaw, warna[i + 2])
        end
end

local function kiosPasar(parent: Instance, x: number, z: number, yaw: number, warnaTeduh: Color3, hasil: { Color3 })
        local m = Instance.new("Model")
        m.Name = "KiosPasar"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        for _, sx in ipairs({ -1, 1 }) do
                for _, sz in ipairs({ -1, 1 }) do
                        part(m, Vector3.new(0.28, 3.6, 0.28), cf * CFrame.new(sx * 2.2, 1.8, sz * 1.6), KAYU_TUA, Enum.Material.Wood)
                end
        end
        for i = 0, 4 do
                local strip = part(m, Vector3.new(5.2, 0.14, 0.8), cf * CFrame.new(0, 3.78, -1.55 + i * 0.82) * CFrame.Angles(math.rad(-8), 0, 0), (i % 2 == 0) and warnaTeduh or PUTIH, Enum.Material.SmoothPlastic)
                strip.CanCollide = false
        end
        part(m, Vector3.new(4.8, 0.9, 1.5), cf * CFrame.new(0, 0.45, 0.9), KAYU, Enum.Material.WoodPlanks)
        for i, w in ipairs(hasil) do
                local kotak = part(m, Vector3.new(1.05, 0.7, 0.9), cf * CFrame.new(-1.5 + (i - 1) * 1.5, 1.25, 0.9), KAYU, Enum.Material.WoodPlanks)
                kotak.CanCollide = false
                local isian = part(m, Vector3.new(0.7, 0.55, 0.6), cf * CFrame.new(-1.5 + (i - 1) * 1.5, 1.8, 0.9), w, Enum.Material.SmoothPlastic)
                isian.Shape = Enum.PartType.Ball
                isian.CanCollide = false
        end
end

local function bungaLiar(parent: Instance, x: number, z: number, jumlah: number?)
        local n = jumlah or 3
        for i = 1, n do
                local dx = ((i * 37) % 9) - 4
                local dz = ((i * 53) % 9) - 4
                local batang = part(parent, Vector3.new(0.16, 0.55, 0.16), CFrame.new(x + dx, GT + 0.27, z + dz), RUMPUT_TUA, Enum.Material.Grass)
                batang.CanCollide = false
                local kepala = part(parent, Vector3.new(0.42, 0.42, 0.42), CFrame.new(x + dx, GT + 0.66, z + dz), BUNGA_LIAR[(i + math.floor(x) + math.floor(z)) % #BUNGA_LIAR + 1], Enum.Material.SmoothPlastic)
                kepala.Shape = Enum.PartType.Ball
                kepala.CanCollide = false
        end
end

-- Papan petunjuk arah bertingkat (sebelumnya 4 papan bertumpuk saling
-- menembus; sekarang satu tiang, papan berjajar rapi).
local function papanPetunjuk(parent: Instance, x: number, z: number, y0: number?)
        local y = y0 or GT
        local m = Instance.new("Model")
        m.Name = "PapanPetunjuk"
        m.Parent = parent
        part(m, Vector3.new(0.5, 9.2, 0.5), CFrame.new(x, y + 4.6, z), KAYU_TUA, Enum.Material.Wood)
        local daftar = {
                { "SABANA (Utara)", 8.2 },
                { "STEPA (Timur)", 6.35 },
                { "KAMPUNG (Barat)", 4.5 },
                { "PERLADANGAN (Selatan)", 2.65 },
        }
        for _, d in ipairs(daftar) do
                local papan = part(m, Vector3.new(6.6, 1.55, 0.3), CFrame.new(x + 3.4, y + d[2], z), KAYU, Enum.Material.Wood)
                teksPapan(papan, Enum.NormalId.Front, d[1])
                teksPapan(papan, Enum.NormalId.Back, d[1])
        end
end

-- Papan nama jalan kecil di pinggir persimpangan (sentuhan masterplan).
local function papanJalan(parent: Instance, x: number, z: number, teks: string, yaw: number)
        local m = Instance.new("Model")
        m.Name = "PapanJalan"
        m.Parent = parent
        part(m, Vector3.new(0.35, 3.2, 0.35), CFrame.new(x, GT + 1.6, z), KAYU_TUA, Enum.Material.Metal)
        local papan = part(m, Vector3.new(4.6, 1.2, 0.25), CFrame.new(x, GT + 3.5, z) * CFrame.Angles(0, yaw, 0), PUTIH, Enum.Material.SmoothPlastic)
        teksPapan(papan, Enum.NormalId.Front, teks)
        teksPapan(papan, Enum.NormalId.Back, teks)
        return papan
end

local function kawananBurung(parent: Instance, cx: number, cz: number)
        local m = Instance.new("Model")
        m.Name = "KawananBurung"
        m.Parent = parent
        for i = 1, 5 do
                local burung = part(m, Vector3.new(0.5, 0.3, 0.95), CFrame.new(cx, GT + 12 + i * 0.7, cz), Color3.fromRGB(72, 72, 80), Enum.Material.SmoothPlastic)
                burung.Name = "Burung"
                burung.CanCollide = false
                local radius = 9 + i * 2.2
                local laju = 0.4 + i * 0.06
                local fase = i * 1.25
                task.spawn(function()
                        local t = fase
                        while burung.Parent do
                                local dt = RunService.Heartbeat:Wait()
                                t += dt * laju
                                local y = GT + 12 + i * 0.7 + math.sin(t * 2.2) * 0.7
                                burung.CFrame = CFrame.new(cx + math.cos(t) * radius, y, cz + math.sin(t) * radius) * CFrame.Angles(0, math.pi - t, 0)
                        end
                end)
        end
end

-- ====================================================================
-- PENGAYAAN v71: mengisi lahan kosong dengan 4 kawasan bertema supaya
-- dataran terasa hidup, bukan rumput luas yang polos.
-- ====================================================================

local function semak(parent: Instance, x: number, z: number, skala: number?)
        local k = skala or 1
        local b = part(parent, Vector3.new(1.5 * k, 1 * k, 1.5 * k), CFrame.new(x, GT + 0.5 * k, z), RUMPUT_TUA, Enum.Material.Grass)
        b.Shape = Enum.PartType.Ball
end

-- Petak bunga terangkat: bingkai batu + tanah gembur + bola bunga warna.
local function petakBunga(parent: Instance, x: number, z: number, w: number, d: number)
        part(parent, Vector3.new(w + 0.6, 0.5, 0.45), CFrame.new(x, GT + 0.25, z - d / 2), TROTOAR, Enum.Material.Concrete)
        part(parent, Vector3.new(w + 0.6, 0.5, 0.45), CFrame.new(x, GT + 0.25, z + d / 2), TROTOAR, Enum.Material.Concrete)
        part(parent, Vector3.new(0.45, 0.5, d + 0.6), CFrame.new(x - w / 2, GT + 0.25, z), TROTOAR, Enum.Material.Concrete)
        part(parent, Vector3.new(0.45, 0.5, d + 0.6), CFrame.new(x + w / 2, GT + 0.25, z), TROTOAR, Enum.Material.Concrete)
        part(parent, Vector3.new(w, 0.35, d), CFrame.new(x, GT + 0.32, z), TANAH, Enum.Material.Ground)
        local nx = math.max(math.floor(w / 1.6), 2)
        local nz = math.max(math.floor(d / 1.6), 2)
        for i = 0, nx - 1 do
                for j = 0, nz - 1 do
                        local fx = x - w / 2 + (w / nx) * (i + 0.5)
                        local fz = z - d / 2 + (d / nz) * (j + 0.5)
                        local batang = part(parent, Vector3.new(0.16, 0.6, 0.16), CFrame.new(fx, GT + 0.75, fz), RUMPUT_TUA, Enum.Material.Grass)
                        batang.CanCollide = false
                        local kepala = part(parent, Vector3.new(0.5, 0.5, 0.5), CFrame.new(fx, GT + 1.15, fz), BUNGA_LIAR[(i * 3 + j + math.floor(x)) % #BUNGA_LIAR + 1], Enum.Material.SmoothPlastic)
                        kepala.Shape = Enum.PartType.Ball
                        kepala.CanCollide = false
                end
        end
end

-- Saung (gazebo): lantai batu, 4 pilar, atap pelana, bangku di dalam.
local function gazebo(parent: Instance, x: number, z: number, lebar: number)
        local m = Instance.new("Model")
        m.Name = "Gazebo"
        m.Parent = parent
        part(m, Vector3.new(lebar, 0.5, lebar), CFrame.new(0, 0.25, 0), BATU, Enum.Material.Concrete)
        for _, sx in ipairs({ -1, 1 }) do
                for _, sz in ipairs({ -1, 1 }) do
                        part(m, Vector3.new(0.6, lebar * 0.62, 0.6), CFrame.new(sx * (lebar / 2 - 0.8), 0.5 + lebar * 0.31, sz * (lebar / 2 - 0.8)), KAYU_TUA, Enum.Material.Wood)
                end
        end
        for _, sx in ipairs({ -1, 1 }) do
                part(m, Vector3.new(0.25, 0.65, 0.8), CFrame.new(sx * lebar * 0.18, 0.825, lebar / 2 - 1.4), KAYU_TUA, Enum.Material.Wood)
        end
        part(m, Vector3.new(lebar * 0.5, 0.25, 1), CFrame.new(0, 1.15, lebar / 2 - 1.4), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(lebar * 0.5, 0.7, 0.2), CFrame.new(0, 1.6, lebar / 2 - 0.9), KAYU, Enum.Material.Wood)
        BuildingKit.gableRoof(m, lebar, lebar, 1.4, 0.5 + lebar * 0.62, ATAP)
        m.WorldPivot = CFrame.new(0, 0, 0)
        m:PivotTo(CFrame.new(x, GT, z))
end

-- Ayunan ganda: rangka A dua sisi, balok atas, dua dudukan tali.
local function ayunan(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "Ayunan"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        for _, sx in ipairs({ -2.2, 2.2 }) do
                part(m, Vector3.new(0.5, 3.4, 0.5), cf * CFrame.new(sx, 1.7, -1), KAYU_TUA, Enum.Material.Wood)
                part(m, Vector3.new(0.5, 3.4, 0.5), cf * CFrame.new(sx, 1.7, 1), KAYU_TUA, Enum.Material.Wood)
        end
        part(m, Vector3.new(5.2, 0.5, 0.5), cf * CFrame.new(0, 3.55, 0), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(5.2, 0.4, 2.6), cf * CFrame.new(0, 0.2, 0), KAYU_TUA, Enum.Material.Wood)
        for _, sx in ipairs({ -1.2, 1.2 }) do
                for _, dt in ipairs({ -0.22, 0.22 }) do
                        local tali = part(m, Vector3.new(0.12, 1.9, 0.12), cf * CFrame.new(sx + dt, 2.55, 0), KAYU_TUA, Enum.Material.Wood)
                        tali.CanCollide = false
                end
                part(m, Vector3.new(1.1, 0.22, 0.55), cf * CFrame.new(sx, 1.5, 0), KAYU, Enum.Material.Wood)
        end
end

-- Perosotan: tangga samping, platform atas, seluncuran biru miring.
local function perosotan(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "Perosotan"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        for _, sx in ipairs({ -0.9, 0.9 }) do
                part(m, Vector3.new(0.35, 3, 0.35), cf * CFrame.new(sx, 1.5, -3.5), KAYU_TUA, Enum.Material.Wood)
                part(m, Vector3.new(0.35, 3, 0.35), cf * CFrame.new(sx, 1.5, -1.7), KAYU_TUA, Enum.Material.Wood)
        end
        part(m, Vector3.new(2.4, 0.35, 2.2), cf * CFrame.new(0, 3.15, -2.6), KAYU, Enum.Material.WoodPlanks)
        for i = 0, 3 do
                part(m, Vector3.new(1.5, 0.16, 0.4), cf * CFrame.new(1.7, 0.75 + i * 0.8, -2.6), KAYU, Enum.Material.Wood)
        end
        part(m, Vector3.new(0.3, 2.6, 0.3), cf * CFrame.new(2.45, 1.3, -1.9), KAYU_TUA, Enum.Material.Wood)
        part(m, Vector3.new(0.3, 2.6, 0.3), cf * CFrame.new(2.45, 1.3, -3.3), KAYU_TUA, Enum.Material.Wood)
        local lereng = math.rad(31)
        local seluncur = part(m, Vector3.new(1.6, 0.25, 5.7), cf * CFrame.new(0, 1.83, 0.1) * CFrame.Angles(lereng, 0, 0), Color3.fromRGB(90, 160, 205), Enum.Material.SmoothPlastic)
        seluncur.Name = "Seluncuran"
        for _, sx in ipairs({ -0.75, 0.75 }) do
                local pag = part(m, Vector3.new(0.15, 0.5, 5.7), cf * CFrame.new(sx, 2.05, 0.1) * CFrame.Angles(lereng, 0, 0), Color3.fromRGB(70, 130, 175), Enum.Material.SmoothPlastic)
                pag.CanCollide = false
        end
end

-- Jungkat-jungkit: tumpuan beton, papan jungkit, pegangan dua ujung.
local function jungkatJungkit(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "JungkatJungkit"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(1, 0.9, 1), cf * CFrame.new(0, 0.45, 0), BATU, Enum.Material.Concrete)
        part(m, Vector3.new(0.4, 0.22, 7.2), cf * CFrame.new(0, 1.02, 0) * CFrame.Angles(math.rad(6), 0, 0), KAYU, Enum.Material.Wood)
        for _, sz in ipairs({ -1, 1 }) do
                local yPapan = 1.02 - sz * 2.9 * math.sin(math.rad(6))
                for _, sx in ipairs({ -0.45, 0.45 }) do
                        part(m, Vector3.new(0.28, 0.7, 0.28), cf * CFrame.new(sx, yPapan + 0.55, sz * 2.9), KAYU_TUA, Enum.Material.Wood)
                end
                part(m, Vector3.new(1.2, 0.24, 0.3), cf * CFrame.new(0, yPapan + 1.0, sz * 2.9), KAYU, Enum.Material.Wood)
        end
end

-- Kotak pasir bermain: bingkai kayu, pasir, ember & kotak mainan.
local function kotakPasir(parent: Instance, x: number, z: number)
        local m = Instance.new("Model")
        m.Name = "KotakPasir"
        m.Parent = parent
        part(m, Vector3.new(6.4, 0.5, 0.4), CFrame.new(x, GT + 0.25, z - 3), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(6.4, 0.5, 0.4), CFrame.new(x, GT + 0.25, z + 3), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(0.4, 0.5, 5.6), CFrame.new(x - 3, GT + 0.25, z), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(0.4, 0.5, 5.6), CFrame.new(x + 3, GT + 0.25, z), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(5.6, 0.3, 5.2), CFrame.new(x, GT + 0.2, z), KERING, Enum.Material.Ground)
        part(m, Vector3.new(0.7, 0.7, 0.7), CFrame.new(x + 1.3, GT + 0.55, z - 1), Color3.fromRGB(206, 84, 70), Enum.Material.SmoothPlastic)
        part(m, Vector3.new(0.5, 0.5, 0.5), CFrame.new(x - 1.4, GT + 0.45, z + 0.8), Color3.fromRGB(236, 196, 90), Enum.Material.SmoothPlastic)
end

-- Bebek kolam: badan + kepala + paruh (mengapung di kolam).
local function bebek(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "Bebek"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        local badan = part(m, Vector3.new(1.5, 1, 1.1), cf * CFrame.new(0, 0.55, 0), PUTIH, Enum.Material.SmoothPlastic)
        badan.Shape = Enum.PartType.Ball
        local kepala = part(m, Vector3.new(0.7, 0.7, 0.7), cf * CFrame.new(0.6, 1.2, 0), PUTIH, Enum.Material.SmoothPlastic)
        kepala.Shape = Enum.PartType.Ball
        local paruh = part(m, Vector3.new(0.45, 0.2, 0.3), cf * CFrame.new(1.05, 1.15, 0), Color3.fromRGB(236, 160, 60), Enum.Material.SmoothPlastic)
        paruh.CanCollide = false
end

-- Kolam bebek: cakram air, batu pinggir, dua bebek renang.
local function kolamBebek(parent: Instance, x: number, z: number)
        local m = Instance.new("Model")
        m.Name = "KolamBebek"
        m.Parent = parent
        local air = part(m, Vector3.new(0.24, 13, 13), CFrame.new(x, GT + 0.12, z) * CFrame.Angles(0, 0, math.rad(90)), AIR, Enum.Material.Glass, 0.3)
        air.Shape = Enum.PartType.Cylinder
        air.CanCollide = false
        for i = 0, 9 do
                local a = i * math.pi / 5 + 0.3
                part(m, Vector3.new(1.3, 0.5, 1.3), CFrame.new(x + math.cos(a) * 7, GT + 0.25, z + math.sin(a) * 7) * CFrame.Angles(0, a, 0), BATU, Enum.Material.Slate)
        end
        bebek(m, x - 2.2, z + 1.2, math.rad(25))
        bebek(m, x + 2.6, z - 1.4, math.rad(-55))
end

-- Lampu sorot lapangan: tiang tinggi + kepala neon + SpotLight.
local function lampuSorot(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "LampuSorot"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(0.6, 8, 0.6), cf * CFrame.new(0, 4, 0), KAYU_TUA, Enum.Material.Metal)
        local kepala = part(m, Vector3.new(2.4, 1.2, 0.8), cf * CFrame.new(0, 8.4, 0) * CFrame.Angles(math.rad(-30), 0, 0), PUTIH, Enum.Material.Neon)
        local sorot = Instance.new("SpotLight")
        sorot.Range = 44
        sorot.Angle = 80
        sorot.Brightness = 1.4
        sorot.Parent = kepala
end

-- Lapangan bulu tangkis: slab hijau, garis putih, net di tengah.
local function lapanganBuluTangkis(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "LapanganBuluTangkis"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(9, 0.14, 17), cf * CFrame.new(0, 0.07, 0), Color3.fromRGB(96, 148, 98), Enum.Material.Concrete)
        for _, sx in ipairs({ -1, 1 }) do
                local garis = part(m, Vector3.new(0.3, 0.06, 16.4), cf * CFrame.new(sx * 4.2, 0.18, 0), MARKA, Enum.Material.SmoothPlastic)
                garis.CanCollide = false
        end
        for _, sz in ipairs({ -1, 1 }) do
                local garis = part(m, Vector3.new(8.4, 0.06, 0.3), cf * CFrame.new(0, 0.18, sz * 8.2), MARKA, Enum.Material.SmoothPlastic)
                garis.CanCollide = false
        end
        for _, sx in ipairs({ -1, 1 }) do
                part(m, Vector3.new(0.22, 1.7, 0.22), cf * CFrame.new(sx * 4.6, 0.85, 0), KAYU_TUA, Enum.Material.Metal)
        end
        local net = part(m, Vector3.new(9.2, 0.55, 0.08), cf * CFrame.new(0, 1.35, 0), Color3.fromRGB(52, 54, 58), Enum.Material.Fabric)
        net.CanCollide = false
        local pitaNet = part(m, Vector3.new(9.2, 0.18, 0.1), cf * CFrame.new(0, 1.72, 0), PUTIH, Enum.Material.SmoothPlastic)
        pitaNet.CanCollide = false
end

-- Lapangan basket mini: slab abu, papan pantul, ring oranye.
local function lapanganBasket(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "LapanganBasket"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        part(m, Vector3.new(14, 0.14, 10), cf * CFrame.new(0, 0.07, 0), Color3.fromRGB(122, 126, 132), Enum.Material.Concrete)
        part(m, Vector3.new(0.4, 3.4, 0.4), cf * CFrame.new(0, 1.7, -4.6), KAYU_TUA, Enum.Material.Metal)
        part(m, Vector3.new(2.8, 1.8, 0.16), cf * CFrame.new(0, 3.6, -4.4), PUTIH, Enum.Material.SmoothPlastic)
        local ring = part(m, Vector3.new(1, 0.14, 1), cf * CFrame.new(0, 3.05, -3.55), Color3.fromRGB(232, 122, 52), Enum.Material.Metal)
        ring.Shape = Enum.PartType.Cylinder
end

-- Pergola jejala: deretan tiang + balok + kisi-kisi + sulur bunga.
local function pergola(parent: Instance, x: number, z: number, panjang: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "Pergola"
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
        for i = 0, 2 do
                for _, sz in ipairs({ -1, 1 }) do
                        part(m, Vector3.new(0.45, 3.4, 0.45), cf * CFrame.new(-panjang / 2 + i * (panjang / 2), 1.7, sz * 1.7), KAYU_TUA, Enum.Material.Wood)
                end
        end
        for _, sz in ipairs({ -1, 1 }) do
                part(m, Vector3.new(panjang + 0.9, 0.4, 0.5), cf * CFrame.new(0, 3.6, sz * 1.7), KAYU, Enum.Material.Wood)
        end
        local n = math.floor(panjang / 1.3)
        for i = 0, n do
                local gel = part(m, Vector3.new(0.26, 0.16, 4.4), cf * CFrame.new(-panjang / 2 + i * (panjang / n), 3.88, 0), KAYU, Enum.Material.Wood)
                gel.CanCollide = false
        end
        for i = 1, 4 do
                local vx = -panjang / 2 + panjang * i / 5
                local sulur = part(m, Vector3.new(1.1, 0.8, 1.6), cf * CFrame.new(vx, 3.35, (i % 2 == 0) and 0.5 or -0.5), RUMPUT_TUA, Enum.Material.Grass)
                sulur.Shape = Enum.PartType.Ball
                sulur.CanCollide = false
                local bungaKecil = part(m, Vector3.new(0.4, 0.4, 0.4), cf * CFrame.new(vx + 0.25, 2.9, (i % 2 == 0) and 0.9 or -0.9), BUNGA_LIAR[i], Enum.Material.SmoothPlastic)
                bungaKecil.Shape = Enum.PartType.Ball
                bungaKecil.CanCollide = false
        end
end

-- Rumah kaca mini: rangka putih, dinding & atap kaca, bed tanaman di dalam.
local function rumahKaca(parent: Instance, x: number, z: number)
        local m = Instance.new("Model")
        m.Name = "RumahKaca"
        m.Parent = parent
        local kaca = Color3.fromRGB(205, 232, 238)
        part(m, Vector3.new(10, 0.3, 8), CFrame.new(0, 0.15, 0), TROTOAR, Enum.Material.Concrete)
        part(m, Vector3.new(10, 3, 0.14), CFrame.new(0, 1.8, -4), kaca, Enum.Material.Glass, 0.55)
        part(m, Vector3.new(0.14, 3, 8), CFrame.new(-5, 1.8, 0), kaca, Enum.Material.Glass, 0.55)
        part(m, Vector3.new(0.14, 3, 8), CFrame.new(5, 1.8, 0), kaca, Enum.Material.Glass, 0.55)
        part(m, Vector3.new(3.8, 3, 0.14), CFrame.new(-3.1, 1.8, 4), kaca, Enum.Material.Glass, 0.55)
        part(m, Vector3.new(3.8, 3, 0.14), CFrame.new(3.1, 1.8, 4), kaca, Enum.Material.Glass, 0.55)
        for _, sx in ipairs({ -1, 1 }) do
                for _, sz in ipairs({ -1, 1 }) do
                        part(m, Vector3.new(0.3, 3, 0.3), CFrame.new(sx * 5, 1.8, sz * 4), PUTIH, Enum.Material.Metal)
                end
        end
        part(m, Vector3.new(10.4, 0.25, 0.25), CFrame.new(0, 3.4, -4), PUTIH, Enum.Material.Metal)
        part(m, Vector3.new(10.4, 0.25, 0.25), CFrame.new(0, 3.4, 4), PUTIH, Enum.Material.Metal)
        local slope = math.rad(30)
        local hd = 4 + 1.2
        local rise = hd * math.tan(slope)
        local slabLen = hd / math.cos(slope)
        local atap1 = part(m, Vector3.new(10.8, 0.14, slabLen), CFrame.new(0, 3.4 + rise / 2, -hd / 2) * CFrame.Angles(-slope, 0, 0), kaca, Enum.Material.Glass, 0.5)
        atap1.CanCollide = false
        local atap2 = part(m, Vector3.new(10.8, 0.14, slabLen), CFrame.new(0, 3.4 + rise / 2, hd / 2) * CFrame.Angles(slope, 0, 0), kaca, Enum.Material.Glass, 0.5)
        atap2.CanCollide = false
        part(m, Vector3.new(8, 0.4, 2), CFrame.new(0, 0.5, -2.4), TANAH, Enum.Material.Ground)
        part(m, Vector3.new(8, 0.4, 2), CFrame.new(0, 0.5, 2.4), TANAH, Enum.Material.Ground)
        m.WorldPivot = CFrame.new(0, 0, 0)
        m:PivotTo(CFrame.new(x, GT, z))
        tanamanDemo(m, x - 2.5, z - 2.4, "wortel")
        tanamanDemo(m, x, z - 2.4, "kubis")
        tanamanDemo(m, x + 2.5, z - 2.4, "selada")
        tanamanDemo(m, x - 2.5, z + 2.4, "seledri")
        tanamanDemo(m, x + 2.5, z + 2.4, "brokoli")
end

-- Panggung budaya: lantai kayu tinggi, dinding belakang, atap, tangga.
local function panggung(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "Panggung"
        m.Parent = parent
        part(m, Vector3.new(14, 1, 9), CFrame.new(0, 0.5, 0), KAYU, Enum.Material.WoodPlanks)
        part(m, Vector3.new(6, 0.4, 1.2), CFrame.new(0, 0.2, 5.1), BATU, Enum.Material.Concrete)
        part(m, Vector3.new(6, 0.4, 1.2), CFrame.new(0, 0.6, 4.0), BATU, Enum.Material.Concrete)
        part(m, Vector3.new(14, 4.5, 0.4), CFrame.new(0, 3.25, -4.3), DINDING, Enum.Material.WoodPlanks)
        part(m, Vector3.new(0.4, 4.5, 9), CFrame.new(-6.8, 3.25, 0), DINDING, Enum.Material.WoodPlanks)
        part(m, Vector3.new(0.4, 4.5, 9), CFrame.new(6.8, 3.25, 0), DINDING, Enum.Material.WoodPlanks)
        for _, sx in ipairs({ -1, 1 }) do
                for _, sz in ipairs({ -1, 1 }) do
                        part(m, Vector3.new(0.5, 3.2, 0.5), CFrame.new(sx * 5.6, 3.4, sz * 3.2), KAYU_TUA, Enum.Material.Wood)
                end
        end
        BuildingKit.gableRoof(m, 13.6, 8.4, 1.5, 5, ATAP)
        m.WorldPivot = CFrame.new(0, 0, 0)
        m:PivotTo(CFrame.new(x, GT, z))
end

-- Tiang bendera merah putih dengan alas beton bundar.
local function benderaMerahPutih(parent: Instance, x: number, z: number)
        local m = Instance.new("Model")
        m.Name = "BenderaMerahPutih"
        m.Parent = parent
        local alas = part(m, Vector3.new(0.5, 3.4, 3.4), CFrame.new(x, GT + 0.25, z) * CFrame.Angles(0, 0, math.rad(90)), BATU, Enum.Material.Concrete)
        alas.Shape = Enum.PartType.Cylinder
        part(m, Vector3.new(0.3, 9.4, 0.3), CFrame.new(x, GT + 4.9, z), PUTIH, Enum.Material.Metal)
        local pucuk = part(m, Vector3.new(0.4, 0.4, 0.4), CFrame.new(x, GT + 9.75, z), Color3.fromRGB(236, 196, 90), Enum.Material.Metal)
        pucuk.Shape = Enum.PartType.Ball
        pucuk.CanCollide = false
        local merah = part(m, Vector3.new(2.6, 0.8, 0.1), CFrame.new(x + 1.5, GT + 8.9, z), Color3.fromRGB(206, 36, 44), Enum.Material.SmoothPlastic)
        merah.CanCollide = false
        local putihBawah = part(m, Vector3.new(2.6, 0.8, 0.1), CFrame.new(x + 1.5, GT + 8.1, z), PUTIH, Enum.Material.SmoothPlastic)
        putihBawah.CanCollide = false
end

-- Sepasang kupu-kupu beterbangan mengitari petak bunga.
local function kupuKupu(parent: Instance, cx: number, cz: number)
        local m = Instance.new("Model")
        m.Name = "KupuKupu"
        m.Parent = parent
        local warna = { Color3.fromRGB(236, 152, 66), Color3.fromRGB(150, 110, 208) }
        for i = 1, 2 do
                local kupu = part(m, Vector3.new(0.55, 0.16, 0.4), CFrame.new(cx, GT + 2.2, cz), warna[i], Enum.Material.SmoothPlastic)
                kupu.Name = "Kupu"
                kupu.CanCollide = false
                local radius = 3.5 + i * 2
                local laju = 0.9 + i * 0.3
                local fase = i * 2.1
                task.spawn(function()
                        local t = fase
                        while kupu.Parent do
                                local dt = RunService.Heartbeat:Wait()
                                t += dt * laju
                                kupu.CFrame = CFrame.new(cx + math.cos(t) * radius, GT + 2.2 + math.sin(t * 3) * 0.6, cz + math.sin(t) * radius) * CFrame.Angles(0, -t, 0)
                        end
                end)
        end
end

-- KAWASAN 1 (barat laut): TAMAN RAKYAT — taman bermain + saung + kolam bebek.
local function tamanRakyat(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "TamanRakyat"
        m.Parent = parent
        papanTeks(m, -95, -57, "TAMAN RAKYAT", math.rad(180), 4.5)
        part(m, Vector3.new(3, 0.2, 33), CFrame.new(-95, GT + 0.1, -38.5), JALAN, Enum.Material.Concrete).Name = "SetapakTaman"
        ayunan(m, -106, -72, 0)
        perosotan(m, -88, -72, 0)
        jungkatJungkit(m, -97, -81, 0)
        kotakPasir(m, -114, -72)
        gazebo(m, -78, -98, 8)
        gazebo(m, -114, -104, 7)
        kolamBebek(m, -96, -116)
        part(m, Vector3.new(24, 0.2, 3), CFrame.new(-98, GT + 0.1, -87), JALAN, Enum.Material.Concrete).Name = "SetapakTaman"
        part(m, Vector3.new(3, 0.2, 21), CFrame.new(-98, GT + 0.1, -97.5), JALAN, Enum.Material.Concrete).Name = "SetapakTaman"
        bangku(m, -84, -66, 0)
        bangku(m, -108, -88, math.rad(180))
        bangku(m, -86, -104, math.rad(-90))
        lampuTaman(m, -70, -64)
        lampuTaman(m, -122, -64)
        lampuTaman(m, -70, -126)
        lampuTaman(m, -122, -126)
        pohonAlam(m, -70, -86)
        pohonAlam(m, -70, -112)
        pohonAlam(m, -124, -84)
        pohonAlam(m, -124, -112)
        pohonAlam(m, -84, -128)
        bungaLiar(m, -72, -76, 3)
        bungaLiar(m, -118, -84, 3)
        bungaLiar(m, -92, -66, 3)
        bungaLiar(m, -108, -122, 3)
        bungaLiar(m, -84, -116, 3)
        semak(m, -72, -60)
        semak(m, -100, -62)
        semak(m, -120, -74)
        semak(m, -70, -100)
        semak(m, -66, -120)
        semak(m, -92, -132)
        semak(m, -116, -128)
        batuAlam(m, -66, -92, 1.6)
        batuAlam(m, -126, -100, 2)
        npc(m, -90, -62, math.rad(135), "Penjaga Taman", Color3.fromRGB(96, 148, 92))
end

-- KAWASAN 2 (barat daya): LAPANGAN DESA — 2 lapangan bulu tangkis + basket.
local function lapanganDesa(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "LapanganDesa"
        m.Parent = parent
        papanTeks(m, -22, 60, "LAPANGAN DESA", 0, 4.5)
        part(m, Vector3.new(3, 0.2, 68), CFrame.new(-15, GT + 0.1, 31), JALAN, Enum.Material.Concrete).Name = "SetapakLapangan"
        lapanganBuluTangkis(m, -18, 78, 0)
        lapanganBuluTangkis(m, -18, 98, 0)
        lapanganBasket(m, 8, 88, 0)
        lampuSorot(m, -30, 72, math.rad(-90))
        lampuSorot(m, -30, 104, math.rad(-90))
        bangku(m, -18, 66, 0)
        bangku(m, -26, 78, math.rad(-90))
        bangku(m, 19, 88, math.rad(90))
        bangku(m, -18, 110, 0)
        pohonAlam(m, 24, 70, 1)
        pohonAlam(m, 24, 110, 0.95)
        pohonAlam(m, -32, 88, 1.05)
        pohonAlam(m, -30, 122, 0.9)
        bungaLiar(m, -26, 70, 3)
        bungaLiar(m, 14, 74, 3)
        bungaLiar(m, 16, 104, 3)
        bungaLiar(m, -36, 66, 3)
        semak(m, -28, 62)
        semak(m, -4, 64)
        semak(m, 18, 66)
        semak(m, 22, 96)
        semak(m, -2, 118)
        semak(m, -36, 116)
        npc(m, -6, 70, math.rad(90), "Anak Lapangan", Color3.fromRGB(208, 148, 70))
end

-- KAWASAN 3 (timur laut): KEBUN RAYA — 6 petak bunga + pergola + rumah kaca.
local function kebunRaya(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "KebunRaya"
        m.Parent = parent
        papanTeks(m, 79, -55, "KEBUN RAYA", math.rad(-90), 4.5)
        part(m, Vector3.new(11, 0.2, 3), CFrame.new(69.5, GT + 0.1, -60), JALAN, Enum.Material.Concrete).Name = "SetapakRaya"
        part(m, Vector3.new(14, 0.2, 3), CFrame.new(82, GT + 0.1, -60), JALAN, Enum.Material.Concrete).Name = "SetapakRaya"
        part(m, Vector3.new(3, 0.2, 44), CFrame.new(90, GT + 0.1, -86), JALAN, Enum.Material.Concrete).Name = "SetapakRaya"
        petakBunga(m, 82, -72, 12, 6)
        petakBunga(m, 98, -72, 12, 6)
        petakBunga(m, 82, -86, 12, 6)
        petakBunga(m, 98, -86, 12, 6)
        petakBunga(m, 82, -100, 12, 6)
        petakBunga(m, 98, -100, 12, 6)
        pergola(m, 112, -80, 20, 0)
        rumahKaca(m, 124, -64)
        kupuKupu(m, 90, -86)
        bangku(m, 76, -76, math.rad(90))
        bangku(m, 106, -94, math.rad(-90))
        bangku(m, 90, -108, 0)
        lampuTaman(m, 72, -66)
        lampuTaman(m, 108, -66)
        pohonAlam(m, 70, -78, 0.95)
        pohonAlam(m, 70, -104, 1.05)
        pohonAlam(m, 114, -112, 1)
        pohonAlam(m, 128, -92, 0.9)
        pohonAlam(m, 76, -122, 1.05)
        bungaLiar(m, 72, -90, 3)
        bungaLiar(m, 108, -116, 3)
        bungaLiar(m, 122, -76, 3)
        bungaLiar(m, 86, -112, 3)
        semak(m, 72, -64)
        semak(m, 104, -52)
        semak(m, 76, -108)
        semak(m, 118, -104)
        semak(m, 94, -120)
        batuAlam(m, 70, -68, 1.4)
        batuAlam(m, 112, -108, 1.8)
        npc(m, 78, -66, math.rad(45), "Tukang Kebun", Color3.fromRGB(120, 128, 88))
end

-- KAWASAN 4 (tenggara): PANGGUNG BUDAYA — panggung + tribun + bendera + sawah mini.
local function panggungBudaya(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "PanggungBudaya"
        m.Parent = parent
        papanTeks(m, 66, 70, "PANGGUNG BUDAYA", math.rad(-90), 4.5)
        part(m, Vector3.new(26, 0.2, 3), CFrame.new(77, GT + 0.1, 75), JALAN, Enum.Material.Concrete).Name = "SetapakPanggung"
        panggung(m, 92, 75, 0)
        for _, sz in ipairs({ 84, 90 }) do
                for _, sx in ipairs({ 86, 92, 98 }) do
                        bangku(m, sx, sz, math.rad(180))
                end
        end
        benderaMerahPutih(m, 78, 100)
        gazebo(m, 118, 66, 9)
        for _, petak in ipairs({ { 98, 110 }, { 112, 110 }, { 98, 122 }, { 112, 122 } }) do
                local px, pz = petak[1], petak[2]
                part(m, Vector3.new(11, 0.35, 9), CFrame.new(px, GT + 0.175, pz), TANAH, Enum.Material.Ground)
                local air = part(m, Vector3.new(9.6, 0.12, 7.6), CFrame.new(px, GT + 0.41, pz), AIR, Enum.Material.Glass, 0.4)
                air.CanCollide = false
                tanamanDemo(m, px - 3, pz, "gandum")
                tanamanDemo(m, px, pz, "gandum")
                tanamanDemo(m, px + 3, pz, "gandum")
        end
        gerobak(m, 108, 90, math.rad(15))
        lampuTaman(m, 84, 60)
        lampuTaman(m, 104, 96)
        pohonAlam(m, 72, 108, 1)
        pohonAlam(m, 128, 100, 0.95)
        pohonAlam(m, 76, 134, 1.05)
        pohonAlam(m, 124, 134, 0.9)
        bungaLiar(m, 72, 84, 3)
        bungaLiar(m, 86, 106, 3)
        bungaLiar(m, 122, 84, 3)
        bungaLiar(m, 104, 132, 3)
        semak(m, 70, 62)
        semak(m, 70, 92)
        semak(m, 100, 60)
        semak(m, 130, 76)
        semak(m, 90, 132)
        semak(m, 116, 118)
        batuAlam(m, 70, 118, 1.6)
        npc(m, 92, 76, math.rad(180), "Seniman Dataran", Color3.fromRGB(150, 96, 120), 1)
        npc(m, 84, 88, math.rad(90), "Penjual Jajan", Color3.fromRGB(96, 148, 92))
end

-- Suasana: sore hangat khas kepulauan + awan (aman jika layanan tak ada).
local function penerangan()
        pcall(function()
                local Lighting = game:GetService("Lighting")
                Lighting.ClockTime = 14.7
                Lighting.GeographicLatitude = 8
                Lighting.Brightness = 2.6
                Lighting.OutdoorAmbient = Color3.fromRGB(128, 124, 116)
                if not Lighting:FindFirstChildOfClass("Atmosphere") then
                        local atmo = Instance.new("Atmosphere")
                        atmo.Density = 0.32
                        atmo.Offset = 0.3
                        atmo.Color = Color3.fromRGB(199, 188, 172)
                        atmo.Decay = Color3.fromRGB(106, 98, 90)
                        atmo.Glare = 0.18
                        atmo.Haze = 1.7
                        atmo.Parent = Lighting
                end
        end)
        pcall(function()
                local terrain = workspace:FindFirstChildOfClass("Terrain")
                if terrain and not terrain:FindFirstChildOfClass("Clouds") then
                        local awan = Instance.new("Clouds")
                        awan.Cover = 0.6
                        awan.Density = 0.38
                        awan.Parent = terrain
                end
        end)
end

local function kebunDemonstrasi(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "KebunDemonstrasi"
        m.Parent = parent
        papanTeks(m, 96, 8, "KEBUN DEMONSTRASI", 0, 4)
        local z = 18
        for _, kat in ipairs(CropData.TokoBenihUrutan) do
                local daftar = CropData.TokoBenih[kat]
                local lebar = math.max(#daftar * 2.3 + 2, 10)
                part(m, Vector3.new(lebar, 0.4, 3.6), CFrame.new(112, GT + 0.2, z), TANAH, Enum.Material.Ground)
                papanTeks(m, 112 - lebar / 2 - 1.6, z + 1.4, kat, math.rad(-90), 2.6)
                local mulaiX = 112 - (lebar / 2) + 1.8
                for i, id in ipairs(daftar) do
                        tanamanDemo(m, mulaiX + (i - 1) * 2.3, z, id)
                end
                z += 5.4
        end
end

local function permukiman(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "Permukiman"
        m.Parent = parent
        papanTeks(m, -52, 42, "PERMUKIMAN", math.rad(-90), 4)
        rumahDesa(m, -78, 26, true)
        rumahDesa(m, -108, 30, false)
        rumahDesa(m, -78, 62, true)
        rumahDesa(m, -108, 66, false)
        -- Jaringan jalan setapak permukiman (grid masterplan):
        -- gang utara-selatan (diperpanjang sampai menyambung jalan aspal
        -- Barat) + jalan lintang antar-baris + jalan masuk rumah.
        part(m, Vector3.new(4, 0.2, 96), CFrame.new(-62, GT + 0.12, 36), JALAN, Enum.Material.Concrete).Name = "GangPermukiman"
        part(m, Vector3.new(60, 0.22, 4), CFrame.new(-90, GT + 0.12, 49), JALAN, Enum.Material.Concrete).Name = "GangPermukiman"
        part(m, Vector3.new(11, 0.14, 3), CFrame.new(-67.5, GT + 0.10, 30), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(11, 0.14, 3), CFrame.new(-67.5, GT + 0.10, 66), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(8, 0.14, 3), CFrame.new(-117, GT + 0.10, 30), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(8, 0.14, 3), CFrame.new(-117, GT + 0.10, 66), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(3, 0.18, 16), CFrame.new(-73, GT + 0.11, 39), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(3, 0.18, 16), CFrame.new(-117, GT + 0.11, 39), JALAN, Enum.Material.Concrete)
        BuildingKit.fenceLine(m, -92, 20, -92, 42, GT)
        BuildingKit.fenceLine(m, -122, 24, -122, 46, GT)
        BuildingKit.fenceLine(m, -92, 56, -92, 78, GT)
        BuildingKit.fenceLine(m, -122, 60, -122, 82, GT)
        part(m, Vector3.new(4, 0.3, 4), CFrame.new(-88, GT + 0.15, 32), TANAH, Enum.Material.Ground)
        tanamanDemo(m, -88, 32, "selada")
        part(m, Vector3.new(4, 0.3, 4), CFrame.new(-118, GT + 0.15, 38), TANAH, Enum.Material.Ground)
        tanamanDemo(m, -118, 38, "kubis")
        lampuTaman(m, -62, 22)
        lampuTaman(m, -62, 80)
        lampuTaman(m, -70, 44)
        lampuTaman(m, -100, 48)
        bangku(m, -58, 36, math.rad(-90))
        bungaLiar(m, -54, 30, 3)
        bungaLiar(m, -70, 58, 3)
        npc(m, -84, 44, math.rad(90), "Warga Desa", Color3.fromRGB(176, 92, 82))
        npc(m, -100, 52, math.rad(-90), "Kurir Desa", Color3.fromRGB(84, 120, 168))
end

local function perbukitanAlam(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "PerbukitanAlam"
        m.Parent = parent
        papanTeks(m, -44, 92, "PERBUKITAN ALAM", math.rad(180), 4)
        bukit(m, -62, 122, 74, 9)
        bukit(m, -112, 148, 96, 13)
        bukit(m, -152, 104, 62, 7)
        pohonAlam(m, -48, 98)
        pohonAlam(m, -80, 108, 1.15)
        pohonAlam(m, -96, 128)
        pohonAlam(m, -132, 122, 1.1)
        pohonAlam(m, -140, 152, 0.9)
        pohonAlam(m, -56, 152)
        pohonAlam(m, -170, 130, 1.2)
        batuAlam(m, -70, 92, 2.4)
        batuAlam(m, -116, 102, 3.2)
        batuAlam(m, -92, 162, 2)
        batuAlam(m, -160, 88, 2.6)
        kincirAngin(m, -122, 178, math.rad(135))
        sumur(m, -44, 76)
        gerobak(m, -56, 84, math.rad(20))
end

local function alunAlun(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "AlunAlun"
        m.Parent = parent
        -- PERBAIKAN TENGGELAM PLAZA: slab plaza 0.275 stud di atas tanah,
        -- jadi SEMUA perabot plaza memakai lantai PLAZA_Y (0.28) — tanpa ini
        -- bangku/NPC/papan terkubur setengah kaki di beton.
        local PLAZA_Y = GT + 0.28
        part(m, Vector3.new(46, 0.25, 46), CFrame.new(55, GT + 0.15, -15), JALAN, Enum.Material.Concrete)
        -- lingkaran andalan di sekeliling air mancur
        local ring = part(m, Vector3.new(0.12, 19, 19), CFrame.new(55, GT + 0.36, -15) * CFrame.Angles(0, 0, math.rad(90)), TROTOAR, Enum.Material.Concrete)
        ring.Name = "PlazaRing"
        ring.Shape = Enum.PartType.Cylinder
        ring.CanCollide = false
        airMancur(m, 55, -15)
        kawananBurung(m, 55, -15)
        bangku(m, 43, -15, math.rad(-90), PLAZA_Y)
        bangku(m, 67, -15, math.rad(90), PLAZA_Y)
        bangku(m, 55, -3, math.rad(180), PLAZA_Y)
        bangku(m, 55, -27, 0, PLAZA_Y)
        lampuTaman(m, 38, -33, PLAZA_Y)
        lampuTaman(m, 72, -33, PLAZA_Y)
        lampuTaman(m, 38, 3, PLAZA_Y)
        lampuTaman(m, 72, 3, PLAZA_Y)
        -- bendera hias dua sisi air mancur
        benderaHias(m, 36, -15, 46, -15, PLAZA_Y)
        benderaHias(m, 64, -15, 74, -15, PLAZA_Y)
        -- rak sepeda pengunjung (di rumput timur plaza, bukan di slab)
        rakSepeda(m, 84, 4, 0)
        -- papan petunjuk arah bertingkat
        papanPetunjuk(m, 33, -23, PLAZA_Y)
        -- papan selamat datang dipindah dari z=-6 (dulu tepat di koridor
        -- jalan Penghubung z -12..-2, tiangnya menghalangi jalan) ke tepi
        -- barat daya plaza, bebas jalan tetapi tetap terlihat dari spawn
        part(m, Vector3.new(0.5, 9.4, 0.5), CFrame.new(33, PLAZA_Y + 4.7, -13.5), KAYU_TUA, Enum.Material.Wood)
        local papanSelamat = part(m, Vector3.new(9, 3, 0.35), CFrame.new(33, PLAZA_Y + 7.9, -13.5), KAYU, Enum.Material.Wood)
        teksPapan(papanSelamat, Enum.NormalId.Front, "SELAMAT DATANG DI DATARAN")
        teksPapan(papanSelamat, Enum.NormalId.Back, "SELAMAT DATANG DI DATARAN")
        local papanToko = part(m, Vector3.new(7.5, 2.4, 0.35), CFrame.new(33, PLAZA_Y + 4.9, -13.5), KAYU, Enum.Material.Wood)
        teksPapan(papanToko, Enum.NormalId.Front, "Toko Benih Dataran")
        teksPapan(papanToko, Enum.NormalId.Back, "Toko Benih Dataran")
        npc(m, 48, -8, math.rad(45), "Pengelola Alun-alun", Color3.fromRGB(96, 148, 92), PLAZA_Y)
        npc(m, 62, 2, math.rad(135), "Bocah Alun-alun", Color3.fromRGB(208, 148, 70), PLAZA_Y)
end

local function jalurDanGerbang(parent: Instance, hooks)
        local m = Instance.new("Model")
        m.Name = "JalurGerbang"
        m.Parent = parent

        -- === Jaringan jalan aspal masterplan ===
        -- tebal 0.24: beda 0.04 dari path hub (0.2) supaya tidak koplanar
        -- (permukaan sejajar = z-fighting kedip-kedip di persimpangan).
        -- Barat -> Kampung
        local _, hB, cxB, czB, lenB = jalanAspal(m, -170, -15, 35, -15, { nama = "Barat", tebal = 0.24 })
        hiasJalan(m, hB, cxB, czB, lenB, 12, { { -19, 47 }, { -174, -160 } })
        -- Timur -> Stepa (melintasi jembatan sungai)
        local _, hT, cxT, czT, lenT = jalanAspal(m, 77, -15, 172, -15, { nama = "Timur", tebal = 0.24 })
        hiasJalan(m, hT, cxT, czT, lenT, 12, { { 76, 90 }, { 145, 158 }, { 160, 174 } })
        -- Utara -> Sabana
        local _, hU, cxU, czU, lenU = jalanAspal(m, 55, -172, 55, -37, { nama = "Utara", tebal = 0.24 })
        hiasJalan(m, hU, cxU, czU, lenU, 12, { { -48, -36 }, { -176, -164 } })
        -- Selatan -> Perladangan
        local _, hS, cxS, czS, lenS = jalanAspal(m, 55, 6, 55, 172, { nama = "Selatan", tebal = 0.24 })
        hiasJalan(m, hS, cxS, czS, lenS, 12, { { 6, 20 }, { 160, 172 } })
        -- Penghubung spawn -> alun-alun (di atas jalur lama, sedikit lebih
        -- tebal agar rapi menimpa pertemuan jalan)
        local _, hP, cxP, czP, lenP = jalanAspal(m, -17, -7, 45, -7, { nama = "Penghubung", lebar = 10, tebal = 0.3 })
        hiasJalan(m, hP, cxP, czP, lenP, 10, { { -17, 10 }, { 30, 45 } })
        -- Jalan aspal menuju Toko Benih (berhenti sebelum dinding depan
        -- toko di z=-42 supaya aspal tidak menembus bangunan)
        jalanAspal(m, 0, -41.5, 0, -33, { nama = "PusatKota", lebar = 10, tebal = 0.24 })

        -- Zebra cross di keempat mulut jalan alun-alun
        zebraCross(m, 26, -15, true)
        zebraCross(m, 84, -15, true)
        zebraCross(m, 55, -44, false)
        zebraCross(m, 55, 14, false)

        -- Papan nama jalan di pinggir persimpangan utama
        papanJalan(m, -26, -26, "JL. KAMPUNG", math.rad(90))
        papanJalan(m, 92, -26, "JL. STEPA", math.rad(90))
        papanJalan(m, 44, -56, "JL. SABANA", 0)
        papanJalan(m, 42, 32, "JL. PERLADANGAN", 0)

        -- Jalur setapak masuk Kebun Demonstrasi dari jalan Timur
        part(m, Vector3.new(4, 0.2, 23), CFrame.new(110, GT + 0.12, 2.5), JALAN, Enum.Material.Concrete).Name = "SetapakKebun"

        gerbangKawasan(m, -170, -15, math.rad(90), "Kampung", "kampung", KAYU_TUA, hooks)
        gerbangKawasan(m, 55, -172, 0, "Sabana", "sabana", KERING, hooks)
        gerbangKawasan(m, 172, -15, math.rad(90), "Stepa", "stepa", BATU, hooks)
        gerbangKawasan(m, 55, 172, 0, "Perladangan", "perladangan", TANAH, hooks)
        BuildingKit.fenceLine(m, -174, -26, -166, -26, GT)
        BuildingKit.fenceLine(m, -174, -4, -166, -4, GT)
        part(m, Vector3.new(4, 0.3, 4), CFrame.new(-162, GT + 0.15, -24), TANAH, Enum.Material.Ground)
        tanamanDemo(m, -162, -24, "kacang_polong")
        part(m, Vector3.new(6, 0.15, 6), CFrame.new(44, GT + 0.1, -162), KERING, Enum.Material.Ground)
        part(m, Vector3.new(5, 0.15, 5), CFrame.new(67, GT + 0.1, -158), KERING, Enum.Material.Ground)
        batuAlam(m, 44, -158, 1.8)
        batuAlam(m, 166, -26, 2.2)
        batuAlam(m, 178, -6, 1.6)
        -- petak contoh sayur di tepi jalan Selatan (pindah dari tengah jalan)
        part(m, Vector3.new(8, 0.3, 2), CFrame.new(44, GT + 0.2, 164), TANAH, Enum.Material.Ground)
        part(m, Vector3.new(8, 0.3, 2), CFrame.new(66, GT + 0.2, 164), TANAH, Enum.Material.Ground)
        part(m, Vector3.new(8, 0.3, 2), CFrame.new(44, GT + 0.2, 158), TANAH, Enum.Material.Ground)
        tanamanDemo(m, 44, 164, "selada")
        tanamanDemo(m, 66, 164, "brokoli")
        tanamanDemo(m, 44, 158, "seledri")
end

-- Pasar tani di tepi jalan Selatan: 4 kios beratap garis + pedagang.
local function pasarTani(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "PasarTani"
        m.Parent = parent
        papanTeks(m, 46, 36, "PASAR TANI", math.rad(90), 6.5)
        local hijau = Color3.fromRGB(76, 140, 86)
        local merah = Color3.fromRGB(176, 84, 66)
        kiosPasar(m, 44, 18, math.rad(90), hijau, { Color3.fromRGB(96, 148, 92), Color3.fromRGB(134, 168, 72), Color3.fromRGB(196, 178, 108) })
        kiosPasar(m, 44, 28, math.rad(90), merah, { Color3.fromRGB(232, 96, 84), Color3.fromRGB(240, 196, 84), Color3.fromRGB(150, 96, 60) })
        kiosPasar(m, 66, 18, math.rad(-90), merah, { Color3.fromRGB(232, 96, 84), Color3.fromRGB(134, 168, 72), Color3.fromRGB(240, 196, 84) })
        kiosPasar(m, 66, 28, math.rad(-90), hijau, { Color3.fromRGB(96, 148, 92), Color3.fromRGB(196, 178, 108), Color3.fromRGB(150, 96, 60) })
        npc(m, 44, 23, math.rad(90), "Pedagang Sayur", Color3.fromRGB(96, 148, 92))
        npc(m, 66, 23, math.rad(-90), "Pedagang Buah", Color3.fromRGB(208, 148, 70))
        npc(m, 105.5, 4, math.rad(-90), "Penjaga Kebun", Color3.fromRGB(120, 128, 88))
        npc(m, 100, 46, math.rad(180), "Petani Muda", Color3.fromRGB(88, 108, 160))
        npc(m, 8, -52, math.rad(-90), "Penjaga Toko", Color3.fromRGB(150, 96, 120))
        -- sepeda terparkir di trotoar penghubung dekat spawn
        rakSepeda(m, 16, -2.4, 0)
        bungaLiar(m, 10, -26, 3)
end

local function sungaiJembatan(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "SungaiJembatan"
        m.Parent = parent
        local air = part(m, Vector3.new(16, 0.35, 400), CFrame.new(150, GT - 0.08, 0), AIR, Enum.Material.Glass, 0.35)
        air.CanCollide = false
        -- JEMBATAN RATA JALAN: dulu papan dek 0.6 timbul di atas jalan aspal
        -- sehingga jalan menabrak sisi dek; kini dek dihapus, jalan aspal
        -- sendiri yang melintasi sungai, ditopang tiang jembatan + pagar
        -- pengaman di kedua sisi persis di tepi jalan.
        for _, pz in ipairs({ -19.2, -10.8 }) do
                for _, px in ipairs({ 145, 155 }) do
                        part(m, Vector3.new(1.6, 4.2, 1.6), CFrame.new(px, GT - 2, pz), BATU, Enum.Material.Concrete).Name = "TiangJembatan"
                end
        end
        part(m, Vector3.new(22, 0.9, 0.45), CFrame.new(150, GT + 0.69, -20.6), KAYU_TUA, Enum.Material.Wood).Name = "PagarJembatan"
        part(m, Vector3.new(22, 0.9, 0.45), CFrame.new(150, GT + 0.69, -9.4), KAYU_TUA, Enum.Material.Wood).Name = "PagarJembatan"
        pohonAlam(m, 138, 40)
        pohonAlam(m, 166, -60, 1.1)
        pohonAlam(m, 138, -80)
        pohonAlam(m, 165, 30)
        pohonAlam(m, 137, -120)
        batuAlam(m, 160, 60, 2.4)
        batuAlam(m, 140, 100, 1.8)
        batuAlam(m, 163, -90, 2)
        -- gerobak dipindah dari tepi air (dulu setengah roda di sungai)
        gerobak(m, 137, 12, math.rad(-30))
end

-- Titik bunga liar di area rumput (dipilih manual agar tidak menginjak
-- jalan maupun bangunan).
local BUNGA_TITIK = {
        { 24, -32 }, { 20, 2 }, { 26, 6 }, { -24, 30 }, { 16, 26 }, { -20, 14 },
        { 72, 40 }, { 66, 56 }, { 42, 30 }, { 38, 52 }, { 44, 70 }, { -56, 22 },
        { -52, 66 }, { 90, 34 }, { 134, 24 }, { 40, -60 }, { 72, -56 },
        { 36, -100 }, { 72, -110 }, { -30, 10 }, { -40, -34 },
        -- pengayaan v2: rumput kosong di sepanjang koridor jalan ditanami
        { -40, 0 }, { -28, 8 }, { 30, 80 }, { 40, 140 }, { 68, 95 },
        { 72, -150 }, { 34, -90 }, { 136, 44 }, { 88, -40 }, { 20, -48 },
}

-- Pohon pelanjang untuk rumput kosong di sekitar jaringan jalan
-- (koordinat dicek manual: bebas koridor jalan, trotoar, dan bangunan).
local POHON_LAWN = {
        { -34, -2, 1 }, { 88, 4, 0.9 }, { 40, -70, 1.05 }, { 38, -110, 0.95 },
        { 70, -70, 1 }, { 75, -120, 0.9 }, { 38, 60, 1.1 }, { 36, 110, 0.95 },
        { 72, 70, 1 }, { 78, 120, 1.05 }, { -30, -32, 0.9 }, { 96, 12, 0.85 },
        -- pengayaan v71: pohon pelanjang untuk rumput kosong sisa
        { -60, -60, 1 }, { -140, -60, 1.05 }, { -140, 20, 0.95 },
        { 90, -160, 1 }, { 120, -150, 0.95 }, { 100, 60, 0.9 },
        { 30, 140, 1 }, { -20, 150, 1.05 }, { 96, -120, 0.9 }, { 136, 126, 1.05 },
}

-- Semak bulat penyeimbang rumput kosong di sepanjang jaringan jalan
local SEMAK_TITIK = {
        { -22, -30 }, { 12, -30 }, { 42, -28 }, { 92, -28 }, { 122, -30 },
        { 30, -58 }, { 80, -50 }, { 28, 22 }, { 84, 22 }, { 94, 46 },
        { 28, 90 }, { 28, 140 }, { 82, 142 }, { -32, -60 }, { -60, -30 },
        { -60, 8 }, { -6, 66 }, { 0, 96 }, { 40, 100 }, { 40, 130 },
        { 130, -40 }, { -6, 150 }, { 24, 160 }, { 90, 40 },
}

function DataranBuilder.build(hooks)
        local existing = workspace:FindFirstChild("Dataran")
        if existing then
                existing:Destroy()
        end
        local folder = Instance.new("Folder")
        folder.Name = "Dataran"
        folder.Parent = workspace
        jalurDanGerbang(folder, hooks)
        alunAlun(folder)
        permukiman(folder)
        pasarTani(folder)
        kebunDemonstrasi(folder)
        perbukitanAlam(folder)
        sungaiJembatan(folder)
        -- kawasan baru v71: isi 4 lahan kosong besar
        tamanRakyat(folder)
        lapanganDesa(folder)
        kebunRaya(folder)
        panggungBudaya(folder)
        for _, t in ipairs(BUNGA_TITIK) do
                bungaLiar(folder, t[1], t[2], 3)
        end
        for _, p in ipairs(POHON_LAWN) do
                pohonAlam(folder, p[1], p[2], p[3])
        end
        for _, s in ipairs(SEMAK_TITIK) do
                semak(folder, s[1], s[2])
        end
        penerangan()
        return folder
end

return DataranBuilder
