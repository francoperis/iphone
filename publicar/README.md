# Tech&Co. — contenido listo para subir

Cada carpeta es una sección. Las imágenes (`_post.png`) son de 1080×1350 para el feed; los videos `_historia.mp4`
y `_reel.mp4` son de 1080×1920. Todo se regenera con `./publicar.sh` (o `./publicar.sh imagenes` para solo los PNG).

Reglas que ya están aplicadas en todas las piezas:
- Los equipos son **Swap** o **en caja sellada** (nunca "usados").
- La cuenta no se presenta como "solo iPhone": se habla de *equipos*. iPhone aparece solo cuando se muestra un iPhone.
- Posts: el CTA va como texto al pie ("Link en la bio"). Historias: "Saber más" con flecha a la casilla de respuesta.
- Antes de publicar, completar los datos entre corchetes ([ZONA], envíos) en el texto y en las piezas que los tengan.

| Carpeta | Qué hay | Cuándo se usa |
|---|---|---|
| `00-marca/` | Foto de perfil (lima, hueso, negro), logotipo y hoja de marca | Al armar la cuenta |
| `01-teasers/` | Expediente, Carga, Pantalla y "En camino": no dicen qué vendemos | Los días antes de abrir |
| `02-apertura/` | Abrimos, revelación (continuación de Carga o Pantalla), presentación, "¿Hay uno para vos?" | El día que abrimos |
| `03-que-vendemos/` | "Lo mejor, a tu alcance." (Swap y sellado), "Todo a la vista.", encuesta "¿Qué buscás?" | Primera semana, y cada tanto |
| `04-como-comprar/` | 3 pasos: elegilo, tocá «Lo quiero», es tuyo | Primera semana, y fijar en el perfil |
| `05-plan-canje/` | Canje en 3D (13 → 17 Pro, 12 → 16 Pro) y reel "¿Cuánto vale tu equipo viejo?" | Una vez por semana |
| `06-tips/` | Reel "No compres un iPhone Swap sin chequear esto" | Contenido para guardar/compartir |
| `equipos/iphone/` | Línea completa (X → 18), flyers de nuevos en caja sellada, "Llegó" (ingresos) y reel "primera foto" | Cuando entra stock o para mostrar la línea |
| `equipos/samsung/`, `equipos/xiaomi/` | Vacías por ahora | Cuando se sumen esas marcas |

## Textos para copiar

**01 · Teasers**
- Expediente: *Todavía no podemos mostrarlo. Muy pronto, todo a la vista.*
- Carga / Pantalla: *Estábamos por mostrarles algo… y se cortó.* 🔌 (se sube una de las dos, no ambas)

**02 · Apertura**
> Abrimos. 🟢
> Somos Tech&Co.: equipos Swap y en caja sellada.
> Cada equipo con su batería, capacidad y estado a la vista. Y si tenés un equipo, lo tomamos como parte de pago.
>
> Todo el stock está en el catálogo: link en la bio.
> 📍 [ZONA] · Envíos [__]

Revelación: subir la continuación de la idea elegida (Carga → `revelacion-carga_reel.mp4`, Pantalla → `revelacion-pantalla_reel.mp4`).

**03 · Qué vendemos**
> Lo mejor, a tu alcance.
> Swap o en caja sellada: vos elegís. Mirá el stock en el link de la bio.

En la historia "¿Qué buscás?" agregar el sticker de **encuesta** (Swap / Sellado) en el espacio libre entre el título y los equipos.

**05 · Plan canje**
> Tu equipo vale. Entregalo como parte de pago y llevate uno más nuevo.
> Escribinos por DM con modelo, capacidad y batería. [condiciones del canje]

**Equipos · nuevos en caja sellada**
> Nuevo. [Modelo] [GB] en caja sellada, 0 km. Precio: consultanos por DM.

Para hacer un flyer de otro modelo:
`node exportar_video.js plantillas/sellado.html "modelo=iphone-17-pro&color=deepblue&gb=512&formato=post" publicar/equipos/iphone/nuevos-caja-sellada/iphone-17-pro-azul_post.png --cuadro 7999`
(sin `&formato=post` y sin `--cuadro` sale la historia en video).

Hashtags base: #tecnologia #celulares #swap #cajasellada #argentina (+ #iphone #iphoneswap cuando la pieza muestra un iPhone).
