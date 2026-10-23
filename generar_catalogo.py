#!/usr/bin/env python3
"""Genera los datos del catálogo web a partir de fuentes verificadas.

    catalogo/modelos.js   modelos (iPhone X al 18 Pro Max), familia, capacidades y colores oficiales
                          (fichas de Apple Support en datos/specs_apple.json), nombres de color en
                          castellano y el tono de cada muestra tomado de la foto real del equipo.
    catalogo/stock.csv    stock de EJEMPLO para armar el esqueleto: una unidad por modelo y capacidad,
                          sin precio, marcada demo=si. Se reemplaza por el stock real (planilla).

Uso:
    python3 verificar_specs.py && python3 generar_catalogo.py
    python3 generar_catalogo.py --sin-stock     # regenera modelos.js y no toca stock.csv
"""

import argparse
import csv
import importlib.util
import json
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parent
SPECS = RAIZ / "datos/specs_apple.json"
IMG = RAIZ / "catalogo/img"
SALIDA = RAIZ / "catalogo"

# nombres oficiales en castellano (Apple Latinoamérica)
COLOR_ES = {
    "Space Gray": "Gris espacial", "Silver": "Plata", "Gold": "Oro", "Black": "Negro", "White": "Blanco",
    "Blue": "Azul", "Yellow": "Amarillo", "Coral": "Coral", "(PRODUCT)RED": "(PRODUCT)RED", "Green": "Verde",
    "Purple": "Morado", "Midnight Green": "Verde noche", "Graphite": "Grafito", "Pacific Blue": "Azul pacífico",
    "Pink": "Rosa", "Midnight": "Medianoche", "Starlight": "Blanco estelar", "Sierra Blue": "Azul sierra",
    "Alpine Green": "Verde alpino", "Space Black": "Negro espacial", "Deep Purple": "Morado oscuro",
    "Black Titanium": "Titanio negro", "White Titanium": "Titanio blanco", "Blue Titanium": "Titanio azul",
    "Natural Titanium": "Titanio natural", "Teal": "Verde azulado", "Ultramarine": "Ultramar",
    "Desert Titanium": "Titanio del desierto", "Mist Blue": "Azul niebla", "Sage": "Salvia",
    "Lavender": "Lavanda", "Cloud White": "Blanco nube", "Light Gold": "Dorado claro", "Sky Blue": "Azul cielo",
    "Cosmic Orange": "Naranja cósmico", "Deep Blue": "Azul profundo", "Soft Pink": "Rosa suave",
    "Glacier": "Glaciar", "Burgundy": "Borgoña",
}

# familias en orden (la web muestra primero las más nuevas)
FAMILIAS = [
    ("x", "iPhone X · XS · XR", ["iphone-x", "iphone-xr", "iphone-xs", "iphone-xs-max"]),
    ("11", "iPhone 11", ["iphone-11", "iphone-11-pro", "iphone-11-pro-max"]),
    ("se", "iPhone SE", ["iphone-se-2", "iphone-se-3"]),
    ("12", "iPhone 12", ["iphone-12-mini", "iphone-12", "iphone-12-pro", "iphone-12-pro-max"]),
    ("13", "iPhone 13", ["iphone-13-mini", "iphone-13", "iphone-13-pro", "iphone-13-pro-max"]),
    ("14", "iPhone 14", ["iphone-14", "iphone-14-plus", "iphone-14-pro", "iphone-14-pro-max"]),
    ("15", "iPhone 15", ["iphone-15", "iphone-15-plus", "iphone-15-pro", "iphone-15-pro-max"]),
    ("16", "iPhone 16", ["iphone-16e", "iphone-16", "iphone-16-plus", "iphone-16-pro", "iphone-16-pro-max"]),
    ("17", "iPhone 17 · Air", ["iphone-17e", "iphone-17", "iphone-air", "iphone-17-pro", "iphone-17-pro-max"]),
    ("18", "iPhone 18", ["iphone-18-pro", "iphone-18-pro-max"]),
]
# modelos que hoy se consiguen en caja sellada (el resto, Swap)
SELLADOS = {"iphone-17", "iphone-17e", "iphone-air", "iphone-17-pro", "iphone-17-pro-max",
            "iphone-18-pro", "iphone-18-pro-max", "iphone-16e", "iphone-16"}


def cargar_descargador():
    spec = importlib.util.spec_from_file_location("descargar", RAIZ / "descargar_iphones.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {m["id"]: m for m in mod.MODELOS}


def muestra_color(ruta):
    """Tono promedio del dorso (franja central baja de la mitad izquierda de la foto, lejos de la cámara)."""
    if not ruta.exists():
        return None
    im = Image.open(ruta).convert("RGBA")
    w, h = im.size
    zona = im.crop((int(w * 0.08), int(h * 0.55), int(w * 0.32), int(h * 0.8)))
    a = np.asarray(zona)
    px = a[a[..., 3] > 200][:, :3]
    if not len(px):
        return None
    r, g, b = (int(v) for v in px.mean(axis=0))
    return f"#{r:02x}{g:02x}{b:02x}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-stock", action="store_true")
    a = ap.parse_args()

    specs = json.loads(SPECS.read_text(encoding="utf-8"))
    desc = cargar_descargador()
    modelos, avisos = [], []
    for orden_fam, (fam_id, fam_nombre, ids) in enumerate(FAMILIAS):
        for orden, mid in enumerate(ids):
            sp, d = specs.get(mid), desc.get(mid)
            if not sp or not d:
                avisos.append(f"{mid}: falta en specs o en descargar_iphones.py")
                continue
            colores = []
            for slug, nombre_en in d["colores"].items():
                clave = nombre_en.replace("(PRODUCT)RED", "(PRODUCT) RED")
                if clave.split(" ")[0] not in sp["colores_texto"] and nombre_en not in sp["colores_texto"]:
                    avisos.append(f"{mid}: el color {nombre_en} no figura en la ficha de Apple")
                img = IMG / f"{mid}_{slug}.webp"
                colores.append({
                    "id": slug, "nombre": COLOR_ES.get(nombre_en, nombre_en),
                    "muestra": muestra_color(img) or "#8E8E96",
                    "img": f"img/{img.name}" if img.exists() else "",
                })
            modelos.append({
                "id": mid, "nombre": sp["nombre"].replace(" (2nd generation)", " (2.ª gen.)").replace(" (3rd generation)", " (3.ª gen.)"),
                "familia": fam_id, "familiaNombre": fam_nombre, "anio": d["anio"],
                "orden": orden_fam * 10 + orden, "capacidades": sp["capacidades"], "colores": colores,
                "fuente": sp["fuente"],
            })

    js = ("// Generado por generar_catalogo.py a partir de las fichas oficiales de Apple. No editar a mano.\n"
          "window.MODELOS_CATALOGO = " + json.dumps(modelos, ensure_ascii=False, indent=1) + ";\n")
    (SALIDA / "modelos.js").write_text(js, encoding="utf-8")
    print(f"{len(modelos)} modelos -> catalogo/modelos.js")

    if not a.sin_stock:
        rnd = random.Random(7)
        estados = ["Impecable", "Muy bueno", "Bueno"]
        filas = []
        for m in modelos:
            for i, cap in enumerate(m["capacidades"]):
                color = m["colores"][i % len(m["colores"])]
                sellado = m["id"] in SELLADOS and i == 0
                filas.append({
                    "id": f"{m['id']}-{cap.lower()}",
                    "modelo": m["id"], "capacidad": cap, "color": color["id"],
                    "condicion": "sellado" if sellado else "swap",
                    "bateria": "" if sellado else str(rnd.randint(78, 100)),
                    "estado": "" if sellado else rnd.choice(estados),
                    "precio": "", "disponible": rnd.choice(["si", "si", "si", "reservado"]),
                    "notas": "", "demo": "si",
                })
        with open(SALIDA / "stock.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(filas)
        # copia embebida para poder abrir index.html con doble clic (sin servidor)
        (SALIDA / "stock-demo.js").write_text(
            "// Copia de stock.csv para abrir el catálogo sin servidor. La genera generar_catalogo.py.\n"
            "window.STOCK_DEMO = " + json.dumps(filas, ensure_ascii=False) + ";\n", encoding="utf-8")
        print(f"{len(filas)} unidades de ejemplo -> catalogo/stock.csv")

    for x in avisos:
        print("  aviso:", x)


if __name__ == "__main__":
    sys.exit(main())
