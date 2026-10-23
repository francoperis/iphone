# Proyecto: tienda de iPhone — marca: Tech&Co.

Negocio familiar de venta de iPhone **Swap** y en caja sellada, en Argentina.
**Los equipos NO se llaman "usados": son "Swap"** (en piezas, catálogo, textos y hashtags: #iphoneswap).
Objetivo: contenido orgánico DE CALIDAD para Instagram (historias, reels, carruseles)
y una página de catálogo con botón de WhatsApp.

Idioma de todo el contenido: español rioplatense (vos, "escribinos", "tuyo").

## Decisiones tomadas (2026-10-21)
- Nombre de marca: **Celu&Co.** (reemplaza el nombre de trabajo "LOTE"). → Desde 2026-10-23 la marca es **Tech&Co.** (ver "Marca elegida").
- El repo arrancó vacío: el script de fotos y los prototipos se rehacen de cero según este brief.
- Fotos: no hay fotos propias. Armar una base de fotos en máxima calidad desde varias fuentes:
  Apple oficial (Newsroom + apple.com), Wikimedia Commons, Unsplash / Pexels y sitios de reviews.
  Registrar en `indice.csv` la fuente, URL, autor y licencia de cada foto.
  Licencias: Apple = uso editorial; Wikimedia = CC (citar autor); Unsplash/Pexels = uso comercial libre;
  sitios de reviews = copyright de terceros → marcar como "solo referencia", no usar en publicidad.
- Fotos de Apple en publicidad: el usuario fue avisado de que la licencia es editorial / no comercial
  y decidió usarlas igual, asumiendo el riesgo (2026-10-21).
- Estado de las fuentes (2026-10-21): tienda de Apple y Newsroom funcionan (mejor calidad).
  Wikimedia limita mucho las consultas desde este entorno (429). Openverse ahora pide registro (401).
  Unsplash/Pexels necesitan claves gratuitas (UNSPLASH_ACCESS_KEY / PEXELS_API_KEY).
  GSMArena bloquea descargas automáticas (Cloudflare).
- Precios: se definen más adelante (USD vs. pesos, cotización). Por ahora usar la tabla de abajo.
- Primer avance: plantilla animada "Llegó" exportada a MP4 1080×1920, en 4 variantes:
  iPhone 13, 15 Pro, 16 Pro y 17 Pro.

## Datos que faltan (pedírselos al usuario antes de publicar nada)
- Logo, @ de Instagram, número de WhatsApp.
- Zona de retiro / envíos, medios de pago, cuotas, meses de garantía.
- Reglas del plan canje.
- Stock real: modelo, GB, color, % batería, precio, estado. Nunca inventar estos datos:
  usar marcadores como [__]% o [ZONA] hasta tenerlos.

## Precios actuales (del flyer original, en pesos)
| Modelo | GB | Precio |
|---|---|---|
| iPhone 12 | 128 | $510.000 |
| iPhone 12 Pro | 128 | $600.000 |
| iPhone 12 Pro Max | 128 | $640.000 |
| iPhone 13 mini | 128 | $530.000 |
| iPhone 13 | 128 | $610.000 |
| iPhone 13 Pro | 128 | $750.000 |
| iPhone 13 Pro Max | 128 | $830.000 |
| iPhone 14 | 128 | $670.000 |
| iPhone 14 Pro | 128 | $850.000 |
| iPhone 14 Pro Max | 128 | $980.000 |
| iPhone 15 | 128 | $920.000 |
| iPhone 15 Pro | 128 | $1.120.000 |
| iPhone 15 Pro Max | 256 | $1.315.000 |
| iPhone 16 | 128 | $1.290.000 |
| iPhone 16 Pro | 128 | $1.435.000 |
| iPhone 16 Pro Max | 256 | $1.655.000 |
| iPhone 17 Pro | 256 | $1.900.000 |

Caja sellada: "consultar". NO mostrar nunca la cotización del dólar en las piezas.

## Identidad visual
- Fondo negro tinta #0C0C0D, texto #EDEAE3, acento verde ácido #D4FF3A,
  urgencia naranja #FF5B2E, gris secundario #9A9AA2.
- Tipografías (Google Fonts): Unbounded 800/900 para títulos y precios,
  JetBrains Mono para specs/etiquetas, Manrope para texto.
- Precios con miles grandes y ".000" chico: $1.120.000 → "$" + "1.120" + ".000".
- Estilo "drop" de streetwear: tipografía gigante calada, cintas de texto que corren,
  stickers que giran, sellos (VENDIDO / APROBADO). Nada de dorado ni plantillas genéricas.
- Movimiento: entradas escalonadas, teléfonos que flotan / se inclinan en 3D.

## Fotos
- `descargar_iphones.py` (a escribir) baja fotos del iPhone X al 18 Pro Max
  a `fotos-iphone/<modelo>/producto|ambiente` + `indice.csv`.
- Nunca usar imágenes con marca de agua ni fondos cuadriculados falsos.
- No mostrar colores que el modelo no tiene (ej.: el 17 Pro es plata, naranja cósmico o azul profundo).
- Recortar fondos con `rembg` (modelo isnet-general-use) y exportar en WebP para la web.

## Cómo se usa
- `python3 descargar_iphones.py --solo-producto --modelos iphone-13,iphone-17-pro` → `fotos-iphone/` (no se sube a git, salvo `indice.csv`).
- `python3 procesar_fotos.py` → `plantillas/assets/telefonos/<modelo>_<color>.webp` (recorte con transparencia).
- `npm install` y después `node exportar_video.js plantillas/llego.html "modelo=iphone-17-pro" salida/llego.mp4`
  (graba cuadro a cuadro a 30 fps; `--cuadro 3000` saca un PNG de ese instante).
- Las plantillas leen los datos de `plantillas/datos.js` y aceptan `?modelo=&color=&bateria=&estado=&formato=historia|post`.
  Para verlas en el navegador hace falta un servidor local (`python3 -m http.server` en la raíz del repo).
- Teléfono 3D: `plantillas/telefono3d.js` (three.js) arma el equipo con medidas reales, canto con grosor,
  módulo de cámara y lentes en relieve, botones y pantalla. Textura = `<modelo>_<color>_dorso.webp`.
  Para sumar un modelo: medidas, módulo y lentes en `datos.js` (fracciones del dorso) y en `MEDIDAS` de procesar_fotos.py.

- Catálogo: `python3 verificar_specs.py && python3 procesar_fotos.py --salida catalogo/img --alto 900 --sin-dorso && python3 generar_catalogo.py`.
  Se abre `catalogo/index.html` (con doble clic usa `stock-demo.js`; con servidor lee `stock.csv`).
  `catalogo/config.js`: número de WhatsApp, link CSV de la Google Sheet con el stock real y `demo: true/false`.
- Reels: `plantillas/reel.html` + guiones en `plantillas/reels.js`.
  `node exportar_video.js plantillas/reel.html "reel=canje&exportar=1" salida/reel_canje.mp4 --fondo <clip> --desde <s> --encuadre <0..1>`.
  Antes de usar un clip, verificar con zoom que el teléfono sea un iPhone (en Mixkit hay muchos Android).
  Clips verificados con iPhone: Mixkit 100050, 100046, 100053 (iPhone rojo); Coverr "close-up of a man taking a selfie on iPhone 15".
- Plan de contenido: `contenido/plan-2-semanas.md`.
- Apertura: `plantillas/apertura.html?pieza=post1..6|story1..6` + `plantillas/canje.html?de=&a=&formato=historia|post`
  (canje 3D, 9 s). Guía en `contenido/apertura.md`. Componentes compartidos: `plantillas/piezas.css` y `piezas.js`
  (callouts técnicos con `<i class="co">`, bloque "Saber más" para historias; los posts cierran con una línea "Link en la bio", sin caja).
  Los teléfonos se ubican por su centro.

## Feedback del usuario sobre "Llegó" (2026-10-21)
- Aprobó la dirección visual.
- El título gigante es el nombre del modelo ("iPhone" chico + "17 PRO" gigante), no "LLEGÓ".
- Sin cintas de texto cruzadas.
- Nada de fotos planas: el teléfono tiene que verse en 3D, con grosor.

## Marca elegida (2026-10-21)
- (2026-10-23) **Cambio de nombre: Tech&Co.** (reemplaza a Celu&Co. en todas las piezas, el catálogo y los textos).
- Logo elegido: **Ruta B "solo logotipo"**: TECH&CO. en Archivo 900 condensada (wdth 62), mayúsculas, el "&" en lima
  y un punto cuadrado lima. Avatar = el logotipo apilado "TECH / &CO." dentro de un círculo hueso o lima (un solo color).
  Sobre fondos claros (lima / hueso) el logotipo va en un solo color (tinta). Ya no se usa el monograma "C&".
  En código: `plantillas/logo.css` (`<span class="logo-tc">Tech<b>&amp;</b>Co<i></i></span>`, variantes `apilado` y `plano`).
  Archivos para Instagram (avatar, logotipo): `plantillas/marca.html` → `salida/marca/`.
- (Antes: Logo A "Celu&Co." en Unbounded 900 + monograma "C&", descartado.)
- Territorio 4 "Drop + tech": Tinta #0A0A0B, Hueso #EEEBE4, Lima #CCFF00, Voltio #8B6CFF, Acero #8E8E96.
  Unbounded (títulos y precios) + JetBrains Mono (todo lo demás). Callouts técnicos, código de barras, "ficha" por equipo.
  Exploración completa: https://claude.ai/artifact/FRYkppJACfMZGxUtbGxx1K
- Las piezas ya hechas ("Llegó") usan la paleta anterior (ácido #D4FF3A); migrarlas al territorio 4.

## Videos
- NO usar videos subidos por terceros en redes ni quitar marcas de agua (copyright). El usuario lo pidió y se le explicó.
- Fuente: Mixkit, solo clips con "Stock Video Free License" (uso comercial y en publicidad online, editable,
  sin atribución). `buscar_videos.py` busca, filtra por licencia y arma `videos/hoja.jpg`; `--bajar ids` baja en 4K/1080.

## Specs
- `verificar_specs.py` lee las fichas técnicas oficiales de Apple Support → `datos/specs_apple.json`
  (capacidades, colores, medidas, URL de la fuente). Usar SIEMPRE esto para specs, no cargar a mano.

## Catálogo web
- Por ahora solo archivo local (no publicar). Stock de EJEMPLO (ficticio, marcado como demo), sin precios:
  todos los modelos del X al 18 Pro Max con sus capacidades y colores reales. Es un esqueleto para editar después.

## Feedback del usuario sobre la apertura (2026-10-22)
- Estilo elegido para el feed: C "Manifiesto" (frases grandes + iPhone 3D sobre lima / voltio / hueso / tinta).
- Cuidar los detalles: teléfonos centrados y lejos de los márgenes (revisar cada pieza).
- Sin recuadros/cajas con texto (chips, tablas): usar callouts técnicos (líneas finas del equipo al dato).
- "Respondé QUIERO" NO va más como gancho. El CTA es una tarjeta que lleva al catálogo online:
  en historias, con el sticker de link nativo de Instagram; en posts, "catálogo en el link de la bio".
- Canje: mostrar que se entrega un modelo viejo/de menor valor y se lleva uno nuevo (animación 3D):
  13 → 17 Pro y 12 → 16 Pro. Nunca un 17 Pro como "el que entregás".
- Por ahora todo es iPhone. Más adelante se van a sumar líneas de celulares más económicos para otro mercado.
- (2026-10-22, 2.ª ronda) Los videos/historias no admiten links: sacar la tarjeta "Catálogo online" de los videos y
  cerrar con "Saber más" + flecha a la casilla de respuesta de la historia. En posts queda "link en la bio".
- (2026-10-23) Nada de "pies" de color: sin tarjetas ni franjas lima/oscuras al pie de los posts. El CTA de los posts es
  una línea de texto mono al pie ("Catálogo online · Link en la bio →"), como el "Deslizá →" de la portada. En los cierres
  de reels el CTA va como texto lima, sin caja.
- Más opciones de "Abrimos" con misterio (reels + posts, marca completa, sin decir qué vendemos):
  expediente sin celular, carga 99 % que pierde la señal, pantalla que se prende y se apaga, y la continuación
  que revela todo. Plantilla `plantillas/misterio.html`, guía `contenido/misterio.md`.

## Tareas pendientes, en orden
1. Script de fotos multi-fuente + revisar calidad por modelo.
2. Kit de plantillas animadas (HTML/CSS) con las fotos reales:
   "Llegó" (equipo nuevo), lista de precios del día, plan canje, caja sellada, sello VENDIDO,
   comparador de 2 modelos, "cómo comprar en 3 pasos".
3. Exportar cada pieza a MP4: 1080×1920 (historias/reels) y 1080×1350 (posts),
   grabando la página con Playwright + ffmpeg. Loop limpio, 8–12 s.
4. Carruseles educativos: "¿15 Pro o 16?", "Qué iPhone comprar con $X",
   "Cómo revisar un iPhone Swap (batería, Face ID, iCloud, IMEI)".
5. Calendario semanal: historias diarias, 3 reels y 1–2 carruseles por semana,
   con textos (copy), hooks del primer segundo y llamado a la acción (tarjeta de link al catálogo).
6. Página de catálogo: modelos ordenados por generación, filtros, batería, precio,
   botón "Lo quiero" que abre WhatsApp con el mensaje armado; stock editable sin tocar código.

## Reglas
- Nunca inventar reseñas, testimonios, ventas ni datos de stock.
- Verificar specs de cada modelo antes de usarlas en una comparación.
- Mostrar avances (imagen o video) antes de producir en cantidad.
