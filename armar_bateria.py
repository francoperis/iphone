#!/usr/bin/env python3
"""Clip «Te muestro la batería»: pone la pantalla de Ajustes › Batería (plantillas/pantalla-bateria.html) en un
video real de una mano con un iPhone con pantalla verde (Coverr, gratis para uso comercial, sin atribución:
https://coverr.co/videos/scrolling-on-green-screen-iphone).

El video horizontal se recorta a vertical 1080×1920; la pantalla se sigue cuadro a cuadro por su borde de arriba
y su borde derecho (el izquierdo queda fuera de cuadro). Los dedos quedan delante (se detecta la piel) y las
marcas de seguimiento quedan tapadas por la pantalla
(se rellenan los huecos encerrados por el verde; los dedos entran desde afuera, así que nunca son huecos).

Uso:
    python3 armar_bateria.py videos/clips/bateria_vertical.mp4 [--desde 0 --duracion 10 --encender 4.2]
    (--encender: la pantalla arranca apagada, así el hook del reel se lee, y se prende en ese segundo)
"""

import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, binary_fill_holes, gaussian_filter, label, median_filter, uniform_filter1d

RAIZ = Path(__file__).resolve().parent
CLIP = RAIZ / "videos/clips/coverr-scrolling-on-green-screen-iphone.mp4"
URL = "https://cdn.coverr.co/videos/coverr-scrolling-on-green-screen-iphone-2240/1080p.mp4"
W, H, FPS = 1080, 1920, 25
RECORTE = "crop=607:1080:640:0,scale=1080:1920:flags=lanczos"   # la pantalla, a lo alto
UI_W, UI_H = 1304, 2319                                          # la pantalla del clip, en px del video vertical


def pantalla():
    """Captura la pantalla de batería con Playwright."""
    png = RAIZ / "videos/clips/pantalla-bateria.png"
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: {UI_W}, height: {UI_H} }} }});
  await p.goto('file://{RAIZ}/plantillas/pantalla-bateria.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({{ path: '{png}' }});
  await b.close();
}})();"""
    subprocess.run(["node", "-e", js], check=True, env={**__import__("os").environ,
                   "NODE_PATH": subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()})
    return np.asarray(Image.open(png).convert("RGB")).astype(np.float32)


def cuadros(desde, duracion):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(desde), "-t", str(duracion), "-i", str(CLIP),
                          "-vf", f"{RECORTE},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
    p.wait()


def verde(a):
    a = a.astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (g > 110) & (g > r * 1.25) & (g > b * 1.25)


def seguir(desde, duracion):
    """Borde de arriba y borde derecho de la pantalla en cada cuadro (suavizados) y las marcas de seguimiento
    (círculos blancos y negros) en coordenadas de la pantalla: [dx, dy, radio]."""
    arriba, derecha, marcas = [], [], []
    for a in cuadros(desde, duracion):
        m = verde(a)
        filas = np.nonzero(m.sum(1) > 300)[0]
        y0 = int(filas[0]) if len(filas) else (arriba[-1] if arriba else 150)
        bordes = [np.nonzero(m[y])[0][-1] for y in range(y0 + 60, min(H, y0 + 500), 8) if m[y].any()]
        x1 = int(np.median(bordes)) if bordes else (derecha[-1] if derecha else 1040)
        arriba.append(y0)
        derecha.append(x1)
        huecos, n = label(binary_fill_holes(m) & ~m)       # las marcas enteras son huecos dentro del verde
        for k in range(1, n + 1):
            ys, xs = np.nonzero(huecos == k)
            if 400 < len(ys) < 40000:
                marcas.append((xs.mean() - x1, ys.mean() - y0, np.sqrt(len(ys) / np.pi)))
    # cada marca aparece en muchos cuadros: se agrupan por cercanía y se toma la mediana
    grupos = []
    for mk in marcas:
        for g_ in grupos:
            if abs(g_[0][0] - mk[0]) < 60 and abs(g_[0][1] - mk[1]) < 60:
                g_.append(mk)
                break
        else:
            grupos.append([mk])
    fijas = [np.median(np.array(g_), 0) for g_ in grupos if len(g_) > len(arriba) * 0.15]
    suave = lambda v: uniform_filter1d(median_filter(np.array(v, float), 7, mode="nearest"), 5, mode="nearest")
    return suave(arriba), suave(derecha), fijas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("salida")
    ap.add_argument("--desde", type=float, default=0)
    ap.add_argument("--duracion", type=float, default=10)
    ap.add_argument("--encender", type=float, default=0, help="la pantalla está apagada (negra) hasta este segundo")
    a = ap.parse_args()
    if not CLIP.exists():
        subprocess.run(["curl", "-sSfL", "-A", "Mozilla/5.0", "-o", str(CLIP), URL], check=True)
    ui = pantalla()
    arriba, derecha, fijas = seguir(a.desde, a.duracion)
    print(f"marcas: {len(fijas)}")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", a.salida],
                           stdin=subprocess.PIPE)
    yy, xx = np.mgrid[0:H, 0:W]
    for i, f in enumerate(cuadros(a.desde, a.duracion)):
        x0, y0 = int(round(derecha[i])) + 4 - UI_W, int(round(arriba[i])) - 4
        # la pantalla ubicada en el cuadro
        lienzo = np.zeros((H, W, 3), np.float32)
        sx0, sy0 = max(0, -x0), max(0, -y0)
        dx0, dy0 = max(0, x0), max(0, y0)
        ancho, alto = min(UI_W - sx0, W - dx0), min(UI_H - sy0, H - dy0)
        if ancho > 0 and alto > 0:
            lienzo[dy0:dy0 + alto, dx0:dx0 + ancho] = ui[sy0:sy0 + alto, sx0:sx0 + ancho]
        cerca = (xx > x0 - 30) & (xx < x0 + UI_W + 30) & (yy > y0 - 30) & (yy < y0 + UI_H + 30)
        v = f.astype(np.float32)
        r, g, b = v[..., 0], v[..., 1], v[..., 2]
        mx = np.maximum(r, b)
        m = (g > 80) & (g > r * 1.12) & (g > b * 1.12) & cerca
        m = binary_fill_holes(m)                                            # tapa las marcas enteras
        # marcas tapadas a medias por un dedo: se pinta su círculo, salvo donde hay piel
        piel = (r - np.maximum(g, b)) > 10
        x1, y1 = derecha[i] + 4, arriba[i] - 4
        for dx, dy, rad in fijas:
            disco = (xx - (x1 + dx)) ** 2 + (yy - (y1 + dy)) ** 2 < (rad + 10) ** 2
            m |= disco & ~piel
        alfa = gaussian_filter(binary_dilation(m, iterations=5).astype(np.float32), 1.5)[..., None]
        v[..., 1] = np.where(cerca, np.minimum(g, mx), g)                  # sin reflejo verde en los bordes de los dedos
        luz = np.clip((i / FPS - a.encender) / 0.35, 0, 1)            # se prende la pantalla
        out = lienzo * luz * alfa + v * (1 - alfa)
        enc.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    print(f"-> {a.salida}")


if __name__ == "__main__":
    main()
