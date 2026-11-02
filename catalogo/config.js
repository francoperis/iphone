// Configuración del catálogo. Es lo único que hace falta tocar para ponerlo en marcha.
window.CONFIG = {
  // Número de WhatsApp en formato internacional, sin "+", espacios ni guiones. Ej.: "5493794123456".
  // Vacío: los botones abren WhatsApp para elegir a quién mandarle el mensaje (sirve para probar).
  whatsapp: "5493795336448",

  // Lista editable sin tocar código: una Google Sheet con las mismas columnas que a-pedido.csv,
  // publicada como CSV (Archivo › Compartir › Publicar en la web › CSV). Pegar acá ese link.
  // Vacío: usa a-pedido.csv (o su copia a-pedido.js si se abre el archivo con doble clic).
  planilla: "",

  instagram: "techco.ctes",
};
