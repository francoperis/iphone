# Proyecto: tienda de iPhone — marca: Tech&Co.

Negocio familiar de venta de equipos **Swap** y en caja sellada, en Argentina. Hoy iPhone; después Samsung y Xiaomi.
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
- Precios: se definen más adelante (ver «Precios»).
- Primer avance: plantilla animada "Llegó" exportada a MP4 1080×1920, en 4 variantes:
  iPhone 13, 15 Pro, 16 Pro y 17 Pro.

## Datos que faltan (pedírselos al usuario antes de publicar nada)
- WhatsApp del negocio: **3795 33-6448** (wa.me/5493795336448, 2026-10-27; ya está en `catalogo/config.js`). (Instagram: **@techco.ctes**, 2026-10-23; «ctes» = Corrientes → confirmar [ZONA].)
- (2026-10-23) Todavía NO hay equipos en la mano: fase 0 = teasers sin prometer stock (ver `publicar/ARRANCAR.md`).
- Zona de retiro / envíos, medios de pago, cuotas, meses de garantía.
- (2026-10-23) Sistema **a pedido**: no hay stock fijo; el proveedor consigue y se consulta en el momento
  (también otros modelos que no están en la lista). Modelos que comercializa el proveedor: `catalogo/a-pedido.csv`
  (sin nombre ni precios del proveedor). El catálogo se organiza por secciones: iPhone (Base / Pro / Pro Max / caja sellada),
  Samsung y Xiaomi (nuevos en caja sellada, entran ya; itel queda afuera). Sin precios.
  Formatos del catálogo: web propia (link en la bio), carrusel para el feed, catálogo de WhatsApp Business e imagen única para historias.
  **Plan completo y pendientes: `contenido/plan-catalogo.md`** (web hecha el 2026-10-27; se publica en Vercel). Sin colores en el catálogo.
  Fotos de Samsung/Xiaomi: `python3 descargar_otros.py` (oficiales, recortadas) → `catalogo/img/`.
- Reglas del plan canje.
- Stock real: modelo, GB, color, % batería, precio, estado. Nunca inventar estos datos:
  usar marcadores como [__]% o [ZONA] hasta tenerlos.

## Precios
- (2026-10-23) **Todavía no hay precios: no publicar precios en ninguna pieza ni en el catálogo.** Los precios del
  proveedor NO se guardan ni se usan (el negocio va a definir los suyos). Las plantillas muestran «Precio a consultar»
  salvo que se les pase `?precio=` con el precio que defina el negocio.
- Lo que manda el proveedor: la lista de iPhone con precio = equipos **Swap**; la lista de Samsung/Xiaomi = equipos
  **nuevos en caja sellada**. Los **sellados siempre van con «Consultar»**.
Caja sellada: "consultar". NO mostrar nunca la cotización del dólar en las piezas.

## Identidad visual
**Fijada en `IDENTIDAD.md` (leerlo antes de generar cualquier pieza).** Valores en código: `plantillas/identidad.css`.
Resumen: tinta #0A0A0B · hueso #EEEBE4 · lima #CCFF00 · voltio #8B6CFF · acero #8E8E96. Títulos en Archivo 900
condensada (62 %) en MAYÚSCULAS, interlineado 0,92; textos en JetBrains Mono 700. Escala fija de tamaños
(--t-xxl 380 … --t-xs 56, --m-l 28 … --m-s 20). Márgenes 72 px. Sin cajas, sin líneas desde los teléfonos, sin «0 KM».

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

- Catálogo (a pedido): se edita `catalogo/a-pedido.csv` y se corre `python3 generar_catalogo.py` (revisa fotos y arma
  `a-pedido.js` para abrirlo con doble clic). `catalogo/config.js`: número de WhatsApp, link CSV de una Google Sheet (opcional), Instagram.
  La carpeta `catalogo/` se publica entera: no poner ahí notas internas ni nada del proveedor.
- Reels: `plantillas/reel.html` + guiones en `plantillas/reels.js`.
  `node exportar_video.js plantillas/reel.html "reel=canje&exportar=1" salida/reel_canje.mp4 --fondo <clip> --desde <s> --encuadre <0..1>`.
  Antes de usar un clip, verificar con zoom que el teléfono sea un iPhone (en Mixkit hay muchos Android).
  Clips verificados con iPhone: Mixkit 100050, 100046, 100053 (iPhone rojo); Coverr "close-up of a man taking a selfie on iPhone 15".
- Reel/anuncio «¿Por qué un Swap?» (15 s): `plantillas/swap.html?hook=porque|que` sobre el clip de Coverr de la selfie con
  iPhone 15 (`--encuadre 0.15`, así la cámara queda a la vista). Hook → «Revisados, uno por uno» con desfile 3D
  (13 → 15 Pro → 16 Pro → 17 Pro) y lo que se revisa → «Decime qué celular buscás y te lo conseguimos». Texto clave entre
  y 250 y 1300 (zona segura de anuncios). «Revisados» lo confirmó el dueño (2026-10-28). → `publicar/03-que-vendemos/por-que-swap_hook-*.mp4`.
- Música: `python3 musica.py salida.wav --duracion 15 --entrada 3.2 --barridos 3.55,5.3,7.05,8.8 --cierre 11 --video in.mp4 --salida-video out.mp4`
  sintetiza una pista ORIGINAL (120 BPM, La menor, sin licencias de terceros) con la entrada y los barridos en los cortes.
  Mixkit Music (Free License) permite redes y anuncios, pero corta las consultas desde este entorno (429): no insistir con reintentos.
  Para el feed conviene igual sumar un audio en tendencia de la biblioteca de Instagram.
- Clips (2026-10-28): no hay en Mixkit ni en Coverr un clip libre de «una mano mostrando varios celulares distintos»;
  Pexels/Pixabay bloquean el acceso automático. Ese tipo de video se filma (ver guía en la respuesta del 2026-10-28).
- Clips con personas reales (2026-10-28, Coverr gratis): reels `unboxing` y `bateria` en `plantillas/reels.js` (10 s, con música)
  → `publicar/03-que-vendemos/unboxing_reel.mp4`, `bateria_reel.mp4`. «Te muestro la batería»: `armar_bateria.py` pone
  `plantillas/pantalla-bateria.html` (Ajustes › Batería, modo oscuro) en un iPhone con pantalla verde, siguiendo la pantalla
  cuadro a cuadro (dedos adelante, marcas tapadas); la pantalla arranca apagada para que se lea el hook (`--encender 4.2`).
  El porcentaje va BORRONEADO (no es un equipo real: no inventar el número). Los iPhone con pantalla verde de Coverr son
  modelos viejos (con bisel): por eso el clip va bien de cerca.
- Comparar (en curso, sin exportar): `plantillas/comparar.html?c=a56-vs-13|note15pro-vs-a36` (historia con encuesta) y
  `?c=13-vs-14|15pro-vs-16pro` (reel comparador); datos verificados en `plantillas/comparar.js`.
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
  (2026-10-23) Títulos en Archivo condensada (reemplaza a Unbounded) + JetBrains Mono. Ver IDENTIDAD.md.
  Exploración completa: https://claude.ai/artifact/FRYkppJACfMZGxUtbGxx1K
- "Llegó" ya está migrada a la paleta y la tipografía nuevas (2026-10-23).

## Videos
- NO usar videos subidos por terceros en redes ni quitar marcas de agua (copyright). El usuario lo pidió y se le explicó.
- Fuente: Mixkit, solo clips con "Stock Video Free License" (uso comercial y en publicidad online, editable,
  sin atribución). `buscar_videos.py` busca, filtra por licencia y arma `videos/hoja.jpg`; `--bajar ids` baja en 4K/1080.

## Specs
- `verificar_specs.py` lee las fichas técnicas oficiales de Apple Support → `datos/specs_apple.json`
  (capacidades, colores, medidas, URL de la fuente). Usar SIEMPRE esto para specs, no cargar a mano.

## Catálogo web
- (2026-10-27) Modo **a pedido** (reemplaza al esqueleto de stock por unidad): secciones iPhone Swap (Base / Pro / Pro Max),
  iPhone sellado (una sola tarjeta «Todos los modelos»), Samsung, Xiaomi y «¿No lo ves? Te lo conseguimos».
  Tarjeta = foto, SWAP o NUEVO · CAJA SELLADA, modelo, capacidad (+ RAM en Android) y botón «Consultar» → WhatsApp.
  Sin precios ni colores. Se publica en Vercel (Root Directory `catalogo`); guía en `contenido/plan-catalogo.md`.

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
- (2026-10-23, 3.ª ronda)
  - Sin encabezados de sección en las piezas ("// 001 · Apertura", "// 02 · Qué vendemos", "// Quiénes somos"…): solo el logo.
  - "Ficha" / "con ficha" no se entiende: no usarlo. Se dice "batería, capacidad y estado a la vista" / "Todo a la vista."
  - Swap = equipos reacondicionados (refurbished). No hace falta explicarlo más en las piezas.
  - Gancho de "qué vendemos": **"Lo mejor, a tu alcance."** Descartados: "Usado/Swap no es segunda opción",
    cualquier frase con "estrenar", "Sellado o Swap. Vos elegís", "Como nuevo. A otro precio.".
  - El nombre Tech&Co. es para abarcar más mercado: **Samsung y Xiaomi más adelante** (con su propio lanzamiento) y,
    algún día, otras cosas tech (PlayStation, etc.). Por eso, cuando se habla de la cuenta, NO anclar la marca a
    "solo iPhone": decir "equipos". iPhone se nombra solo cuando la pieza muestra un iPhone.
  - Flyer de equipos nuevos en caja sellada: `plantillas/sellado.html?modelo=&color=&gb=&formato=historia|post`
    (precio "consultar", sello "NUEVO · CAJA SELLADA"; la historia arranca con un video real de unboxing de Coverr).
    (2026-10-27) También sirve para Samsung/Xiaomi e iPhone sin 3D: foto oficial de `EQUIPOS_FOTO` (datos.js), RAM en vez
    de color, y `&condicion=swap` (título «Swap.»). El clip de unboxing muestra una caja de iPhone: solo va en iPhone nuevos.
    Historias de «los más buscados» (ranking de Mercado Libre AR, oct. 2026) en `publicar/equipos/mas-buscados/`.
  - Todo lo listo para subir va en **`publicar/`** (sí se sube a git), por sección (00-marca, 01-teasers, 02-apertura,
    03-que-vendemos, 04-como-comprar, 05-plan-canje, 06-tips) y por marca (`equipos/iphone|samsung|xiaomi`).
    Se regenera con `./publicar.sh`; guía y textos en `publicar/README.md`.
- (2026-10-23, 4.ª ronda) Títulos: **Archivo condensada** (elegida entre Unbounded, Space Grotesk y Bricolage).
  Nada de «0 KM» (no es un vehículo): el sello dice «NUEVO · CAJA SELLADA». Sin líneas/flechas que salgan de los teléfonos.
  «ABRIMOS» en una sola línea, grande, superpuesto al equipo flotando. **Elegida la B: la palabra encima del equipo** (plata),
  también en el reel de revelación (`?abrimos=a` deja la otra prueba).
  La animación de la caja 3D se descartó (fea): el flyer de nuevos usa un video real de unboxing con licencia libre.
  Teaser elegido: Carga 99 % (Pantalla descartada); sin «Expediente 001».
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
