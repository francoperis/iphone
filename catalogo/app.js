// Catálogo Tech&Co.: carga el stock (planilla publicada, stock.csv o la copia de ejemplo),
// lo cruza con los modelos verificados y arma la grilla con filtros y el botón de WhatsApp.
(function () {
  const CFG = window.CONFIG || {};
  const MODELOS = Object.fromEntries((window.MODELOS_CATALOGO || []).map((m) => [m.id, m]));
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const filtros = { texto: "", capacidad: "", bateria: 0, condicion: "", familia: "", disponibles: false, orden: "nuevo" };
  let stock = [];

  // ---------------------------------------------------------------- datos
  function parsearCSV(texto) {
    const filas = [];
    let fila = [], campo = "", comillas = false;
    for (let i = 0; i < texto.length; i++) {
      const c = texto[i];
      if (comillas) {
        if (c === '"' && texto[i + 1] === '"') { campo += '"'; i++; }
        else if (c === '"') comillas = false;
        else campo += c;
      } else if (c === '"') comillas = true;
      else if (c === ",") { fila.push(campo); campo = ""; }
      else if (c === "\n" || c === "\r") {
        if (c === "\r" && texto[i + 1] === "\n") i++;
        fila.push(campo); campo = "";
        if (fila.some((x) => x.trim() !== "")) filas.push(fila);
        fila = [];
      } else campo += c;
    }
    fila.push(campo);
    if (fila.some((x) => x.trim() !== "")) filas.push(fila);
    const [cab, ...resto] = filas;
    const claves = cab.map((h) => h.trim().toLowerCase());
    return resto.map((f) => Object.fromEntries(claves.map((k, i) => [k, (f[i] || "").trim()])));
  }

  async function cargarStock() {
    const fuentes = [CFG.planilla, "stock.csv"].filter(Boolean);
    for (const url of fuentes) {
      try {
        const r = await fetch(url, { cache: "no-store" });
        if (r.ok) return parsearCSV(await r.text());
      } catch (e) { /* abierto con doble clic (file://) o sin conexión: se prueba la siguiente */ }
    }
    return window.STOCK_DEMO || [];
  }

  function preparar(fila) {
    const m = MODELOS[fila.modelo];
    if (!m) return null;
    const color = m.colores.find((c) => c.id === fila.color) || { id: fila.color, nombre: fila.color, muestra: "#8E8E96", img: "" };
    const bateria = fila.bateria === "" ? null : Number(fila.bateria);
    // los equipos no nuevos se llaman Swap ("usado" en planillas viejas también cuenta como swap)
    const condicion = String(fila.condicion || "").trim().toLowerCase() === "sellado" ? "sellado" : "swap";
    return {
      ...fila, condicion, m, colorInfo: color, bateria,
      precioNum: fila.precio ? Number(String(fila.precio).replace(/[^\d]/g, "")) : null,
      busqueda: `${m.nombre} ${fila.capacidad} ${color.nombre} ${condicion}`.toLowerCase(),
    };
  }

  // ---------------------------------------------------------------- vista
  function precioHTML(n) {
    if (!n) return `<span class="precio consultar">Consultar</span>`;
    const s = n.toLocaleString("es-AR");
    const i = s.lastIndexOf(".");
    const miles = i < 0 ? s : s.slice(0, i), resto = i < 0 ? "" : s.slice(i);
    return `<span class="precio"><span class="signo">$</span><span class="miles">${miles}</span><span class="resto">${resto}</span></span>`;
  }

  function linkWhatsApp(u) {
    const partes = [`${u.m.nombre} de ${u.capacidad}`, u.colorInfo.nombre];
    partes.push(u.condicion === "sellado" ? "en caja sellada" : "Swap");
    else if (u.bateria !== null) partes.push(`batería ${u.bateria} %`);
    const msg = `¡Hola Tech&Co.! Quiero el ${partes.join(", ")}. ¿Sigue disponible?`;
    const num = String(CFG.whatsapp || "").replace(/\D/g, "");
    return `https://wa.me/${num}?text=${encodeURIComponent(msg)}`;
  }

  function tarjeta(u) {
    const disp = (u.disponible || "si").toLowerCase();
    const textoDisp = { si: "● DISPONIBLE", reservado: "○ RESERVADO", no: "VENDIDO" }[disp] || "● DISPONIBLE";
    const foto = u.colorInfo.img
      ? `<img src="${esc(u.colorInfo.img)}" alt="${esc(u.m.nombre)} ${esc(u.colorInfo.nombre)}" loading="lazy">`
      : `<div class="silueta" aria-hidden="true"></div>`;
    const datos = [
      `<span class="dato">${esc(u.capacidad)}</span>`,
      `<span class="dato"><span class="punto" aria-hidden="true"></span>${esc(u.colorInfo.nombre)}</span>`,
      u.bateria !== null ? `<span class="dato${u.bateria >= 90 ? " bat-alta" : ""}">Bat ${u.bateria} %</span>` : "",
      u.estado ? `<span class="dato">${esc(u.estado)}</span>` : "",
    ].join("");
    const vendido = disp === "no";
    return `<article class="tarjeta" style="--muestra:${esc(u.colorInfo.muestra)}">
      <div class="foto">${foto}
        <span class="estado-tag ${esc(disp)}">${textoDisp}</span>
        <span class="sellado-tag">${u.condicion === "sellado" ? "SELLADO" : "SWAP"}</span>
        ${u.demo === "si" ? `<span class="demo-tag">EJEMPLO</span>` : ""}
      </div>
      <div class="ficha">
        <div class="ficha-cabeza"><h3>${esc(u.m.nombre)}</h3><span class="barras" aria-hidden="true"></span></div>
        <div class="datos">${datos}</div>
        <div class="pie-ficha">
          ${precioHTML(u.precioNum)}
          <a class="lo-quiero" href="${vendido ? "#" : linkWhatsApp(u)}" target="_blank" rel="noopener"
             ${vendido ? 'aria-disabled="true" tabindex="-1"' : ""}>${vendido ? "Vendido" : "Lo quiero →"}</a>
        </div>
      </div>
    </article>`;
  }

  function filtrar() {
    const t = filtros.texto.trim().toLowerCase();
    return stock.filter((u) =>
      (!t || t.split(/\s+/).every((p) => u.busqueda.includes(p))) &&
      (!filtros.capacidad || u.capacidad === filtros.capacidad) &&
      (!filtros.bateria || u.condicion === "sellado" || (u.bateria !== null && u.bateria >= filtros.bateria)) &&
      (!filtros.condicion || u.condicion === filtros.condicion) &&
      (!filtros.familia || u.m.familia === filtros.familia) &&
      (!filtros.disponibles || (u.disponible || "si") === "si"));
  }

  function render() {
    const lista = filtrar();
    const signo = filtros.orden === "nuevo" ? -1 : 1;
    const porFamilia = new Map();
    lista.sort((a, b) => signo * (a.m.orden - b.m.orden) || capacidadGB(a.capacidad) - capacidadGB(b.capacidad))
      .forEach((u) => {
        if (!porFamilia.has(u.m.familia)) porFamilia.set(u.m.familia, { nombre: u.m.familiaNombre, items: [] });
        porFamilia.get(u.m.familia).items.push(u);
      });
    $("resultados").innerHTML = [...porFamilia.values()].map((f) => `
      <section class="familia">
        <div class="familia-cabeza"><h2>${esc(f.nombre)}</h2><span class="familia-cuenta">${f.items.length} ${f.items.length === 1 ? "equipo" : "equipos"}</span></div>
        <div class="grilla">${f.items.map(tarjeta).join("")}</div>
      </section>`).join("");
    $("vacio").hidden = lista.length > 0;
    const modelos = new Set(lista.map((u) => u.modelo)).size;
    $("resumen").textContent = `${lista.length} equipos · ${modelos} modelos`;
  }

  function capacidadGB(c) { const n = parseInt(c, 10); return /TB/i.test(c) ? n * 1024 : n; }

  // ---------------------------------------------------------------- controles
  function armarControles() {
    const caps = [...new Set(stock.map((u) => u.capacidad))].sort((a, b) => capacidadGB(a) - capacidadGB(b));
    $("capacidad").insertAdjacentHTML("beforeend", caps.map((c) => `<option value="${esc(c)}">${esc(c)}</option>`).join(""));

    const familias = [];
    (window.MODELOS_CATALOGO || []).forEach((m) => { if (!familias.find((f) => f.id === m.familia)) familias.push({ id: m.familia, nombre: m.familiaNombre }); });
    $("familias").innerHTML = `<button type="button" class="chip activo" data-valor="">Todas</button>` +
      familias.reverse().map((f) => `<button type="button" class="chip" data-valor="${esc(f.id)}">${esc(f.nombre.replace("iPhone ", ""))}</button>`).join("");

    const grupoChips = (id, clave) => $(id).addEventListener("click", (e) => {
      const b = e.target.closest("button.chip");
      if (!b) return;
      $(id).querySelectorAll("button.chip").forEach((x) => x.classList.toggle("activo", x === b));
      filtros[clave] = b.dataset.valor;
      render();
    });
    grupoChips("condicion", "condicion");
    grupoChips("familias", "familia");
    $("buscar").addEventListener("input", (e) => { filtros.texto = e.target.value; render(); });
    $("capacidad").addEventListener("change", (e) => { filtros.capacidad = e.target.value; render(); });
    $("bateria").addEventListener("change", (e) => { filtros.bateria = Number(e.target.value); render(); });
    $("orden").addEventListener("change", (e) => { filtros.orden = e.target.value; render(); });
    $("disponibles").addEventListener("change", (e) => { filtros.disponibles = e.target.checked; render(); });

    const num = String(CFG.whatsapp || "").replace(/\D/g, "");
    $("barraWa").href = `https://wa.me/${num}?text=${encodeURIComponent("¡Hola Tech&Co.! Quiero consultar por un equipo.")}`;
    $("avisoDemo").hidden = !CFG.demo;
  }

  cargarStock().then((filas) => {
    stock = filas.map(preparar).filter(Boolean);
    armarControles();
    render();
  });
})();
