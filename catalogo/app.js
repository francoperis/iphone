// Catálogo Tech&Co. (a pedido): lee la lista de modelos (planilla publicada, a-pedido.csv o su copia a-pedido.js),
// la ordena por secciones y arma las tarjetas con el botón «Consultar», que abre WhatsApp con el mensaje armado.
(function () {
  const CFG = window.CONFIG || {};
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // secciones en el orden de la página; cada fila del CSV cae en una según marca y condición
  const SECCIONES = [
    { id: "swap", titulo: "iPhone <span>Swap.</span>", bajada: "Reacondicionados, traídos directamente de EE. UU.",
      es: (f) => f.marca === "Apple" && f.condicion === "Swap", lineas: { Base: "iPhone", Pro: "Pro", "Pro Max": "Pro Max" } },
    { id: "sellado", titulo: "iPhone <span>sellado.</span>", bajada: "Nuevos, en su caja.",
      es: (f) => f.marca === "Apple" && f.condicion !== "Swap" },
    { id: "samsung", titulo: "Samsung<span>.</span>", bajada: "Nuevos, en caja sellada.", es: (f) => f.marca === "Samsung" },
    { id: "xiaomi", titulo: "Xiaomi<span>.</span>", bajada: "Nuevos, en caja sellada.", es: (f) => f.marca === "Xiaomi" },
  ];

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

  async function cargar() {
    for (const url of [CFG.planilla, "a-pedido.csv"].filter(Boolean)) {
      try {
        const r = await fetch(url, { cache: "no-store" });
        if (r.ok) return parsearCSV(await r.text());
      } catch (e) { /* abierto con doble clic (file://) o sin conexión: se prueba la siguiente */ }
    }
    return window.A_PEDIDO || [];
  }

  // ---------------------------------------------------------------- vista
  const gb = (c) => String(c || "").replace(/\s*GB$/i, " GB").replace(/\s*TB$/i, " TB");

  function linkWhatsApp(msg) {
    const num = String(CFG.whatsapp || "").replace(/\D/g, "");
    return `https://wa.me/${num}?text=${encodeURIComponent(msg)}`;
  }

  function mensaje(f) {
    const cap = f.capacidad ? ` de ${gb(f.capacidad)}` : "";
    return f.condicion === "Swap"
      ? `¡Hola Tech&Co.! Quiero consultar por el ${f.modelo} Swap${cap}.`
      : `¡Hola Tech&Co.! Quiero consultar por el ${f.modelo}${cap}, nuevo en caja sellada.`;
  }

  function foto(f) {
    if (f.foto) return `<img src="${esc(f.foto)}" alt="${esc(f.modelo)}" loading="lazy">`;
    // sin foto oficial todavía: el nombre corto del modelo, grande y apagado
    const corto = f.modelo.replace(/^(Galaxy|Redmi|iPhone)\s+/i, "").replace(/\s+5G$/i, "");
    return `<span class="sin-foto" aria-hidden="true">${esc(corto)}</span>`;
  }

  function tarjeta(f) {
    const cap = [gb(f.capacidad), f.ram ? `${gb(f.ram)} RAM` : ""].filter(Boolean).join(" · ");
    const tag = f.condicion === "Swap" ? `<p class="tag">Swap</p>` : `<p class="tag sellado">Nuevo · Caja sellada</p>`;
    return `<article class="tarjeta">
      <div class="foto">${foto(f)}</div>
      ${tag}
      <h3>${esc(f.modelo)}</h3>
      <p class="cap">${esc(cap)}</p>
      <a class="boton" href="${linkWhatsApp(mensaje(f))}" target="_blank" rel="noopener">Consultar <span aria-hidden="true">→</span></a>
    </article>`;
  }

  // iPhone en caja sellada: no hay lista de modelos, se consulta por modelo, capacidad y color
  function tarjetaAncha(f) {
    return `<article class="ancha">
      <div class="foto">${foto(f)}</div>
      <div>
        <p class="tag sellado">Nuevo · Caja sellada</p>
        <h3>Todos los modelos.</h3>
        <p class="cap">Consultá por el modelo, la capacidad y el color que buscás.</p>
        <a class="boton" href="${linkWhatsApp("¡Hola Tech&Co.! Quiero consultar por un iPhone nuevo en caja sellada. Busco el ")}" target="_blank" rel="noopener">Consultar <span aria-hidden="true">→</span></a>
      </div>
    </article>`;
  }

  function seccion(s, filas) {
    let cuerpo;
    if (s.id === "sellado") cuerpo = filas.map(tarjetaAncha).join("");
    else if (s.lineas) {
      cuerpo = Object.entries(s.lineas).map(([linea, nombre]) => {
        const items = filas.filter((f) => f.linea === linea);
        return items.length ? `<div class="linea"><h3>${esc(nombre)}</h3><span>${items.length} modelos</span></div>
          <div class="grilla">${items.map(tarjeta).join("")}</div>` : "";
      }).join("");
    } else cuerpo = `<div class="grilla">${filas.map(tarjeta).join("")}</div>`;
    return `<section class="seccion" id="${s.id}" data-seccion="${s.id}">
      <div class="seccion-cabeza"><h2>${s.titulo}</h2><p>${esc(s.bajada)}</p></div>
      ${cuerpo}
    </section>`;
  }

  function armar(filas) {
    const visibles = filas.filter((f) => f.modelo && (f.visible || "si").toLowerCase() !== "no");
    $("secciones").innerHTML = SECCIONES.map((s) => {
      const suyas = visibles.filter(s.es);
      return suyas.length ? seccion(s, suyas) : "";
    }).join("");
    // ocultar los botones de secciones vacías
    document.querySelectorAll("#chips .chip[data-seccion]").forEach((b) => {
      if (b.dataset.seccion) b.hidden = !document.getElementById(b.dataset.seccion);
    });
  }

  function filtrar(id) {
    document.querySelectorAll("#chips .chip").forEach((b) => b.classList.toggle("activo", b.dataset.seccion === id));
    document.querySelectorAll("#secciones .seccion").forEach((s) => { s.hidden = Boolean(id) && s.dataset.seccion !== id; });
    const destino = id ? document.getElementById(id) : $("secciones");
    if (destino && window.scrollY > destino.offsetTop - 140) destino.scrollIntoView({ behavior: "smooth" });
  }

  $("chips").addEventListener("click", (e) => {
    const b = e.target.closest(".chip");
    if (b) filtrar(b.dataset.seccion);
  });
  document.querySelectorAll("[data-wa]").forEach((a) => { a.href = linkWhatsApp(a.dataset.wa); });
  if (CFG.instagram) { $("ig").href = `https://instagram.com/${CFG.instagram}`; $("ig").textContent = `@${CFG.instagram}`; }

  cargar().then(armar);
})();
