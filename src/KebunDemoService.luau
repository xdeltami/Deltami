local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameConfig = require(ReplicatedStorage:WaitForChild("GameConfig"))
local Remotes = require(ReplicatedStorage:WaitForChild("Remotes"))
local RateLimit = require(script.Parent:WaitForChild("RateLimit"))
local DataService = require(script.Parent:WaitForChild("DataService"))

local kebun = workspace:WaitForChild("KebunDemo")
local statusPetak = {}

local function aturPrompt(petak, teks, aktif)
	local prompt = petak:FindFirstChildOfClass("ProximityPrompt")
	if not prompt then
		prompt = Instance.new("ProximityPrompt")
		prompt.Name = "PromptPetak"
		prompt.ObjectText = "Petak Semai"
		prompt.HoldDuration = 0.4
		prompt.MaxActivationDistance = GameConfig.RadiusPetak
		prompt.RequiresLineOfSight = false
		prompt.Parent = petak
	end
	prompt.ActionText = teks
	prompt.Enabled = aktif
	return prompt
end

local function hapusVisual(petak)
	local visual = petak:FindFirstChild("VisualTanaman")
	if visual then
		visual:Destroy()
	end
end

local function buatBagian(induk, nama, ukuran, cframe, warna, bentuk)
	local bagian = Instance.new("Part")
	bagian.Name = nama
	bagian.Size = ukuran
	bagian.CFrame = cframe
	bagian.Anchored = true
	bagian.CanCollide = false
	bagian.Color = warna
	bagian.Material = Enum.Material.SmoothPlastic
	if bentuk then
		bagian.Shape = bentuk
	end
	bagian.Parent = induk
	return bagian
end

local function buatVisual(petak, benih, siap)
	hapusVisual(petak)
	local model = Instance.new("Model")
	model.Name = "VisualTanaman"
	local puncak = petak.CFrame * CFrame.new(0, petak.Size.Y / 2, 0)
	buatBagian(model, "Batang", Vector3.new(0.6, 2.4, 0.6), puncak * CFrame.new(0, 1.2, 0), Color3.fromRGB(96, 128, 56), nil)
	local daun = buatBagian(model, "Daun", Vector3.new(1.1, 1.1, 1.1), puncak * CFrame.new(0, 2.6, 0), Color3.fromRGB(104, 152, 66), Enum.PartType.Ball)
	daun.Transparency = 0.1
	local ukuranBuah = siap and Vector3.new(1.8, 1.8, 1.8) or Vector3.new(0.9, 0.9, 0.9)
	buatBagian(model, "Buah", ukuranBuah, puncak * CFrame.new(0, 3.4, 0), benih.Warna, Enum.PartType.Ball)
	model.Parent = petak
end

local function jarakAman(player, petak)
	local karakter = player.Character
	local akar = karakter and karakter:FindFirstChild("HumanoidRootPart")
	if not akar then
		return false
	end
	return (akar.Position - petak.Position).Magnitude <= GameConfig.RadiusPetak + 6
end

local function tanam(player, petak, benihId)
	local benih = GameConfig.BenihPerId[benihId]
	if not benih then
		return
	end
	if not jarakAman(player, petak) then
		return
	end
	if statusPetak[petak] then
		Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Petak sedang dipakai"})
		return
	end
	if not DataService.KurangiItem(player, "Benih", benih.Id, 1) then
		Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Benih tidak ada di tas"})
		return
	end
	statusPetak[petak] = {Pemilik = player.UserId, Benih = benih, Siap = false}
	aturPrompt(petak, "Menumbuhkan", false)
	buatVisual(petak, benih, false)
	DataService.KirimData(player)
	task.delay(benih.WaktuTumbuh, function()
		local status = statusPetak[petak]
		if not status or status.Benih.Id ~= benih.Id then
			return
		end
		status.Siap = true
		buatVisual(petak, benih, true)
		aturPrompt(petak, "Panen", true)
		local pemilik = Players:GetPlayerByUserId(status.Pemilik)
		if pemilik then
			Remotes.InfoDataran:FireClient(pemilik, {Jenis = "Pesan", Teks = benih.Nama .. " siap dipanen"})
		else
			statusPetak[petak] = nil
			hapusVisual(petak)
			aturPrompt(petak, "Tanam", true)
		end
	end)
end

local function panen(player, petak)
	local status = statusPetak[petak]
	if not status or not status.Siap then
		return
	end
	if status.Pemilik ~= player.UserId then
		Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Ini petak pemain lain"})
		return
	end
	if not jarakAman(player, petak) then
		return
	end
	local jumlah = math.random(1, 3)
	if not DataService.TambahItem(player, "Hasil", status.Benih.Id, jumlah) then
		Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Tas penuh"})
		return
	end
	local nama = status.Benih.Nama
	statusPetak[petak] = nil
	hapusVisual(petak)
	aturPrompt(petak, "Tanam", true)
	DataService.KirimData(player)
	Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Panen: " .. jumlah .. "x " .. nama})
end

local function benihPemain(player)
	local data = DataService.Ambil(player)
	local pilihan = {}
	if data then
		for _, slot in pairs(data.Tas) do
			if slot.Jenis == "Benih" and slot.Jumlah > 0 then
				table.insert(pilihan, slot.Id)
			end
		end
	end
	table.sort(pilihan)
	return pilihan
end

for i = 1, 6 do
	local petak = kebun:WaitForChild("PetakSemai" .. i)
	aturPrompt(petak, "Tanam", true).Triggered:Connect(function(player)
		if not RateLimit.Izinkan(player, "Kebun", GameConfig.BatasPermintaanPerDetik) then
			return
		end
		local status = statusPetak[petak]
		if status and status.Siap and status.Pemilik == player.UserId then
			panen(player, petak)
		elseif not status then
			local pilihan = benihPemain(player)
			if #pilihan == 0 then
				Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Belum punya benih, beli di Toko Benih"})
				return
			end
			if #pilihan == 1 then
				tanam(player, petak, pilihan[1])
			else
				Remotes.InfoDataran:FireClient(player, {Jenis = "MintaPilihBenih", Petak = petak.Name})
			end
		end
	end)
end

Remotes.AksiKebun.OnServerEvent:Connect(function(player, paket)
	if type(paket) ~= "table" or paket.Aksi ~= "Tanam" then
		return
	end
	if not RateLimit.Izinkan(player, "Kebun", GameConfig.BatasPermintaanPerDetik) then
		return
	end
	local namaPetak = tostring(paket.Petak)
	if string.sub(namaPetak, 1, 11) ~= "PetakSemai" then
		return
	end
	local petak = kebun:FindFirstChild(namaPetak)
	if not petak or statusPetak[petak] then
		return
	end
	tanam(player, petak, tonumber(paket.BenihId))
end)

Players.PlayerRemoving:Connect(function(player)
	for petak, status in pairs(statusPetak) do
		if status.Pemilik == player.UserId then
			statusPetak[petak] = nil
			hapusVisual(petak)
			aturPrompt(petak, "Tanam", true)
		end
	end
end)
