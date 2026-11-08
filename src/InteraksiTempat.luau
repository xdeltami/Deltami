local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameConfig = require(ReplicatedStorage:WaitForChild("GameConfig"))
local Remotes = require(ReplicatedStorage:WaitForChild("Remotes"))

local function tambahPrompt(induk, aksi, objek)
	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = aksi
	prompt.ObjectText = objek
	prompt.HoldDuration = 0.3
	prompt.MaxActivationDistance = 16
	prompt.RequiresLineOfSight = false
	prompt.Parent = induk
	return prompt
end

task.spawn(function()
	local folderNPC = workspace:WaitForChild("NPC", 60)
	if not folderNPC then
		return
	end
	for _, npc in ipairs(folderNPC:GetChildren()) do
		local torso = npc:FindFirstChild("Torso")
		local daftar = GameConfig.NPCTeks and GameConfig.NPCTeks[npc.Name]
		if torso and daftar then
			local prompt = tambahPrompt(torso, "Bicara", string.gsub(npc.Name, "NPC_", ""))
			prompt.Triggered:Connect(function(player)
				local teks = daftar[math.random(1, #daftar)]
				Remotes.InfoDataran:FireClient(player, {Jenis = "NPCBicara", NPC = npc.Name, Teks = teks})
			end)
		end
	end
end)

task.spawn(function()
	local folderGerbang = workspace:WaitForChild("Gerbang", 60)
	if not folderGerbang then
		return
	end
	for _, gerbang in ipairs(folderGerbang:GetChildren()) do
		local papan = gerbang:FindFirstChild("PapanGerbang", true)
		if papan then
			local tujuan = string.gsub(gerbang.Name, "^Gerbang", "")
			local prompt = tambahPrompt(papan, "Info Gerbang", "Gerbang " .. tujuan)
			prompt.Triggered:Connect(function(player)
				local teks = "Gerbang menuju " .. tujuan .. ". Dekati papan dan pilih 'Masuk Gerbang' untuk teleport ke kawasan itu."
				if tujuan == GameConfig.TempatIni then
					teks = "Gerbang kembali ke Dataran, pusat seluruh kawasan. Pilih 'Masuk Gerbang' untuk teleport."
				end
				Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = teks})
			end)
		end
	end
end)

task.spawn(function()
	local alun = workspace:FindFirstChild("PapanKawasan", true)
	if alun then
		local prompt = tambahPrompt(alun, "Baca", "Papan Informasi")
		prompt.Triggered:Connect(function(player)
			Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = GameConfig.PesanKawasan})
		end)
	end
end)
