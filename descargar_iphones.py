#!/usr/bin/env python3
"""Arma la base de fotos de iPhone (X al 18 Pro Max) desde varias fuentes.

Estructura de salida:
    fotos-iphone/<modelo>/producto/    fotos del equipo solo (para plantillas)
    fotos-iphone/<modelo>/ambiente/    equipo en uso, accesorios, fotos de usuarios
    fotos-iphone/<modelo>/referencia/  solo para consulta interna, NO publicar
    fotos-iphone/indice.csv            fuente, autor y licencia de cada archivo
    fotos-iphone/hojas/<modelo>.jpg    hoja de contactos para revisar calidad

Fuentes:
    apple-store  imágenes de la tienda de Apple: un equipo por color, fondo transparente
    newsroom     fotos de prensa de Apple Newsroom (zip con el original)
    wikimedia    Wikimedia Commons (licencias CC / dominio público)
    openverse    buscador de imágenes con licencia libre (Flickr, Wikimedia y otros)
    unsplash     requiere UNSPLASH_ACCESS_KEY
    pexels       requiere PEXELS_API_KEY
    gsmarena     renders de GSMArena: copyright de terceros, solo referencia

Uso:
    python3 descargar_iphones.py                          # todo
    python3 descargar_iphones.py --solo-producto          # solo apple-store + newsroom
    python3 descargar_iphones.py --modelos iphone-13,iphone-17-pro
    python3 descargar_iphones.py --fuentes wikimedia,openverse --max-por-fuente 5

Licencias: las fotos de Apple son de uso editorial (el zip trae un aviso legal);
usarlas en publicidad es un riesgo que el negocio decidió asumir. Las de GSMArena
quedan en referencia/ y no se usan en piezas publicadas.
"""

import argparse
import concurrent.futures as cf
import csv
import io
import json
import os
import re
import sys
import time
import zipfile
from html import unescape
from pathlib import Path
from urllib.parse import quote, urljoin

import requests

try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
except ImportError:  # Pillow es opcional: sin él no hay medidas ni hojas de contacto
    Image = None

UA_NAVEGADOR = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
UA_BOT = "TechCoFotos/1.0 (fotos de catalogo; contacto: repo francoperis/iphone)"
STORE = "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/"
NEWSROOM = "https://www.apple.com/newsroom/"
LADO_MINIMO = 1500  # px del lado mayor para aceptar fotos de fuentes libres

# ---------------------------------------------------------------------------
# Modelos: colores oficiales y artículos de Newsroom.
# "colores": slug de color -> nombre oficial (en inglés, como lo publica Apple).
# "store": plantillas de nombre de imagen en la tienda ({c} = slug de color).
#          Si ninguna existe, se prueban patrones genéricos (ver candidatos_store).
# "alias_color": variantes del slug que usa la tienda para algunos modelos.
# ---------------------------------------------------------------------------
MODELOS = [
    {"id": "iphone-x", "nombre": "iPhone X", "anio": 2017,
     "colores": {"silver": "Silver", "spacegray": "Space Gray"},
     "alias_color": {"spacegray": "gray"},
     "store": ["iphone-x-{c}-select-2017"],
     "newsroom": ["2017/09/the-future-is-here-iphone-x"]},
    {"id": "iphone-xr", "nombre": "iPhone XR", "anio": 2018,
     "colores": {"black": "Black", "white": "White", "blue": "Blue", "yellow": "Yellow",
                 "coral": "Coral", "red": "(PRODUCT)RED"},
     "store": ["iphone-xr-{c}-select-201809"],
     "newsroom": ["2018/09/apple-introduces-iphone-xr"]},
    {"id": "iphone-xs", "nombre": "iPhone XS", "anio": 2018,
     "colores": {"silver": "Silver", "spacegray": "Space Gray", "gold": "Gold"},
     "store": ["iphone-xs-{c}-select-2018"],
     "newsroom": ["2018/09/iphone-xs-and-iphone-xs-max-bring-the-best-and-biggest-displays-to-iphone"]},
    {"id": "iphone-xs-max", "nombre": "iPhone XS Max", "anio": 2018,
     "colores": {"silver": "Silver", "spacegray": "Space Gray", "gold": "Gold"},
     "store": ["iphone-xs-max-{c}-select-2018"],
     "newsroom": ["2018/09/iphone-xs-and-iphone-xs-max-bring-the-best-and-biggest-displays-to-iphone"]},
    {"id": "iphone-11", "nombre": "iPhone 11", "anio": 2019,
     "colores": {"black": "Black", "white": "White", "green": "Green", "yellow": "Yellow",
                 "purple": "Purple", "red": "(PRODUCT)RED"},
     "store": ["iphone11-{c}-select-2019"],
     "newsroom": ["2019/09/apple-introduces-dual-camera-iphone-11"]},
    {"id": "iphone-11-pro", "nombre": "iPhone 11 Pro", "anio": 2019,
     "colores": {"midnightgreen": "Midnight Green", "spacegray": "Space Gray", "silver": "Silver", "gold": "Gold"},
     "alias_color": {"midnightgreen": "midnight-green", "spacegray": "space-gray"},
     "store": ["iphone-11-pro-{c}-select-2019"],
     "newsroom": ["2019/09/iphone-11-pro-and-iphone-11-pro-max-the-most-powerful-and-advanced-smartphones"]},
    {"id": "iphone-11-pro-max", "nombre": "iPhone 11 Pro Max", "anio": 2019,
     "colores": {"midnightgreen": "Midnight Green", "spacegray": "Space Gray", "silver": "Silver", "gold": "Gold"},
     "alias_color": {"midnightgreen": "midnight-green", "spacegray": "space-gray"},
     "store": ["iphone-11-pro-max-{c}-select-2019"],
     "newsroom": ["2019/09/iphone-11-pro-and-iphone-11-pro-max-the-most-powerful-and-advanced-smartphones"]},
    {"id": "iphone-se-2", "nombre": "iPhone SE (2.ª gen.)", "anio": 2020,
     "colores": {"black": "Black", "white": "White", "red": "(PRODUCT)RED"},
     "store": ["iphone-se-{c}-select-2020"],
     "newsroom": ["2020/04/iphone-se-a-powerful-new-smartphone-in-a-popular-design"]},
    {"id": "iphone-12-mini", "nombre": "iPhone 12 mini", "anio": 2020,
     "colores": {"black": "Black", "white": "White", "red": "(PRODUCT)RED", "green": "Green",
                 "blue": "Blue", "purple": "Purple"},
     "store": ["iphone-12-mini-{c}-select-2020", "iphone-12-mini-{c}-select-2021"],
     "newsroom": ["2020/10/apple-announces-iphone-12-and-iphone-12-mini-a-new-era-for-iphone-with-5g"]},
    {"id": "iphone-12", "nombre": "iPhone 12", "anio": 2020,
     "colores": {"black": "Black", "white": "White", "red": "(PRODUCT)RED", "green": "Green",
                 "blue": "Blue", "purple": "Purple"},
     "store": ["iphone-12-{c}-select-2020", "iphone-12-{c}-select-2021", "refurb-iphone-12-{c}-2020",
               "refurb-iphone-12-{c}-2021"],
     "newsroom": ["2020/10/apple-announces-iphone-12-and-iphone-12-mini-a-new-era-for-iphone-with-5g"]},
    {"id": "iphone-12-pro", "nombre": "iPhone 12 Pro", "anio": 2020,
     "colores": {"silver": "Silver", "graphite": "Graphite", "gold": "Gold", "pacificblue": "Pacific Blue"},
     "alias_color": {"pacificblue": "blue"},
     "store": ["refurb-iphone-12-pro-{c}-2020"],
     "newsroom": ["2020/10/apple-introduces-iphone-12-pro-and-iphone-12-pro-max-with-5g"]},
    {"id": "iphone-12-pro-max", "nombre": "iPhone 12 Pro Max", "anio": 2020,
     "colores": {"silver": "Silver", "graphite": "Graphite", "gold": "Gold", "pacificblue": "Pacific Blue"},
     "alias_color": {"pacificblue": "blue"},
     "store": ["refurb-iphone-12-pro-max-{c}-2020"],
     "newsroom": ["2020/10/apple-introduces-iphone-12-pro-and-iphone-12-pro-max-with-5g"]},
    {"id": "iphone-13-mini", "nombre": "iPhone 13 mini", "anio": 2021,
     "colores": {"pink": "Pink", "blue": "Blue", "midnight": "Midnight", "starlight": "Starlight",
                 "red": "(PRODUCT)RED", "green": "Green"},
     "alias_color": {"red": "product-red"},
     "store": ["iphone-13-mini-{c}-select-2021", "iphone-13-mini-{c}-select"],
     "newsroom": ["2021/09/apple-introduces-iphone-13-and-iphone-13-mini"]},
    {"id": "iphone-13", "nombre": "iPhone 13", "anio": 2021,
     "colores": {"pink": "Pink", "blue": "Blue", "midnight": "Midnight", "starlight": "Starlight",
                 "red": "(PRODUCT)RED", "green": "Green"},
     "alias_color": {"red": "product-red"},
     "store": ["iphone-13-finish-select-202207-6-1inch-{c}", "iphone-13-{c}-select-2021", "iphone-13-{c}-select", "refurb-iphone-13-{c}-2023"],
     "newsroom": ["2021/09/apple-introduces-iphone-13-and-iphone-13-mini"]},
    {"id": "iphone-13-pro", "nombre": "iPhone 13 Pro", "anio": 2021,
     "colores": {"graphite": "Graphite", "gold": "Gold", "silver": "Silver", "sierrablue": "Sierra Blue",
                 "alpinegreen": "Alpine Green"},
     "alias_color": {"sierrablue": "blue", "alpinegreen": "green"},
     "store": ["iphone-13-pro-{c}-select"],
     "newsroom": ["2021/09/apple-unveils-iphone-13-pro-and-iphone-13-pro-max-more-pro-than-ever-before"]},
    {"id": "iphone-13-pro-max", "nombre": "iPhone 13 Pro Max", "anio": 2021,
     "colores": {"graphite": "Graphite", "gold": "Gold", "silver": "Silver", "sierrablue": "Sierra Blue",
                 "alpinegreen": "Alpine Green"},
     "alias_color": {"sierrablue": "blue", "alpinegreen": "green"},
     "store": ["iphone-13-pro-max-{c}-select"],
     "newsroom": ["2021/09/apple-unveils-iphone-13-pro-and-iphone-13-pro-max-more-pro-than-ever-before"]},
    {"id": "iphone-se-3", "nombre": "iPhone SE (3.ª gen.)", "anio": 2022,
     "colores": {"midnight": "Midnight", "starlight": "Starlight", "red": "(PRODUCT)RED"},
     "store": ["iphone-se-{c}-select-202203"],
     "newsroom": ["2022/03/apple-announces-the-new-iphone-se-a-powerful-smartphone-in-an-iconic-design"]},
    {"id": "iphone-14", "nombre": "iPhone 14", "anio": 2022,
     "colores": {"midnight": "Midnight", "purple": "Purple", "starlight": "Starlight", "red": "(PRODUCT)RED",
                 "blue": "Blue", "yellow": "Yellow"},
     "store": ["iphone-14-finish-select-202209-6-1inch-{c}", "iphone-14-{c}-select-202209"],
     "newsroom": ["2022/09/apple-introduces-iphone-14-and-iphone-14-plus"]},
    {"id": "iphone-14-plus", "nombre": "iPhone 14 Plus", "anio": 2022,
     "colores": {"midnight": "Midnight", "purple": "Purple", "starlight": "Starlight", "red": "(PRODUCT)RED",
                 "blue": "Blue", "yellow": "Yellow"},
     "store": ["iphone-14-finish-select-202209-6-7inch-{c}", "iphone-14-plus-{c}-select-202209"],
     "newsroom": ["2022/09/apple-introduces-iphone-14-and-iphone-14-plus"]},
    {"id": "iphone-14-pro", "nombre": "iPhone 14 Pro", "anio": 2022,
     "colores": {"spaceblack": "Space Black", "silver": "Silver", "gold": "Gold", "deeppurple": "Deep Purple"},
     "store": ["iphone-14-pro-finish-select-202209-6-1inch-{c}", "iphone-14-pro-{c}-select"],
     "newsroom": ["2022/09/apple-debuts-iphone-14-pro-and-iphone-14-pro-max"]},
    {"id": "iphone-14-pro-max", "nombre": "iPhone 14 Pro Max", "anio": 2022,
     "colores": {"spaceblack": "Space Black", "silver": "Silver", "gold": "Gold", "deeppurple": "Deep Purple"},
     "store": ["iphone-14-pro-finish-select-202209-6-7inch-{c}", "iphone-14-pro-max-{c}-select"],
     "newsroom": ["2022/09/apple-debuts-iphone-14-pro-and-iphone-14-pro-max"]},
    {"id": "iphone-15", "nombre": "iPhone 15", "anio": 2023,
     "colores": {"black": "Black", "blue": "Blue", "green": "Green", "yellow": "Yellow", "pink": "Pink"},
     "store": ["iphone-15-finish-select-202309-6-1inch-{c}", "iphone-15-{c}-select-202309"],
     "newsroom": ["2023/09/apple-debuts-iphone-15-and-iphone-15-plus"]},
    {"id": "iphone-15-plus", "nombre": "iPhone 15 Plus", "anio": 2023,
     "colores": {"black": "Black", "blue": "Blue", "green": "Green", "yellow": "Yellow", "pink": "Pink"},
     "store": ["iphone-15-finish-select-202309-6-7inch-{c}", "iphone-15-plus-{c}-select-202309"],
     "newsroom": ["2023/09/apple-debuts-iphone-15-and-iphone-15-plus"]},
    {"id": "iphone-15-pro", "nombre": "iPhone 15 Pro", "anio": 2023,
     "colores": {"naturaltitanium": "Natural Titanium", "bluetitanium": "Blue Titanium",
                 "whitetitanium": "White Titanium", "blacktitanium": "Black Titanium"},
     "store": ["iphone-15-pro-finish-select-202309-6-1inch-{c}"],
     "newsroom": ["2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max"]},
    {"id": "iphone-15-pro-max", "nombre": "iPhone 15 Pro Max", "anio": 2023,
     "colores": {"naturaltitanium": "Natural Titanium", "bluetitanium": "Blue Titanium",
                 "whitetitanium": "White Titanium", "blacktitanium": "Black Titanium"},
     "store": ["iphone-15-pro-finish-select-202309-6-7inch-{c}"],
     "newsroom": ["2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max"]},
    {"id": "iphone-16", "nombre": "iPhone 16", "anio": 2024,
     "colores": {"black": "Black", "white": "White", "pink": "Pink", "teal": "Teal", "ultramarine": "Ultramarine"},
     "store": ["iphone-16-finish-select-202409-6-1inch-{c}", "iphone-16-{c}-select-202409"],
     "newsroom": ["2024/09/apple-introduces-iphone-16-and-iphone-16-plus"]},
    {"id": "iphone-16-plus", "nombre": "iPhone 16 Plus", "anio": 2024,
     "colores": {"black": "Black", "white": "White", "pink": "Pink", "teal": "Teal", "ultramarine": "Ultramarine"},
     "store": ["iphone-16-finish-select-202409-6-7inch-{c}", "iphone-16-plus-{c}-select-202409"],
     "newsroom": ["2024/09/apple-introduces-iphone-16-and-iphone-16-plus"]},
    {"id": "iphone-16-pro", "nombre": "iPhone 16 Pro", "anio": 2024,
     "colores": {"blacktitanium": "Black Titanium", "whitetitanium": "White Titanium",
                 "naturaltitanium": "Natural Titanium", "deserttitanium": "Desert Titanium"},
     "store": ["iphone-16-pro-finish-select-202409-6-3inch-{c}"],
     "newsroom": ["2024/09/apple-debuts-iphone-16-pro-and-iphone-16-pro-max"]},
    {"id": "iphone-16-pro-max", "nombre": "iPhone 16 Pro Max", "anio": 2024,
     "colores": {"blacktitanium": "Black Titanium", "whitetitanium": "White Titanium",
                 "naturaltitanium": "Natural Titanium", "deserttitanium": "Desert Titanium"},
     "store": ["iphone-16-pro-finish-select-202409-6-9inch-{c}"],
     "newsroom": ["2024/09/apple-debuts-iphone-16-pro-and-iphone-16-pro-max"]},
    {"id": "iphone-16e", "nombre": "iPhone 16e", "anio": 2025,
     "colores": {"black": "Black", "white": "White"},
     "store": ["iphone-16e-finish-select-202502-{c}", "iphone-16e-{c}-select-202502"],
     "newsroom": ["2025/02/apple-debuts-iphone-16e-a-powerful-new-member-of-the-iphone-16-family"]},
    {"id": "iphone-17", "nombre": "iPhone 17", "anio": 2025,
     "colores": {"black": "Black", "white": "White", "mistblue": "Mist Blue", "lavender": "Lavender", "sage": "Sage"},
     "store": ["iphone-17-finish-select-{c}-202509"],
     "newsroom": ["2025/09/apple-debuts-iphone-17"]},
    {"id": "iphone-air", "nombre": "iPhone Air", "anio": 2025,
     "colores": {"spaceblack": "Space Black", "cloudwhite": "Cloud White", "lightgold": "Light Gold", "skyblue": "Sky Blue"},
     "store": ["iphone-air-finish-select-{c}-202509"],
     "newsroom": ["2025/09/introducing-iphone-air-a-powerful-new-iphone-with-a-breakthrough-design"]},
    {"id": "iphone-17-pro", "nombre": "iPhone 17 Pro", "anio": 2025,
     "colores": {"silver": "Silver", "cosmicorange": "Cosmic Orange", "deepblue": "Deep Blue"},
     "store": ["iphone-17-pro-finish-select-202509-6-3inch-{c}"],
     "newsroom": ["2025/09/apple-unveils-iphone-17-pro-and-iphone-17-pro-max"]},
    {"id": "iphone-17-pro-max", "nombre": "iPhone 17 Pro Max", "anio": 2025,
     "colores": {"silver": "Silver", "cosmicorange": "Cosmic Orange", "deepblue": "Deep Blue"},
     "store": ["iphone-17-pro-finish-select-202509-6-9inch-{c}"],
     "newsroom": ["2025/09/apple-unveils-iphone-17-pro-and-iphone-17-pro-max"]},
    {"id": "iphone-17e", "nombre": "iPhone 17e", "anio": 2026,
     "colores": {"black": "Black", "white": "White", "softpink": "Soft Pink"},
     "store": ["iphone-17e-finish-select-{c}-202603"],
     "newsroom": ["2026/03/apple-introduces-iphone-17e"]},
    {"id": "iphone-18-pro", "nombre": "iPhone 18 Pro", "anio": 2026,
     "colores": {"black": "Black", "silver": "Silver", "glacier": "Glacier", "burgundy": "Burgundy"},
     "store": ["iphone-18-pro-finish-select-{c}-202609"],
     "newsroom": ["2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max"]},
    {"id": "iphone-18-pro-max", "nombre": "iPhone 18 Pro Max", "anio": 2026,
     "colores": {"black": "Black", "silver": "Silver", "glacier": "Glacier", "burgundy": "Burgundy"},
     "store": ["iphone-18-pro-max-finish-select-{c}-202609"],
     "newsroom": ["2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max"]},
]

# Fotos de Newsroom que no muestran el equipo (capturas de apps, fotos sacadas CON el iPhone, etc.)
NEWSROOM_DESCARTAR = re.compile(
    r"photograph|photo-mode|night-?mode|portrait|smart-hdr|lowlight|low-light|ultrawide|telephoto-camera|"
    r"cinematic|macro|48mp|fusion|ethereal|stark|vibrant|bright-style|genmoji|writing-tools|siri|"
    r"intelligence|chatgpt|darkroom|maps|facetime|notification|live-text|swing|contact-poster|namedrop|"
    r"crash|satellite|sos|roadside|live-sticker|ios-?\d|lock-screen|screen|app-|game|gaming|messages|"
    r"wallet-app|health|fitness|camera-app|visual-intelligence|music|keynote|tim-cook|store|exec|"
    r"carbon|environment|recycl|packaging|mapillary",
    re.I)
NEWSROOM_PRODUCTO = re.compile(
    r"hero|lineup|colou?rs?|finish|design|back|front|camera-system|camera-close|close-up|titanium|"
    r"family|geo|3-?up|cosmic|orange|blue|silver|black|white|pink|green|yellow|purple|red|gold|"
    r"glacier|burgundy|sage|lavender|teal|ultramarine|desert|natural|graphite|sierra|midnight|starlight|"
    r"aluminum|forged|unibody|ceramic|action-button|camera-control",
    re.I)

# Muestran el equipo pero con accesorios, personas o en uso: van a ambiente/
NEWSROOM_AMBIENTE = re.compile(
    r"case|wallet|strap|magsafe|usb|cable|charger|shoot|video|hand|lifestyle|accessor|person|people|"
    r"woman|man-|kid|desk|table|outdoor|vapor|internal|architecture",
    re.I)

LICENCIAS_LIBRES = {"cc0", "pd", "public domain", "cc by", "cc by-sa", "cc-by", "cc-by-sa"}
CAMPOS_INDICE = ["modelo", "color", "tipo", "fuente", "archivo", "ancho", "alto", "fondo_transparente",
                 "uso", "licencia", "autor", "url", "pagina", "notas"]


class Descargador:
    def __init__(self, salida, max_por_fuente, pausa_bot=1.0):
        self.salida = Path(salida)
        self.max_por_fuente = max_por_fuente
        self.pausa_bot = pausa_bot
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA_NAVEGADOR
        self.indice_path = self.salida / "indice.csv"
        self.cache_path = self.salida / ".cache-fuentes.json"
        self.indice = {}
        self.cache = {}
        self._ultimo_bot = 0.0
        if self.indice_path.exists():
            with open(self.indice_path, newline="", encoding="utf-8") as f:
                for fila in csv.DictReader(f):
                    self.indice[fila["archivo"]] = fila
        if self.cache_path.exists():
            self.cache = json.loads(self.cache_path.read_text(encoding="utf-8"))

    # ----------------------------------------------------------------- utilidades
    def get(self, url, bot=False, intentos=4, **kw):
        """GET con reintentos. bot=True respeta límites de APIs públicas (Wikimedia, Openverse)."""
        headers = kw.pop("headers", {})
        if bot:
            headers.setdefault("User-Agent", UA_BOT)
        for i in range(intentos):
            if bot:
                espera = self.pausa_bot - (time.time() - self._ultimo_bot)
                if espera > 0:
                    time.sleep(espera)
                self._ultimo_bot = time.time()
            try:
                r = self.s.get(url, headers=headers, timeout=60, **kw)
            except requests.RequestException as e:
                if i == intentos - 1:
                    raise
                time.sleep(2 ** (i + 1))
                continue
            if r.status_code in (429, 502, 503, 504) and i < intentos - 1:
                pedido = r.headers.get("Retry-After", "")
                time.sleep(min(int(pedido) if pedido.isdigit() else 2 ** (i + 2), 30))
                continue
            return r
        return r

    def existe(self, url):
        try:
            return self.s.get(url, timeout=30).status_code == 200
        except requests.RequestException:
            return False

    def guardar(self, datos, destino, fila):
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(datos)
        fila["archivo"] = destino.relative_to(self.salida).as_posix()
        fila.setdefault("ancho", "")
        fila.setdefault("alto", "")
        fila.setdefault("fondo_transparente", "")
        if Image:
            try:
                im = Image.open(io.BytesIO(datos))
                fila["ancho"], fila["alto"] = im.size
                if im.mode in ("RGBA", "LA", "P"):
                    a = im.convert("RGBA").getchannel("A")
                    fila["fondo_transparente"] = "si" if a.getextrema()[0] < 255 else "no"
                else:
                    fila["fondo_transparente"] = "no"
            except Exception:
                fila["notas"] = (fila.get("notas", "") + " no se pudo leer la imagen").strip()
        self.indice[fila["archivo"]] = {k: fila.get(k, "") for k in CAMPOS_INDICE}

    def ya_esta(self, url, modelo):
        return any(f["url"] == url and f["modelo"] == modelo for f in self.indice.values())

    def escribir_indice(self):
        self.salida.mkdir(parents=True, exist_ok=True)
        filas = sorted(self.indice.values(), key=lambda f: (f["modelo"], f["tipo"], f["fuente"], f["archivo"]))
        with open(self.indice_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS_INDICE)
            w.writeheader()
            w.writerows(filas)
        self.cache_path.write_text(json.dumps(self.cache, indent=1, ensure_ascii=False), encoding="utf-8")

    # ---------------------------------------------------------------- apple store
    def candidatos_store(self, m, c):
        """Nombres posibles de la imagen en la tienda, de más a menos probable."""
        colores = [c] + ([m["alias_color"][c]] if c in m.get("alias_color", {}) else [])
        base = m["id"]
        y = m["anio"]
        vistos = []
        for col in colores:
            for t in m.get("store", []):
                vistos.append(t.format(c=col))
        for col in colores:
            for ym in (f"{y}09", f"{y}10", str(y), f"{y + 1}03", f"{y}03", f"{y}02"):
                vistos += [f"{base}-finish-select-{col}-{ym}", f"{base}-{col}-select-{ym}"]
            vistos.append(f"{base}-{col}-select")
            # tienda de reacondicionados: suele tener el dorso completo, sin la pantalla encima
            for ym in (f"{y + 1}12", f"{y + 2}", f"{y + 2}09", f"{y + 2}12", f"{y + 3}"):
                vistos.append(f"refurb-{base}-{col}-{ym}")
        return list(dict.fromkeys(vistos))

    def apple_store(self, m):
        n = 0
        for c, nombre_color in m["colores"].items():
            clave = f"store:{m['id']}:{c}"
            if clave not in self.cache:
                cands = self.candidatos_store(m, c)
                with cf.ThreadPoolExecutor(12) as ex:
                    ok = list(ex.map(lambda s: self.existe(f"{STORE}{s}?wid=64&fmt=jpeg"), cands))
                self.cache[clave] = [s for s, o in zip(cands, ok) if o]
            slugs = self.cache[clave]
            if not slugs:
                print(f"    tienda: sin imagen para {nombre_color}")
                continue
            for slug in slugs:
                url = f"{STORE}{slug}?scl=1&fmt=png-alpha"  # scl=1 = resolución original, sin agrandar
                destino = self.salida / m["id"] / "producto" / f"apple-store_{c}_{slug}.png"
                if destino.exists() and destino.relative_to(self.salida).as_posix() in self.indice:
                    continue
                if destino.exists():  # bajada en una corrida que se cortó: solo falta indexarla
                    datos = destino.read_bytes()
                else:
                    r = self.get(url)
                    if r.status_code != 200:
                        continue
                    datos = r.content
                self.guardar(datos, destino, {
                    "modelo": m["id"], "color": nombre_color, "tipo": "producto", "fuente": "apple-store",
                    "uso": "riesgo (Apple, sin licencia comercial)", "licencia": "© Apple", "autor": "Apple",
                    "url": url, "pagina": "https://www.apple.com/shop/buy-iphone"})
                n += 1
        return n

    # ------------------------------------------------------------------- newsroom
    def newsroom(self, m, incluir_ambiente=True):
        n = 0
        for art in m.get("newsroom", []):
            pagina = f"{NEWSROOM}{art}/"
            clave = f"newsroom:{art}"
            if clave not in self.cache:
                r = self.get(pagina)
                if r.status_code != 200:
                    print(f"    newsroom: {r.status_code} en {pagina}")
                    continue
                zips = re.findall(r'/newsroom/images/[^"\s]+?\.zip', r.text)
                self.cache[clave] = [z for z in dict.fromkeys(zips) if "/Images-of-" not in z
                                     and "/images-of-" not in z]
            for z in self.cache[clave]:
                nombre = z.rsplit("/", 1)[1][:-4]
                if NEWSROOM_DESCARTAR.search(nombre):
                    continue
                es_producto = NEWSROOM_PRODUCTO.search(nombre) and not NEWSROOM_AMBIENTE.search(nombre)
                tipo = "producto" if es_producto else "ambiente"
                if tipo == "ambiente" and not incluir_ambiente:
                    continue
                url = urljoin("https://www.apple.com", z)
                if self.ya_esta(url, m["id"]):
                    continue
                r = self.get(url)
                if r.status_code != 200:
                    continue
                try:
                    zf = zipfile.ZipFile(io.BytesIO(r.content))
                except zipfile.BadZipFile:
                    continue
                for info in zf.infolist():
                    if not re.search(r"\.(jpe?g|png|tiff?)$", info.filename, re.I) or "__MACOSX" in info.filename:
                        continue
                    destino = self.salida / m["id"] / tipo / f"newsroom_{Path(info.filename).name}"
                    self.guardar(zf.read(info), destino, {
                        "modelo": m["id"], "color": self.color_en_nombre(nombre, m), "tipo": tipo,
                        "fuente": "apple-newsroom", "uso": "riesgo (Apple, uso editorial)",
                        "licencia": "© Apple — uso editorial, no modificar", "autor": "Apple",
                        "url": url, "pagina": pagina})
                    n += 1
        return n

    @staticmethod
    def color_en_nombre(nombre, m):
        plano = nombre.lower().replace("-", "").replace("_", "")
        for c, nombre_color in m["colores"].items():
            if c in plano:
                return nombre_color
        return ""

    # ---------------------------------------------------------------- coincidencia
    @staticmethod
    def titulo_coincide(texto, m):
        """True si el texto habla de ESTE modelo y no de un hermano (Pro vs Pro Max, 15 vs 15 Pro...)."""
        def normal(x):
            x = re.sub(r"[^a-z0-9]+", " ", x.lower())
            return " " + re.sub(r"\biphone(?=\d|x)", "iphone ", x).strip() + " "
        t = normal(texto)
        nombre = normal(re.sub(r"\(.*?\)", "", m["nombre"]))
        pos = t.find(nombre)
        if pos < 0:
            return False
        siguiente = t[pos + len(nombre):].split(" ", 1)[0]
        return siguiente not in {"pro", "max", "plus", "mini"}

    # ------------------------------------------------------------------ wikimedia
    def wikimedia(self, m):
        nombre = re.sub(r"\s*\(.*?\)", "", m["nombre"])
        api = "https://commons.wikimedia.org/w/api.php"
        params = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
                  "gsrsearch": f'filetype:bitmap intitle:"{nombre}"', "gsrlimit": 50,
                  "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime",
                  "iiextmetadatafilter": "LicenseShortName|Artist|Credit"}
        r = self.get(api, bot=True, params=params)
        if r.status_code != 200 or not r.text.startswith("{"):
            print(f"    wikimedia: respuesta {r.status_code}")
            return 0
        paginas = (r.json().get("query") or {}).get("pages", {}).values()
        n = 0
        for p in sorted(paginas, key=lambda p: -p["imageinfo"][0].get("width", 0)):
            if n >= self.max_por_fuente:
                break
            ii = p["imageinfo"][0]
            meta = ii.get("extmetadata", {})
            lic = meta.get("LicenseShortName", {}).get("value", "")
            if not any(lic.lower().startswith(l) for l in LICENCIAS_LIBRES):
                continue
            if max(ii.get("width", 0), ii.get("height", 0)) < LADO_MINIMO:
                continue
            if not self.titulo_coincide(p["title"], m) or re.search(r"screenshot|screen|captura", p["title"], re.I):
                continue
            if self.ya_esta(ii["url"], m["id"]):
                continue
            img = self.get(ii["url"], bot=True)
            if img.status_code != 200:
                continue
            ext = Path(ii["url"]).suffix.lower() or ".jpg"
            destino = self.salida / m["id"] / "ambiente" / f"wikimedia_{p['pageid']}{ext}"
            autor = re.sub(r"<[^>]+>", "", unescape(meta.get("Artist", {}).get("value", ""))).strip()
            self.guardar(img.content, destino, {
                "modelo": m["id"], "color": "", "tipo": "ambiente", "fuente": "wikimedia",
                "uso": "comercial ok citando autor" + (" (compartir igual)" if "sa" in lic.lower() else ""),
                "licencia": lic, "autor": autor[:120], "url": ii["url"],
                "pagina": ii.get("descriptionurl", ""), "notas": p["title"]})
            n += 1
        return n

    # ------------------------------------------------------------------ openverse
    def openverse(self, m):
        nombre = re.sub(r"\s*\(.*?\)", "", m["nombre"])
        r = self.get("https://api.openverse.org/v1/images/", bot=True, params={
            "q": nombre, "license_type": "commercial", "page_size": 40, "mature": "false"})
        if r.status_code == 401:
            print("    openverse: la API ahora pide registrarse (401); se saltea")
            return 0
        if r.status_code != 200 or not r.text.startswith("{"):
            print(f"    openverse: respuesta {r.status_code}")
            return 0
        n = 0
        for it in r.json().get("results", []):
            if n >= self.max_por_fuente:
                break
            if it.get("source") == "wikimedia":  # ya cubierto por la fuente wikimedia
                continue
            if max(it.get("width") or 0, it.get("height") or 0) < LADO_MINIMO:
                continue
            if not self.titulo_coincide(it.get("title") or "", m) or self.ya_esta(it["url"], m["id"]):
                continue
            img = self.get(it["url"], bot=True)
            if img.status_code != 200 or not img.headers.get("content-type", "").startswith("image"):
                continue
            ext = ".png" if "png" in img.headers["content-type"] else ".jpg"
            destino = self.salida / m["id"] / "ambiente" / f"openverse-{it.get('source', 'x')}_{it['id'][:12]}{ext}"
            lic = f"CC {it.get('license', '').upper()} {it.get('license_version') or ''}".strip()
            self.guardar(img.content, destino, {
                "modelo": m["id"], "color": "", "tipo": "ambiente", "fuente": f"openverse/{it.get('source')}",
                "uso": "comercial ok citando autor", "licencia": lic, "autor": (it.get("creator") or "")[:120],
                "url": it["url"], "pagina": it.get("foreign_landing_url", ""), "notas": it.get("title", "")})
            n += 1
        return n

    # ------------------------------------------------------------ unsplash / pexels
    def unsplash(self, m):
        clave = os.environ.get("UNSPLASH_ACCESS_KEY")
        if not clave:
            return self.sin_clave("unsplash", "UNSPLASH_ACCESS_KEY")
        nombre = re.sub(r"\s*\(.*?\)", "", m["nombre"])
        r = self.get("https://api.unsplash.com/search/photos", params={"query": nombre, "per_page": 30},
                     headers={"Authorization": f"Client-ID {clave}", "Accept-Version": "v1"})
        if r.status_code != 200:
            print(f"    unsplash: respuesta {r.status_code}")
            return 0
        n = 0
        for f in r.json().get("results", []):
            if n >= self.max_por_fuente:
                break
            texto = " ".join(filter(None, [f.get("description"), f.get("alt_description")]))
            if not self.titulo_coincide(texto, m):
                continue
            url = f["urls"]["raw"] + "&fm=jpg&q=90&w=4000"
            if self.ya_esta(url, m["id"]):
                continue
            img = self.get(url)
            if img.status_code != 200:
                continue
            self.get(f["links"]["download_location"], headers={"Authorization": f"Client-ID {clave}"})  # requisito de la API
            self.guardar(img.content, self.salida / m["id"] / "ambiente" / f"unsplash_{f['id']}.jpg", {
                "modelo": m["id"], "color": "", "tipo": "ambiente", "fuente": "unsplash",
                "uso": "comercial ok", "licencia": "Unsplash License", "autor": f["user"]["name"],
                "url": url, "pagina": f["links"]["html"], "notas": texto[:120]})
            n += 1
        return n

    def pexels(self, m):
        clave = os.environ.get("PEXELS_API_KEY")
        if not clave:
            return self.sin_clave("pexels", "PEXELS_API_KEY")
        nombre = re.sub(r"\s*\(.*?\)", "", m["nombre"])
        r = self.get("https://api.pexels.com/v1/search", params={"query": nombre, "per_page": 40},
                     headers={"Authorization": clave})
        if r.status_code != 200:
            print(f"    pexels: respuesta {r.status_code}")
            return 0
        n = 0
        for f in r.json().get("photos", []):
            if n >= self.max_por_fuente:
                break
            if not self.titulo_coincide(f.get("alt") or "", m):
                continue
            url = f["src"]["original"]
            if self.ya_esta(url, m["id"]):
                continue
            img = self.get(url)
            if img.status_code != 200:
                continue
            self.guardar(img.content, self.salida / m["id"] / "ambiente" / f"pexels_{f['id']}.jpg", {
                "modelo": m["id"], "color": "", "tipo": "ambiente", "fuente": "pexels",
                "uso": "comercial ok", "licencia": "Pexels License", "autor": f.get("photographer", ""),
                "url": url, "pagina": f.get("url", ""), "notas": (f.get("alt") or "")[:120]})
            n += 1
        return n

    _avisos = set()

    def sin_clave(self, fuente, var):
        if fuente not in self._avisos:
            print(f"    {fuente}: falta la variable {var} (clave gratuita); se saltea")
            self._avisos.add(fuente)
        return 0

    # ------------------------------------------------------------------- gsmarena
    def gsmarena(self, m):
        """Renders oficiales que publica GSMArena. Copyright de terceros: van a referencia/."""
        slug = "apple_" + m["id"].replace("-", "_")
        if m["id"] == "iphone-se-2":
            slug = "apple_iphone_se_(2020)"
        elif m["id"] == "iphone-se-3":
            slug = "apple_iphone_se_(2022)"
        clave = f"gsmarena:{m['id']}"
        if clave not in self.cache:
            r = self.get("https://www.gsmarena.com/results.php3", bot=True,
                         params={"sQuickSearch": "yes", "sName": m["nombre"].replace("(", "").replace(")", "")})
            if "cloudflare" in r.text.lower() and "apple_iphone" not in r.text:
                print("    gsmarena: bloqueado por Cloudflare (no acepta descargas automáticas); se saltea")
                return 0
            ids = re.findall(re.escape(slug) + r"-(\d+)\.php", r.text) if r.status_code == 200 else []
            self.cache[clave] = ids[0] if ids else ""
        if not self.cache[clave]:
            print("    gsmarena: modelo no encontrado")
            return 0
        pag = f"https://www.gsmarena.com/{slug}-pictures-{self.cache[clave]}.php"
        r = self.get(pag, bot=True)
        if r.status_code != 200:
            print(f"    gsmarena: respuesta {r.status_code}")
            return 0
        urls = list(dict.fromkeys(re.findall(r'https://fdn2?\.gsmarena\.com/vv/pics/apple/[^"\']+\.(?:jpg|png)', r.text)))
        n = 0
        for url in urls[: self.max_por_fuente]:
            if self.ya_esta(url, m["id"]):
                continue
            img = self.get(url, bot=True)
            if img.status_code != 200:
                continue
            self.guardar(img.content, self.salida / m["id"] / "referencia" / f"gsmarena_{Path(url).name}", {
                "modelo": m["id"], "color": "", "tipo": "referencia", "fuente": "gsmarena",
                "uso": "NO publicar (solo referencia)", "licencia": "© GSMArena / fabricante", "autor": "",
                "url": url, "pagina": pag})
            n += 1
        return n

    # --------------------------------------------------------------- hojas contacto
    def hoja_contactos(self, m):
        if not Image:
            return
        archivos = sorted((f for f in self.indice.values() if f["modelo"] == m["id"]), key=lambda f: f["archivo"])
        if not archivos:
            return
        lado, pie, cols = 360, 46, 5
        from PIL import ImageDraw
        filas = (len(archivos) + cols - 1) // cols
        hoja = Image.new("RGB", (cols * lado, filas * (lado + pie)), (12, 12, 13))
        d = ImageDraw.Draw(hoja)
        for i, f in enumerate(archivos):
            x, y = (i % cols) * lado, (i // cols) * (lado + pie)
            try:
                im = Image.open(self.salida / f["archivo"]).convert("RGBA")
                im.thumbnail((lado - 10, lado - 10))
                fondo = Image.new("RGB", (lado, lado), (40, 40, 44))
                fondo.paste(im, ((lado - im.width) // 2, (lado - im.height) // 2), im)
                hoja.paste(fondo, (x, y))
            except Exception:
                pass
            uso = "REF" if f["tipo"] == "referencia" else ("LIBRE" if "ok" in f["uso"] else "APPLE")
            d.text((x + 6, y + lado + 4), f"{f['fuente']} · {f['ancho']}x{f['alto']} · {uso}", fill=(212, 255, 58))
            d.text((x + 6, y + lado + 22), Path(f["archivo"]).name[:52], fill=(154, 154, 162))
        destino = self.salida / "hojas" / f"{m['id']}.jpg"
        destino.parent.mkdir(parents=True, exist_ok=True)
        hoja.save(destino, quality=82)


FUENTES = ["apple-store", "newsroom", "wikimedia", "openverse", "unsplash", "pexels", "gsmarena"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", default="fotos-iphone")
    ap.add_argument("--modelos", help="ids separados por coma (ej.: iphone-13,iphone-17-pro). Por defecto, todos")
    ap.add_argument("--fuentes", default=",".join(FUENTES), help="fuentes separadas por coma")
    ap.add_argument("--solo-producto", action="store_true",
                    help="solo fotos del equipo (tienda de Apple + producto de Newsroom)")
    ap.add_argument("--max-por-fuente", type=int, default=10,
                    help="máximo de fotos por modelo en fuentes libres y referencia")
    ap.add_argument("--sin-hojas", action="store_true", help="no generar hojas de contacto")
    ap.add_argument("--listar", action="store_true", help="mostrar los modelos disponibles y salir")
    a = ap.parse_args()

    if a.listar:
        for m in MODELOS:
            print(f"{m['id']:20} {m['nombre']:24} {', '.join(m['colores'].values())}")
        return

    modelos = MODELOS
    if a.modelos:
        pedidos = [x.strip() for x in a.modelos.split(",") if x.strip()]
        desconocidos = set(pedidos) - {m["id"] for m in MODELOS}
        if desconocidos:
            sys.exit(f"Modelos desconocidos: {', '.join(sorted(desconocidos))}. Usá --listar.")
        modelos = [m for m in MODELOS if m["id"] in pedidos]
    fuentes = [f.strip() for f in a.fuentes.split(",") if f.strip()]
    if a.solo_producto:
        fuentes = [f for f in fuentes if f in ("apple-store", "newsroom")]
    malas = set(fuentes) - set(FUENTES)
    if malas:
        sys.exit(f"Fuentes desconocidas: {', '.join(sorted(malas))}. Opciones: {', '.join(FUENTES)}")

    d = Descargador(a.salida, a.max_por_fuente)
    try:
        for m in modelos:
            print(f"\n== {m['nombre']}")
            for fuente in fuentes:
                try:
                    if fuente == "newsroom":
                        n = d.newsroom(m, incluir_ambiente=not a.solo_producto)
                    else:
                        n = getattr(d, fuente.replace("-", "_"))(m)
                except requests.RequestException as e:
                    print(f"    {fuente}: error de red ({e.__class__.__name__}); se sigue con la próxima")
                    n = 0
                print(f"  {fuente:12} +{n}")
            d.escribir_indice()
            if not a.sin_hojas:
                d.hoja_contactos(m)
    finally:
        d.escribir_indice()
    print(f"\nListo. Índice: {d.indice_path}  ({len(d.indice)} archivos)")


if __name__ == "__main__":
    main()
