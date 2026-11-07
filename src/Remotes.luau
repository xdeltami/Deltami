local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Remotes = {}
local namaFolder = "RemoteDataran"
local daftarRemote = {
	{Nama = "PermintaanToko", Kelas = "RemoteEvent"},
	{Nama = "AksiKebun", Kelas = "RemoteEvent"},
	{Nama = "InfoDataran", Kelas = "RemoteEvent"},
	{Nama = "AmbilData", Kelas = "RemoteFunction"},
}

local folder
if RunService:IsServer() then
	folder = ReplicatedStorage:FindFirstChild(namaFolder)
	if not folder then
		folder = Instance.new("Folder")
		folder.Name = namaFolder
		folder.Parent = ReplicatedStorage
	end
	for _, info in ipairs(daftarRemote) do
		if not folder:FindFirstChild(info.Nama) then
			local remote = Instance.new(info.Kelas)
			remote.Name = info.Nama
			remote.Parent = folder
		end
	end
else
	folder = ReplicatedStorage:WaitForChild(namaFolder, 20)
end

for _, info in ipairs(daftarRemote) do
	if folder then
		if RunService:IsServer() then
			Remotes[info.Nama] = folder:FindFirstChild(info.Nama)
		else
			Remotes[info.Nama] = folder:WaitForChild(info.Nama, 20)
		end
	end
end

return Remotes
