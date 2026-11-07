local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local GuiService = game:GetService("GuiService")

local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

if playerGui:FindFirstChild("TokoBenihGui") then
	return
end

local GameConfig = require(ReplicatedStorage:WaitForChild("GameConfig"))
local Remotes = require(ReplicatedStorage:WaitForChild("Remotes"))

local keadaan = {Micda = GameConfig.MicdaAwal, Tas = {}}
local tabAktif = "Toko"
local kategoriAktif = "Semua"
local petakDipilih = nil
local tokenBanner = 0

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

local gui = buat("ScreenGui", {Name = "TokoBenihGui", ResetOnSpawn = false, DisplayOrder = 5}, playerGui)

local root = buat("Frame", {
	Name = "Root",
	AnchorPoint = Vector2.new(0.5, 0.5),
	Position = UDim2.new(0.5, 0, 0.5, 0),
	Size = UDim2.new(0.94, 0, 0.86, 0),
	BackgroundColor3 = Color3.fromRGB(28, 32, 26),
	BackgroundTransparency = 0.04,
	BorderSizePixel = 0,
	Visible = false,
}, gui)
buat("UICorner", {CornerRadius = UDim.new(0, 14)}, root)
buat("UIStroke", {Color = Color3.fromRGB(96, 116, 76), Thickness = 2}, root)

local judul = buat("TextLabel", {
	Text = "TOKO BENIH DATARAN",
	Position = UDim2.new(0, 14, 0, 10),
	Size = UDim2.new(0.5, 0, 0, 32),
	BackgroundTransparency = 1,
	TextColor3 = Color3.fromRGB(240, 236, 220),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	TextXAlignment = Enum.TextXAlignment.Left,
}, root)

local labelMicda = buat("TextLabel", {
	Text = "Micda: 0",
	AnchorPoint = Vector2.new(1, 0),
	Position = UDim2.new(1, -56, 0, 10),
	Size = UDim2.new(0, 170, 0, 30),
	BackgroundColor3 = Color3.fromRGB(46, 52, 42),
	TextColor3 = Color3.fromRGB(255, 214, 120),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	BorderSizePixel = 0,
}, root)
buat("UICorner", {CornerRadius = UDim.new(0, 8)}, labelMicda)

local tombolTutup = buat("TextButton", {
	Text = "X",
	AnchorPoint = Vector2.new(1, 0),
	Position = UDim2.new(1, -10, 0, 10),
	Size = UDim2.new(0, 36, 0, 30),
	BackgroundColor3 = Color3.fromRGB(140, 56, 48),
	TextColor3 = Color3.fromRGB(255, 255, 255),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	BorderSizePixel = 0,
}, root)
buat("UICorner", {CornerRadius = UDim.new(0, 8)}, tombolTutup)

local tabToko = buat("TextButton", {
	Text = "Toko",
	Position = UDim2.new(0, 14, 0, 48),
	Size = UDim2.new(0, 90, 0, 30),
	BackgroundColor3 = Color3.fromRGB(64, 128, 66),
	TextColor3 = Color3.fromRGB(255, 255, 255),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	BorderSizePixel = 0,
}, root)
buat("UICorner", {CornerRadius = UDim.new(0, 8)}, tabToko)

local tabTas = buat("TextButton", {
	Text = "Tas",
	Position = UDim2.new(0, 112, 0, 48),
	Size = UDim2.new(0, 90, 0, 30),
	BackgroundColor3 = Color3.fromRGB(56, 62, 50),
	TextColor3 = Color3.fromRGB(220, 220, 210),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	BorderSizePixel = 0,
}, root)
buat("UICorner", {CornerRadius = UDim.new(0, 8)}, tabTas)

local barKategori = buat("Frame", {
	Position = UDim2.new(0, 14, 0, 86),
	Size = UDim2.new(1, -28, 0, 26),
	BackgroundTransparency = 1,
}, root)
buat("UIListLayout", {FillDirection = Enum.FillDirection.Horizontal, Padding = UDim.new(0, 6), SortOrder = Enum.SortOrder.LayoutOrder}, barKategori)

local daftarToko = buat("ScrollingFrame", {
	Position = UDim2.new(0, 14, 0, 120),
	Size = UDim2.new(1, -28, 1, -134),
	BackgroundTransparency = 1,
	BorderSizePixel = 0,
	ScrollBarThickness = 6,
	CanvasSize = UDim2.new(0, 0, 0, 0),
	AutomaticCanvasSize = Enum.AutomaticSize.Y,
}, root)
buat("UIGridLayout", {CellSize = UDim2.new(0.5, -6, 0, 140), CellPadding = UDim2.new(0, 6, 0, 6), SortOrder = Enum.SortOrder.LayoutOrder}, daftarToko)

local daftarTas = buat("ScrollingFrame", {
	Position = UDim2.new(0, 14, 0, 120),
	Size = UDim2.new(1, -28, 1, -134),
	BackgroundTransparency = 1,
	BorderSizePixel = 0,
	ScrollBarThickness = 6,
	CanvasSize = UDim2.new(0, 0, 0, 0),
	AutomaticCanvasSize = Enum.AutomaticSize.Y,
	Visible = false,
}, root)
buat("UIListLayout", {Padding = UDim.new(0, 6), SortOrder = Enum.SortOrder.LayoutOrder}, daftarTas)

local banner = buat("TextLabel", {
	Text = "",
	AnchorPoint = Vector2.new(0.5, 1),
	Position = UDim2.new(0.5, 0, 1, -14),
	Size = UDim2.new(0.84, 0, 0, 34),
	BackgroundColor3 = Color3.fromRGB(18, 20, 16),
	BackgroundTransparency = 0.1,
	TextColor3 = Color3.fromRGB(245, 240, 226),
	TextScaled = true,
	Font = Enum.Font.GothamMedium,
	BorderSizePixel = 0,
	Visible = false,
}, root)
buat("UICorner", {CornerRadius = UDim.new(0, 10)}, banner)

local picker = buat("Frame", {
	Name = "Picker",
	AnchorPoint = Vector2.new(0.5, 0.5),
	Position = UDim2.new(0.5, 0, 0.5, 0),
	Size = UDim2.new(0, 300, 0, 330),
	BackgroundColor3 = Color3.fromRGB(36, 42, 34),
	BorderSizePixel = 0,
	Visible = false,
	ZIndex = 10,
}, root)
buat("UICorner", {CornerRadius = UDim.new(0, 12)}, picker)
buat("UIStroke", {Color = Color3.fromRGB(96, 116, 76), Thickness = 2}, picker)

buat("TextLabel", {
	Text = "Pilih Benih untuk Ditanam",
	Position = UDim2.new(0, 10, 0, 8),
	Size = UDim2.new(1, -20, 0, 28),
	BackgroundTransparency = 1,
	TextColor3 = Color3.fromRGB(240, 236, 220),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	ZIndex = 10,
}, picker)

local daftarPicker = buat("ScrollingFrame", {
	Position = UDim2.new(0, 10, 0, 42),
	Size = UDim2.new(1, -20, 1, -56),
	BackgroundTransparency = 1,
	BorderSizePixel = 0,
	ScrollBarThickness = 6,
	CanvasSize = UDim2.new(0, 0, 0, 0),
	AutomaticCanvasSize = Enum.AutomaticSize.Y,
	ZIndex = 10,
}, picker)
buat("UIListLayout", {Padding = UDim.new(0, 6), SortOrder = Enum.SortOrder.LayoutOrder}, daftarPicker)

local tombolPickerTutup = buat("TextButton", {
	Text = "Batal",
	Position = UDim2.new(0, 10, 1, -36),
	Size = UDim2.new(1, -20, 0, 28),
	BackgroundColor3 = Color3.fromRGB(96, 62, 52),
	TextColor3 = Color3.fromRGB(255, 255, 255),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	BorderSizePixel = 0,
	ZIndex = 10,
}, picker)
buat("UICorner", {CornerRadius = UDim.new(0, 8)}, tombolPickerTutup)

local tombolToko = buat("TextButton", {
	Text = "TOKO",
	AnchorPoint = Vector2.new(1, 1),
	Position = UDim2.new(1, -14, 1, -14),
	Size = UDim2.new(0, 68, 0, 46),
	BackgroundColor3 = Color3.fromRGB(64, 128, 66),
	TextColor3 = Color3.fromRGB(255, 255, 255),
	TextScaled = true,
	Font = Enum.Font.GothamBold,
	BorderSizePixel = 0,
}, gui)
buat("UICorner", {CornerRadius = UDim.new(0, 10)}, tombolToko)

local function tampilBanner(teks)
	tokenBanner += 1
	local token = tokenBanner
	banner.Text = teks
	banner.Visible = true
	task.delay(3, function()
		if tokenBanner == token then
			banner.Visible = false
		end
	end)
end

local function perbaruiMicda()
	labelMicda.Text = "Micda: " .. GameConfig.FormatMicda(keadaan.Micda)
	labelPil.Text = GameConfig.FormatMicda(keadaan.Micda)
end

local function bersihkan(induk)
	for _, anak in ipairs(induk:GetChildren()) do
		if not anak:IsA("UIGridLayout") and not anak:IsA("UIListLayout") then
			anak:Destroy()
		end
	end
end

local function buatKartu(benih)
	local kartu = buat("Frame", {Name = "Kartu" .. benih.Id, BackgroundColor3 = Color3.fromRGB(46, 52, 42), BorderSizePixel = 0}, daftarToko)
	buat("UICorner", {CornerRadius = UDim.new(0, 10)}, kartu)
	local swatch = buat("Frame", {Size = UDim2.new(0, 26, 0, 26), Position = UDim2.new(0.5, -13, 0, 8), BackgroundColor3 = benih.Warna, BorderSizePixel = 0}, kartu)
	buat("UICorner", {CornerRadius = UDim.new(1, 0)}, swatch)
	buat("TextLabel", {Text = benih.Nama, Position = UDim2.new(0, 6, 0, 38), Size = UDim2.new(1, -12, 0, 36), BackgroundTransparency = 1, TextColor3 = Color3.fromRGB(240, 236, 220), TextScaled = true, TextWrapped = true, Font = Enum.Font.GothamBold}, kartu)
	buat("TextLabel", {Text = "Harga: " .. benih.Harga .. " " .. GameConfig.MataUang, Position = UDim2.new(0, 6, 0, 74), Size = UDim2.new(1, -12, 0, 16), BackgroundTransparency = 1, TextColor3 = Color3.fromRGB(255, 214, 120), TextScaled = true, Font = Enum.Font.Gotham}, kartu)
	buat("TextLabel", {Text = "Tumbuh: " .. benih.WaktuTumbuh .. " detik", Position = UDim2.new(0, 6, 0, 90), Size = UDim2.new(1, -12, 0, 16), BackgroundTransparency = 1, TextColor3 = Color3.fromRGB(190, 196, 184), TextScaled = true, Font = Enum.Font.Gotham}, kartu)
	local tombol = buat("TextButton", {Text = "BELI BENIH", Position = UDim2.new(0, 10, 0, 108), Size = UDim2.new(1, -20, 0, 24), BackgroundColor3 = Color3.fromRGB(64, 128, 66), TextColor3 = Color3.fromRGB(255, 255, 255), TextScaled = true, Font = Enum.Font.GothamBold, BorderSizePixel = 0}, kartu)
	buat("UICorner", {CornerRadius = UDim.new(0, 8)}, tombol)
	tombol.MouseButton1Click:Connect(function()
		Remotes.PermintaanToko:FireServer({Aksi = "Beli", BenihId = benih.Id})
	end)
end

local function renderToko()
	bersihkan(daftarToko)
	for _, benih in ipairs(GameConfig.Benih) do
		if kategoriAktif == "Semua" or benih.Kategori == kategoriAktif then
			buatKartu(benih)
		end
	end
end

local function renderTas()
	bersihkan(daftarTas)
	local entri = {}
	for kunci, slot in pairs(keadaan.Tas) do
		table.insert(entri, slot)
	end
	table.sort(entri, function(a, b)
		if a.Jenis == b.Jenis then
			return a.Id < b.Id
		end
		return a.Jenis < b.Jenis
	end)
	if #entri == 0 then
		buat("TextLabel", {Text = "Tas masih kosong", Size = UDim2.new(1, -8, 0, 40), BackgroundTransparency = 1, TextColor3 = Color3.fromRGB(190, 196, 184), TextScaled = true, Font = Enum.Font.Gotham}, daftarTas)
		return
	end
	for _, slot in ipairs(entri) do
		local benih = GameConfig.BenihPerId[slot.Id]
		local baris = buat("Frame", {Size = UDim2.new(1, -8, 0, 32), BackgroundColor3 = Color3.fromRGB(46, 52, 42), BorderSizePixel = 0}, daftarTas)
		buat("UICorner", {CornerRadius = UDim.new(0, 8)}, baris)
		local dot = buat("Frame", {Size = UDim2.new(0, 18, 0, 18), Position = UDim2.new(0, 8, 0.5, -9), BackgroundColor3 = benih and benih.Warna or Color3.fromRGB(160, 160, 160), BorderSizePixel = 0}, baris)
		buat("UICorner", {CornerRadius = UDim.new(1, 0)}, dot)
		buat("TextLabel", {Text = (slot.Jenis == "Benih" and "Benih " or "Hasil ") .. (benih and benih.Nama or tostring(slot.Id)) .. "  x" .. tostring(slot.Jumlah), Position = UDim2.new(0, 34, 0, 0), Size = UDim2.new(1, -42, 1, 0), BackgroundTransparency = 1, TextColor3 = Color3.fromRGB(240, 236, 220), TextScaled = true, TextXAlignment = Enum.TextXAlignment.Left, Font = Enum.Font.Gotham}, baris)
	end
end

local function renderKategori()
	bersihkan(barKategori)
	local daftar = {"Semua"}
	for _, kategori in ipairs(GameConfig.Kategori) do
		table.insert(daftar, kategori)
	end
	for urutan, nama in ipairs(daftar) do
		local aktif = nama == kategoriAktif
		local tombol = buat("TextButton", {
			Text = nama,
			Size = UDim2.new(0, 84, 1, 0),
			BackgroundColor3 = aktif and Color3.fromRGB(64, 128, 66) or Color3.fromRGB(56, 62, 50),
			TextColor3 = aktif and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(200, 204, 192),
			TextScaled = true,
			Font = Enum.Font.GothamMedium,
			BorderSizePixel = 0,
			LayoutOrder = urutan,
		}, barKategori)
		buat("UICorner", {CornerRadius = UDim.new(0, 8)}, tombol)
		tombol.MouseButton1Click:Connect(function()
			kategoriAktif = nama
			renderKategori()
			renderToko()
		end)
	end
end

local function aturTab(nama)
	tabAktif = nama
	daftarToko.Visible = nama == "Toko"
	daftarTas.Visible = nama == "Tas"
	barKategori.Visible = nama == "Toko"
	tabToko.BackgroundColor3 = nama == "Toko" and Color3.fromRGB(64, 128, 66) or Color3.fromRGB(56, 62, 50)
	tabTas.BackgroundColor3 = nama == "Tas" and Color3.fromRGB(64, 128, 66) or Color3.fromRGB(56, 62, 50)
	if nama == "Tas" then
		renderTas()
	end
end

tabToko.MouseButton1Click:Connect(function()
	aturTab("Toko")
end)
tabTas.MouseButton1Click:Connect(function()
	aturTab("Tas")
end)
tombolTutup.MouseButton1Click:Connect(function()
	root.Visible = false
end)
tombolToko.MouseButton1Click:Connect(function()
	root.Visible = not root.Visible
end)

local function bukaPicker(namaPetak)
	petakDipilih = namaPetak
	bersihkan(daftarPicker)
	local ada = false
	local entri = {}
	for _, slot in pairs(keadaan.Tas) do
		if slot.Jenis == "Benih" and slot.Jumlah > 0 then
			table.insert(entri, slot)
		end
	end
	table.sort(entri, function(a, b)
		return a.Id < b.Id
	end)
	for _, slot in ipairs(entri) do
		local benih = GameConfig.BenihPerId[slot.Id]
		if benih then
			ada = true
			local tombol = buat("TextButton", {Text = benih.Nama .. "  x" .. slot.Jumlah, Size = UDim2.new(1, -8, 0, 34), BackgroundColor3 = Color3.fromRGB(56, 62, 50), TextColor3 = Color3.fromRGB(240, 236, 220), TextScaled = true, Font = Enum.Font.GothamMedium, BorderSizePixel = 0}, daftarPicker)
			buat("UICorner", {CornerRadius = UDim.new(0, 8)}, tombol)
			tombol.MouseButton1Click:Connect(function()
				if petakDipilih then
					Remotes.AksiKebun:FireServer({Aksi = "Tanam", Petak = petakDipilih, BenihId = benih.Id})
				end
				picker.Visible = false
			end)
		end
	end
	if not ada then
		buat("TextLabel", {Text = "Tidak ada benih di tas", Size = UDim2.new(1, -8, 0, 34), BackgroundTransparency = 1, TextColor3 = Color3.fromRGB(220, 140, 120), TextScaled = true, Font = Enum.Font.Gotham}, daftarPicker)
	end
	picker.Visible = true
end

tombolPickerTutup.MouseButton1Click:Connect(function()
	picker.Visible = false
end)

local function tampilBubble(namaNPC, teks)
	local folderNPC = workspace:FindFirstChild("NPC")
	local npc = folderNPC and folderNPC:FindFirstChild(namaNPC)
	local kepala = npc and npc:FindFirstChild("Kepala")
	if not kepala then
		return
	end
	local lama = kepala:FindFirstChild("BubbleDataran")
	if lama then
		lama:Destroy()
	end
	local bubble = buat("BillboardGui", {Name = "BubbleDataran", Size = UDim2.new(0, 230, 0, 70), StudsOffset = Vector3.new(0, 3.6, 0), AlwaysOnTop = true, MaxDistance = 60}, kepala)
	local kotak = buat("Frame", {Size = UDim2.new(1, 0, 1, 0), BackgroundColor3 = Color3.fromRGB(248, 244, 232), BorderSizePixel = 0}, bubble)
	buat("UICorner", {CornerRadius = UDim.new(0, 10)}, kotak)
	buat("TextLabel", {Text = teks, Size = UDim2.new(1, -12, 1, -8), Position = UDim2.new(0, 6, 0, 4), BackgroundTransparency = 1, TextColor3 = Color3.fromRGB(40, 40, 34), TextScaled = true, TextWrapped = true, Font = Enum.Font.Gotham}, kotak)
	task.delay(4, function()
		if bubble.Parent then
			bubble:Destroy()
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
		keadaan.Tas = type(paket.Tas) == "table" and paket.Tas or keadaan.Tas
		perbaruiMicda()
		if tabAktif == "Tas" then
			renderTas()
		end
	elseif jenis == "Pesan" then
		tampilBanner(tostring(paket.Teks))
	elseif jenis == "BeliSukses" then
		tampilBanner("Berhasil membeli " .. tostring(paket.Nama))
	elseif jenis == "BukaToko" then
		root.Visible = true
		aturTab("Toko")
	elseif jenis == "NPCBicara" then
		tampilBubble(tostring(paket.NPC), tostring(paket.Teks))
	elseif jenis == "MintaPilihBenih" then
		bukaPicker(tostring(paket.Petak))
	end
end)

task.spawn(function()
	local ok, data = pcall(function()
		return Remotes.AmbilData:InvokeServer()
	end)
	if ok and type(data) == "table" then
		keadaan.Micda = tonumber(data.Micda) or keadaan.Micda
		keadaan.Tas = type(data.Tas) == "table" and data.Tas or keadaan.Tas
		perbaruiMicda()
	end
end)

renderKategori()
renderToko()
perbaruiMicda()
