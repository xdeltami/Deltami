local GameConfig = {}

GameConfig.NamaPlace = "Dataran"
GameConfig.MataUang = "Koin"
GameConfig.KoinAwal = 50
GameConfig.HargaBawaan = 1
GameConfig.WaktuTumbuhBawaan = 1
GameConfig.TasSlotMaks = 50
GameConfig.IsiPerSlotMaks = 250
GameConfig.RadiusInteraksi = 16
GameConfig.RadiusPetak = 12
GameConfig.BatasPermintaanPerDetik = 5

GameConfig.Kategori = {"Serealia", "Legum", "Sayuran", "Buah-buahan", "Tanaman Lainnya"}

GameConfig.Benih = {
	{Id = 1, Nama = "Gandum", Kategori = "Serealia", Warna = Color3.fromRGB(198, 168, 88)},
	{Id = 2, Nama = "Jelai", Kategori = "Serealia", Warna = Color3.fromRGB(176, 150, 80)},
	{Id = 3, Nama = "Oat", Kategori = "Serealia", Warna = Color3.fromRGB(210, 186, 120)},
	{Id = 4, Nama = "Rye", Kategori = "Serealia", Warna = Color3.fromRGB(146, 124, 88)},
	{Id = 5, Nama = "Sorgum", Kategori = "Serealia", Warna = Color3.fromRGB(168, 96, 60)},
	{Id = 6, Nama = "Jewawut", Kategori = "Serealia", Warna = Color3.fromRGB(204, 178, 98)},
	{Id = 7, Nama = "Buckwheat", Kategori = "Serealia", Warna = Color3.fromRGB(120, 96, 72)},
	{Id = 8, Nama = "Kacang polong", Kategori = "Legum", Warna = Color3.fromRGB(108, 180, 78)},
	{Id = 9, Nama = "Kacang lentil", Kategori = "Legum", Warna = Color3.fromRGB(198, 132, 64)},
	{Id = 10, Nama = "Kacang arab", Kategori = "Legum", Warna = Color3.fromRGB(214, 190, 140)},
	{Id = 11, Nama = "Kacang hitam", Kategori = "Legum", Warna = Color3.fromRGB(70, 62, 56)},
	{Id = 12, Nama = "Kacang merah", Kategori = "Legum", Warna = Color3.fromRGB(168, 64, 52)},
	{Id = 13, Nama = "Bit", Kategori = "Sayuran", Warna = Color3.fromRGB(164, 44, 96)},
	{Id = 14, Nama = "Asparagus", Kategori = "Sayuran", Warna = Color3.fromRGB(96, 150, 70)},
	{Id = 15, Nama = "Seledri", Kategori = "Sayuran", Warna = Color3.fromRGB(140, 190, 96)},
	{Id = 16, Nama = "Selada", Kategori = "Sayuran", Warna = Color3.fromRGB(116, 178, 84)},
	{Id = 17, Nama = "Brokoli", Kategori = "Sayuran", Warna = Color3.fromRGB(72, 124, 58)},
	{Id = 18, Nama = "Kembang kol", Kategori = "Sayuran", Warna = Color3.fromRGB(238, 232, 214)},
	{Id = 19, Nama = "Kubis", Kategori = "Sayuran", Warna = Color3.fromRGB(128, 168, 96)},
	{Id = 20, Nama = "Paprika", Kategori = "Sayuran", Warna = Color3.fromRGB(196, 44, 44)},
	{Id = 21, Nama = "Mentimun", Kategori = "Sayuran", Warna = Color3.fromRGB(78, 148, 72)},
	{Id = 22, Nama = "Apel", Kategori = "Buah-buahan", Warna = Color3.fromRGB(196, 52, 48)},
	{Id = 23, Nama = "Pir", Kategori = "Buah-buahan", Warna = Color3.fromRGB(188, 196, 96)},
	{Id = 24, Nama = "Anggur (buah saja)", Kategori = "Buah-buahan", Warna = Color3.fromRGB(124, 64, 152)},
	{Id = 25, Nama = "Plum", Kategori = "Buah-buahan", Warna = Color3.fromRGB(110, 54, 128)},
	{Id = 26, Nama = "Aprikot", Kategori = "Buah-buahan", Warna = Color3.fromRGB(232, 140, 72)},
	{Id = 27, Nama = "Persik", Kategori = "Buah-buahan", Warna = Color3.fromRGB(238, 150, 130)},
	{Id = 28, Nama = "Nektarin", Kategori = "Buah-buahan", Warna = Color3.fromRGB(212, 88, 56)},
	{Id = 29, Nama = "Ceri", Kategori = "Buah-buahan", Warna = Color3.fromRGB(140, 28, 36)},
	{Id = 30, Nama = "Zaitun", Kategori = "Tanaman Lainnya", Warna = Color3.fromRGB(118, 132, 66)},
}

GameConfig.BenihPerId = {}
for _, benih in ipairs(GameConfig.Benih) do
	benih.Harga = GameConfig.HargaBawaan
	benih.WaktuTumbuh = GameConfig.WaktuTumbuhBawaan
	GameConfig.BenihPerId[benih.Id] = benih
end

function GameConfig.SlotTasTerpakai(tas)
	local isi = 0
	for _ in pairs(tas) do
		isi += 1
	end
	return isi
end

return GameConfig
