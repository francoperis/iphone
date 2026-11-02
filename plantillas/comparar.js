// Comparaciones para plantillas/comparar.html. Specs SOLO de fichas oficiales (fuentes abajo, revisadas el 2026-10-28):
//   iPhone: Apple Support (13: 111872 · 14: 111850 · 15 Pro: 111829 · 16 Pro: 121031)
//   Galaxy A56 5G / A36 5G: samsung.com/ar (fichas del producto) · Redmi Note 15 Pro: mi.com/global/product/redmi-note-15-pro/specs
//   Capacidad / RAM: la configuración del catálogo (catalogo/a-pedido.csv).
// modo "encuesta": historia de 8 s para el sticker de encuesta (sin ganador marcado).
// modo "comparador": reel de 15 s; en cada fila, "a" / "b" = cuál gana (va en lima), "=" = iguales.
window.COMPARACIONES = {
  "a56-vs-13": {
    modo: "encuesta",
    a: { nombre: "Galaxy A56 5G", tag: "Nuevo · caja sellada", foto: "galaxy-a56" },
    b: { nombre: "iPhone 13", tag: "Swap", foto: "iphone-13_midnight" },
    filas: [["Pantalla", "6,7\"", "6,1\""], ["Cámara principal", "50 MP", "12 MP"], ["Capacidad", "256 GB", "128 GB"]],
  },
  "note15pro-vs-a36": {
    modo: "encuesta",
    a: { nombre: "Redmi Note 15 Pro", tag: "Nuevo · caja sellada", foto: "redmi-note-15-pro" },
    b: { nombre: "Galaxy A36 5G", tag: "Nuevo · caja sellada", foto: "galaxy-a36" },
    filas: [["Pantalla", "6,77\"", "6,7\""], ["Cámara principal", "200 MP", "50 MP"], ["Batería", "6500 mAh", "5000 mAh"],
            ["Capacidad", "256 GB", "256 GB"]],
  },
  "13-vs-14": {
    modo: "comparador",
    titulo: ["¿13", "o 14?"],
    a: { nombre: "iPhone 13", tag: "Swap", foto: "iphone-13_midnight" },
    b: { nombre: "iPhone 14", tag: "Swap", foto: "iphone-14_midnight" },
    filas: [
      ["Pantalla", "6,1\"", "6,1\"", "="],
      ["Chip A15 · gráficos", "4 núcleos", "5 núcleos", "b"],
      ["Cámara principal", "ƒ/1.6", "ƒ/1.5", "b"],
      ["Cámara de selfie", "Foco fijo", "Autofoco", "b"],
      ["Batería (video)", "Hasta 19 h", "Hasta 20 h", "b"],
      ["Detección de choques", "No", "Sí", "b"],
    ],
    veredicto: "Casi iguales: el 14 suma cámara, batería y detección de choques.",
  },
  "15pro-vs-16pro": {
    modo: "comparador",
    titulo: ["¿15 Pro", "o 16 Pro?"],
    a: { nombre: "iPhone 15 Pro", tag: "Swap", foto: "iphone-15-pro_naturaltitanium" },
    b: { nombre: "iPhone 16 Pro", tag: "Swap", foto: "iphone-16-pro_deserttitanium" },
    filas: [
      ["Pantalla", "6,1\"", "6,3\"", "b"],
      ["Chip", "A17 Pro", "A18 Pro", "b"],
      ["Ultra gran angular", "12 MP", "48 MP", "b"],
      ["Teleobjetivo", "3x", "5x", "b"],
      ["Batería (video)", "Hasta 23 h", "Hasta 27 h", "b"],
      ["Control de Cámara", "No", "Sí", "b"],
    ],
    veredicto: "El 16 Pro suma pantalla, zoom y batería. El 15 Pro sigue siendo un Pro.",
  },
};
