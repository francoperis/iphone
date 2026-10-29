#!/usr/bin/env python3
"""Limpia las capturas de las historias del proveedor: recorta la interfaz (barra de estado, nombre del proveedor,
textos con nombres de clientes, «Responder») y mejora tamaño, nitidez, luz y color.

Las originales NO se suben a git (tienen nombres de clientes del proveedor). Salida: fotos-proveedor/<nombre>.jpg
Uso: python3 limpiar_proveedor.py <carpeta_con_las_capturas>
"""
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# archivo -> (nombre, y0, y1) en px de la captura de 590×1280 (ancho completo)
RECORTES = {
    "5123260290773486867.jpg": ("galaxy-a17_caja", 335, 935),
    "5123260290773486868.jpg": ("iphone-13-mini_rosa_accesorios", 150, 1000),
    "5123260290773486869.jpg": ("iphone-14-pro_plata_accesorios", 210, 1005),
    "5123260290773486870.jpg": ("iphone-13-pro_plata_dorso", 200, 1000),
    "5123260290773486871.jpg": ("iphone-13-pro_plata_accesorios", 280, 1000),
    "5123260290773486873.jpg": ("iphone-17-pro_naranja_camara", 160, 1150),
    "5123260290773486874.jpg": ("iphone-17-pro_naranja_mano", 160, 1130),
    "5123260290773486875.jpg": ("iphone-17-pro_naranja_accesorios", 160, 1120),
    "5123260290773486876.jpg": ("iphone-17-pro_tres-colores_mano", 212, 1060),
    "5123260290773486877.jpg": ("iphone-17-pro_tres-colores_cajas", 80, 1035),
}
ANCHO = 1080
# zonas a borronear (px de la foto ya agrandada a 1080 de ancho): etiquetas con número de serie
BORRONEAR = {"iphone-13-pro_plata_dorso": [(290, 870, 840, 1170)]}


def mejorar(im):
    im = im.convert("RGB")
    alto = round(im.height * ANCHO / im.width)
    im = im.resize((ANCHO, alto), Image.LANCZOS)
    im = im.filter(ImageFilter.MedianFilter(3))                       # baja el ruido de compresión
    im = ImageOps.autocontrast(im, cutoff=0.5)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    return im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=90, threshold=2))


def main():
    origen = Path(sys.argv[1])
    salida = Path(__file__).resolve().parent / "fotos-proveedor"
    salida.mkdir(exist_ok=True)
    for archivo, (nombre, y0, y1) in RECORTES.items():
        im = Image.open(origen / archivo)
        k = im.height / 1280                                            # una captura vino más chica (369×800)
        im = im.crop((0, round(y0 * k), im.width, round(y1 * k)))
        im = mejorar(im)
        for caja in BORRONEAR.get(nombre, []):
            im.paste(im.crop(caja).filter(ImageFilter.GaussianBlur(14)), caja[:2])
        im.save(salida / f"{nombre}.jpg", quality=92)
        print(nombre)


if __name__ == "__main__":
    main()
