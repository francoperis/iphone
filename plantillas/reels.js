// Guiones de los reels. Cada uno: clip de fondo (videos/clips/…, licencia libre Mixkit),
// segundo desde donde se toma, hook del primer segundo, contenido y cierre.
// "resaltar": palabra del hook que va sobre bloque lima.
window.REELS = {
  "primera-foto": {
    clip: "", desde: 0,
    etiqueta: "// POV",
    hook: ["Tu primera foto", "con tu iPhone", "nuevo."], resaltar: "nuevo.",
    lineas: ["Del X al 18 Pro Max", "Usados y en caja sellada", "Cada uno con su ficha"],
    cierre: { titulo: "Encontrá el tuyo.", cta: "Respondé QUIERO" },
  },
  "chequea-esto": {
    clip: "", desde: 0,
    etiqueta: "// ANTES DE COMPRAR",
    hook: ["No compres", "un iPhone usado", "sin chequear esto"], resaltar: "usado",
    lista: ["Salud de batería", "Face ID", "iCloud desvinculado", "IMEI limpio"],
    cierre: { titulo: "Guardalo para después.", cta: "Respondé QUIERO" },
  },
  "canje": {
    clip: "", desde: 0,
    etiqueta: "// PLAN CANJE",
    hook: ["¿Cuánto vale", "tu iPhone", "viejo?"], resaltar: "viejo?",
    lineas: ["Entregalo como parte de pago", "y llevate uno más nuevo"],
    cierre: { titulo: "Mandanos tu modelo.", cta: "Respondé CANJE" },
  },
};
