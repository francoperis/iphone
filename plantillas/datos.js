// Datos que usan las plantillas. Editar acá, no en el HTML.
// Precios en pesos (tabla del flyer). Nunca mostrar la cotización del dólar.
// Lo que todavía no sabemos queda como marcador: [__].

window.MARCA = {
  nombre: "Celu&Co.",
  instagram: "@[INSTAGRAM]",
  whatsapp: "[WHATSAPP]",
};

window.MODELOS = {
  "iphone-13": {
    nombre: "iPhone 13", gb: 128, precio: 610000,
    colores: {
      blue: { nombre: "Azul", brillo: "#3d7fb0" },
      pink: { nombre: "Rosa", brillo: "#f2b8c6" },
      midnight: { nombre: "Medianoche", brillo: "#4a5568" },
      starlight: { nombre: "Blanco estelar", brillo: "#e9e3d6" },
      green: { nombre: "Verde", brillo: "#4f6b55" },
    },
    color: "blue",
  },
  "iphone-15-pro": {
    nombre: "iPhone 15 Pro", gb: 128, precio: 1120000,
    colores: {
      naturaltitanium: { nombre: "Titanio natural", brillo: "#b9b2a6" },
      bluetitanium: { nombre: "Titanio azul", brillo: "#4b5869" },
      whitetitanium: { nombre: "Titanio blanco", brillo: "#e4e2dc" },
      blacktitanium: { nombre: "Titanio negro", brillo: "#55565a" },
    },
    color: "naturaltitanium",
  },
  "iphone-16-pro": {
    nombre: "iPhone 16 Pro", gb: 128, precio: 1435000,
    colores: {
      deserttitanium: { nombre: "Titanio del desierto", brillo: "#c9a98a" },
      naturaltitanium: { nombre: "Titanio natural", brillo: "#b9b2a6" },
      whitetitanium: { nombre: "Titanio blanco", brillo: "#e4e2dc" },
      blacktitanium: { nombre: "Titanio negro", brillo: "#55565a" },
    },
    color: "deserttitanium",
  },
  "iphone-17-pro": {
    nombre: "iPhone 17 Pro", gb: 256, precio: 1900000,
    colores: {
      cosmicorange: { nombre: "Naranja cósmico", brillo: "#f07a2c" },
      deepblue: { nombre: "Azul profundo", brillo: "#34405e" },
      silver: { nombre: "Plata", brillo: "#dcdcdc" },
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
