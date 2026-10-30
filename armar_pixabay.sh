#!/bin/bash
# Fondos verticales (10 s) para los reels estilo creador (plantillas/creador.html), con clips de PERSONAS REALES de Pixabay
# (Pixabay Content License: uso comercial, editable, sin atribución). Cada reel usa clips propios: no se repiten entre reels.
# Los clips se bajan con la API de Pixabay (hace falta PIXABAY_API_KEY en el entorno; la clave NUNCA va al repo).
# Registro de clips usados: videos-usados.md. Los cortes tienen que coincidir con los tiempos de GUIONES en creador.html.
set -e
cd "$(dirname "$0")"
C=videos/clips/pixabay
mkdir -p $C
bajar() {
  [ -f "$C/$1.mp4" ] && return
  : "${PIXABAY_API_KEY:?Falta PIXABAY_API_KEY para bajar el clip $1}"
  url=$(curl -sS -A "Mozilla/5.0" "https://pixabay.com/api/videos/?key=$PIXABAY_API_KEY&id=$1" | python3 -c "import json,sys; v=json.load(sys.stdin)['hits'][0]['videos']; print((v['large'] if v['large']['url'] else v['medium'])['url'])")
  curl -sSfL -A "Mozilla/5.0" -o "$C/$1.mp4" "$url"
}
# montar salida "id:desde:duración:encuadre" ...  (encuadre: dónde cae el recorte vertical, 0 izquierda … 1 derecha)
montar() {
  local out=$1; shift
  local args=() fil="" cat="" n=0
  for t in "$@"; do
    IFS=: read -r id ss dur f <<< "$t"
    bajar "$id"
    args+=(-ss "$ss" -t "$dur" -i "$C/$id.mp4")
    fil+="[$n:v]scale=-2:1920:flags=lanczos,crop=1080:1920:'(iw-1080)*$f':0,setsar=1,fps=30[v$n];"
    cat+="[v$n]"; n=$((n+1))
  done
  ffmpeg -v error -y "${args[@]}" -filter_complex "${fil}${cat}concat=n=$n:v=1:a=0[v]" -map "[v]" -c:v libx264 -crf 16 -pix_fmt yuv420p -an "$C/$out"
}
# «¿No sabés qué celu comprarte?» — cortes 0 · 2,4 · 3,8 · 5,0 · 6,2 · 8,0 · 10
montar cual_vertical.mp4 284347:6:2.4:0.5 8255:4.5:1.4:0.85 138875:2:1.2:0.65 129426:3:1.2:0.5 212637:2:1.8:0.28 45119:7:2.0:0.5
# «¿No encontrás el celu que querés?» — cortes 0 · 2,4 · 4,0 · 5,6 · 7,2 · 8,8 · 10
montar conseguimos_vertical.mp4 122389:0.3:2.4:0.5 203251:4:1.6:0.57 209854:4:1.6:0.82 174009:4:1.6:0.65 130720:3:1.6:0.21 174009:9:1.2:0.65
# «¿Ya sabés qué regalar esta Navidad?» — cortes 0 · 2,4 · 4,4 · 6,0 · 7,6 · 10
montar navidad-px_vertical.mp4 186535:1:2.4:0.28 50017:6.0:2.0:0.21 172681:6:1.6:0.65 50017:9.5:1.6:0.57 186535:8:2.4:0.28
echo "listo"
