#!/bin/bash
# Fondo vertical (10 s) del reel «iPhone 17 Pro, ¿cuál te llevás?» con las fotos del proveedor ya limpias
# (limpiar_proveedor.py → fotos-proveedor/), con un zoom lento en cada una.
set -e
cd "$(dirname "$0")"
F=fotos-proveedor
seg() {  # foto duración zoom_final x_centro(0..1)
  local n=$(python3 -c "print(round($2*30))")
  echo "scale=-2:2112,crop=1188:2112:'(iw-1188)*$4':0,zoompan=z='1+($3-1)*on/$n':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$n:s=1080x1920:fps=30,setsar=1"
}
ffmpeg -v error -y -i $F/iphone-17-pro_tres-colores_mano.jpg -i $F/iphone-17-pro_naranja_camara.jpg \
  -i $F/iphone-17-pro_naranja_mano.jpg -i $F/iphone-17-pro_tres-colores_cajas.jpg \
  -filter_complex "[0:v]$(seg 0 4.4 1.10 0.55)[a];[1:v]$(seg 1 1.6 1.06 0.5)[b];[2:v]$(seg 2 1.5 1.06 0.5)[c];[3:v]$(seg 3 2.5 1.05 0.5)[d];[a][b][c][d]concat=n=4:v=1:a=0[v]" \
  -map "[v]" -c:v libx264 -crf 17 -pix_fmt yuv420p -t 10 videos/clips/17pro_vertical.mp4
echo "videos/clips/17pro_vertical.mp4 listo"
