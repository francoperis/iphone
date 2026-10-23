# Tech&Co. — Apertura de la cuenta (estilo Manifiesto)

Archivos en `salida/apertura/`. Se regeneran con `plantillas/apertura.html` y `plantillas/canje.html`:

```
node exportar_video.js plantillas/apertura.html "pieza=post1" salida/apertura/post1.png --cuadro 500
node exportar_video.js plantillas/apertura.html "pieza=story1" salida/apertura/story1.mp4
node exportar_video.js plantillas/canje.html "de=iphone-13&a=iphone-17-pro" salida/apertura/story5_canje_13-17pro.mp4
node exportar_video.js plantillas/canje.html "de=iphone-13&a=iphone-17-pro&formato=post" salida/apertura/post5.png --cuadro 8999
```

## Llamado a la acción

Ya no se usa "Respondé QUIERO".

- **Historias (videos)**: no se les puede poner hipervínculo, así que cierran con **"Saber más"** y una flecha que
  apunta a la casilla para responder la historia ("Escribinos acá abajo").
- **Posts (imágenes)**: tarjeta "Catálogo online · LINK EN LA BIO". El link va en la bio cuando el catálogo esté online.

## Orden sugerido para el día de la apertura

1. **Historias** a la mañana, en orden (story1 → story6).
2. **Carrusel "Abrimos"** al mediodía (post1 → post6).
3. La animación de canje 12 → 16 Pro (`canje_12-16pro.mp4`) queda para otro día de la semana.

## Carrusel — 6 láminas 1080×1350

| # | Lámina | Qué dice |
|---|---|---|
| 1 | Portada (lima) | **Abrimos.** · callouts "Usados / con ficha" y "Caja sellada / sin abrir" · Deslizá → |
| 2 | Qué vendemos (hueso) | Usado no es *segunda* opción. · callouts Usado / Sellado |
| 3 | Línea completa (tinta) | X→18 · Del X al 18 Pro Max. |
| 4 | Nuestra regla (lima) | Ficha a la vista: callouts Batería, Capacidad, Color, Estado |
| 5 | Plan canje (voltio) | Tu iPhone vale. · Entregás iPhone 13 → Te llevás iPhone 17 Pro · tarjeta de catálogo |
| 6 | Cómo comprar (tinta) | 3 pasos: Elegilo · Tocá «Lo quiero» · Es tuyo · tarjeta de catálogo |

Texto de la publicación:

> Abrimos. 🟢
> Somos Tech&Co.: iPhone usados y en caja sellada, del X al 18 Pro Max.
> Cada equipo con su ficha a la vista. Y si tenés un iPhone, lo tomamos como parte de pago.
>
> Todo el stock está en el catálogo: link en la bio.
> 📍 [ZONA] · Envíos [__]
>
> #iphone #iphoneusado #iphoneargentina #celulares #applear

Antes de publicar: completar [ZONA] y envíos en la lámina 6 y en el texto.

## Historias — 1080×1920

| # | Historia | Sticker de Instagram a agregar |
|---|---|---|
| 1 | Cuenta regresiva 3 · 2 · 1 → **Abrimos.** (6 s) | — (o música) |
| 2 | Quiénes somos: "Usado no es segunda opción." (6 s) | Mención a la cuenta |
| 3 | **¿Qué buscás?** (6 s) | **Encuesta** "Usado" / "Sellado", en el espacio libre entre el título y los teléfonos |
| 4 | Del X al 18 Pro Max (6 s) | — |
| 5 | **Tu iPhone vale.** Canje animado en 3D: entregás un iPhone 13, te llevás un 17 Pro (9 s) · Saber más ↓ | **Preguntas** opcional: "¿Qué iPhone tenés?" |
| 6 | ¿Hay uno para vos? · Saber más ↓ (6 s) | — (la flecha apunta a la casilla de respuesta) |

Después de la apertura, guardar las historias en una destacada "Tech&Co.".

## Plan canje — dos animaciones

- `story5_canje_13-17pro.mp4` + `post5.png`: iPhone 13 → iPhone 17 Pro.
- `canje_12-16pro.mp4` + `canje_12-16pro_post.png`: iPhone 12 → iPhone 16 Pro.

Se entrega siempre un modelo más viejo y se lleva uno más nuevo. Las condiciones del canje (cuánto se toma cada equipo)
todavía no están definidas: las piezas no prometen montos.
