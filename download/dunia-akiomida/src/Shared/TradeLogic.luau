local TradeLogic = {}

local function jumlahTas(tas: any, kind: string, id: string): number
        local total = 0
        for _, s in ipairs(tas) do
                if s.kind == kind and s.id == id then
                        total += s.count
                end
        end
        return total
end

-- Aturan trade ditentukan server; modul ini murni logika tanpa dependensi agar
-- bisa diuji langsung lewat luau CLI. Konstanta dijaga selaras dengan TasLogic
-- (50 slot x 250 stack) dan UangLogic (MaksSaldo) lewat tes persamaan.
TradeLogic.MaksEntri = 4
TradeLogic.WaktuTawar = 150
TradeLogic.WaktuKonfirmasi = 45
TradeLogic.JarakMaks = 64
TradeLogic.TasSlotMaks = 50
TradeLogic.TasStackMaks = 250
TradeLogic.MaksSaldo = 1000000000000000

function TradeLogic.kindOk(kind: any): boolean
        return kind == "benih" or kind == "hasil"
end

function TradeLogic.entriValid(e: any, byId: any): boolean
        if type(e) ~= "table" then
                return false
        end
        if not TradeLogic.kindOk(e.kind) then
                return false
        end
        if type(e.id) ~= "string" or not byId[e.id] then
                return false
        end
        local n = e.count
        if type(n) ~= "number" or n ~= n or n == math.huge or n == -math.huge then
                return false
        end
        if n ~= math.floor(n) or n < 1 then
                return false
        end
        if n > TradeLogic.TasStackMaks * TradeLogic.TasSlotMaks then
                return false
        end
        return true
end

function TradeLogic.micdaValid(v: any): boolean
        if type(v) ~= "number" or v ~= v or v == math.huge or v == -math.huge then
                return false
        end
        if v < 0 or v ~= math.floor(v) or v > TradeLogic.MaksSaldo then
                return false
        end
        return true
end

-- Rapikan tawaran mentah dari klien: maks 4 entri unik, angka bulat, tanpa sampah.
function TradeLogic.rapikan(raw: any, byId: any): { items: { any }, micda: number }
        local out = { items = {}, micda = 0 }
        if type(raw) ~= "table" then
                return out
        end
        local seen = {}
        local items = type(raw.items) == "table" and raw.items or {}
        for _, e in ipairs(items) do
                if #out.items >= TradeLogic.MaksEntri then
                        break
                end
                if TradeLogic.entriValid(e, byId) then
                        local k = e.kind .. ":" .. e.id
                        if not seen[k] then
                                seen[k] = true
                                table.insert(out.items, { kind = e.kind, id = e.id, count = math.floor(e.count) })
                        end
                end
        end
        if TradeLogic.micdaValid(raw.micda) then
                out.micda = math.floor(raw.micda)
        end
        return out
end

-- Kunci item yang sedang ditawarkan (dipakai untuk menutup sistem lain).
function TradeLogic.kunciOf(tawar: any): { [string]: number }
        local k = {}
        for _, e in ipairs(tawar.items) do
                local s = e.kind .. ":" .. e.id
                k[s] = (k[s] or 0) + e.count
        end
        return k
end

-- Tawaran sah: tiap entri benar, jumlahnya masih dimiliki di tas, micda tidak melebihi saldo.
function TradeLogic.tawaranSah(tawar: any, byId: any, tas: any, saldo: number): (boolean, string)
        if type(tawar) ~= "table" or type(tawar.items) ~= "table" then
                return false, "Tawaran tidak sah."
        end
        if #tawar.items > TradeLogic.MaksEntri then
                return false, "Maksimal " .. tostring(TradeLogic.MaksEntri) .. " jenis item dalam satu tawaran."
        end
        for _, e in ipairs(tawar.items) do
                if not TradeLogic.entriValid(e, byId) then
                        return false, "Ada item tawaran yang tidak sah."
                end
                if jumlahTas(tas, e.kind, e.id) < e.count then
                        return false, "Item tidak cukup di tas."
                end
        end
        if not TradeLogic.micdaValid(tawar.micda) or tawar.micda > saldo then
                return false, "Micda tidak cukup."
        end
        return true, "ok"
end

-- Simulasi: tas mampu menerima barang masuk setelah barang keluar ditarik.
-- addTas/removeTas dipasok pemanggil (TasLogic.add/remove) agar tetap tanpa dependensi.
function TradeLogic.muatCukup(tas: any, keluar: any, masuk: any, addTas: any, removeTas: any): boolean
        if type(tas) ~= "table" then
                return false
        end
        local klon = TradeLogic.klonTas(tas)
        for _, e in ipairs(keluar.items) do
                removeTas(klon, e.kind, e.id, e.count)
        end
        for _, e in ipairs(masuk.items) do
                local put = addTas(klon, e.kind, e.id, e.count)
                if put < e.count then
                        return false
                end
        end
        return true
end

-- Validasi akhir sebelum eksekusi: kedua sisi sah + rekening & tas penerima cukup ruang.
-- addTas/removeTas = TasLogic.add & TasLogic.remove (dipasok pemanggil).
function TradeLogic.eksekusiSah(tawarA: any, tawarB: any, tasA: any, saldoA: number, tasB: any, saldoB: number, byId: any, addTas: any, removeTas: any): (boolean, string)
        local okA, msgA = TradeLogic.tawaranSah(tawarA, byId, tasA, saldoA)
        if not okA then
                return false, msgA
        end
        local okB, msgB = TradeLogic.tawaranSah(tawarB, byId, tasB, saldoB)
        if not okB then
                return false, msgB
        end
        if saldoB + tawarA.micda > TradeLogic.MaksSaldo then
                return false, "Rekening lawan tidak cukup ruang untuk Micdamu."
        end
        if saldoA + tawarB.micda > TradeLogic.MaksSaldo then
                return false, "Rekeningmu tidak cukup ruang untuk Micda lawan."
        end
        if not TradeLogic.muatCukup(tasA, tawarA, tawarB, addTas, removeTas) then
                return false, "Tas lawan tidak muat untuk barangmu."
        end
        if not TradeLogic.muatCukup(tasB, tawarB, tawarA, addTas, removeTas) then
                return false, "Tasmu tidak muat untuk barang lawan."
        end
        return true, "ok"
end

function TradeLogic.klonTas(tas: { any }): { any }
        local klon = {}
        for i, s in ipairs(tas) do
                klon[i] = { kind = s.kind, id = s.id, count = s.count }
        end
        return klon
end

-- Kembalikan isi tas persis seperti sebelum eksekusi (rollback atomik).
function TradeLogic.pasangKembali(tas: { any }, klon: { any })
        for i = #tas, 1, -1 do
                table.remove(tas, i)
        end
        for _, s in ipairs(klon) do
                table.insert(tas, { kind = s.kind, id = s.id, count = s.count })
        end
end

function TradeLogic.totalItem(tawar: any): number
        local n = 0
        for _, e in ipairs(tawar.items) do
                n += e.count
        end
        return n
end

return TradeLogic
