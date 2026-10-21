#!/usr/bin/env python3
"""Lee las fichas técnicas oficiales de Apple Support (iPhone X al 18 Pro Max) y guarda
capacidades, colores y medidas en datos/specs_apple.json, con la URL de cada ficha.

Es la fuente para el catálogo y para cualquier comparación: no se cargan specs a mano.

Uso:  python3 verificar_specs.py
"""

import html
import json
import re
import sys
import time
from pathlib import Path

import requests

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
INDICE = "https://support.apple.com/en-us/docs/iphone"
SALIDA = Path("datos/specs_apple.json")

# id del catálogo -> nombre exacto en el índice de Apple Support
MODELOS = {
    "iphone-x": "iPhone X", "iphone-xr": "iPhone XR", "iphone-xs": "iPhone XS", "iphone-xs-max": "iPhone XS Max",
    "iphone-11": "iPhone 11", "iphone-11-pro": "iPhone 11 Pro", "iphone-11-pro-max": "iPhone 11 Pro Max",
    "iphone-se-2": "iPhone SE (2nd generation)",
    "iphone-12-mini": "iPhone 12 mini", "iphone-12": "iPhone 12", "iphone-12-pro": "iPhone 12 Pro",
    "iphone-12-pro-max": "iPhone 12 Pro Max",
    "iphone-13-mini": "iPhone 13 mini", "iphone-13": "iPhone 13", "iphone-13-pro": "iPhone 13 Pro",
    "iphone-13-pro-max": "iPhone 13 Pro Max", "iphone-se-3": "iPhone SE (3rd generation)",
    "iphone-14": "iPhone 14", "iphone-14-plus": "iPhone 14 Plus", "iphone-14-pro": "iPhone 14 Pro",
    "iphone-14-pro-max": "iPhone 14 Pro Max",
    "iphone-15": "iPhone 15", "iphone-15-plus": "iPhone 15 Plus", "iphone-15-pro": "iPhone 15 Pro",
    "iphone-15-pro-max": "iPhone 15 Pro Max",
    "iphone-16": "iPhone 16", "iphone-16-plus": "iPhone 16 Plus", "iphone-16-pro": "iPhone 16 Pro",
    "iphone-16-pro-max": "iPhone 16 Pro Max", "iphone-16e": "iPhone 16e",
    "iphone-17": "iPhone 17", "iphone-air": "iPhone Air", "iphone-17-pro": "iPhone 17 Pro",
    "iphone-17-pro-max": "iPhone 17 Pro Max", "iphone-17e": "iPhone 17e",
    "iphone-18-pro": "iPhone 18 Pro", "iphone-18-pro-max": "iPhone 18 Pro Max",
}


def texto_plano(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def seccion(t, titulo, siguientes):
    i = t.find(titulo)
    if i < 0:
        return ""
    fin = min([j for j in (t.find(x, i + len(titulo)) for x in siguientes) if j > 0] or [i + 600])
    return t[i + len(titulo):fin]


def main():
    s = requests.Session()
    s.headers["User-Agent"] = UA
    indice = s.get(INDICE, timeout=60).text
    enlaces = {}
    for href, nombre in re.findall(r'<a[^>]+href="([^"]+/docs/iphone/\d+)"[^>]*>\s*(?:<[^>]+>\s*)*([^<]+)<', indice):
        enlaces.setdefault(" ".join(nombre.split()), href)

    datos = {}
    for mid, nombre in MODELOS.items():
        url = enlaces.get(nombre)
        if not url:
            print(f"  {mid}: no está en el índice de Apple Support")
            continue
        # la página del índice es de documentos; la ficha técnica está enlazada en "Tech Specs"
        docs = s.get(url, timeout=60).text
        ficha = re.search(r'docs-product-documentation-techSpecs">\s*<a href="([^"]+)"', docs)
        if not ficha:
            print(f"  {mid}: sin enlace a la ficha técnica en {url}")
            continue
        url = ficha.group(1)
        t = texto_plano(s.get(url, timeout=60).text)
        cap = seccion(t, "Capacity", ["Size and Weight", "Weight", "Display", "Chip"])
        capacidades = list(dict.fromkeys(re.findall(r"\b(\d+\s?(?:GB|TB))\b", cap)))
        # en las fichas de Pro / Pro Max compartidas, Apple separa por modelo; se toma el bloque de este
        if "Pro Max" in cap and "Pro Max" not in nombre:
            capacidades = list(dict.fromkeys(re.findall(r"\b(\d+\s?(?:GB|TB))\b", cap.split("Pro Max")[0])))
        elif "Pro Max" in nombre and "Pro Max" in cap:
            capacidades = list(dict.fromkeys(re.findall(r"\b(\d+\s?(?:GB|TB))\b", cap.split("Pro Max", 1)[1])))
        colores = seccion(t, "Finish", ["Capacity", "Size and Weight"]) or seccion(t, "Color", ["Capacity", "Size"])
        medidas = re.findall(r"(Width|Height|Depth): [^()]*\(([\d.]+) mm\)", t)
        datos[mid] = {
            "nombre": nombre, "fuente": url,
            "capacidades": [c.replace(" ", "") for c in capacidades],
            "colores_texto": colores.strip()[:300],
            "medidas_mm": {k.lower(): float(v) for k, v in medidas[:3]},
        }
        print(f"  {nombre:28} {', '.join(datos[mid]['capacidades']):30} {colores.strip()[:70]}")
        time.sleep(0.5)

    SALIDA.parent.mkdir(exist_ok=True)
    SALIDA.write_text(json.dumps(datos, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(datos)} modelos -> {SALIDA}")


if __name__ == "__main__":
    sys.exit(main())
