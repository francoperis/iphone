#!/usr/bin/env python3
"""Busca clips de video con licencia libre para uso comercial (gente usando el celular,
sacando fotos, filmando) y arma una hoja de contactos para elegir.

Fuente: Mixkit (Stock Video Free License: uso comercial y en publicidad online, se puede
editar, sin atribución obligatoria). Los clips con licencia "Restricted" se descartan.
No se usan videos subidos por terceros a redes ni se quitan marcas de agua.

Uso:
    python3 buscar_videos.py                    # busca y arma videos/candidatos.csv + videos/hoja.jpg
    python3 buscar_videos.py --bajar 4915,41165 # baja esos clips en la mejor calidad a videos/clips/
"""

import argparse
import csv
import io
import json
import re
import sys
import time
from pathlib import Path

import requests

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
BASE = "https://mixkit.co"
CATEGORIAS = ["phone", "smartphone", "selfie", "mobile-phone", "photographer", "photo", "camera",
              "social-media", "influencer", "iphone", "apple", "recording", "filming", "video-call"]
PAGINAS = 3
# el clip tiene que hablar de teléfonos o de sacar fotos / filmar
RELEVANTE = re.compile(r"phone|smartphone|cellphone|cell phone|mobile|selfie|photo|picture|camera|"
                       r"record|film|video call|iphone|screen|social media|influencer", re.I)
DESCARTE = re.compile(r"laptop only|typing on a laptop|signing a contract|notepad", re.I)
SALIDA = Path("videos")


def sesion():
    s = requests.Session()
    s.headers["User-Agent"] = UA
    return s


def obtener(s, url, intentos=3):
    for i in range(intentos):
        try:
            r = s.get(url, timeout=40)
            if r.status_code == 200:
                return r
            if r.status_code in (429, 503):
                time.sleep(3 * (i + 1))
                continue
            return r
        except requests.RequestException:
            time.sleep(2 * (i + 1))
    return None


def objetos_video(texto):
    """VideoObject del JSON-LD de una página de Mixkit."""
    out = []
    for bloque in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', texto, re.S):
        try:
            data = json.loads(bloque)
        except json.JSONDecodeError:
            continue
        pila = [data]
        while pila:
            x = pila.pop()
            if isinstance(x, dict):
                if x.get("@type") == "VideoObject":
                    out.append(x)
                pila.extend(x.values())
            elif isinstance(x, list):
                pila.extend(x)
    return out


def buscar():
    s = sesion()
    enlaces = {}
    for cat in CATEGORIAS:
        for pag in range(1, PAGINAS + 1):
            url = f"{BASE}/free-stock-video/{cat}/" + (f"?page={pag}" if pag > 1 else "")
            r = obtener(s, url)
            if not r or r.status_code != 200:
                break
            nuevos = re.findall(r'href="(/free-stock-video/[a-z0-9-]+-(\d+)/)"', r.text)
            if not nuevos:
                break
            for ruta, vid in nuevos:
                enlaces.setdefault(vid, ruta)
            time.sleep(0.4)
        print(f"  {cat}: {len(enlaces)} clips acumulados")

    candidatos = []
    for n, (vid, ruta) in enumerate(sorted(enlaces.items(), key=lambda x: -int(x[0]))):
        r = obtener(s, BASE + ruta)
        if not r or r.status_code != 200:
            continue
        objs = [o for o in objetos_video(r.text) if str(vid) in o.get("@id", "") or str(vid) in o.get("contentUrl", "")]
        if not objs:
            continue
        o = objs[0]
        nombre, desc = o.get("name", ""), o.get("description", "")
        texto = f"{nombre} {desc}"
        licencia = o.get("license", "")
        if "videoFree" not in licencia:
            continue
        if not RELEVANTE.search(texto) or DESCARTE.search(texto):
            continue
        calidad = o.get("videoQuality") or []
        vertical = "vertical" in texto.lower() or bool(re.search(r"vertical", ruta))
        candidatos.append({
            "id": vid, "nombre": nombre, "descripcion": desc, "calidad": "/".join(calidad),
            "vertical": "si" if vertical else "", "licencia": "Mixkit Stock Video Free License",
            "pagina": BASE + ruta, "miniatura": o.get("thumbnailUrl", ""), "video": o.get("contentUrl", ""),
        })
        if n % 20 == 0:
            print(f"  revisados {n + 1}/{len(enlaces)} · candidatos {len(candidatos)}")
        time.sleep(0.3)

    SALIDA.mkdir(exist_ok=True)
    # primero 4K, después los que hablan de fotos/selfies (lo que más sirve para los reels)
    candidatos.sort(key=lambda c: ("4K" not in c["calidad"],
                                   not re.search(r"photo|selfie|picture|camera|record|film", c["nombre"] + c["descripcion"], re.I)))
    with open(SALIDA / "candidatos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(candidatos[0].keys()) if candidatos else ["id"])
        w.writeheader()
        w.writerows(candidatos)
    print(f"{len(candidatos)} candidatos -> {SALIDA / 'candidatos.csv'}")
    hoja(s, candidatos)


def hoja(s, candidatos, columnas=6, ancho=320):
    if not Image or not candidatos:
        return
    alto = ancho * 9 // 16
    filas = (len(candidatos) + columnas - 1) // columnas
    lienzo = Image.new("RGB", (columnas * ancho, filas * (alto + 40)), (12, 12, 13))
    d = ImageDraw.Draw(lienzo)
    for i, c in enumerate(candidatos):
        x, y = (i % columnas) * ancho, (i // columnas) * (alto + 40)
        r = obtener(s, c["miniatura"]) if c["miniatura"] else None
        if r and r.status_code == 200:
            try:
                im = Image.open(io.BytesIO(r.content)).convert("RGB")
                im.thumbnail((ancho - 6, alto - 6))
                lienzo.paste(im, (x + (ancho - im.width) // 2, y + (alto - im.height) // 2))
            except Exception:
                pass
        d.text((x + 6, y + alto + 4), f"#{c['id']} · {c['calidad']}", fill=(204, 255, 0))
        d.text((x + 6, y + alto + 20), c["nombre"][:48], fill=(200, 200, 205))
    lienzo.save(SALIDA / "hoja.jpg", quality=85)
    print(f"Hoja de contactos -> {SALIDA / 'hoja.jpg'}")


def bajar(ids):
    s = sesion()
    destino = SALIDA / "clips"
    destino.mkdir(parents=True, exist_ok=True)
    filas = []
    if (SALIDA / "candidatos.csv").exists():
        with open(SALIDA / "candidatos.csv", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
    for vid in ids:
        info = next((x for x in filas if x["id"] == vid), {})
        # descarga oficial de Mixkit: la página de descarga trae la URL del archivo en esa resolución
        for sufijo in ("2160", "1080"):
            pagina = obtener(s, f"{BASE}/free-stock-video/download/{vid}/?context=sidebar&type={sufijo}p")
            url = re.search(r'data-download--modal-url-value="([^"]+)"', pagina.text) if pagina else None
            if not url:
                continue
            r = s.get(url.group(1), timeout=300, stream=True)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("video"):
                ruta = destino / f"mixkit_{vid}_{sufijo}.mp4"
                with open(ruta, "wb") as f:
                    for trozo in r.iter_content(1 << 20):
                        f.write(trozo)
                print(f"  {ruta}  ({ruta.stat().st_size // 1024} KB)  {info.get('nombre', '')}")
                break
        else:
            print(f"  {vid}: no se pudo bajar")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bajar", help="ids de clips separados por coma")
    a = ap.parse_args()
    if a.bajar:
        bajar([x.strip() for x in a.bajar.split(",") if x.strip()])
    else:
        buscar()


if __name__ == "__main__":
    sys.exit(main())
