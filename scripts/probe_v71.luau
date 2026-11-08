-- probe v71: identifikasi model fasilitas yang terdeteksi terkubur (logika naif + prefix)
local Workspace = Stub.Services.Workspace
Stub.Scheduler.advance(0.05)
script = Stub.serverScript()
RUN_init_server()
Stub.Scheduler.advance(0.2)

local dataran = Workspace:FindFirstChild("Dataran")
local FASILITAS = { "Ayunan", "Perosotan", "JungkatJungkit", "KotakPasir", "Gazebo", "KolamBebek", "Bebek", "Panggung", "RumahKaca", "Pergola", "LampuSorot", "LapanganBuluTangkis", "LapanganBasket", "BenderaMerahPutih" }
local total, sink = 0, 0
for _, nama in ipairs(FASILITAS) do
	for _, b in ipairs(dataran:GetDescendants()) do
		if b:IsA("Model") and string.sub(b.Name, 1, #nama) == nama then
			total += 1
			for _, d in ipairs(b:GetDescendants()) do
				if d:IsA("BasePart") then
					local mn = d.CFrame.Position.Y - d.Size.Y / 2
					if mn < -0.06 then
						sink += 1
						print(string.format("[SINK] prefix=%s model=%s part=%s min=%.2f pos=(%.1f,%.1f,%.1f) sz=(%.1f,%.1f,%.1f)", nama, b.Name, d.Name, mn, d.Position.X, d.Position.Y, d.Position.Z, d.Size.X, d.Size.Y, d.Size.Z))
					end
				end
			end
		end
	end
end
print("PROBE SELESAI total=" .. total .. " sink=" .. sink)
