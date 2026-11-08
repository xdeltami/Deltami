local IkonTrade = {}

-- Ikon kunci inggris (wrench) untuk tombol trade. Digambar dari Frame murni
-- supaya tidak bergantung aset eksternal dan aman di semua perangkat.
-- warnaLubang: warna yang sama dengan latar tombol agar lubang kepala terlihat.
function IkonTrade.buat(parent: Instance?, ukuran: number?, warnaLubang: Color3?): Frame
        local px = tonumber(ukuran) or 20
        if px ~= px or px < 10 then
                px = 20
        end
        px = math.floor(px)
        local emas = Color3.fromRGB(255, 199, 71)
        local gelap = Color3.fromRGB(148, 94, 16)
        local lubang = warnaLubang or Color3.fromRGB(23, 25, 30)

        local wadah = Instance.new("Frame")
        wadah.Name = "IkonTrade"
        wadah.Size = UDim2.fromOffset(px, px)
        wadah.BackgroundTransparency = 1

        -- kepala kunci inggris (cincin dengan celah)
        local kepala = Instance.new("Frame")
        kepala.Name = "Kepala"
        kepala.AnchorPoint = Vector2.new(0.5, 0.5)
        kepala.Position = UDim2.fromScale(0.34, 0.34)
        kepala.Size = UDim2.fromScale(0.5, 0.5)
        kepala.Rotation = 45
        kepala.BackgroundColor3 = emas
        kepala.BorderSizePixel = 0
        kepala.Parent = wadah
        local sudutKepala = Instance.new("UICorner")
        sudutKepala.CornerRadius = UDim.new(0.5, 0)
        sudutKepala.Parent = kepala
        local tepi = Instance.new("UIStroke")
        tepi.Color = gelap
        tepi.Thickness = math.max(1, math.floor(px / 14))
        tepi.Transparency = 0.15
        tepi.Parent = kepala

        -- celah cincin (dipotong dengan blok kecil warna latar)
        local celah = Instance.new("Frame")
        celah.Name = "Celah"
        celah.AnchorPoint = Vector2.new(0.5, 0.5)
        celah.Position = UDim2.fromScale(0.5, 0.18)
        celah.Size = UDim2.fromScale(0.44, 0.34)
        celah.Rotation = 45
        celah.BackgroundColor3 = lubang
        celah.BorderSizePixel = 0
        celah.ZIndex = 2
        celah.Parent = kepala
        local sudutCelah = Instance.new("UICorner")
        sudutCelah.CornerRadius = UDim.new(0.3, 0)
        sudutCelah.Parent = celah

        -- tangkai diagonal
        local tangkai = Instance.new("Frame")
        tangkai.Name = "Tangkai"
        tangkai.AnchorPoint = Vector2.new(0.5, 0.5)
        tangkai.Position = UDim2.fromScale(0.64, 0.64)
        tangkai.Size = UDim2.fromScale(0.2, 0.66)
        tangkai.Rotation = 45
        tangkai.BackgroundColor3 = emas
        tangkai.BorderSizePixel = 0
        tangkai.Parent = wadah
        local sudutTangkai = Instance.new("UICorner")
        sudutTangkai.CornerRadius = UDim.new(0.5, 0)
        sudutTangkai.Parent = tangkai
        local tepiTangkai = Instance.new("UIStroke")
        tepiTangkai.Color = gelap
        tepiTangkai.Thickness = math.max(1, math.floor(px / 16))
        tepiTangkai.Transparency = 0.2
        tepiTangkai.Parent = tangkai

        wadah.Parent = parent
        return wadah
end

return IkonTrade
