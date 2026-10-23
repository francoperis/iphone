#!/bin/bash
# Arma videos/clips/unboxing_vertical.mp4 (fondo de la historia "Nuevo · caja sellada", plantillas/sellado.html):
# dos clips gratuitos de Coverr (no premium, licencia de Coverr: uso comercial sin atribución), recortados a 9:16.
#   1) "Close-Up of Apple iPhone Packaging Label"  https://coverr.co/videos/close-up-of-apple-iphone-packaging-label
#   2) "Close-Up Unboxing of iPhone 15"            https://coverr.co/videos/close-up-unboxing-of-iphone-15-a-detailed-look-at-apples-product
# Ojo: el equipo del video es un iPhone 15 negro; el flyer después muestra el modelo real en 3D.
set -e
cd "$(dirname "$0")"
mkdir -p videos/clips
for s in coverr-close-up-of-iphone-packaging coverr-close-up-of-unboxing-iphone-15; do
  [ -f "videos/clips/$s.mp4" ] || curl -sfL -A "Mozilla/5.0" -o "videos/clips/$s.mp4" "https://cdn.coverr.co/videos/$s/1080p.mp4"
done
# etiqueta "iPhone" de la caja (1,6 s) + la mano que abre la caja (4,2 s); se estira el último cuadro para que dure 11 s
ffmpeg -v error -y -ss 0.4 -t 1.6 -i videos/clips/coverr-close-up-of-iphone-packaging.mp4 \
  -ss 0.6 -t 4.2 -i videos/clips/coverr-close-up-of-unboxing-iphone-15.mp4 \
  -filter_complex "[0:v]scale=-2:1920,crop=1080:1920:'iw*0.56-540':0,setsar=1,fps=30[a];[1:v]scale=-2:1920,crop=1080:1920:'iw*0.5-540':0,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0,eq=brightness=0.03:contrast=1.06:saturation=0.95,tpad=stop_mode=clone:stop_duration=6[v]" \
  -map "[v]" -c:v libx264 -crf 17 -pix_fmt yuv420p -an videos/clips/unboxing_vertical.mp4
echo "videos/clips/unboxing_vertical.mp4 listo"
