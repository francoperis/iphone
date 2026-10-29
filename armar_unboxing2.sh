#!/bin/bash
# Fondos verticales (10 s) para los reels de unboxing: clips gratuitos de Coverr (no premium, uso comercial sin atribución).
#   unboxing2_vertical.mp4: etiqueta de la caja · mano que abre la caja · chico abriendo un iPhone 15 · iPhone 15 en mano
#   navidad_vertical.mp4:   chicos abriendo regalos · mellizos con regalos · mano que abre la caja · chico abriendo un iPhone 15
# El primer corte grande cae en 4,4 s (fin del hook del reel, entrada del beat).
set -e
cd "$(dirname "$0")"
C=videos/clips
for s in coverr-close-up-of-iphone-packaging coverr-close-up-of-unboxing-iphone-15 coverr-a-man-unboxes-iphone-15 coverr-close-up-of-iphone-15 \
         coverr-opening-christmas-gifts-3271 coverr-twins-opening-christmas-presents-4462; do
  [ -f "$C/$s.mp4" ] || curl -sfL -A "Mozilla/5.0" -o "$C/$s.mp4" "https://cdn.coverr.co/videos/$s/1080p.mp4"
done
v() { echo "[$1:v]scale=-2:1920,crop=1080:1920:'(iw-1080)*$2':0,setsar=1,fps=30[$3]"; }
ffmpeg -v error -y -ss 0.4 -t 1.4 -i $C/coverr-close-up-of-iphone-packaging.mp4 -ss 0.6 -t 3.0 -i $C/coverr-close-up-of-unboxing-iphone-15.mp4 \
  -ss 1.0 -t 2.8 -i $C/coverr-a-man-unboxes-iphone-15.mp4 -ss 2.0 -t 2.8 -i $C/coverr-close-up-of-iphone-15.mp4 \
  -filter_complex "$(v 0 0.56 a);$(v 1 0.5 b);$(v 2 0.72 c);$(v 3 0.42 d);[a][b][c][d]concat=n=4:v=1:a=0[v]" \
  -map "[v]" -c:v libx264 -crf 17 -pix_fmt yuv420p -an $C/unboxing2_vertical.mp4
ffmpeg -v error -y -ss 3.0 -t 2.2 -i $C/coverr-opening-christmas-gifts-3271.mp4 -ss 4.5 -t 2.2 -i $C/coverr-twins-opening-christmas-presents-4462.mp4 \
  -ss 0.6 -t 3.0 -i $C/coverr-close-up-of-unboxing-iphone-15.mp4 -ss 1.0 -t 2.6 -i $C/coverr-a-man-unboxes-iphone-15.mp4 \
  -filter_complex "$(v 0 0.4 a);$(v 1 0.38 b);$(v 2 0.5 c);$(v 3 0.72 d);[a][b][c][d]concat=n=4:v=1:a=0[v]" \
  -map "[v]" -c:v libx264 -crf 17 -pix_fmt yuv420p -an $C/navidad_vertical.mp4
echo "listo"
