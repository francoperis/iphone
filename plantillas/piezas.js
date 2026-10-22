// Callouts técnicos para las piezas de Celu&Co.
//   <i class="co" data-l="@tel:0.1:0.55 h:72" data-etq="id" data-pos="sobre-izq" data-t="ms"></i>
// Puntos de la línea, separados por espacios:
//   @id:u:v   punto del <img class="tel" id="id"> en fracciones de la imagen (0..1), con su rotación
//   x,y       punto absoluto en px
//   h:x       horizontal hasta x (misma altura que el punto anterior)
//   v:y       vertical hasta y (misma x que el punto anterior)
// El primer punto lleva punto + aro. La etiqueta (data-etq) se acomoda en el último punto:
//   sobre-izq / sobre-der: arriba de la línea, alineada a la izquierda / derecha · bajo: centrada debajo.
// Llamar después de que carguen las imágenes. Devuelve [{ el, linea, etq, t }] para animar el dibujo.
function puntoDeTel(id, u, v) {
  const img = document.getElementById(id);
  const h = parseFloat(img.style.height), w = h * img.naturalWidth / img.naturalHeight;
  const r = (parseFloat(img.style.rotate) || 0) * Math.PI / 180;
  const dx = (u - 0.5) * w, dy = (v - 0.5) * h;
  return [parseFloat(img.style.left) + dx * Math.cos(r) - dy * Math.sin(r),
          parseFloat(img.style.top) + dx * Math.sin(r) + dy * Math.cos(r)];
}

function armarCallouts(raiz) {
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.classList.add("trazos");
  raiz.appendChild(svg);
  const trazos = [];
  for (const co of raiz.querySelectorAll("i.co")) {
    const pts = [];
    for (const p of co.dataset.l.trim().split(/\s+/)) {
      const ant = pts[pts.length - 1];
      if (p.startsWith("@")) { const [id, u, v] = p.slice(1).split(":"); pts.push(puntoDeTel(id, Number(u), Number(v))); }
      else if (p.startsWith("h:")) pts.push([Number(p.slice(2)), ant[1]]);
      else if (p.startsWith("v:")) pts.push([ant[0], Number(p.slice(2))]);
      else pts.push(p.split(",").map(Number));
    }
    const g = document.createElementNS(ns, "g");
    if (co.style.color) g.style.color = co.style.color;
    const linea = document.createElementNS(ns, "polyline");
    linea.setAttribute("points", pts.map((p) => p.map((n) => n.toFixed(1)).join(",")).join(" "));
    linea.setAttribute("pathLength", "1");
    const [x, y] = pts[0];
    const aro = document.createElementNS(ns, "circle");
    aro.setAttribute("cx", x); aro.setAttribute("cy", y); aro.setAttribute("r", 15); aro.classList.add("aro");
    const punto = document.createElementNS(ns, "circle");
    punto.setAttribute("cx", x); punto.setAttribute("cy", y); punto.setAttribute("r", 6); punto.classList.add("punto");
    g.append(linea, aro, punto);
    svg.appendChild(g);

    const etq = co.dataset.etq ? document.getElementById(co.dataset.etq) : null;
    if (etq) {
      const [ex, ey] = pts[pts.length - 1];
      const pos = co.dataset.pos || "sobre-izq";
      const H = raiz.clientHeight, W = raiz.clientWidth;
      if (pos === "bajo") { etq.classList.add("centro"); etq.style.left = ex + "px"; etq.style.top = ey + 16 + "px"; }
      else if (pos === "sobre-der") { etq.classList.add("der"); etq.style.right = W - ex + "px"; etq.style.bottom = H - ey + 16 + "px"; }
      else { etq.style.left = ex + "px"; etq.style.bottom = H - ey + 16 + "px"; }
    }
    trazos.push({ el: g, linea, etq, t: Number(co.dataset.t || 0) });
    co.remove();
  }
  return trazos;
}
