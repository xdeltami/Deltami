local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameConfig = require(ReplicatedStorage:WaitForChild("GameConfig"))
local Remotes = require(ReplicatedStorage:WaitForChild("Remotes"))
local RateLimit = require(script.Parent:WaitForChild("RateLimit"))
local DataService = require(script.Parent:WaitForChild("DataService"))

task.spawn(function()
	local zonaToko = workspace:WaitForChild("ZonaToko")
	local counter = zonaToko:WaitForChild("CounterToko")

	Remotes.PermintaanToko.OnServerEvent:Connect(function(player, paket)
		if type(paket) ~= "table" then
			return
		end
		if paket.Aksi ~= "Beli" then
			return
		end
		if not RateLimit.Izinkan(player, "Toko", GameConfig.BatasPermintaanPerDetik) then
			return
		end
		local karakter = player.Character
		local akar = karakter and karakter:FindFirstChild("HumanoidRootPart")
		if not akar then
			return
		end
		if (akar.Position - counter.Position).Magnitude > GameConfig.RadiusInteraksi + 10 then
			return
		end
		local benih = GameConfig.BenihPerId[tonumber(paket.BenihId)]
		if not benih then
			return
		end
		local data = DataService.Ambil(player)
		if not data then
			return
		end
		if data.Micda < benih.Harga then
			Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Micda tidak cukup"})
			return
		end
		if not DataService.TambahItem(player, "Benih", benih.Id, 1) then
			Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Tas penuh"})
			return
		end
		DataService.UbahMicda(player, -benih.Harga)
		DataService.KirimData(player)
		Remotes.InfoDataran:FireClient(player, {Jenis = "BeliSukses", Nama = benih.Nama})
	end)
end)
