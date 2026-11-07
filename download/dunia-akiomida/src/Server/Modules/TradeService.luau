local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local CropData = require(ReplicatedStorage.Shared.CropData)
local TradeLogic = require(ReplicatedStorage.Shared.TradeLogic)
local TasLogic = require(ReplicatedStorage.Shared.TasLogic)
local UangLogic = require(ReplicatedStorage.Shared.UangLogic)

local TradeService = {}

-- Server-authoritative trade: klien hanya mengirim aksi; semua stok, micda,
-- fase, waktu, dan eksekusi dihitung & divalidasi server. Eksekusi atomik:
-- snapshot kedua tas + rekening dulu; kegagalan apa pun memulihkan persis.
local Data, Audit, Net
local sesiByUser: { [number]: any } = {}
local semua: { any } = {}
local urutanSesi = 0
local clock = os.clock

function TradeService.bind(deps)
        Data = deps.Data
        Audit = deps.Audit
        Net = deps.Net
end

function TradeService.setClock(fn)
        clock = fn
end

function TradeService.sesiOf(player: Player): any
        return sesiByUser[player.UserId]
end

function TradeService.blokir(player: Player): string?
        if sesiByUser[player.UserId] then
                return "Selesaikan atau batalkan trade dulu."
        end
        return nil
end

local function playerOf(userId: number): Player?
        return Players:GetPlayerByUserId(userId)
end

local function payload(sesi: any, userId: number, penutup: string?, pesan: string?): any
        local lawanId = sesi.pasangan[userId]
        local p: any = {
                id = sesi.id,
                fase = sesi.fase,
                lawan = sesi.nama[lawanId],
                ku = sesi.tawar[userId],
                lawanTawar = sesi.tawar[lawanId],
                setujuKu = sesi.setuju[userId],
                setujuLawan = sesi.setuju[lawanId],
                konfirmKu = sesi.konfirmasi[userId],
                konfirmLawan = sesi.konfirmasi[lawanId],
                sisa = math.max(0, math.ceil(sesi.batas - clock())),
        }
        if penutup then
                p.penutup = penutup
        end
        if pesan then
                p.pesan = pesan
        end
        return p
end

local function siar(sesi: any, penutup: string?, pesan: string?)
        for uid in pairs(sesi.pasangan) do
                local p = playerOf(uid)
                if p then
                        Net.get("TradeSync"):FireClient(p, payload(sesi, uid, penutup, pesan))
                end
        end
end

local function hapusSesi(sesi: any)
        for uid in pairs(sesi.pasangan) do
                if sesiByUser[uid] == sesi then
                        sesiByUser[uid] = nil
                end
        end
        for i = #semua, 1, -1 do
                if semua[i] == sesi then
                        table.remove(semua, i)
                end
        end
end

local function dekat(a: Player, b: Player): boolean
        local ca, cb = a.Character, b.Character
        local ra = ca and (ca.PrimaryPart or ca:FindFirstChild("HumanoidRootPart"))
        local rb = cb and (cb.PrimaryPart or cb:FindFirstChild("HumanoidRootPart"))
        if not ra or not rb then
                return false
        end
        local jarak = (ra.Position - rb.Position).Magnitude
        if jarak ~= jarak then
                return false
        end
        return jarak <= TradeLogic.JarakMaks
end

function TradeService.ajukan(pemohon: Player, targetId: any): (boolean, string)
        if type(targetId) ~= "number" or targetId ~= targetId or targetId % 1 ~= 0 then
                return false, "Target trade tidak sah."
        end
        local target = Players:GetPlayerByUserId(targetId)
        if not target then
                return false, "Pemain itu tidak ada di server ini."
        end
        if target == pemohon then
                return false, "Tidak bisa trade dengan diri sendiri."
        end
        if sesiByUser[pemohon.UserId] then
                return false, "Kamu sedang ada dalam trade."
        end
        if sesiByUser[targetId] then
                return false, "Lawan sedang ada dalam trade lain."
        end
        if not Data.bolehSimpan(pemohon) then
                return false, "Datamu masih disinkronkan. Coba lagi sebentar."
        end
        if not Data.bolehSimpan(target) then
                return false, "Data lawan masih disinkronkan."
        end
        if not dekat(pemohon, target) then
                return false, "Dekati pemain itu dulu untuk trade."
        end
        urutanSesi += 1
        local sesi = {
                id = urutanSesi,
                pemilikA = pemohon.UserId,
                pasangan = { [pemohon.UserId] = target.UserId, [target.UserId] = pemohon.UserId },
                nama = {
                        [pemohon.UserId] = (pemohon.DisplayName and pemohon.DisplayName ~= "" and pemohon.DisplayName) or pemohon.Name,
                        [target.UserId] = (target.DisplayName and target.DisplayName ~= "" and target.DisplayName) or target.Name,
                },
                tawar = {
                        [pemohon.UserId] = { items = {}, micda = 0 },
                        [target.UserId] = { items = {}, micda = 0 },
                },
                setuju = { [pemohon.UserId] = false, [target.UserId] = false },
                konfirmasi = { [pemohon.UserId] = false, [target.UserId] = false },
                fase = "tawar",
                batas = clock() + TradeLogic.WaktuTawar,
        }
        sesiByUser[pemohon.UserId] = sesi
        sesiByUser[target.UserId] = sesi
        table.insert(semua, sesi)
        siar(sesi)
        return true, "ok"
end

function TradeService.ubah(player: Player, raw: any): (boolean, string)
        local sesi = sesiByUser[player.UserId]
        if not sesi then
                return false, "Tidak ada trade yang berjalan."
        end
        if sesi.fase ~= "tawar" then
                return false, "Tawaran sudah dikunci, hanya bisa konfirmasi atau batal."
        end
        local uid = player.UserId
        local rapi = TradeLogic.rapikan(raw, CropData.byId)
        local d = Data.get(player)
        if not d then
                return false, "Data belum siap."
        end
        local ok, msg = TradeLogic.tawaranSah(rapi, CropData.byId, d.t, UangLogic.saldo(d.u))
        if not ok then
                if Audit then
                        Audit.catat(player, "argumen", "trade_ubah:" .. tostring(msg))
                end
                return false, msg
        end
        sesi.tawar[uid] = rapi
        sesi.setuju[uid] = false
        sesi.setuju[sesi.pasangan[uid]] = false
        sesi.batas = clock() + TradeLogic.WaktuTawar
        siar(sesi)
        return true, "ok"
end

function TradeService.setuju(player: Player): (boolean, string)
        local sesi = sesiByUser[player.UserId]
        if not sesi then
                return false, "Tidak ada trade yang berjalan."
        end
        if sesi.fase ~= "tawar" then
                return false, "Sudah masuk tahap konfirmasi."
        end
        local uid = player.UserId
        local lawanId = sesi.pasangan[uid]
        sesi.setuju[uid] = not sesi.setuju[uid]
        if sesi.setuju[uid] and sesi.setuju[lawanId] then
                -- keduanya siap: validasi ulang dengan stok terbaru sebelum mengunci
                local okA, msgA = TradeService.verifikasi(sesi, sesi.pemilikA)
                local okB, msgB = TradeService.verifikasi(sesi, lawanId)
                if not okA or not okB then
                        sesi.setuju[uid] = false
                        sesi.setuju[lawanId] = false
                        local gagal = (not okA) and msgA or msgB
                        siar(sesi, nil)
                        return false, tostring(gagal)
                end
                sesi.fase = "konfirm"
                sesi.konfirmasi[uid] = false
                sesi.konfirmasi[lawanId] = false
                sesi.batas = clock() + TradeLogic.WaktuKonfirmasi
        end
        siar(sesi)
        return true, "ok"
end

-- Periksa tawaran satu sisi terhadap data TERKINI (dipakai sebelum kunci & eksekusi).
function TradeService.verifikasi(sesi: any, uid: number): (boolean, string)
        local p = playerOf(uid)
        if not p then
                return false, "Lawan tidak ada."
        end
        local d = Data.get(p)
        if not d then
                return false, "Data belum siap."
        end
        return TradeLogic.tawaranSah(sesi.tawar[uid], CropData.byId, d.t, UangLogic.saldo(d.u))
end

function TradeService.konfirm(player: Player): (boolean, string)
        local sesi = sesiByUser[player.UserId]
        if not sesi then
                return false, "Tidak ada trade yang berjalan."
        end
        if sesi.fase ~= "konfirm" then
                return false, "Belum masuk tahap konfirmasi."
        end
        local uid = player.UserId
        sesi.konfirmasi[uid] = true
        if sesi.konfirmasi[sesi.pasangan[uid]] then
                return TradeService.eksekusi(sesi)
        end
        siar(sesi)
        return true, "ok"
end

function TradeService.batalkan(sesi: any, penutup: string, pesan: string)
        hapusSesi(sesi)
        siar(sesi, penutup, pesan)
end

function TradeService.batal(player: Player): (boolean, string)
        local sesi = sesiByUser[player.UserId]
        if not sesi then
                return false, "Tidak ada trade yang berjalan."
        end
        TradeService.batalkan(sesi, "batal", "Trade dibatalkan. Semua tawaran dikembalikan.")
        return true, "ok"
end

-- Pemain keluar/mati: sesi langsung bubar, lawan diberi tahu.
function TradeService.hilang(player: Player)
        local sesi = sesiByUser[player.UserId]
        if not sesi then
                return
        end
        TradeService.batalkan(sesi, "batal", tostring(sesi.nama[player.UserId]) .. " keluar. Trade dibatalkan, tawaranmu aman.")
end

local function potongLedger(u: any, panjang: number)
        while u.ledger and #u.ledger > panjang do
                table.remove(u.ledger, #u.ledger)
        end
end

function TradeService.eksekusi(sesi: any): (boolean, string)
        local uidA, uidB = sesi.pemilikA, sesi.pasangan[sesi.pemilikA]
        local pA, pB = playerOf(uidA), playerOf(uidB)
        if not pA or not pB then
                TradeService.batalkan(sesi, "batal", "Lawan tidak ada. Trade dibatalkan.")
                return false, "Pemain hilang."
        end
        local dA, dB = Data.get(pA), Data.get(pB)
        if not dA or not dB then
                TradeService.batalkan(sesi, "batal", "Data belum siap. Trade dibatalkan.")
                return false, "Data belum siap."
        end
        local tawarA, tawarB = sesi.tawar[uidA], sesi.tawar[uidB]
        local saldoA, saldoB = UangLogic.saldo(dA.u), UangLogic.saldo(dB.u)
        local ok, msg = TradeLogic.eksekusiSah(tawarA, tawarB, dA.t, saldoA, dB.t, saldoB, CropData.byId, TasLogic.add, TasLogic.remove)
        if not ok then
                TradeService.batalkan(sesi, "batal", "Trade dibatalkan: " .. tostring(msg))
                return false, tostring(msg)
        end

        -- snapshot untuk rollback atomik
        local snapA = { tas = TradeLogic.klonTas(dA.t), m = dA.u.m, ledger = dA.u.ledger and #dA.u.ledger or 0 }
        local snapB = { tas = TradeLogic.klonTas(dB.t), m = dB.u.m, ledger = dB.u.ledger and #dB.u.ledger or 0 }
        local waktu = os.time()

        local jalan = pcall(function()
                for _, e in ipairs(tawarA.items) do
                        if TasLogic.remove(dA.t, e.kind, e.id, e.count) < e.count then
                                error("stok A berubah: " .. e.id)
                        end
                end
                for _, e in ipairs(tawarB.items) do
                        if TasLogic.remove(dB.t, e.kind, e.id, e.count) < e.count then
                                error("stok B berubah: " .. e.id)
                        end
                end
                if tawarA.micda > 0 then
                        local okB1 = UangLogic.bayar(dA.u, tawarA.micda, "trade", waktu)
                        if not okB1 then
                                error("micda A berubah")
                        end
                end
                if tawarB.micda > 0 then
                        local okB2 = UangLogic.bayar(dB.u, tawarB.micda, "trade", waktu)
                        if not okB2 then
                                error("micda B berubah")
                        end
                end
                if tawarB.micda > 0 then
                        local okT1 = UangLogic.tambah(dA.u, tawarB.micda, "trade", waktu)
                        if not okT1 then
                                error("ruang rekening A")
                        end
                end
                if tawarA.micda > 0 then
                        local okT2 = UangLogic.tambah(dB.u, tawarA.micda, "trade", waktu)
                        if not okT2 then
                                error("ruang rekening B")
                        end
                end
                for _, e in ipairs(tawarB.items) do
                        if TasLogic.add(dA.t, e.kind, e.id, e.count) < e.count then
                                error("tas A penuh")
                        end
                end
                for _, e in ipairs(tawarA.items) do
                        if TasLogic.add(dB.t, e.kind, e.id, e.count) < e.count then
                                error("tas B penuh")
                        end
                end
        end)

        if not jalan then
                TradeLogic.pasangKembali(dA.t, snapA.tas)
                TradeLogic.pasangKembali(dB.t, snapB.tas)
                dA.u.m = snapA.m
                dB.u.m = snapB.m
                potongLedger(dA.u, snapA.ledger)
                potongLedger(dB.u, snapB.ledger)
                Data.markDirty(pA)
                Data.markDirty(pB)
                Data.push(pA)
                Data.push(pB)
                if Audit then
                        Audit.catat(pA, "argumen", "trade_rollback")
                        Audit.catat(pB, "argumen", "trade_rollback")
                end
                TradeService.batalkan(sesi, "batal", "Trade gagal di tengah jalan. Semua item & Micda dikembalikan utuh.")
                return false, "Trade gagal, dikembalikan."
        end

        Data.markDirty(pA)
        Data.markDirty(pB)
        Data.push(pA)
        Data.push(pB)
        hapusSesi(sesi)
        siar(sesi, "sukses", "Trade berhasil! Barang dan Micda sudah bertukar tempat.")
        return true, "ok"
end

function TradeService.startLoops()
        task.spawn(function()
                while true do
                        task.wait(1)
                        local sekarang = clock()
                        for i = #semua, 1, -1 do
                                local s = semua[i]
                                if sekarang >= s.batas then
                                        TradeService.batalkan(s, "waktu", "Waktu trade habis. Semua tawaran dikembalikan.")
                                end
                        end
                end
        end)
end

return TradeService
