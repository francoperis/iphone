#!/bin/bash
# Fondos verticales (10 s) para los reels estilo creador (plantillas/creador.html), con clips de PERSONAS REALES de Pixabay
# (Pixabay Content License: uso comercial, editable, sin atribución). Cada reel usa clips propios: no se repiten entre reels.
# Los clips se bajan con la API de Pixabay (hace falta PIXABAY_API_KEY en el entorno; la clave NUNCA va al repo).
# Registro de clips usados: videos-usados.md
#   de-mas_vertical.mp4: 183448 (chico en el parque) · 130650 (chica en la cama) · 204527 (manos, iPhone 11 rojo) · 130647 (chica en el escritorio) · 183448
#   pov_vertical.mp4:    79336 (chica en el sillón) · 130652 (chica de saco) · 204529 (iPhone 11 rojo) · 174004 (selfie, camisa amarilla) · 204529
set -e
cd "$(dirname "$0")"
C=videos/clips/pixabay
mkdir -p $C
for id in 183448 130650 204527 130647 79336 130652 204529 174004; do
  [ -f "$C/$id.mp4" ] && continue
  : "${PIXABAY_API_KEY:?Falta PIXABAY_API_KEY para bajar el clip $id}"
  url=$(curl -sS -A "Mozilla/5.0" "https://pixabay.com/api/videos/?key=$PIXABAY_API_KEY&id=$id" | python3 -c "import json,sys; print(json.load(sys.stdin)['hits'][0]['videos']['large']['url'])")
  curl -sSfL -A "Mozilla/5.0" -o "$C/$id.mp4" "$url"
done
# clip 4K horizontal → vertical 1080×1920; $2 = dónde cae el recorte (0 izquierda … 1 derecha)
v() { echo "[$1:v]scale=-2:1920:flags=lanczos,crop=1080:1920:'(iw-1080)*$2':0,setsar=1,fps=30[$3]"; }
# cortes: 0 · 2,4 · 4,2 · 6,0 · 7,6 · 10
ffmpeg -v error -y -ss 1.0 -t 2.4 -i $C/183448.mp4 -ss 3.0 -t 1.8 -i $C/130650.mp4 -ss 1.0 -t 1.8 -i $C/204527.mp4 \
  -ss 6.0 -t 1.6 -i $C/130647.mp4 -ss 20.0 -t 2.4 -i $C/183448.mp4 \
  -filter_complex "$(v 0 0.52 a);$(v 1 0.8 b);$(v 2 0.55 c);$(v 3 0.6 d);$(v 4 0.66 e);[a][b][c][d][e]concat=n=5:v=1:a=0[v]" \
  -map "[v]" -c:v libx264 -crf 16 -pix_fmt yuv420p -an $C/de-mas_vertical.mp4
# cortes: 0 · 2,4 · 4,4 · 6,2 · 7,8 · 10
ffmpeg -v error -y -ss 1.0 -t 2.4 -i $C/79336.mp4 -ss 2.0 -t 2.0 -i $C/130652.mp4 -ss 1.0 -t 1.8 -i $C/204529.mp4 \
  -ss 6.0 -t 1.6 -i $C/174004.mp4 -ss 6.0 -t 2.2 -i $C/204529.mp4 \
  -filter_complex "$(v 0 0.43 a);$(v 1 0.28 b);$(v 2 0.43 c);$(v 3 0.44 d);$(v 4 0.43 e);[a][b][c][d][e]concat=n=5:v=1:a=0[v]" \
  -map "[v]" -c:v libx264 -crf 16 -pix_fmt yuv420p -an $C/pov_vertical.mp4
echo "listo"
