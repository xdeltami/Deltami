local rawreq = require
local Stub = rawreq("./sim/roblox_stub")
Stub.install()
local Players = Stub.Services.Players
local RS = Stub.Services.ReplicatedStorage
local netInit = require(RS.Remotes)
netInit.init()
local P1 = Stub.addPlayer(1, "u1")
Stub.setLocalPlayer(P1)
local f = RS:FindFirstChild("Remotes")
local r = f:FindFirstChild("Notify")
r.OnClientEvent:Connect(function(a, b)
        print("CLIENT-TERIMA:", a, b)
end)
print("kirim...")
r.FireClient(P1, "Judul", "Isi")
print("selesai; LocalPlayer =", tostring(Players.LocalPlayer))
