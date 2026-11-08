#!/bin/bash
# Publish 5 place Akiomida ke Roblox (Open Cloud).
# Prasyarat: /home/z/my-project/.secrets/akiomida.env berisi ROBLOX_SECURITY
# (kunci BARU, baseApiKey+JWT, 736 karakter), UNIVERSE_ID, PLACE_*.
# Kunci dari pemilik dunia hanya berlaku 1 JAM sejak dibuat — jalankan segera
# setelah kunci baru diunggah. File .rbxl ada di download/Dataran-Roblox/.
set -a
source /home/z/my-project/.secrets/akiomida.env
set +a
DIR=/home/z/my-project/download/Dataran-Roblox
for pasangan in "Dataran PLACE_DATARAN" "Kampung PLACE_KAMPUNG" "Sabana PLACE_SABANA" "Stepa PLACE_STEP" "Perladangan PLACE_PERLADANGAN"; do
  set -- $pasangan
  NAMA=$1; KUNCI=$2; P="${!KUNCI}"
  printf "%-12s -> " "$NAMA"
  curl -s --max-time 240 -X POST \
    "https://apis.roblox.com/universes/v1/$UNIVERSE_ID/places/$P/versions?versionType=Published" \
    -H "x-api-key: $ROBLOX_SECURITY" \
    -H "Content-Type: application/octet-stream" \
    --data-binary "$DIR/$NAMA.rbxl" | head -c 160
  echo
  sleep 2
done
echo "--- verifikasi ---"
curl -s --max-time 30 "https://games.roblox.com/v1/games?universeIds=$UNIVERSE_ID" | head -c 400
echo
