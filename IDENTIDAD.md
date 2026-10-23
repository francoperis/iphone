# Tech&Co. — Manual de identidad

Este documento fija la identidad de la marca. **Toda pieza nueva (flyer, post, historia, reel, catálogo) sale de acá.**
Los valores viven en código en `plantillas/identidad.css` (colores, tipografías, escala, márgenes); el logotipo en
`plantillas/logo.css` y los componentes en `plantillas/piezas.css` + `piezas.js`. Si hace falta un valor nuevo,
se agrega en `identidad.css` **y** en este archivo, nunca a mano en una plantilla.

Aprobado: 2026-10-23 (logo Ruta B, nombre Tech&Co., títulos en Archivo condensada).

---

## 1. Marca

- **Nombre:** Tech&Co. (se escribe así en textos: T mayúscula, «&», punto final).
- **Qué es:** venta de equipos **Swap** (reacondicionados) y **en caja sellada**. Hoy iPhone; después Samsung y Xiaomi,
  y más adelante otras cosas tech. Por eso la cuenta se presenta con «equipos», nunca como «solo iPhone».
  iPhone se nombra cuando la pieza muestra un iPhone.
- **Tono:** español rioplatense (vos, «escribinos», «tuyo»). Directo, corto, seguro. Nada de exageraciones.

## 2. Logotipo

| | |
|---|---|
| Forma | **TECH&CO.** en una línea: Archivo 900, ancho 62 %, mayúsculas, espaciado −0,02 em |
| «&» | lima `#CCFF00` |
| Punto | un cuadrado lima de 0,184 em de lado (no es un punto tipográfico) |
| Avatar | apilado «TECH / &CO.» dentro de un círculo hueso o lima, todo en tinta (un solo color) |
| Sobre fondos claros (lima, hueso) | todo en tinta, sin lima (clase `plano`) |
| Sobre tinta o voltio | letras hueso, «&» y punto lima |
| Tamaño en piezas | 54 px de alto de letra (`--logo`), arriba a la derecha |
| Tamaño mínimo | 40 px de avatar (círculo); 24 px de alto de letra en línea |

Código: `<span class="logo-tc">Tech<b>&amp;</b>Co<i></i></span>` · apilado: `class="logo-tc apilado"` · un color: `plano`.
Archivos listos: `publicar/00-marca/` (avatar lima, hueso, negro; logotipo; hoja de marca).

**No:** cambiarle la letra, deformarlo, ponerle sombra o contorno, usar el «&» en otro color que no sea lima o tinta,
reemplazar el punto cuadrado por un punto redondo, usar el monograma «C&» (descartado).

## 3. Colores

| Token | Hex | Rol |
|---|---|---|
| `--tinta` | `#0A0A0B` | fondo oscuro; texto sobre fondos claros |
| `--hueso` | `#EEEBE4` | fondo claro; texto sobre tinta y voltio |
| `--lima` | `#CCFF00` | acento principal: «&» del logo, resaltados, «Saber más», sellos, fondo de portadas |
| `--voltio` | `#8B6CFF` | acento secundario: fondo del plan canje, resaltado detrás de una palabra, disco detrás del equipo |
| `--acero` | `#8E8E96` | textos secundarios sobre tinta (rótulos, aclaraciones) |

Fondos permitidos y su texto:

| Fondo | Texto | Acento |
|---|---|---|
| tinta | hueso | lima (y voltio para discos) |
| lima | tinta | voltio (resaltado) |
| hueso | tinta | voltio (resaltado) |
| voltio | tinta | lima (disco, resaltado del equipo nuevo) |

Proporción aproximada por pieza: 60 % fondo · 30 % texto/equipo · 10 % acento. Un solo acento fuerte por pieza.
**No:** degradados de color, dorado, naranja de «urgencia», ni colores fuera de esta tabla
(los colores de los equipos son los reales de cada modelo).

## 4. Tipografía

Dos familias, las dos de Google Fonts:

| Uso | Familia | Peso | Ancho | Caja |
|---|---|---|---|---|
| Títulos, valores, precios, «Saber más» | **Archivo** | 900 | 62 % (condensada) | MAYÚSCULAS |
| Todo lo demás (bajadas, etiquetas, pies, datos) | **JetBrains Mono** | 700 (500 en párrafos largos) | normal | MAYÚSCULAS en etiquetas y pies |

Link: `https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,800..900&family=JetBrains+Mono:wght@500;700&display=block`

### Escala (px sobre un lienzo de 1080 de ancho)

| Token | Tamaño | Uso | Ejemplo |
|---|---|---|---|
| `--t-cuenta` | 560 | solo la cuenta regresiva | 3 · 2 · 1 |
| `--t-xxl` | 380 | cifras y una palabra corta gigante | 99 %, X→18, «17 PRO» |
| `--t-xl` | 250 | portada de una palabra; ocupa casi todo el ancho | ABRIMOS., NUEVO. |
| `--t-l` | 170 | título principal de 2–3 renglones | LO MEJOR, / A TU / ALCANCE. |
| `--t-m` | 120 | título largo, hook de reel, frase de una línea | DEL X AL 18 PRO MAX. |
| `--t-s` | 88 | subtítulo, nombre del modelo, «Saber más» | IPHONE 17 PRO |
| `--t-xs` | 56 | valor de una etiqueta, pasos | SWAP · 256 GB |
| `--m-l` | 28 | bajada debajo de un título | ENTREGALO COMO PARTE DE PAGO |
| `--m-m` | 24 | etiquetas, pie de post, encabezado | LINK EN LA BIO → |
| `--m-s` | 20 | rótulos chicos, códigos | X · XS · 11 · … |

Referencia de ancho (Archivo 900, 62 %, mayúsculas): a 100 px, «ABRIMOS.» mide 367 px y «LO MEJOR,» 387 px.
Ancho útil: 936 px (1080 − 2 × 72). Una línea entra si `ancho a 100 px × tamaño / 100 ≤ 936`.

### Interlineado y espaciado

| | Interlineado | Espaciado entre letras |
|---|---|---|
| Títulos (Archivo) | 0,92 (deja lugar a las tildes: QUÉ, BUSCÁS) | −0,01 em |
| Textos (JetBrains Mono) | 1,4 | +0,12 em |
| Logotipo | 0,8 | −0,02 em |

Reglas: los títulos no se cortan con guion («ABRI-MOS» no); una palabra por renglón si hace falta, nunca partida.
Los renglones se cortan a mano con `<br>`. Mayúsculas con tilde siempre (TODAVÍA, MÁS).

## 5. Formatos, márgenes y zonas

| | Post | Historia / reel |
|---|---|---|
| Tamaño | 1080 × 1350 | 1080 × 1920 |
| Margen lateral | 72 px (`--margen`) | 72 px |
| Logo | arriba a la derecha, a 64 px del borde superior | a 250 px (zona segura) |
| Título | empieza a 130–150 px | empieza a 320–330 px |
| Pie | a 60 px del borde inferior, una línea mono | — |
| Zona segura | — | nada importante arriba de 250 px ni debajo de 1700 px |
| Cierre | pie «Catálogo online · Link en la bio →» | «Saber más» + flecha hacia la casilla de respuesta (abajo a la izquierda, a 190 px del borde) |

## 6. Componentes

- **Equipo en 3D** (`telefono3d.js`): siempre con grosor, nunca foto plana. Se ubica por su **centro** y lejos de los
  márgenes; flota (sube y baja 6 px, gira ±5°). Sombra suave debajo. Colores reales del modelo.
- **Disco** detrás del equipo: círculo voltio (sobre tinta) o lima (sobre voltio), diámetro ≈ 0,8 × alto del equipo.
- **Etiquetas del equipo:** valor en Archivo `--t-xs` + rótulo en mono `--m-m` al 75 %. **Sin líneas ni flechas
  saliendo del teléfono.** Van al costado o debajo, alineadas al margen.
- **Resaltado:** fondo voltio (o lima) detrás de una palabra del título; uno por pieza.
- **Sello:** círculo lima de 250 px con texto girando «CAJA SELLADA ·» y una palabra al centro en Archivo («NUEVO»).
  Nunca «0 KM».
- **Saber más:** flecha mono hacia abajo (76 × 170) + «SABER MÁS» en lima `--t-s` + «ESCRIBINOS ACÁ ABAJO» en `--m-m`.
- **Pie de post:** una línea en JetBrains Mono `--m-m`, izquierda y derecha. Sin caja ni franja de color.

## 7. Movimiento

- Entradas escalonadas: cada elemento entra 50 px desde abajo con opacidad, en 450 ms, curva `cubic-bezier(.2,.8,.2,1)`;
  separación de 150–250 ms entre elementos.
- Rebotes (discos, sellos): `cubic-bezier(.34,1.56,.64,1)`, 500–600 ms.
- Cortinas y cortes: `cubic-bezier(.7,0,.2,1)`, 500–600 ms.
- El equipo entra girando (≈ 1 vuelta) y queda flotando.
- Duración: historias 6–11 s, reels 8–12 s; 30 fps; exportación cuadro a cuadro (`exportar_video.js`).

## 8. Textos

- Los equipos son **Swap** o **en caja sellada**. Nunca «usado».
- Se habla de **equipos**; «iPhone» solo cuando se muestra un iPhone.
- No usar: «ficha» / «con ficha» (se dice «batería, capacidad y estado a la vista»), «estrenar», «segunda opción»,
  «0 km», «Respondé QUIERO».
- Ganchos aprobados: «Lo mejor, a tu alcance.», «Todo a la vista.», «Tu equipo vale.», «Abrimos.», «Nuevo.».
- Datos que no tenemos van como marcadores: [ZONA], [__]%, envíos [__]. Nunca inventar stock, precios, reseñas ni ventas.
- Precios: miles grandes y «.000» chico ($ + 1.900 + .000). Caja sellada: «Precio: consultar». Nunca la cotización del dólar.
- Hashtags base: #tecnologia #celulares #swap #cajasellada #argentina (+ #iphone #iphoneswap si se muestra un iPhone).

## 9. Prohibido

Cajas o recuadros con texto, chips con borde, franjas o tarjetas de color al pie, encabezados de sección («// 001 · …»),
líneas o flechas desde los teléfonos, fotos planas, marcas de agua, videos subidos por terceros a redes,
colores que el modelo no tiene, degradados, dorado, el monograma «C&», y la tipografía Unbounded (reemplazada por Archivo).

## 10. Fotos y video

- Fotos de equipos: tienda y Newsroom de Apple (licencia editorial; riesgo asumido por el dueño, 2026-10-21).
- Video: solo clips con licencia libre para uso comercial (Mixkit «Stock Video Free License», Coverr no premium),
  verificando que el teléfono sea el que se nombra. Unboxing: Coverr «close-up of unboxing iPhone 15» y
  «close-up of iPhone packaging» (`videos/clips/unboxing_vertical.mp4`).
