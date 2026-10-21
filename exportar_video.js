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
const http = require("http");

// mueve la plantilla a ese instante y espera dos cuadros del navegador para que se pinte
async function ir(pagina, ms) {
  await pagina.evaluate(async (t) => {
    window.PLANTILLA.ir(t);
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  }, ms);
}

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
  const limite = opt("--cuadros", null); // solo para pruebas: graba los primeros N cuadros
  const [plantilla, query = "", salida] = args;
  if (!plantilla || !salida) {
    console.error('Uso: node exportar_video.js <plantilla.html> "<parametros>" <salida.mp4|png> [--fps 30] [--cuadro ms]');
    process.exit(1);
  }
  const post = /formato=post/.test(query);
  const ancho = 1080, alto = post ? 1350 : 1920;
  fs.mkdirSync(path.dirname(path.resolve(salida)), { recursive: true });

  // servidor local: los módulos ES y las texturas WebGL no cargan desde file://
  const raiz = process.cwd();
  const tipos = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".webp": "image/webp",
                  ".png": "image/png", ".jpg": "image/jpeg", ".json": "application/json", ".svg": "image/svg+xml" };
  const servidor = http.createServer((req, res) => {
    const ruta = path.join(raiz, decodeURIComponent(new URL(req.url, "http://x").pathname));
    if (!ruta.startsWith(raiz) || !fs.existsSync(ruta) || fs.statSync(ruta).isDirectory()) {
      res.writeHead(404); res.end(); return;
    }
    res.writeHead(200, { "Content-Type": tipos[path.extname(ruta)] || "application/octet-stream" });
    fs.createReadStream(ruta).pipe(res);
  });
  await new Promise((ok) => servidor.listen(0, "127.0.0.1", ok));
  const relativa = path.relative(raiz, path.resolve(plantilla)).split(path.sep).join("/");
  const url = `http://127.0.0.1:${servidor.address().port}/${relativa}` + (query ? "?" + query : "");

  const navegador = await chromium.launch({
    ...(fs.existsSync("/opt/pw-browsers/chromium") ? { executablePath: "/opt/pw-browsers/chromium" } : {}),
    args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"],
  });
  const pagina = await navegador.newPage({ viewport: { width: ancho, height: alto }, deviceScaleFactor: 1 });
  pagina.on("pageerror", (e) => console.error("Error en la plantilla:", e.message));
  pagina.on("console", (msg) => { if (msg.type() === "error") console.error("Consola:", msg.text()); });
  await pagina.goto(url, { waitUntil: "networkidle" });
  await pagina.evaluate(() => window.PLANTILLA.listo());
  // la primera vez que se pausan las animaciones, el compositor tarda en tomar el nuevo estado
  await ir(pagina, 0);
  await pagina.waitForTimeout(800);
  const duracion = await pagina.evaluate(() => window.PLANTILLA.duracion);

  if (cuadro !== null) {
    await ir(pagina, Number(cuadro));
    await pagina.screenshot({ path: salida });
    await navegador.close();
    servidor.close();
    console.log(`Cuadro ${cuadro} ms -> ${salida}`);
    return;
  }

  const total = limite ? Number(limite) : Math.round((duracion / 1000) * fps);
  // capturas descartables: obligan al compositor a tomar el estado pausado antes del primer cuadro real
  for (const t of [duracion / 2, 0]) { await ir(pagina, t); await pagina.screenshot({ type: "png" }); }
  const ff = spawn("ffmpeg", [
    "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-movflags", "+faststart", salida,
  ], { stdio: ["pipe", "inherit", "inherit"] });
  const terminado = new Promise((ok, mal) => ff.on("close", (c) => (c === 0 ? ok() : mal(new Error("ffmpeg salió con " + c)))));

  for (let i = 0; i < total; i++) {
    await ir(pagina, (i * 1000) / fps);
    const png = await pagina.screenshot({ type: "png" });
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % fps === 0) process.stdout.write(`\r  ${Math.round((i / total) * 100)}%`);
  }
  ff.stdin.end();
  await terminado;
  await navegador.close();
  servidor.close();
  console.log(`\r  100% -> ${salida} (${total} cuadros, ${fps} fps, ${ancho}x${alto})`);
}

main().catch((e) => { console.error(e); process.exit(1); });
