local TeleportService = game:GetService("TeleportService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameConfig = require(ReplicatedStorage:WaitForChild("GameConfig"))
local Remotes = require(ReplicatedStorage:WaitForChild("Remotes"))
local RateLimit = require(script.Parent:WaitForChild("RateLimit"))

local cooldown = {}

local function tujuanDari(namaGerbang)
	local target = string.gsub(namaGerbang, "^Gerbang", "")
	if target == GameConfig.TempatIni then
		return nil
	end
	local id = GameConfig.Places[target]
	if id and id ~= GameConfig.Places[GameConfig.TempatIni] then
		return id, target
	end
	return nil
end

task.spawn(function()
	local folderGerbang = workspace:WaitForChild("Gerbang", 60)
	if not folderGerbang then
		return
	end
	for _, gerbang in ipairs(folderGerbang:GetChildren()) do
		local id, nama = tujuanDari(gerbang.Name)
		local papan = gerbang:FindFirstChild("PapanGerbang", true)
		if id and papan then
			local prompt = Instance.new("ProximityPrompt")
			prompt.Name = "PromptTeleport"
			prompt.ActionText = "Masuk Gerbang"
			prompt.ObjectText = "Menuju " .. nama
			prompt.HoldDuration = 0.5
			prompt.MaxActivationDistance = 18
			prompt.RequiresLineOfSight = false
			prompt.Parent = papan
			prompt.Triggered:Connect(function(player)
				if not RateLimit.Izinkan(player, "Teleport", 2) then
					return
				end
				local sekarang = os.clock()
				if cooldown[player.UserId] and sekarang - cooldown[player.UserId] < 4 then
					return
				end
				cooldown[player.UserId] = sekarang
				Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Gerbang terbuka... menuju " .. nama .. "!"})
				local ok, err = pcall(function()
					TeleportService:TeleportAsync(id, {player})
				end)
				if not ok then
					Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Gerbang gagal membuka, coba lagi. (" .. tostring(err) .. ")"})
				end
			end)
		end
	end
end)

TeleportService.TeleportInitFailed:Connect(function(player, _, hasil)
	if player.Parent then
		Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Teleport gagal (" .. tostring(hasil) .. "), coba masuk gerbang lagi."})
	end
end)

Players.PlayerRemoving:Connect(function(player)
	cooldown[player.UserId] = nil
end)
