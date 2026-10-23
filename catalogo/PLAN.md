# Catálogo Tech&Co. — plan (para el lunes)

Decisiones del dueño (2026-10-23):

- **Sistema a pedido:** no hay stock fijo. El proveedor consigue y se consulta en el momento; también consigue
  modelos que no están en la lista («¿No lo ves? Te lo conseguimos»).
- **Qué entra:** iPhone (Swap y caja sellada) + **Samsung y Xiaomi (nuevos en caja sellada)**. itel queda afuera.
- **Sin precios en nada** (ni web, ni carrusel, ni WhatsApp, ni historias). Los sellados siempre «Consultar».
  Los precios del proveedor no se guardan; el negocio va a poner los suyos más adelante.
- **Sin colores:** solo modelo y capacidad; el color se habla por WhatsApp.
- **Fotos:** oficiales de cada fabricante (Apple, Samsung, Xiaomi), recortadas. `procesar_fotos.py` (iPhone) y
  `descargar_otros.py` (Samsung/Xiaomi) → `catalogo/img/`. Fuentes en `fotos-iphone/indice.csv` y `fotos-otros/indice.csv`.
- **WhatsApp:** todavía no hay número del negocio → todo se arma con el número vacío en `catalogo/config.js`.
- **Web:** se publica en **Vercel o Netlify** (lunes).

Fuente de datos: **`catalogo/a-pedido.csv`** (sección, marca, línea, modelo, capacidad, RAM, condición, notas).

## Secciones

1. **iPhone · Swap** — Base (12, 13 mini, 13, 14, 15, 16) · Pro (12 Pro → 17 Pro) · Pro Max (12 Pro Max → 16 Pro Max).
2. **iPhone · Caja sellada** — «Consultá por modelo».
3. **Samsung · Nuevos en caja sellada** — Galaxy A17 (128/4), Galaxy A26 5G (128/6), Galaxy S25 Ultra 5G (256/12).
4. **Xiaomi · Nuevos en caja sellada** — Redmi 13C (128/4), Redmi 15R 5G (256/8), Redmi Note 15 Pro (256/8), Redmi Note 17 Pro 5G (256/16).
5. **¿No lo ves? Te lo conseguimos.** — botón a WhatsApp con «Hola Tech&Co., busco un [modelo]».

## Lo que hay que hacer

### 1. Web (link en la bio)
- Adaptar `catalogo/` del modo «stock por unidad» (batería, estado, precio) al **modo a pedido**: tarjetas por modelo con
  foto, nombre, capacidad (y RAM en Android), etiqueta SWAP o NUEVO · CAJA SELLADA y botón **«Consultar»**
  que abre WhatsApp con el mensaje armado («¡Hola Tech&Co.! Quiero consultar por el Galaxy S25 Ultra 256 GB»).
- Filtros: marca (iPhone / Samsung / Xiaomi) y condición (Swap / Sellado).
- Datos desde `a-pedido.csv` (o una Google Sheet publicada como CSV, para editar sin tocar código).
- Identidad de `IDENTIDAD.md`: Archivo condensada en mayúsculas, tinta/hueso/lima/voltio, sin cajas con texto.
- Publicar en Vercel o Netlify (cuenta gratis del dueño) y poner el link en la bio.

### 2. Carrusel para el feed (1080×1350)
- Portada «CATÁLOGO.» + una lámina por sección (iPhone Swap, iPhone sellado, Samsung, Xiaomi) + cierre
  «¿No lo ves? Te lo conseguimos.» Fijarlo en el perfil.

### 3. Imagen única para historias (1080×1920)
- Una placa vertical con todos los modelos por sección, sin precios, con «Saber más» + flecha a la casilla de respuesta.
  Se guarda en la destacada CATÁLOGO y se comparte seguido.

### 4. Catálogo de WhatsApp Business
- Texto listo para cargar cada producto en la app (nombre, descripción, «Consultar») + las fotos de `catalogo/img/`.

## Pendientes / a confirmar con el proveedor
- **Galaxy A26 5G:** ya no está en ningún sitio de Samsung (lo reemplazó el A27). Sin foto oficial: preguntar si
  sigue entrando o si es el A27.
- **Redmi 15R 5G:** es un modelo de China; en el sitio global el equivalente es el **Redmi 15 5G** (la foto es esa).
  Confirmar cuál es.
- **Redmi Note 17 Pro 5G:** el nombre existe (mi.com global), pero la foto del proveedor no coincide con la oficial.
  Confirmar el modelo exacto.
- **iPhone 17 Pro:** el proveedor lo tachó en su historia (sin stock ese día). Va igual con «Consultar».
- Número de WhatsApp del negocio.
