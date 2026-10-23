// Configuración del catálogo. Es lo único que hace falta tocar para ponerlo en marcha.
window.CONFIG = {
  // Número de WhatsApp en formato internacional, sin "+", espacios ni guiones. Ej.: "5491122334455".
  // Vacío: el botón "Lo quiero" abre WhatsApp para elegir a quién mandarle el mensaje (modo prueba).
  whatsapp: "",

  // Stock editable sin tocar código: una Google Sheet con las mismas columnas que stock.csv,
  // publicada como CSV (Archivo › Compartir › Publicar en la web › CSV). Pegar acá ese link.
  // Vacío: usa stock.csv (o su copia stock-demo.js si se abre el archivo con doble clic).
  planilla: "",

  // Mientras sea true se muestra el aviso de "stock de ejemplo".
  demo: true,
};
