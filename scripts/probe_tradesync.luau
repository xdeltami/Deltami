-- PROBE: apakah handler TradeSync terhubung di klien?
local rawreq = require
local Stub = rawreq("./sim/roblox_stub")
Stub.install()

-- minimal: load server + client seperti playtest
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local MOD_CropData = (function()
local d = require("./../../download/dunia-akiomida/src/Shared/CropData")
return d
end)()

-- gunakan pola playtest: server init lalu client init
script = Stub.serverScript()
local __SIM_IS_SERVER = true
local RUN_init_server = nil

local f = ReplicatedStorage:FindFirstChild("Remotes")
local netInit = require(ReplicatedStorage.Remotes)
netInit.init()

local profStore = Stub.Services.DataStoreService:GetDataStore("AKM_T1")
profStore.__data["u_1001"] = { m = 10000, t = {}, dev = false }
local P1 = Stub.addPlayer(1001, "akiomida")
Stub.giveCharacter(P1, 0, 6, 44)
Players.PlayerAdded:Fire(P1)
Stub.Scheduler.advance(0.5)

local pg = Instance.new("Folder")
pg.Name = "PlayerGui"
pg.Parent = P1
__SIM_IS_SERVER = false
script = Stub.clientScript()
Stub.setLocalPlayer(P1)

-- load UIController (yang memanggil TradeUI)
local uiSrc = MOD_TradeUI -- akan nil; muat manual lewat require file
