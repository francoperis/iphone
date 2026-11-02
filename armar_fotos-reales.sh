#!/bin/bash
# Piezas con las fotos reales del proveedor en HD (plantillas/foto.html) → publicar/equipos/fotos-reales/
#   carrusel/  4 láminas 1080×1350 (17 Pro): mejor precio · de cerca · naranja · ¿cuál es el tuyo?
#   historias/ encuesta de color + «Te lo conseguimos» por modelo (17 Pro, 14 Pro, 13 Pro, Galaxy A17), 1080×1920
set -e
cd "$(dirname "$0")"
export NODE_PATH=$(npm root -g)
D=publicar/equipos/fotos-reales
mkdir -p $D/carrusel $D/historias
u() { python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1"; }
pieza() { node exportar_video.js plantillas/foto.html "$1" "$2" --cuadro 0 >/dev/null 2>&1 && echo "$2"; }
# carrusel
pieza "p=colores&formato=post&titulo=$(u 'Los mejores Swap<br><b>al mejor precio.</b>')&pie=$(u 'Deslizá →')" $D/carrusel/1_portada.png
pieza "p=naranja&formato=post&ojo=$(u 'iPhone 17 Pro · Naranja cósmico')&titulo=$(u 'Mirá<br><b>de cerca.</b>')&datos=&limpio=1&fundido=1" $D/carrusel/2_de-cerca.png
pieza "p=cajas&formato=post&ojo=$(u 'iPhone 17 Pro')&titulo=$(u 'Tres colores.<br><b>Uno es tuyo.</b>')" $D/carrusel/3_colores.png
pieza "p=colores&formato=post&ojo=$(u 'Comentá tu color ↓')&titulo=$(u '¿Cuál es<br><b>el tuyo?</b>')" $D/carrusel/4_cierre.png
# historias
pieza "p=cajas&formato=historia&titulo=$(u '¿Cuál<br><b>te llevás?</b>')" $D/historias/encuesta_color.png
pieza "p=colores&formato=historia&ojo=$(u 'Swap o en caja sellada')&titulo=$(u 'iPhone<br><b>17 Pro.</b>')&datos=$(u 'Te lo conseguimos')&limpio=1" $D/historias/conseguimos_17pro.png
pieza "p=14pro&formato=historia&ojo=$(u 'Swap · revisado uno por uno')&titulo=$(u 'iPhone<br><b>14 Pro.</b>')&datos=$(u 'Te lo conseguimos')&limpio=1" $D/historias/conseguimos_14pro.png
pieza "p=13pro&formato=historia&ojo=$(u 'Swap · revisado uno por uno')&titulo=$(u 'iPhone<br><b>13 Pro.</b>')&datos=$(u 'Te lo conseguimos')&limpio=1" $D/historias/conseguimos_13pro.png
pieza "p=a17&formato=historia&ojo=$(u 'Samsung · Nuevo, caja sellada')&titulo=$(u 'Galaxy<br><b>A17.</b>')&datos=$(u 'Te lo conseguimos')&limpio=1" $D/historias/conseguimos_a17.png
