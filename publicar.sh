#!/bin/bash
# Exporta todas las piezas listas para subir a publicar/, ordenadas por sección y por marca de equipo.
# Uso: ./publicar.sh            (todo)
#      ./publicar.sh imagenes   (solo los PNG, rápido)
# Requiere: npm install (playwright), ffmpeg y los clips de videos/clips para los reels.
set -u
cd "$(dirname "$0")"
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
SOLO="${1:-todo}"
P=publicar
e() { echo "· $3"; node exportar_video.js "$@" 2>&1 | grep -v "404\|Consola" | tail -1; }
png() { e "$1" "$2" "$3" --cuadro "$4"; }
mp4() { [ "$SOLO" = imagenes ] || e "$@"; }

mkdir -p $P/00-marca $P/01-teasers $P/02-apertura $P/03-que-vendemos $P/04-como-comprar $P/05-plan-canje $P/06-tips \
         $P/equipos/iphone/linea-completa $P/equipos/iphone/nuevos-caja-sellada $P/equipos/iphone/ingresos $P/equipos/iphone/reels \
         $P/equipos/samsung $P/equipos/xiaomi

# 00 · marca (foto de perfil y logo)
png plantillas/marca.html "pieza=avatar&formato=cuadrado" $P/00-marca/avatar-lima.png 0
png plantillas/marca.html "pieza=avatar-hueso&formato=cuadrado" $P/00-marca/avatar-hueso.png 0
png plantillas/marca.html "pieza=avatar-tinta&formato=cuadrado" $P/00-marca/avatar-negro.png 0
png plantillas/marca.html "pieza=logotipo&formato=cuadrado" $P/00-marca/logotipo.png 0
png plantillas/marca.html "pieza=hoja&formato=cuadrado" $P/00-marca/hoja-de-marca.png 0
mkdir -p $P/00-marca/destacadas
for t in Nosotros Swap Sellados Canje Comprar; do
  png plantillas/marca.html "pieza=destacada&texto=$t" $P/00-marca/destacadas/$(echo $t | tr "A-Z" "a-z").png 0
done

# 01 · teasers (antes de abrir: no dicen qué vendemos). Idea elegida: Carga 99 % (Pantalla quedó descartada)
png plantillas/misterio.html "pieza=ficha&formato=post" $P/01-teasers/expediente_post.png 7999
png plantillas/misterio.html "pieza=carga&formato=post" $P/01-teasers/carga_post.png 6250
mp4 plantillas/misterio.html "pieza=ficha" $P/01-teasers/expediente_reel.mp4
mp4 plantillas/misterio.html "pieza=carga" $P/01-teasers/carga_reel.mp4
mp4 plantillas/lanzamiento.html "" $P/01-teasers/en-camino_reel.mp4

# 02 · apertura (el día que abrimos)
png plantillas/apertura.html "pieza=post1" $P/02-apertura/abrimos_post.png 2900
png plantillas/misterio.html "pieza=vuelve-carga&formato=post" $P/02-apertura/revelacion_post.png 8999
png plantillas/presentacion.html "formato=post" $P/02-apertura/presentacion_post.png 0
mp4 plantillas/apertura.html "pieza=story1" $P/02-apertura/abrimos_historia.mp4
mp4 plantillas/apertura.html "pieza=story6" $P/02-apertura/hay-uno-para-vos_historia.mp4
mp4 plantillas/misterio.html "pieza=vuelve-carga" $P/02-apertura/revelacion_reel.mp4

# 03 · qué vendemos (Swap y caja sellada)
png plantillas/apertura.html "pieza=post2" $P/03-que-vendemos/lo-mejor-a-tu-alcance_post.png 2900
png plantillas/apertura.html "pieza=post4" $P/03-que-vendemos/todo-a-la-vista_post.png 2900
mp4 plantillas/apertura.html "pieza=story2" $P/03-que-vendemos/lo-mejor-a-tu-alcance_historia.mp4
mp4 plantillas/apertura.html "pieza=story3" $P/03-que-vendemos/que-buscas_historia-encuesta.mp4

# 04 · cómo comprar
png plantillas/apertura.html "pieza=post6" $P/04-como-comprar/3-pasos_post.png 2900

# 05 · plan canje
png plantillas/canje.html "de=iphone-13&a=iphone-17-pro&formato=post" $P/05-plan-canje/iphone-13-a-17-pro_post.png 8999
png plantillas/canje.html "de=iphone-12&a=iphone-16-pro&formato=post" $P/05-plan-canje/iphone-12-a-16-pro_post.png 8999
mp4 plantillas/canje.html "de=iphone-13&a=iphone-17-pro" $P/05-plan-canje/iphone-13-a-17-pro_historia.mp4
mp4 plantillas/canje.html "de=iphone-12&a=iphone-16-pro" $P/05-plan-canje/iphone-12-a-16-pro_historia.mp4
mp4 plantillas/reel.html "reel=canje&exportar=1" $P/05-plan-canje/cuanto-vale-tu-equipo_reel.mp4 --fondo videos/clips/mixkit_100046_2160.mp4 --desde 0 --encuadre 0.2

# 06 · tips
mp4 plantillas/reel.html "reel=chequea-esto&exportar=1" $P/06-tips/chequea-esto_reel.mp4 --fondo videos/clips/mixkit_100050_2160.mp4 --desde 0 --encuadre 0.22

# equipos · iPhone
[ -f videos/clips/unboxing_vertical.mp4 ] || ./armar_unboxing.sh
I=$P/equipos/iphone
png plantillas/apertura.html "pieza=post3" $I/linea-completa/x-a-18_post.png 2900
mp4 plantillas/apertura.html "pieza=story4" $I/linea-completa/x-a-18_historia.mp4
for par in "iphone-17-pro silver 256" "iphone-16-pro deserttitanium 128"; do
  set -- $par
  png plantillas/sellado.html "modelo=$1&color=$2&gb=$3&formato=post" $I/nuevos-caja-sellada/$1_post.png 5999
  mp4 plantillas/sellado.html "modelo=$1&color=$2&gb=$3" $I/nuevos-caja-sellada/$1_historia.mp4 --fondo videos/clips/unboxing_vertical.mp4
done
for m in iphone-13 iphone-15-pro iphone-16-pro iphone-17-pro; do
  mp4 plantillas/llego.html "modelo=$m" $I/ingresos/llego_${m}_historia.mp4
done
mp4 plantillas/reel.html "reel=primera-foto&exportar=1" $I/reels/primera-foto_reel.mp4 --fondo videos/clips/coverr-close-up-of-a-man-taking-a-selfie-on-iphone-15.mp4 --desde 2.5 --encuadre 0.5

echo LISTO
