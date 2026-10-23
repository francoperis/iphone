// Guiones de los reels. Cada uno: clip de fondo (videos/clips/…, licencia libre Mixkit),
// segundo desde donde se toma, hook del primer segundo, contenido y cierre.
// "resaltar": palabra del hook que va sobre bloque lima.
window.REELS = {
  "primera-foto": {
    clip: "", desde: 0,
    etiqueta: "// POV",
    hook: ["Tu primera foto", "con tu iPhone", "nuevo."], resaltar: "nuevo.",
    lineas: ["Del X al 18 Pro Max", "Swap y en caja sellada", "Cada uno con su ficha"],
    cierre: { titulo: "Encontrá el tuyo.", cta: "Catálogo en la bio" },
  },
  "chequea-esto": {
    clip: "", desde: 0,
    etiqueta: "// ANTES DE COMPRAR",
    hook: ["No compres", "un iPhone Swap", "sin chequear esto"], resaltar: "Swap",
    lista: ["Salud de batería", "Face ID", "iCloud desvinculado", "IMEI limpio"],
    cierre: { titulo: "Guardalo para después.", cta: "Catálogo en la bio" },
  },
  "canje": {
    clip: "", desde: 0,
    etiqueta: "// PLAN CANJE",
    hook: ["¿Cuánto vale", "tu iPhone", "viejo?"], resaltar: "viejo?",
    lineas: ["Entregalo como parte de pago", "y llevate uno más nuevo"],
    cierre: { titulo: "¿A cuál te pasás?", cta: "Catálogo en la bio" },
  },
};
