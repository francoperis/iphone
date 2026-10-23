// Datos que usan las plantillas. Editar acá, no en el HTML.
// Precios en pesos (tabla del flyer). Nunca mostrar la cotización del dólar.
// Lo que todavía no sabemos queda como marcador: [__].
//
// Modelo 3D ("tresd"):
//   medidas  ancho × alto × espesor en mm (fichas oficiales de Apple)
//   bisel    radio del canto redondeado en mm (los Pro tienen cantos curvos; el 13, planos)
//   modulo   módulo de cámara: caja [x0, y0, x1, y1] en fracciones del dorso (0,0 = arriba a la izquierda),
//            radio (fracción del ancho) y alto en mm
//   lentes   [x, y, radio] en fracciones (radio sobre el ancho) y cuánto sobresalen (mm)
//   control  true si tiene Control de Cámara (botón lateral)
//   colores  nombre en castellano, "brillo" (luz de fondo) y "marco" (color del canto metálico)

window.MARCA = {
  nombre: "Tech&Co.",
  instagram: "@techco.ctes",
  whatsapp: "[WHATSAPP]",
};

window.MODELOS = {
  "iphone-12": {
    nombre: "iPhone 12", gb: 128, precio: 510000,
    tresd: {
      medidas: [71.5, 146.7, 7.4], bisel: 0.7, material: "aluminio", isla: false,
      modulo: { caja: [0.063, 0.028, 0.476, 0.238], radio: 0.1, alto: 0.9 },
      lentes: { lista: [[0.185, 0.086, 0.082], [0.185, 0.182, 0.082]], alto: 0.7 },
      control: false,
    },
    colores: {
      blue: { nombre: "Azul", brillo: "#2f5675", marco: "#2c4c66" },
      black: { nombre: "Negro", brillo: "#2b2d31", marco: "#1f2124" },
      white: { nombre: "Blanco", brillo: "#ecebe6", marco: "#e2e1dc" },
      green: { nombre: "Verde", brillo: "#cfe3cf", marco: "#b9d0bb" },
      purple: { nombre: "Púrpura", brillo: "#c9bfdc", marco: "#b7acd0" },
      red: { nombre: "(PRODUCT)RED", brillo: "#b1202c", marco: "#9a1b25" },
    },
    color: "blue",
  },
  "iphone-13": {
    nombre: "iPhone 13", gb: 128, precio: 610000,
    tresd: {
      medidas: [71.5, 146.7, 7.65], bisel: 0.7, material: "aluminio", isla: false,
      modulo: { caja: [0.032, 0.014, 0.458, 0.218], radio: 0.1, alto: 0.9 },
      lentes: { lista: [[0.166, 0.082, 0.083], [0.345, 0.166, 0.083]], alto: 0.7 },
      control: false,
    },
    colores: {
      blue: { nombre: "Azul", brillo: "#3d7fb0", marco: "#3b6a8c" },
      pink: { nombre: "Rosa", brillo: "#f2b8c6", marco: "#e6c3bd" },
      midnight: { nombre: "Medianoche", brillo: "#4a5568", marco: "#2a3039" },
      starlight: { nombre: "Blanco estelar", brillo: "#e9e3d6", marco: "#e3dccf" },
      green: { nombre: "Verde", brillo: "#4f6b55", marco: "#3c5244" },
    },
    color: "blue",
  },
  "iphone-15-pro": {
    nombre: "iPhone 15 Pro", gb: 128, precio: 1120000,
    tresd: {
      medidas: [70.6, 146.6, 8.25], bisel: 2.2, material: "titanio", isla: true,
      modulo: { caja: [0.052, 0.016, 0.602, 0.302], radio: 0.13, alto: 1.3 },
      lentes: { lista: [[0.19, 0.094, 0.104], [0.437, 0.166, 0.104], [0.19, 0.237, 0.104]], alto: 1.5 },
      control: false,
    },
    colores: {
      naturaltitanium: { nombre: "Titanio natural", brillo: "#b9b2a6", marco: "#a19c93" },
      bluetitanium: { nombre: "Titanio azul", brillo: "#4b5869", marco: "#3d4553" },
      whitetitanium: { nombre: "Titanio blanco", brillo: "#e4e2dc", marco: "#d7d5cf" },
      blacktitanium: { nombre: "Titanio negro", brillo: "#55565a", marco: "#3a3a3d" },
    },
    color: "naturaltitanium",
  },
  "iphone-16-pro": {
    nombre: "iPhone 16 Pro", gb: 128, precio: 1435000,
    tresd: {
      medidas: [71.5, 149.6, 8.25], bisel: 2.2, material: "titanio", isla: true,
      modulo: { caja: [0.052, 0.013, 0.622, 0.297], radio: 0.13, alto: 1.3 },
      lentes: { lista: [[0.19, 0.088, 0.104], [0.437, 0.163, 0.104], [0.19, 0.236, 0.104]], alto: 1.5 },
      control: true,
    },
    colores: {
      deserttitanium: { nombre: "Titanio del desierto", brillo: "#c9a98a", marco: "#bba089" },
      naturaltitanium: { nombre: "Titanio natural", brillo: "#b9b2a6", marco: "#a6a197" },
      whitetitanium: { nombre: "Titanio blanco", brillo: "#e4e2dc", marco: "#d8d6d0" },
      blacktitanium: { nombre: "Titanio negro", brillo: "#55565a", marco: "#3a3a3c" },
    },
    color: "deserttitanium",
  },
  "iphone-17-pro": {
    nombre: "iPhone 17 Pro", gb: 256, precio: 1900000,
    tresd: {
      medidas: [71.9, 150.0, 8.75], bisel: 2.6, material: "aluminio", isla: true,
      modulo: { caja: [0.0, 0.0, 1.0, 0.3], radio: 0.16, alto: 1.6, meseta: true },
      lentes: { lista: [[0.2, 0.095, 0.104], [0.457, 0.166, 0.104], [0.2, 0.236, 0.104]], alto: 1.4 },
      control: true,
    },
    colores: {
      cosmicorange: { nombre: "Naranja cósmico", brillo: "#f07a2c", marco: "#e0763a" },
      deepblue: { nombre: "Azul profundo", brillo: "#34405e", marco: "#2e3850" },
      silver: { nombre: "Plata", brillo: "#dcdcdc", marco: "#cfcfd1" },
    },
    color: "cosmicorange",
  },
};

// $1.120.000 -> { miles: "1.120", resto: ".000" }
window.partirPrecio = function (n) {
  const s = Math.round(n).toLocaleString("es-AR");
  const i = s.lastIndexOf(".");
  return i < 0 ? { miles: s, resto: "" } : { miles: s.slice(0, i), resto: s.slice(i) };
};
