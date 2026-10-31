#!/usr/bin/env python3
"""Superresolución por IA (Real-ESRGAN x4plus, BSD-3, versión ONNX de Qualcomm AI Hub) para las fotos del proveedor.

Toma los recortes de limpiar_proveedor.py (desde las capturas originales), los agranda ×4 con el modelo en mosaicos de 128 px
con solapamiento, y los deja en 1080 px de ancho (más nítidos que agrandar directo) → fotos-proveedor/hd/<nombre>.jpg
Modelo: https://huggingface.co/qualcomm/Real-ESRGAN-x4plus (se baja solo la primera vez a ~/.cache/tech-co/).
Uso: python3 mejorar_ia.py <carpeta_capturas> [nombre ...]
"""
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import onnxruntime as ort
import requests
from PIL import Image, ImageEnhance, ImageFilter

from limpiar_proveedor import BORRONEAR, RECORTES

URL = ("https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/models/real_esrgan_x4plus/"
       "releases/v0.65.0/real_esrgan_x4plus-onnx-float.zip")
CACHE = Path.home() / ".cache/tech-co/real_esrgan_x4plus"
T, SOL = 128, 16          # mosaico de entrada y solapamiento


def modelo():
    onnx = CACHE / "real_esrgan_x4plus-onnx-float/real_esrgan_x4plus.onnx"
    if not onnx.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        zipfile.ZipFile(io.BytesIO(requests.get(URL, timeout=300).content)).extractall(CACHE)
    op = ort.SessionOptions()
    op.intra_op_num_threads = 4
    return ort.InferenceSession(str(onnx), op)


def agrandar(sesion, im):
    a = np.asarray(im.convert("RGB"), np.float32) / 255
    h, w = a.shape[:2]
    out = np.zeros((h * 4, w * 4, 3), np.float32)
    peso = np.zeros((h * 4, w * 4, 1), np.float32)
    # rampa para mezclar los bordes de cada mosaico
    r = np.minimum(np.arange(T * 4) + 1, np.arange(T * 4)[::-1] + 1).astype(np.float32)
    rampa = np.clip(np.minimum.outer(r, r) / (SOL * 4), 0, 1)[..., None]
    paso = T - SOL
    ys = list(range(0, max(h - T, 0) + 1, paso)) + ([h - T] if (h - T) % paso else [])
    xs = list(range(0, max(w - T, 0) + 1, paso)) + ([w - T] if (w - T) % paso else [])
    for y in ys:
        for x in xs:
            t = a[y:y + T, x:x + T].transpose(2, 0, 1)[None]
            r4 = sesion.run(None, {"image": t})[0][0].transpose(1, 2, 0)
            out[y * 4:(y + T) * 4, x * 4:(x + T) * 4] += r4 * rampa
            peso[y * 4:(y + T) * 4, x * 4:(x + T) * 4] += rampa
    return Image.fromarray((np.clip(out / np.maximum(peso, 1e-6), 0, 1) * 255).astype(np.uint8))


def main():
    origen = Path(sys.argv[1])
    solo = set(sys.argv[2:])
    salida = Path(__file__).resolve().parent / "fotos-proveedor/hd"
    salida.mkdir(parents=True, exist_ok=True)
    s = modelo()
    for archivo, (nombre, y0, y1) in RECORTES.items():
        if solo and nombre not in solo:
            continue
        im = Image.open(origen / archivo).convert("RGB")
        k = im.height / 1280
        im = im.crop((0, round(y0 * k), im.width, round(y1 * k)))
        g = agrandar(s, im)
        g = g.resize((1080, round(g.height * 1080 / g.width)), Image.LANCZOS)
        g = ImageEnhance.Contrast(g).enhance(1.04)
        g = g.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=3))
        for caja in BORRONEAR.get(nombre, []):
            g.paste(g.crop(caja).filter(ImageFilter.GaussianBlur(14)), caja[:2])
        g.save(salida / f"{nombre}.jpg", quality=93)
        print(nombre, g.size)


if __name__ == "__main__":
    main()
