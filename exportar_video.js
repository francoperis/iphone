#!/usr/bin/env node
// Graba una plantilla HTML a MP4 cuadro por cuadro (sin saltos ni cuadros perdidos).
//
// Uso:
//   node exportar_video.js plantillas/llego.html "modelo=iphone-17-pro" salida/llego-17-pro.mp4
//   node exportar_video.js plantillas/llego.html "modelo=iphone-13&formato=post" salida/post.mp4
//   node exportar_video.js plantillas/llego.html "modelo=iphone-13" salida/cuadro.png --cuadro 3000
//
// Opciones: --fps 30 (por defecto) · --cuadro <ms> guarda un PNG de ese instante en vez del video.
// La plantilla tiene que exponer window.PLANTILLA = { duracion, listo(), ir(ms) }.
// Requiere playwright (npm i) y ffmpeg en el PATH.

const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

async function main() {
  const args = process.argv.slice(2);
  const opt = (n, def) => {
    const i = args.indexOf(n);
    if (i < 0) return def;
    const v = args[i + 1];
    args.splice(i, 2);
    return v;
  };
  const fps = Number(opt("--fps", 30));
  const cuadro = opt("--cuadro", null);
  const [plantilla, query = "", salida] = args;
  if (!plantilla || !salida) {
    console.error('Uso: node exportar_video.js <plantilla.html> "<parametros>" <salida.mp4|png> [--fps 30] [--cuadro ms]');
    process.exit(1);
  }
  const post = /formato=post/.test(query);
  const ancho = 1080, alto = post ? 1350 : 1920;
  const url = pathToFileURL(path.resolve(plantilla)).href + (query ? "?" + query : "");
  fs.mkdirSync(path.dirname(path.resolve(salida)), { recursive: true });

  const navegador = await chromium.launch(fs.existsSync("/opt/pw-browsers/chromium")
    ? { executablePath: "/opt/pw-browsers/chromium" } : {});
  const pagina = await navegador.newPage({ viewport: { width: ancho, height: alto }, deviceScaleFactor: 1 });
  pagina.on("pageerror", (e) => console.error("Error en la plantilla:", e.message));
  await pagina.goto(url, { waitUntil: "networkidle" });
  await pagina.evaluate(() => window.PLANTILLA.listo());
  const duracion = await pagina.evaluate(() => window.PLANTILLA.duracion);

  if (cuadro !== null) {
    await pagina.evaluate((ms) => window.PLANTILLA.ir(ms), Number(cuadro));
    await pagina.screenshot({ path: salida });
    await navegador.close();
    console.log(`Cuadro ${cuadro} ms -> ${salida}`);
    return;
  }

  const total = Math.round((duracion / 1000) * fps);
  const ff = spawn("ffmpeg", [
    "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-movflags", "+faststart", salida,
  ], { stdio: ["pipe", "inherit", "inherit"] });
  const terminado = new Promise((ok, mal) => ff.on("close", (c) => (c === 0 ? ok() : mal(new Error("ffmpeg salió con " + c)))));

  for (let i = 0; i < total; i++) {
    await pagina.evaluate((ms) => window.PLANTILLA.ir(ms), (i * 1000) / fps);
    const png = await pagina.screenshot({ type: "png" });
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % fps === 0) process.stdout.write(`\r  ${Math.round((i / total) * 100)}%`);
  }
  ff.stdin.end();
  await terminado;
  await navegador.close();
  console.log(`\r  100% -> ${salida} (${total} cuadros, ${fps} fps, ${ancho}x${alto})`);
}

main().catch((e) => { console.error(e); process.exit(1); });
