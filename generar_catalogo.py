#!/usr/bin/env python3
"""Prepara el catálogo web a pedido (catalogo/) a partir de catalogo/a-pedido.csv.

    catalogo/a-pedido.csv   la lista que se edita: sección, marca, línea, modelo, capacidad, RAM, condición,
                            foto (img/<archivo>.webp, vacía si no hay foto oficial) y visible (si/no).
                            Se publica tal cual en la web: no poner notas internas ni datos del proveedor.
    catalogo/a-pedido.js    copia del CSV para abrir el catálogo con doble clic (sin servidor).
    catalogo/favicon.png    ícono de la pestaña (avatar lima de la marca).

Revisa que cada foto exista y que no haya columnas de precio. Fotos: procesar_fotos.py (iPhone) y
descargar_otros.py (Samsung/Xiaomi) → catalogo/img/.

Uso:
    python3 generar_catalogo.py
"""

import csv
import json
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent
CATALOGO = RAIZ / "catalogo"
CSV = CATALOGO / "a-pedido.csv"
COLUMNAS = ["seccion", "marca", "linea", "modelo", "capacidad", "ram", "condicion", "foto", "visible"]


def main():
    with open(CSV, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    errores = []
    if list(filas[0]) != COLUMNAS:
        errores.append(f"columnas: {list(filas[0])} (se esperaba {COLUMNAS})")
    for i, fila in enumerate(filas, start=2):
        if fila["foto"] and not (CATALOGO / fila["foto"]).exists():
            errores.append(f"línea {i}: no existe {fila['foto']}")
        if fila["condicion"] not in ("Swap", "Caja sellada"):
            errores.append(f"línea {i}: condición «{fila['condicion']}» (Swap o Caja sellada)")
    if errores:
        sys.exit("\n".join(errores))

    js = CATALOGO / "a-pedido.js"
    js.write_text("// Copia de a-pedido.csv para abrir el catálogo sin servidor. La genera generar_catalogo.py: no editar a mano.\n"
                  f"window.A_PEDIDO = {json.dumps(filas, ensure_ascii=False, indent=1)};\n", encoding="utf-8")
    Image.open(RAIZ / "publicar/00-marca/avatar-lima.png").convert("RGBA").resize((180, 180), Image.LANCZOS).save(CATALOGO / "favicon.png")
    print(f"{len(filas)} modelos → {js.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
