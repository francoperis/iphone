#!/bin/bash
# Arma videos/clips/foto_vertical.mp4 (fondo del reel «Tu próxima foto», plantillas/reels.js "foto"):
# dos clips gratuitos de Coverr (no premium, licencia de Coverr: uso comercial sin atribución), recortados a 9:16.
#   1) "Close-up of a woman taking a photo on the phone and laughing" (iPhone XR rojo)   4,4 s
#   2) "Girl using iPhone in bed" (iPhone 11 Pro, sonriendo)                              5,6 s
# El corte cae en 4,4 s, cuando termina el hook y entra el beat (musica.py --entrada 4.4).
set -e
cd "$(dirname "$0")"
mkdir -p videos/clips
for s in coverr-close-up-of-a-woman-taking-a-photo-on-the-phone-and-laughing-7325 coverr-girl-using-iphone-in-bed-2346; do
  [ -f "videos/clips/$s.mp4" ] || curl -sfL -A "Mozilla/5.0" -o "videos/clips/$s.mp4" "https://cdn.coverr.co/videos/$s/1080p.mp4"
done
ffmpeg -v error -y -ss 0.6 -t 4.4 -i videos/clips/coverr-close-up-of-a-woman-taking-a-photo-on-the-phone-and-laughing-7325.mp4 \
  -ss 6 -t 5.6 -i videos/clips/coverr-girl-using-iphone-in-bed-2346.mp4 \
  -filter_complex "[0:v]scale=-2:1920,crop=1080:1920:'(iw-1080)*0.40':0,setsar=1,fps=30[a];[1:v]scale=-2:1920,crop=1080:1920:'(iw-1080)*0.65':0,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[v]" \
  -map "[v]" -c:v libx264 -crf 17 -pix_fmt yuv420p -an videos/clips/foto_vertical.mp4
echo "videos/clips/foto_vertical.mp4 listo"
