# Proyecto: tienda de iPhone — marca: Celu&Co.

Negocio familiar de venta de iPhone usados y en caja sellada, en Argentina.
Objetivo: contenido orgánico DE CALIDAD para Instagram (historias, reels, carruseles)
y una página de catálogo con botón de WhatsApp.

Idioma de todo el contenido: español rioplatense (vos, "escribinos", "tuyo").

## Decisiones tomadas (2026-10-21)
- Nombre de marca: **Celu&Co.** (reemplaza el nombre de trabajo "LOTE").
- El repo arrancó vacío: el script de fotos y los prototipos se rehacen de cero según este brief.
- Fotos: no hay fotos propias. Armar una base de fotos en máxima calidad desde varias fuentes:
  Apple oficial (Newsroom + apple.com), Wikimedia Commons, Unsplash / Pexels y sitios de reviews.
  Registrar en `indice.csv` la fuente, URL, autor y licencia de cada foto.
  Licencias: Apple = uso editorial; Wikimedia = CC (citar autor); Unsplash/Pexels = uso comercial libre;
  sitios de reviews = copyright de terceros → marcar como "solo referencia", no usar en publicidad.
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

## Tareas pendientes, en orden
1. Script de fotos multi-fuente + revisar calidad por modelo.
2. Kit de plantillas animadas (HTML/CSS) con las fotos reales:
   "Llegó" (equipo nuevo), lista de precios del día, plan canje, caja sellada, sello VENDIDO,
   comparador de 2 modelos, "cómo comprar en 3 pasos".
3. Exportar cada pieza a MP4: 1080×1920 (historias/reels) y 1080×1350 (posts),
   grabando la página con Playwright + ffmpeg. Loop limpio, 8–12 s.
4. Carruseles educativos: "¿15 Pro o 16?", "Qué iPhone comprar con $X",
   "Cómo revisar un iPhone usado (batería, Face ID, iCloud, IMEI)".
5. Calendario semanal: historias diarias, 3 reels y 1–2 carruseles por semana,
   con textos (copy), hooks del primer segundo y llamado a la acción ("Respondé QUIERO").
6. Página de catálogo: modelos ordenados por generación, filtros, batería, precio,
   botón "Lo quiero" que abre WhatsApp con el mensaje armado; stock editable sin tocar código.

## Reglas
- Nunca inventar reseñas, testimonios, ventas ni datos de stock.
- Verificar specs de cada modelo antes de usarlas en una comparación.
- Mostrar avances (imagen o video) antes de producir en cantidad.
