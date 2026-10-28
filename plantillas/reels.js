// Guiones de los reels. Cada uno: clip de fondo (videos/clips/…, licencia libre Mixkit),
// segundo desde donde se toma, hook del primer segundo, contenido y cierre.
// "resaltar": palabra del hook que va sobre bloque lima.
window.REELS = {
  "primera-foto": {
    clip: "", desde: 0,
    etiqueta: "",
    hook: ["Tu primera foto", "con tu iPhone", "nuevo."], resaltar: "nuevo.",
    lineas: ["Del X al 18 Pro Max", "Swap y en caja sellada", "Todo a la vista"],
    cierre: { titulo: "Encontrá el tuyo.", cta: "Catálogo en la bio" },
  },
  "chequea-esto": {
    clip: "", desde: 0,
    etiqueta: "",
    hook: ["No compres", "un iPhone Swap", "sin chequear esto"], resaltar: "Swap",
    lista: ["Salud de batería", "Face ID", "iCloud desvinculado", "IMEI limpio"],
    cierre: { titulo: "Guardalo para después.", cta: "Catálogo en la bio" },
  },
  // clips con personas reales (Coverr, gratis para uso comercial): unboxing_vertical.mp4 (armar_unboxing.sh)
  // y bateria_vertical.mp4 (armar_bateria.py: la pantalla de batería puesta en un iPhone con pantalla verde)
  "unboxing": {
    clip: "../videos/clips/unboxing_vertical.mp4", desde: 0,
    etiqueta: "",
    hook: ["¿Lo querés", "en caja", "sellada?"], resaltar: "sellada?",
    lineas: ["iPhone, Samsung y Xiaomi", "Nuevos, en caja sellada", "Te lo conseguimos"],
    cierre: { titulo: "Decime cuál buscás.", cta: "Escribinos por WhatsApp" },
  },
  "bateria": {
    clip: "../videos/clips/bateria_vertical.mp4", desde: 0,
    etiqueta: "",
    hook: ["Antes de pagar,", "te muestro", "la batería."], resaltar: "batería.",
    lineas: ["Estado de la batería a la vista", "Revisado antes de entregarlo", "Sin sorpresas"],
    cierre: { titulo: "Decime qué celular buscás.", cta: "Escribinos por WhatsApp" },
  },
  "canje": {
    clip: "", desde: 0,
    etiqueta: "",
    hook: ["¿Cuánto vale", "tu equipo", "viejo?"], resaltar: "viejo?",
    lineas: ["Entregalo como parte de pago", "y llevate uno más nuevo"],
    cierre: { titulo: "¿A cuál te pasás?", cta: "Catálogo en la bio" },
  },
};
