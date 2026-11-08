local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameConfig = require(ReplicatedStorage:WaitForChild("GameConfig"))
local Remotes = require(ReplicatedStorage:WaitForChild("Remotes"))
local RateLimit = require(script.Parent:WaitForChild("RateLimit"))

local DataService = {}
local store = nil
local dataPemain = {}

pcall(function()
	store = DataStoreService:GetDataStore("DataranData_v1")
end)

local function dataBaru()
	return {Micda = GameConfig.MicdaAwal, Tas = {}}
end

local function kunciItem(jenis, id)
	return jenis .. "_" .. id
end

local function muatData(player)
	if dataPemain[player.UserId] then
		return
	end
	local data = dataBaru()
	if store then
		local ok, hasil = pcall(function()
			return store:GetAsync("P_" .. player.UserId)
		end)
		if ok and type(hasil) == "table" then
			data.Micda = tonumber(hasil.Micda) or data.Micda
			if type(hasil.Tas) == "table" then
				data.Tas = hasil.Tas
			end
		end
	end
	if data.Micda > GameConfig.MicdaMaks then
		data.Micda = GameConfig.MicdaMaks
	end
	dataPemain[player.UserId] = data
	Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Selamat datang di " .. GameConfig.TempatIni .. "! " .. GameConfig.FormatMicda(data.Micda) .. " Micda sudah terisi di akunmu."})
	DataService.KirimData(player)
end

local function simpanData(player)
	local data = dataPemain[player.UserId]
	if not store or not data then
		return
	end
	pcall(function()
		store:UpdateAsync("P_" .. player.UserId, function()
			return data
		end)
	end)
end

function DataService.Ambil(player)
	return dataPemain[player.UserId]
end

function DataService.KirimData(player)
	local data = dataPemain[player.UserId]
	if data then
		Remotes.InfoDataran:FireClient(player, {Jenis = "Data", Micda = data.Micda, Tas = data.Tas})
	end
end

function DataService.UbahMicda(player, delta)
	local data = dataPemain[player.UserId]
	if not data then
		return false
	end
	local hasil = data.Micda + delta
	if hasil < 0 then
		return false
	end
	if hasil > GameConfig.MicdaMaks then
		hasil = GameConfig.MicdaMaks
	end
	data.Micda = hasil
	return true
end

function DataService.HadiahBicara(player, jumlah)
	if not jumlah or jumlah <= 0 then
		return 0
	end
	if jumlah > GameConfig.HadiahBicaraMaks then
		jumlah = GameConfig.HadiahBicaraMaks
	end
	DataService.UbahMicda(player, jumlah)
	DataService.KirimData(player)
	return jumlah
end

function DataService.TambahItem(player, jenis, id, jumlah)
	local data = dataPemain[player.UserId]
	if not data or jumlah <= 0 then
		return false
	end
	local kunci = kunciItem(jenis, id)
	local slot = data.Tas[kunci]
	if slot then
		if slot.Jumlah + jumlah > GameConfig.IsiPerSlotMaks then
			return false
		end
		slot.Jumlah += jumlah
	else
		if GameConfig.SlotTasTerpakai(data.Tas) >= GameConfig.TasSlotMaks then
			return false
		end
		data.Tas[kunci] = {Jenis = jenis, Id = id, Jumlah = jumlah}
	end
	return true
end

function DataService.KurangiItem(player, jenis, id, jumlah)
	local data = dataPemain[player.UserId]
	if not data or jumlah <= 0 then
		return false
	end
	local kunci = kunciItem(jenis, id)
	local slot = data.Tas[kunci]
	if not slot or slot.Jumlah < jumlah then
		return false
	end
	slot.Jumlah -= jumlah
	if slot.Jumlah <= 0 then
		data.Tas[kunci] = nil
	end
	return true
end

Remotes.AmbilData.OnServerInvoke = function(player)
	if not RateLimit.Izinkan(player, "Data", 3) then
		return nil
	end
	local data = dataPemain[player.UserId]
	if not data then
		return nil
	end
	return {Micda = data.Micda, Tas = data.Tas}
end

Players.PlayerAdded:Connect(muatData)
for _, player in ipairs(Players:GetPlayers()) do
	task.spawn(muatData, player)
end

Players.PlayerRemoving:Connect(function(player)
	simpanData(player)
	dataPemain[player.UserId] = nil
	RateLimit.Bersihkan(player)
end)

task.spawn(function()
	while true do
		task.wait(120)
		for _, player in ipairs(Players:GetPlayers()) do
			simpanData(player)
		end
	end
end)

game:BindToClose(function()
	for _, player in ipairs(Players:GetPlayers()) do
		simpanData(player)
	end
end)

return DataService
