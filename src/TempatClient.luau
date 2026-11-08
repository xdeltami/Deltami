local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local GuiService = game:GetService("GuiService")

local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

if playerGui:FindFirstChild("MicdaHud") then
	return
end

local GameConfig = require(ReplicatedStorage:WaitForChild("GameConfig"))
local Remotes = require(ReplicatedStorage:WaitForChild("Remotes"))

local keadaan = {Micda = GameConfig.MicdaAwal}

local function buat(kelas, sifat, induk)
	local objek = Instance.new(kelas)
	for kunci, nilai in pairs(sifat) do
		objek[kunci] = nilai
	end
	objek.Parent = induk
	return objek
end

local hud = buat("ScreenGui", {Name = "MicdaHud", ResetOnSpawn = false, IgnoreGuiInset = true, DisplayOrder = 20}, playerGui)

local pil = buat("TextButton", {
	Name = "PilMicda",
	AnchorPoint = Vector2.new(0.5, 0),
	Position = UDim2.new(0.5, 0, 0, 70),
	Size = UDim2.new(0, 220, 0, 44),
	BackgroundColor3 = Color3.fromRGB(24, 26, 22),
	BackgroundTransparency = 0.12,
	BorderSizePixel = 0,
	Text = "",
	AutoButtonColor = false,
}, hud)
buat("UICorner", {CornerRadius = UDim.new(1, 0)}, pil)
buat("UIStroke", {Color = Color3.fromRGB(212, 175, 55), Thickness = 2, Transparency = 0.25}, pil)

local ikon = buat("Frame", {
	Name = "IkonMicda",
	Position = UDim2.new(0, 9, 0.5, -13),
	Size = UDim2.new(0, 26, 0, 26),
	BackgroundColor3 = Color3.fromRGB(246, 198, 62),
	BorderSizePixel = 0,
}, pil)
buat("UICorner", {CornerRadius = UDim.new(1, 0)}, ikon)
buat("UIStroke", {Color = Color3.fromRGB(150, 104, 18), Thickness = 2}, ikon)
buat("TextLabel", {
	Text = "M",
	Size = UDim2.new(1, 0, 1, 0),
	BackgroundTransparency = 1,
	TextColor3 = Color3.fromRGB(126, 86, 10),
	TextScaled = true,
	Font = Enum.Font.GothamBlack,
}, ikon)

buat("TextLabel", {
	Text = "MICDA",
	Position = UDim2.new(0, 44, 0, 6),
	Size = UDim2.new(0, 64, 0, 12),
	BackgroundTransparency = 1,
	TextColor3 = Color3.fromRGB(214, 178, 92),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	TextXAlignment = Enum.TextXAlignment.Left,
}, pil)

local labelPil = buat("TextLabel", {
	Name = "JumlahMicda",
	Text = "0",
	Position = UDim2.new(0, 44, 0, 18),
	Size = UDim2.new(1, -98, 0, 22),
	BackgroundTransparency = 1,
	TextColor3 = Color3.fromRGB(255, 222, 130),
	TextScaled = true,
	Font = Enum.Font.GothamBlack,
	TextXAlignment = Enum.TextXAlignment.Left,
}, pil)

local labelPenuh = buat("TextLabel", {
	Name = "MicdaPenuh",
	AnchorPoint = Vector2.new(0.5, 0),
	Position = UDim2.new(0.5, 0, 1, 6),
	Size = UDim2.new(1.4, 0, 0, 24),
	BackgroundColor3 = Color3.fromRGB(18, 20, 16),
	BackgroundTransparency = 0.1,
	TextColor3 = Color3.fromRGB(255, 222, 130),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	BorderSizePixel = 0,
	Visible = false,
}, pil)
buat("UICorner", {CornerRadius = UDim.new(0, 8)}, labelPenuh)
buat("UIStroke", {Color = Color3.fromRGB(212, 175, 55), Thickness = 1}, labelPenuh)

local function aturPosisiHud()
	local inset = GuiService:GetTopbarInsets()
	pil.Position = UDim2.new(0.5, 0, 0, inset.Top + 8)
end
aturPosisiHud()
GuiService:GetPropertyChangedSignal("TopbarInset"):Connect(aturPosisiHud)

local function perbaruiMicda()
	labelPil.Text = GameConfig.FormatMicda(keadaan.Micda)
end

local tokenPenuh = 0
pil.Activated:Connect(function()
	tokenPenuh += 1
	local token = tokenPenuh
	labelPenuh.Text = GameConfig.FormatAngkaPenuh(keadaan.Micda) .. " Micda"
	labelPenuh.Visible = true
	task.delay(3, function()
		if tokenPenuh == token then
			labelPenuh.Visible = false
		end
	end)
end)

local kotak = buat("Frame", {
	Name = "KotakCerita",
	AnchorPoint = Vector2.new(0.5, 1),
	Position = UDim2.new(0.5, 0, 1, -12),
	Size = UDim2.new(0.72, 0, 0, 86),
	BackgroundColor3 = Color3.fromRGB(20, 23, 18),
	BackgroundTransparency = 0.06,
	BorderSizePixel = 0,
	Visible = false,
}, playerGui)
buat("UICorner", {CornerRadius = UDim.new(0, 12)}, kotak)
buat("UIStroke", {Color = Color3.fromRGB(212, 175, 55), Thickness = 1.5, Transparency = 0.3}, kotak)

local labelSiapa = buat("TextLabel", {
	Name = "Siapa",
	Text = "",
	Position = UDim2.new(0, 14, 0, 8),
	Size = UDim2.new(0.6, 0, 0, 18),
	BackgroundTransparency = 1,
	TextColor3 = Color3.fromRGB(214, 178, 92),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	TextXAlignment = Enum.TextXAlignment.Left,
}, kotak)

local labelTeks = buat("TextLabel", {
	Name = "Teks",
	Text = "",
	Position = UDim2.new(0, 14, 0, 28),
	Size = UDim2.new(1, -28, 0, 52),
	BackgroundTransparency = 1,
	TextColor3 = Color3.fromRGB(240, 236, 220),
	TextScaled = true,
	Font = Enum.Font.Gotham,
	TextWrapped = true,
	TextXAlignment = Enum.TextXAlignment.Left,
	TextYAlignment = Enum.TextYAlignment.Top,
}, kotak)

local tokenKotak = 0
local function tampilKotak(siapa, teks, lama)
	tokenKotak += 1
	local token = tokenKotak
	labelSiapa.Text = siapa
	labelTeks.Text = teks
	kotak.Visible = true
	task.delay(lama or 6, function()
		if tokenKotak == token then
			kotak.Visible = false
		end
	end)
end

Remotes.InfoDataran.OnClientEvent:Connect(function(paket)
	if type(paket) ~= "table" then
		return
	end
	local jenis = paket.Jenis
	if jenis == "Data" then
		keadaan.Micda = tonumber(paket.Micda) or keadaan.Micda
		perbaruiMicda()
	elseif jenis == "Pesan" then
		tampilKotak(GameConfig.TempatIni, tostring(paket.Teks))
	elseif jenis == "NPCBicara" then
		tampilKotak(string.gsub(tostring(paket.NPC), "NPC_", ""), tostring(paket.Teks), 7)
	end
end)

task.spawn(function()
	local ok, data = pcall(function()
		return Remotes.AmbilData:InvokeServer()
	end)
	if ok and type(data) == "table" then
		keadaan.Micda = tonumber(data.Micda) or keadaan.Micda
		perbaruiMicda()
	end
end)

perbaruiMicda()
