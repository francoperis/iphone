#!/usr/bin/env python3
"""Fotos oficiales de los equipos Samsung y Xiaomi del catálogo (los que consigue el proveedor, catalogo/a-pedido.csv).

Mismo criterio que descargar_iphones.py: solo fuentes oficiales (samsung.com/ar y mi.com/global), en la mejor calidad,
registrando fuente, URL y licencia en fotos-otros/indice.csv. Licencia: uso editorial (el dueño asume el riesgo de usarlas
en publicidad, igual que con las de Apple, 2026-10-23).

Después recorta: si la foto ya viene con transparencia (Samsung, la mayoría de Xiaomi) solo se recorta el borde vacío;
si viene sobre fondo blanco, se saca el fondo con rembg (isnet-general-use). Sale en WebP a catalogo/img/<modelo>.webp.

Uso:
    python3 descargar_otros.py             # baja lo que falta y regenera los WebP
    python3 descargar_otros.py --alto 900  # alto de los WebP (por defecto 900, como el catálogo de iPhone)
"""

import argparse
import csv
import io
from pathlib import Path

import requests
from PIL import Image

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
RAIZ = Path(__file__).resolve().parent
FOTOS = RAIZ / "fotos-otros"
SALIDA = RAIZ / "catalogo/img"
SAMSUNG = "https://images.samsung.com/is/image/samsung/p6pim/ar/"
LICENCIA = "uso editorial (sitio oficial del fabricante)"

# modelo del catálogo -> foto oficial elegida a mano (vista: dorso + frente o dorso solo).
# Samsung: usar la galería del producto con $ORIGIN_PNG$ (1920×1280); las miniaturas "thumb" son de 330 px.
FOTOS_OFICIALES = {
    "galaxy-a17": {
        "url": SAMSUNG + "sm-a175fzkraro/gallery/ar-galaxy-a17-sm-a175-582491-sm-a175fzkraro-551337027?$ORIGIN_PNG$",
        "pagina": "https://www.samsung.com/ar/smartphones/galaxy-a/galaxy-a17-black-128gb-sm-a175fzkraro/", "fuente": "Samsung Argentina", "color": "negro",
    },
    "galaxy-s25-ultra": {
        "url": SAMSUNG + "sm-s938bzkllea/gallery/ar-galaxy-s25-s938-567282-sm-s938bzkllea-549446835?$ORIGIN_PNG$",
        "pagina": "https://www.samsung.com/ar/smartphones/galaxy-s/galaxy-s25-ultra-titanium-black-256gb-sm-s938bzkllea/", "fuente": "Samsung Argentina", "color": "negro titanio",
    },
    # Galaxy A26 5G: ya no figura en samsung.com (ar, latin, mx, cl, co, br, uk, es, de, it, fr, in): sin foto oficial por ahora
    "redmi-13c": {
        "url": "https://i02.appmifile.com/477_operatorx_operatorx_opx/08/11/2023/a69b2ced4a4e2403fbfd446994c26a06.png",
        "pagina": "https://www.mi.com/global/product/redmi-13c/specs/", "fuente": "Xiaomi (mi.com global)", "color": "verde",
    },
    # el proveedor lo llama "Redmi 15R 5G" (modelo de China); en mi.com global el equivalente es el Redmi 15 5G
    "redmi-15-5g": {
        "url": "https://i02.appmifile.com/932_operatorx_operatorx_opx/13/08/2025/14f80452c6d3bae80190dba0a184438f.png",
        "pagina": "https://www.mi.com/global/product/redmi-15-5g/specs/", "fuente": "Xiaomi (mi.com global)", "color": "verde",
    },
    "redmi-note-15-pro": {
        "url": "https://i02.appmifile.com/139_operatorx_operatorx_opx/08/01/2026/a277a33b5b40a10292c428d138853406.png",
        "pagina": "https://www.mi.com/global/product/redmi-note-15-pro/specs/", "fuente": "Xiaomi (mi.com global)", "color": "negro",
    },
    "redmi-note-17-pro-5g": {
        "url": "https://i02.appmifile.com/mi-com-product/fly-birds/redmi-note-17-pro-5g/pc/icon-screen05-1.png",
        "pagina": "https://www.mi.com/global/product/redmi-note-17-pro-5g/", "fuente": "Xiaomi (mi.com global)", "color": "negro",
    },
}


def bajar(modelo, dato):
    destino = FOTOS / modelo / "producto" / f"{modelo}_oficial.png"
    if destino.exists():
        return destino
    r = requests.get(dato["url"], headers={"User-Agent": UA}, timeout=60)
    r.raise_for_status()
    destino.parent.mkdir(parents=True, exist_ok=True)
    Image.open(io.BytesIO(r.content)).save(destino)
    return destino


def sin_fondo(im):
    """Si la foto ya tiene transparencia se deja; si viene sobre fondo liso, rembg."""
    im = im.convert("RGBA")
    transparente = sum(1 for p in im.getchannel("A").resize((64, 64)).getdata() if p < 10) / 4096
    if transparente > 0.15:
        return im
    from rembg import new_session, remove
    return remove(im, session=new_session("isnet-general-use"))


def recortar(im, alto):
    caja = im.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
    im = im.crop(caja) if caja else im
    if im.height > alto:
        im = im.resize((round(im.width * alto / im.height), alto), Image.LANCZOS)
    return im


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--alto", type=int, default=900)
    args = ap.parse_args()
    SALIDA.mkdir(parents=True, exist_ok=True)
    filas = []
    for modelo, dato in FOTOS_OFICIALES.items():
        archivo = bajar(modelo, dato)
        webp = SALIDA / f"{modelo}.webp"
        recortar(sin_fondo(Image.open(archivo)), args.alto).save(webp, "WEBP", quality=90, method=6)
        print(f"{modelo}: {webp.relative_to(RAIZ)}")
        filas.append({"modelo": modelo, "archivo": str(archivo.relative_to(RAIZ)), "color": dato["color"],
                      "fuente": dato["fuente"], "url": dato["url"], "pagina": dato["pagina"], "licencia": LICENCIA})
    with open(FOTOS / "indice.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    main()
