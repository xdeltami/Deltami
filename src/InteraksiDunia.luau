local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Remotes = require(ReplicatedStorage:WaitForChild("Remotes"))

local sapaan = {
	NPC_BuSari = {
		"Selamat datang di Toko Benih Dataran!",
		"Ada 30 jenis benih, semuanya 1 Micda.",
		"Setelah beli, tanam benihmu di petak semai kebun demonstrasi.",
	},
	NPC_PakDarsa = {
		"Dataran damai sekali hari ini.",
		"Empat gerbang menghubungkan Dataran dengan kawasan lain.",
		"Alun-alun adalah tempat terbaik untuk bertemu pendatang baru.",
	},
	NPC_Mira = {
		"Kebun demonstrasi menampilkan contoh semua 30 jenis benih.",
		"Kenali bentuk tanamannya dulu sebelum membeli.",
		"Petak semai ada di sini, coba tanam satu benih!",
	},
}

local infoGerbang = {
	GerbangKampung = "Gerbang Barat menuju Kampung. Pilih 'Masuk Gerbang' pada papan untuk teleport ke kawasan itu.",
	GerbangSabana = "Gerbang Utara menuju Sabana. Pilih 'Masuk Gerbang' pada papan untuk teleport ke kawasan itu.",
	GerbangStepa = "Gerbang Timur menuju Stepa. Pilih 'Masuk Gerbang' pada papan untuk teleport ke kawasan itu.",
	GerbangPerladangan = "Gerbang Selatan menuju Perladangan. Pilih 'Masuk Gerbang' pada papan untuk teleport ke kawasan itu.",
}

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
	local zonaToko = workspace:WaitForChild("ZonaToko")
	local counter = zonaToko:WaitForChild("CounterToko")
	tambahPrompt(counter, "Buka Toko", "Toko Benih Dataran").Triggered:Connect(function(player)
		Remotes.InfoDataran:FireClient(player, {Jenis = "BukaToko"})
	end)
end)

task.spawn(function()
	local folderNPC = workspace:WaitForChild("NPC")
	for _, npc in ipairs(folderNPC:GetChildren()) do
		local torso = npc:FindFirstChild("Torso")
		if torso and sapaan[npc.Name] then
			local prompt = tambahPrompt(torso, "Bicara", string.gsub(npc.Name, "NPC_", ""))
			prompt.Triggered:Connect(function(player)
				local daftar = sapaan[npc.Name]
				Remotes.InfoDataran:FireClient(player, {Jenis = "NPCBicara", NPC = npc.Name, Teks = daftar[math.random(1, #daftar)]})
			end)
		end
	end
end)

task.spawn(function()
	local folderGerbang = workspace:WaitForChild("Gerbang")
	for _, gerbang in ipairs(folderGerbang:GetChildren()) do
		local papan = gerbang:FindFirstChild("PapanGerbang", true)
		if papan and infoGerbang[gerbang.Name] then
			local prompt = tambahPrompt(papan, "Info Gerbang", string.gsub(gerbang.Name, "Gerbang", "Gerbang "))
			prompt.Triggered:Connect(function(player)
				Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = infoGerbang[gerbang.Name]})
			end)
		end
	end
end)

task.spawn(function()
	local alunAlun = workspace:WaitForChild("AlunAlun")
	local papan = alunAlun:WaitForChild("PapanInfo")
	local prompt = tambahPrompt(papan, "Baca", "Papan Informasi")
	prompt.Triggered:Connect(function(player)
		Remotes.InfoDataran:FireClient(player, {Jenis = "Pesan", Teks = "Selamat datang di Dataran! Toko Benih di barat, kebun demonstrasi di timur, empat gerbang di utara, timur, selatan, dan barat."})
	end)
end)
