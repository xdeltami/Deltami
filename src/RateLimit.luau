local RateLimit = {}
local data = {}

function RateLimit.Izinkan(player, kunci, maksPerDetik)
	local id = player.UserId .. ":" .. kunci
	local sekarang = os.clock()
	local entri = data[id]
	if not entri or sekarang - entri.Awal >= 1 then
		data[id] = {Awal = sekarang, Hitung = 1}
		return true
	end
	entri.Hitung += 1
	return entri.Hitung <= maksPerDetik
end

function RateLimit.Bersihkan(player)
	local awalan = tostring(player.UserId) .. ":"
	for id in pairs(data) do
		if string.sub(id, 1, #awalan) == awalan then
			data[id] = nil
		end
	end
end

return RateLimit
