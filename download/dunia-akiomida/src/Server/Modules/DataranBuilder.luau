local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local BuildingKit = require(script.Parent.BuildingKit)
local CropData = require(ReplicatedStorage.Shared.CropData)

local DataranBuilder = {}

local RUMPUT = Color3.fromRGB(106, 168, 79)
local RUMPUT_TUA = Color3.fromRGB(88, 142, 66)
local TANAH = Color3.fromRGB(134, 100, 62)
local JALAN = Color3.fromRGB(178, 168, 150)
local KAYU = Color3.fromRGB(160, 110, 60)
local KAYU_TUA = Color3.fromRGB(112, 76, 42)
local DINDING = Color3.fromRGB(222, 206, 178)
local ATAP = Color3.fromRGB(168, 78, 58)
local BATU = Color3.fromRGB(142, 140, 134)
local AIR = Color3.fromRGB(96, 168, 220)
local KERING = Color3.fromRGB(196, 178, 108)
local PUTIH = Color3.fromRGB(238, 234, 224)

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

local function bangku(parent: Instance, x: number, z: number, yaw: number)
        local m = Instance.new("Model")
        m.Name = "BangkuTaman"
        m.Parent = parent
        local dudukan = part(m, Vector3.new(3.2, 0.3, 1.1), CFrame.new(x, GT + 0.85, z) * CFrame.Angles(0, yaw, 0), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(3.2, 1.1, 0.25), CFrame.new(x, GT + 1.5, z) * CFrame.Angles(0, yaw, 0) * CFrame.new(0, 0, -0.45), KAYU, Enum.Material.Wood)
        part(m, Vector3.new(0.3, 0.85, 1), CFrame.new(x, GT + 0.43, z) * CFrame.Angles(0, yaw, 0) * CFrame.new(-1.3, 0, 0), KAYU_TUA, Enum.Material.Wood)
        part(m, Vector3.new(0.3, 0.85, 1), CFrame.new(x, GT + 0.43, z) * CFrame.Angles(0, yaw, 0) * CFrame.new(1.3, 0, 0), KAYU_TUA, Enum.Material.Wood)
        return dudukan
end

local function lampuTaman(parent: Instance, x: number, z: number)
        local m = Instance.new("Model")
        m.Name = "LampuTaman"
        m.Parent = parent
        part(m, Vector3.new(0.4, 3.6, 0.4), CFrame.new(x, GT + 1.8, z), KAYU_TUA, Enum.Material.Metal)
        local bola = part(m, Vector3.new(1, 1, 1), CFrame.new(x, GT + 3.9, z), PUTIH, Enum.Material.Neon)
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
        BuildingKit.gableRoof(m, 12, 10, 2.6, 5.6, ATAP)
        m:PivotTo(CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0))
end

local function npc(parent: Instance, x: number, z: number, yaw: number, nama: string, warnaBaju: Color3)
        local m = Instance.new("Model")
        m.Name = "Warga" .. nama
        m.Parent = parent
        local cf = CFrame.new(x, GT, z) * CFrame.Angles(0, yaw, 0)
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
        local dasar = CFrame.new(x, GT, z)
        task.spawn(function()
                local t = 0
                while m.Parent do
                        local dt = RunService.Heartbeat:Wait()
                        t += dt
                        m:PivotTo(dasar * CFrame.new(0, math.abs(math.sin(t * 2)) * 0.16, 0))
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
        BuildingKit.fenceLine(m, -92, 20, -92, 42, GT)
        BuildingKit.fenceLine(m, -122, 24, -122, 46, GT)
        BuildingKit.fenceLine(m, -92, 56, -92, 78, GT)
        BuildingKit.fenceLine(m, -122, 60, -122, 82, GT)
        part(m, Vector3.new(4, 0.3, 4), CFrame.new(-88, GT + 0.15, 32), TANAH, Enum.Material.Ground)
        tanamanDemo(m, -88, 32, "selada")
        part(m, Vector3.new(4, 0.3, 4), CFrame.new(-118, GT + 0.15, 38), TANAH, Enum.Material.Ground)
        tanamanDemo(m, -118, 38, "kubis")
        lampuTaman(m, -70, 44)
        lampuTaman(m, -100, 48)
        bangku(m, -64, 36, math.rad(-90))
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
        gerobak(m, -60, 84, math.rad(20))
end

local function alunAlun(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "AlunAlun"
        m.Parent = parent
        part(m, Vector3.new(46, 0.25, 46), CFrame.new(55, GT + 0.12, -15), JALAN, Enum.Material.Concrete)
        airMancur(m, 55, -15)
        bangku(m, 43, -15, math.rad(-90))
        bangku(m, 67, -15, math.rad(90))
        bangku(m, 55, -3, math.rad(180))
        bangku(m, 55, -27, 0)
        lampuTaman(m, 38, -33)
        lampuTaman(m, 72, -33)
        lampuTaman(m, 38, 3)
        lampuTaman(m, 72, 3)
        papanTeks(m, 32.6, -26, "SABANA (Utara)", 0, 5.4)
        papanTeks(m, 33.4, -25, "KAMPUNG (Barat)", math.rad(90), 4.3)
        papanTeks(m, 34.2, -24, "STEPA (Timur)", math.rad(-90), 3.2)
        papanTeks(m, 33, -23, "PERLADANGAN (Selatan)", math.rad(180), 2.1)
        part(m, Vector3.new(0.5, 9.4, 0.5), CFrame.new(33, GT + 4.7, -6), KAYU_TUA, Enum.Material.Wood)
        local papanSelamat = part(m, Vector3.new(9, 3, 0.35), CFrame.new(33, GT + 7.9, -6), KAYU, Enum.Material.Wood)
        teksPapan(papanSelamat, Enum.NormalId.Front, "SELAMAT DATANG DI DATARAN")
        teksPapan(papanSelamat, Enum.NormalId.Back, "SELAMAT DATANG DI DATARAN")
        local papanToko = part(m, Vector3.new(7.5, 2.4, 0.35), CFrame.new(33, GT + 4.9, -6), KAYU, Enum.Material.Wood)
        teksPapan(papanToko, Enum.NormalId.Front, "Toko Benih di Pusat Kota")
        teksPapan(papanToko, Enum.NormalId.Back, "Toko Benih di Pusat Kota")
        npc(m, 48, -8, math.rad(45), "Pengelola Alun-alun", Color3.fromRGB(96, 148, 92))
end

local function jalurDanGerbang(parent: Instance, hooks)
        local m = Instance.new("Model")
        m.Name = "JalurGerbang"
        m.Parent = parent
        part(m, Vector3.new(62, 0.2, 8), CFrame.new(14, GT + 0.12, -8), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(202, 0.2, 8), CFrame.new(-69, GT + 0.12, -15), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(8, 0.2, 134), CFrame.new(55, GT + 0.12, -105), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(72, 0.2, 8), CFrame.new(114, GT + 0.12, -15), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(22, 0.2, 8), CFrame.new(161, GT + 0.12, -15), JALAN, Enum.Material.Concrete)
        part(m, Vector3.new(8, 0.2, 164), CFrame.new(55, GT + 0.12, 90), JALAN, Enum.Material.Concrete)
        gerbangKawasan(m, -170, -15, math.rad(90), "Kampung", "kampung", KAYU_TUA, hooks)
        gerbangKawasan(m, 55, -172, 0, "Sabana", "sabana", KERING, hooks)
        gerbangKawasan(m, 172, -15, math.rad(90), "Stepa", "stepa", BATU, hooks)
        gerbangKawasan(m, 55, 172, 0, "Perladangan", "perladangan", TANAH, hooks)
        BuildingKit.fenceLine(m, -174, -26, -166, -26, GT)
        BuildingKit.fenceLine(m, -174, -4, -166, -4, GT)
        part(m, Vector3.new(4, 0.3, 4), CFrame.new(-162, GT + 0.15, -24), TANAH, Enum.Material.Ground)
        tanamanDemo(m, -162, -24, "kacang_polong")
        part(m, Vector3.new(6, 0.15, 6), CFrame.new(48, GT + 0.1, -162), KERING, Enum.Material.Ground)
        part(m, Vector3.new(5, 0.15, 5), CFrame.new(63, GT + 0.1, -158), KERING, Enum.Material.Ground)
        batuAlam(m, 44, -158, 1.8)
        batuAlam(m, 166, -26, 2.2)
        batuAlam(m, 178, -6, 1.6)
        part(m, Vector3.new(8, 0.3, 2), CFrame.new(47, GT + 0.2, 164), TANAH, Enum.Material.Ground)
        part(m, Vector3.new(8, 0.3, 2), CFrame.new(55, GT + 0.2, 164), TANAH, Enum.Material.Ground)
        part(m, Vector3.new(8, 0.3, 2), CFrame.new(63, GT + 0.2, 164), TANAH, Enum.Material.Ground)
        tanamanDemo(m, 47, 164, "selada")
        tanamanDemo(m, 55, 164, "brokoli")
        tanamanDemo(m, 63, 164, "seledri")
end

local function sungaiJembatan(parent: Instance)
        local m = Instance.new("Model")
        m.Name = "SungaiJembatan"
        m.Parent = parent
        local air = part(m, Vector3.new(16, 0.35, 400), CFrame.new(150, GT - 0.08, 0), AIR, Enum.Material.Glass, 0.35)
        air.CanCollide = false
        part(m, Vector3.new(22, 0.6, 12), CFrame.new(150, GT + 0.4, -15), KAYU, Enum.Material.WoodPlanks)
        part(m, Vector3.new(22, 0.9, 0.45), CFrame.new(150, GT + 1.35, -20.6), KAYU_TUA, Enum.Material.Wood)
        part(m, Vector3.new(22, 0.9, 0.45), CFrame.new(150, GT + 1.35, -9.4), KAYU_TUA, Enum.Material.Wood)
        pohonAlam(m, 138, 40)
        pohonAlam(m, 166, -60, 1.1)
        pohonAlam(m, 138, -80)
        batuAlam(m, 160, 60, 2.4)
        batuAlam(m, 140, 100, 1.8)
end

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
        kebunDemonstrasi(folder)
        perbukitanAlam(folder)
        sungaiJembatan(folder)
        return folder
end

return DataranBuilder
