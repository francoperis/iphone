#!/usr/bin/env python3
"""Pista de música original para los reels y anuncios (sin licencias de terceros: se sintetiza acá).

Beat electrónico a 120 BPM en La menor (Am · F · C · G), pensado para acompañar los cortes del video:
    --entrada s   donde "cae" el beat completo (con un golpe y una subida antes): el corte del hook al contenido
    --barridos s  barridos cortos (whoosh) cuando entra cada equipo
    --cierre s    desde acá el beat se aliviana (cierre / CTA) y se apaga al final
Uso:
    python3 musica.py salida.wav --duracion 15 --entrada 3.2 --barridos 3.55,5.3,7.05,8.8 --cierre 11
    python3 musica.py salida.wav ... --video entrada.mp4 --salida-video con_musica.mp4   (le pega la pista al video)
"""

import argparse
import subprocess
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100
BPM = 120
BEAT = 60 / BPM
rng = np.random.default_rng(7)  # misma pista cada vez


def env(n, ataque, caida):
    """Envolvente: subida lineal de `ataque` s y caída exponencial con constante `caida` s."""
    t = np.arange(n) / SR
    a = np.clip(t / max(ataque, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(t - ataque, 0) / caida)


def filtro(x, tipo, f, orden=2):
    return sosfilt(butter(orden, f, btype=tipo, fs=SR, output="sos"), x)


def nota(midi):
    return 440 * 2 ** ((midi - 69) / 12)


def poner(pista, x, t, gan=1.0):
    i = int(t * SR)
    if i >= len(pista) or i + len(x) <= 0:
        return
    x = x[max(0, -i):]
    i = max(i, 0)
    n = min(len(x), len(pista) - i)
    pista[i:i + n] += gan * x[:n]


# ------------------------------------------------------------------ instrumentos
def bombo(largo=0.45):
    n = int(largo * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.04)
    cuerpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.16)
    click = filtro(rng.standard_normal(n), "highpass", 2000) * env(n, 0.0005, 0.004) * 0.3
    return np.tanh(1.6 * (cuerpo + click))


def palmas():
    n = int(0.3 * SR)
    ruido = filtro(rng.standard_normal(n), "bandpass", [900, 3500])
    e = np.zeros(n)
    for d in (0, 0.011, 0.022):  # tres golpes muy juntos, como un aplauso
        k = int(d * SR)
        e[k:] += env(n - k, 0.001, 0.05 if d == 0.022 else 0.008)
    return ruido * e * 0.9


def platillo(largo=0.06):
    n = int(largo * SR)
    return filtro(rng.standard_normal(n), "highpass", 7000) * env(n, 0.0005, largo / 4)


def pluck(freqs, largo=0.42, brillo=6):
    """Acorde punteado: armónicos que se apagan más rápido cuanto más agudos."""
    n = int(largo * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for h in range(1, brillo + 1):
            x += np.sin(2 * np.pi * f * h * t + h) / h * np.exp(-t * (5 + 3 * h))
    return x / len(freqs) * env(n, 0.002, 10)


def bajo(f, largo):
    n = int(largo * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return np.tanh(1.4 * x) * env(n, 0.005, largo * 1.5) * np.clip((largo - t) / 0.02, 0, 1)


def barrido(largo=0.45, subir=True):
    n = int(largo * SR)
    ruido = rng.standard_normal(n)
    # se filtra por tramos con un pasabanda que se mueve
    out = np.zeros(n)
    tramos = 12
    for k in range(tramos):
        a, b = k * n // tramos, (k + 1) * n // tramos
        fr = k / (tramos - 1)
        fc = 500 + (5000 if subir else 2500) * (fr if subir else 1 - fr)
        out[a:b] = filtro(ruido, "bandpass", [fc * 0.7, fc * 1.3])[a:b]
    forma = np.sin(np.pi * np.arange(n) / n) ** 2
    return out * forma * 0.35


def subida(largo):
    """Tensión antes de la entrada: ruido que sube de volumen y de brillo."""
    n = int(largo * SR)
    t = np.arange(n) / n
    ruido = rng.standard_normal(n)
    grave, agudo = filtro(ruido, "lowpass", 900), filtro(ruido, "highpass", 3000)
    return (grave * (1 - t) + agudo * t) * t ** 2 * 0.5


def impacto():
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t / 0.08)) / SR) * env(n, 0.002, 0.5)
    cola = filtro(rng.standard_normal(n), "lowpass", 2500) * env(n, 0.002, 0.35) * 0.35
    return np.tanh(1.3 * (boom + cola))


# ------------------------------------------------------------------ arreglo
ACORDES = [  # Am · F · C · G (un compás cada uno)
    ([57, 60, 64], 45), ([53, 57, 60], 41), ([55, 60, 64], 48), ([55, 59, 62], 43),
]
RITMO_PLUCK = [0, 0.75, 1.5, 2.5, 3.0]   # en negras, dentro del compás
RITMO_BAJO = [(0, 0.75), (1.5, 0.5), (2.5, 1.0), (3.5, 0.5)]


def componer(duracion, entrada, barridos, cierre):
    n = int(duracion * SR)
    L, R = np.zeros(n), np.zeros(n)
    bat, bas, aco = np.zeros(n), np.zeros(n), np.zeros(n)
    compas = 4 * BEAT
    # la grilla se corre para que un compás empiece justo en la entrada
    origen = entrada - compas * int(entrada // compas + 1)
    k = 0
    while origen + k * compas < duracion:
        t0 = origen + k * compas
        notas, raiz = ACORDES[k % 4]
        lleno = entrada - 0.01 <= t0 < cierre
        cerrando = t0 >= cierre - 0.01
        for b in range(4):
            tb = t0 + b * BEAT
            if lleno or (cerrando and b == 0 and t0 < duracion - compas):
                poner(bat, bombo(), tb, 0.95)
            if lleno and b in (1, 3):
                poner(bat, palmas(), tb, 0.55)
        for c in range(16):  # platillos en semicorcheas, más suaves en las débiles
            tc = t0 + c * BEAT / 4
            if (lleno and c % 2 == 0) or (c % 4 == 2):
                poner(bat, platillo(), tc, 0.22 if c % 4 == 2 else 0.12)
        for p in RITMO_PLUCK:
            poner(aco, pluck([nota(m) for m in notas], brillo=6 if lleno else 4), t0 + p * BEAT, 0.5 if lleno or cerrando else 0.85)
        if lleno or cerrando:
            for p, largo in RITMO_BAJO:
                poner(bas, bajo(nota(raiz), largo * BEAT * 0.95), t0 + p * BEAT, 0.55 if lleno else 0.35)
        k += 1
    # el bajo y los acordes se "agachan" con cada bombo (sidechain)
    tiempo = np.arange(n) / SR
    fase = ((tiempo - origen) % BEAT) / BEAT
    duck = np.where((tiempo >= entrada) & (tiempo < cierre), 0.35 + 0.65 * np.clip(fase / 0.45, 0, 1), 1.0)
    bas *= duck
    aco *= 0.6 + 0.4 * duck
    # efectos
    efx = np.zeros(n)
    poner(efx, subida(entrada - 0.4), 0.4, 0.9)
    poner(efx, impacto(), entrada, 0.9)
    for s in barridos:
        poner(efx, barrido(), s - 0.25, 1.0)
    poner(efx, barrido(0.8, subir=False), cierre - 0.1, 0.8)
    # mezcla en estéreo: acordes abiertos con un pequeño retardo, el resto al centro
    d = int(0.012 * SR)
    aco_r = np.concatenate([np.zeros(d), aco[:-d]])
    L = bat + bas + 0.9 * aco + efx
    R = bat + bas + 0.9 * aco_r + efx
    # fundido final
    fin = np.clip((duracion - tiempo) / 1.2, 0, 1)
    L, R = L * fin, R * fin
    pico = max(np.abs(L).max(), np.abs(R).max())
    return np.stack([L, R], axis=1) / pico * 0.89


def guardar(audio, ruta):
    datos = (audio * 32767).astype("<i2")
    with wave.open(ruta, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(datos.tobytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("wav")
    ap.add_argument("--duracion", type=float, default=15)
    ap.add_argument("--entrada", type=float, default=3.2)
    ap.add_argument("--barridos", default="")
    ap.add_argument("--cierre", type=float, default=11)
    ap.add_argument("--video")
    ap.add_argument("--salida-video")
    a = ap.parse_args()
    barridos = [float(x) for x in a.barridos.split(",") if x]
    guardar(componer(a.duracion, a.entrada, barridos, a.cierre), a.wav)
    if a.video:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", a.wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", a.salida_video], check=True)


if __name__ == "__main__":
    main()
