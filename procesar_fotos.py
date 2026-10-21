#!/usr/bin/env python3
"""Prepara las fotos de producto para las plantillas y la web.

Para cada modelo y color elige, entre las imágenes de la tienda de Apple bajadas por
descargar_iphones.py, la que tiene el equipo más grande. Si viene con fondo, lo recorta
(fondo liso de estudio: relleno desde los bordes; si no, rembg isnet-general-use). Recorta el borde vacío y exporta WebP con transparencia:

    plantillas/assets/telefonos/<modelo>_<color>.webp        dorso + frente (para piezas 2D)
    plantillas/assets/telefonos/<modelo>_<color>_dorso.webp  solo el dorso (textura del modelo 3D)

Uso:
    python3 procesar_fotos.py                       # todos los modelos bajados
    python3 procesar_fotos.py --modelos iphone-13,iphone-17-pro --alto 1800
"""

import argparse
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None

FOTOS = Path("fotos-iphone")
SALIDA = Path("plantillas/assets/telefonos")
PATRON = re.compile(r"apple-store_(?P<color>[a-z]+)_(?P<slug>.+)\.png$")


def caja_equipo(im):
    """Devuelve (caja, tiene_fondo). Con transparencia usa el canal alfa; si no, la diferencia con la esquina."""
    rgba = im.convert("RGBA")
    alfa = rgba.getchannel("A")
    if alfa.getextrema()[0] < 255:
        return alfa.point(lambda v: 255 if v > 8 else 0).getbbox(), False
    rgb = rgba.convert("RGB")
    fondo = Image.new("RGB", rgb.size, rgb.getpixel((2, 2)))
    dif = ImageChops.difference(rgb, fondo).convert("L").point(lambda v: 255 if v > 10 else 0)
    return dif.getbbox(), True


_sesion = None


def sin_fondo(im):
    """Fondo liso de estudio (tienda de Apple): relleno desde los bordes, que se frena en el marco
    del equipo y no se come dorsos claros (rosa, blanco estelar). Si el fondo no es liso, rembg."""
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    borde = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    if borde.std(axis=0).max() > 3:
        global _sesion
        from rembg import new_session, remove
        if _sesion is None:
            _sesion = new_session("isnet-general-use")
        return remove(im.convert("RGB"), session=_sesion, post_process_mask=True)

    tol, suave = 7, 26
    fondo_rgb = np.median(borde, axis=0)
    dif = np.abs(a - fondo_rgb).max(axis=2)
    etiquetas, _ = ndimage.label(dif <= tol)
    en_borde = np.unique(np.concatenate([etiquetas[0], etiquetas[-1], etiquetas[:, 0], etiquetas[:, -1]]))
    fondo = np.isin(etiquetas, en_borde[en_borde > 0])
    # franja de 2 px: alfa suave y se quita el gris mezclado en el borde
    franja = ndimage.binary_dilation(fondo, iterations=2) & ~fondo
    alfa = np.where(fondo, 0, 255).astype(np.float32)
    alfa[franja] = np.clip((dif[franja] - tol) / (suave - tol), 0, 1) * 255
    rgb = a.astype(np.float32)
    k = np.maximum(alfa / 255, 1e-3)[..., None]
    rgb = np.where(franja[..., None], np.clip((rgb - fondo_rgb * (1 - k)) / k, 0, 255), rgb)
    return Image.fromarray(np.dstack([rgb, alfa]).astype(np.uint8), "RGBA")


def procesar_modelo(modelo, alto, forzar):
    carpeta = FOTOS / modelo / "producto"
    por_color = {}
    for f in sorted(carpeta.glob("apple-store_*.png")):
        mt = PATRON.match(f.name)
        if not mt:
            continue
        im = Image.open(f)
        caja, tiene_fondo = caja_equipo(im)
        if not caja:
            continue
        alto_equipo = caja[3] - caja[1]
        # se prefiere la versión transparente salvo que la otra sea bastante más grande
        puntaje = alto_equipo * (0.8 if tiene_fondo else 1.0)
        actual = por_color.get(mt["color"])
        if not actual or puntaje > actual[0]:
            por_color[mt["color"]] = (puntaje, f, caja, tiene_fondo, alto_equipo)

    for color, (_, f, caja, tiene_fondo, alto_equipo) in sorted(por_color.items()):
        destino = SALIDA / f"{modelo}_{color}.webp"
        if destino.exists() and not forzar:
            print(f"  {destino.name}: ya existe")
            continue
        im = Image.open(f).convert("RGBA")
        margen = 24
        x0, y0, x1, y1 = caja
        im = im.crop((max(0, x0 - margen), max(0, y0 - margen), min(im.width, x1 + margen), min(im.height, y1 + margen)))
        if tiene_fondo:
            im = sin_fondo(im)
        im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
        if im.height > alto:
            im = im.resize((round(im.width * alto / im.height), alto), Image.LANCZOS)
        destino.parent.mkdir(parents=True, exist_ok=True)
        im.save(destino, "WEBP", quality=90, method=6)
        aviso = "  (CHICA: menos de 1200 px de alto)" if im.height < 1200 else ""
        print(f"  {destino.name}: {im.width}x{im.height} desde {f.name}"
              f"{' (fondo recortado)' if tiene_fondo else ''}{aviso}")


# Medidas oficiales (mm): ancho, alto, espesor. Las usa la plantilla 3D (plantillas/datos.js) y el
# recorte del dorso, que toma el ancho del equipo de la proporción ancho/alto.
MEDIDAS = {
    "iphone-13": (71.5, 146.7, 7.65),
    "iphone-15-pro": (70.6, 146.6, 8.25),
    "iphone-16-pro": (71.5, 149.6, 8.25),
    "iphone-17-pro": (71.9, 150.0, 8.75),
}


# Modelos cuyas fotos tienen la pantalla encima del dorso: desde x = "tapado" (fracción del ancho)
# el dorso no se ve. Esa franja es metal liso, así que se reconstruye espejando el lado izquierdo;
# "camara_abajo" es el borde inferior del módulo de cámara, que no se tiene que espejar.
TAPADO = {
    "iphone-15-pro": {"tapado": 0.645, "camara_abajo": 0.335},
    "iphone-16-pro": {"tapado": 0.665, "camara_abajo": 0.33},
}


def completar_dorso(im, tapado, camara_abajo):
    a = np.asarray(im).astype(np.float32)
    alto, ancho = a.shape[:2]
    x0 = int(ancho * tapado)
    n = max(2, int(ancho * 0.03))                 # franja de mezcla antes de x0
    xs = np.arange(x0 - n, ancho)
    espejo = ancho - 1 - xs
    borde_izq = espejo < ancho * 0.05             # el canto izquierdo no tiene cámara: se espeja tal cual
    y_cam, y_tope = int(alto * camara_abajo), int(alto * 0.025)
    relleno = np.empty((alto, len(xs), 4), np.float32)
    for y in range(alto):
        if y < y_tope:                            # filete superior: se estira la última columna visible
            fila = np.repeat(a[y, x0 - n - 1][None], len(xs), axis=0)
        elif y < y_cam:                           # a la altura de la cámara se toma el metal de más abajo
            fila = a[min(alto - 1, 2 * y_cam - y), espejo].copy()
        else:
            fila = a[y, espejo].copy()
        fila[borde_izq] = a[y, espejo[borde_izq]]
        relleno[y] = fila
    # la luz del lado espejado no es la misma: se corrige el brillo por fila (suavizado en vertical)
    # para que el relleno continúe a la parte visible sin escalón
    ref = slice(0, n)
    dif = (a[:, x0 - n:x0, :3] - relleno[:, ref, :3]).mean(axis=1)
    dif = ndimage.gaussian_filter1d(dif, sigma=alto * 0.015, axis=0)
    relleno[:, :, :3] += dif[:, None, :]
    out = a.copy()
    t = np.concatenate([np.linspace(0, 1, n), np.ones(len(xs) - n)])[None, :, None]
    out[:, x0 - n:] = a[:, x0 - n:] * (1 - t) + relleno * t
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")


def tipo_imagen(nombre):
    """En las de reacondicionados y en las -select el dorso está adelante y se ve entero."""
    if "refurb-" in nombre:
        return 3
    if "finish-select" in nombre:
        return 1
    return 2


def procesar_dorsos(modelo, alto, forzar):
    """Exporta <modelo>_<color>_dorso.webp: solo la cara trasera, para usarla como textura del 3D."""
    if modelo not in MEDIDAS:
        print(f"  dorso: faltan las medidas de {modelo} en MEDIDAS; se saltea")
        return
    ancho_mm, alto_mm, _ = MEDIDAS[modelo]
    mejores = {}
    for f in sorted((FOTOS / modelo / "producto").glob("apple-store_*.png")):
        mt = PATRON.match(f.name)
        if not mt:
            continue
        im = Image.open(f)
        caja, tiene_fondo = caja_equipo(im)
        if not caja:
            continue
        alto_equipo = caja[3] - caja[1]
        clave = (alto_equipo >= 1000, tipo_imagen(mt["slug"]), alto_equipo * (0.8 if tiene_fondo else 1.0))
        if mt["color"] not in mejores or clave > mejores[mt["color"]][0]:
            mejores[mt["color"]] = (clave, f, caja, tiene_fondo)

    for color, (clave, f, caja, tiene_fondo) in sorted(mejores.items()):
        destino = SALIDA / f"{modelo}_{color}_dorso.webp"
        if destino.exists() and not forzar:
            print(f"  {destino.name}: ya existe")
            continue
        if clave[1] == 1:
            print(f"  {destino.name}: ojo, sale de una foto donde la pantalla puede tapar parte del dorso")
        im = Image.open(f).convert("RGBA")
        x0, y0, x1, y1 = caja
        im = im.crop((max(0, x0 - 24), max(0, y0 - 24), min(im.width, x1 + 24), min(im.height, y1 + 24)))
        if tiene_fondo:
            im = sin_fondo(im)
        im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
        # el dorso es el equipo de la izquierda. Su alto se mide en una franja donde solo está él
        # (el frente puede estar corrido arriba o abajo) y el ancho sale de la proporción real.
        alfa = np.asarray(im.getchannel("A")) > 128
        x = round(im.height * ancho_mm / alto_mm * 0.18)
        filas = np.flatnonzero(alfa[:, x])
        arriba, abajo = int(filas[0]), int(filas[-1]) + 1
        ancho = round((abajo - arriba) * ancho_mm / alto_mm)
        im = im.crop((0, arriba, min(im.width, ancho), abajo))
        if modelo in TAPADO:
            im = completar_dorso(im, **TAPADO[modelo])
        if im.height > alto:
            im = im.resize((round(im.width * alto / im.height), alto), Image.LANCZOS)
        im.save(destino, "WEBP", quality=92, method=6)
        print(f"  {destino.name}: {im.width}x{im.height} desde {f.name}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modelos", help="ids separados por coma; por defecto, todos los bajados")
    ap.add_argument("--alto", type=int, default=1800, help="alto máximo en px")
    ap.add_argument("--forzar", action="store_true", help="rehacer aunque el archivo exista")
    a = ap.parse_args()
    modelos = a.modelos.split(",") if a.modelos else sorted(p.name for p in FOTOS.iterdir()
                                                            if (p / "producto").is_dir())
    for m in modelos:
        print(f"== {m}")
        procesar_modelo(m.strip(), a.alto, a.forzar)
        procesar_dorsos(m.strip(), a.alto, a.forzar)


if __name__ == "__main__":
    main()
