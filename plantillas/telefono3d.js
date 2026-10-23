// Teléfono en 3D (three.js) armado con las medidas reales del modelo y la foto del dorso como textura.
// Uso:
//   import { crearTelefono } from "./telefono3d.js";
//   const tel = await crearTelefono(canvas, MODELOS[id], colorId, { fotos: "assets/telefonos" });
//   tel.pose({ giroY, giroX, giroZ, subir, correr, escala, acercar });  tel.render();   (subir, correr y acercar en mm)
// Las plantillas deciden la pose en función del tiempo, así la grabación cuadro a cuadro es exacta.

import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

function rectRedondeado(ancho, alto, r) {
  const s = new THREE.Shape();
  const x = -ancho / 2, y = -alto / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + ancho - r, y);
  s.quadraticCurveTo(x + ancho, y, x + ancho, y + r);
  s.lineTo(x + ancho, y + alto - r);
  s.quadraticCurveTo(x + ancho, y + alto, x + ancho - r, y + alto);
  s.lineTo(x + r, y + alto);
  s.quadraticCurveTo(x, y + alto, x, y + alto - r);
  s.lineTo(x, y + r);
  s.quadraticCurveTo(x, y, x + r, y);
  return s;
}

// UV según la posición en el dorso: la foto cubre el equipo entero (ancho × alto en mm)
function uvDesdePosicion(geo, W, H, dx = 0, dy = 0) {
  const p = geo.attributes.position;
  const uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) {
    uv[i * 2] = (p.getX(i) + dx) / W + 0.5;
    uv[i * 2 + 1] = (p.getY(i) + dy) / H + 0.5;
  }
  geo.setAttribute("uv", new THREE.BufferAttribute(uv, 2));
}

function cargarTextura(url) {
  return new Promise((ok, mal) => new THREE.TextureLoader().load(url, (t) => {
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 8;
    ok(t);
  }, undefined, mal));
}

// pantalla generada: vidrio negro, fondo de pantalla con el color del equipo, Dynamic Island o notch
function texturaPantalla(W, H, R, brillo, isla) {
  const k = 12, c = document.createElement("canvas");
  c.width = Math.round(W * k); c.height = Math.round(H * k);
  const g = c.getContext("2d");
  g.fillStyle = "#050506"; g.fillRect(0, 0, c.width, c.height);
  const m = 2.1 * k, rr = (R - 1.6) * k;
  g.save();
  g.beginPath(); g.roundRect(m, m, c.width - 2 * m, c.height - 2 * m, rr); g.clip();
  const fondo = g.createLinearGradient(0, 0, c.width, c.height);
  fondo.addColorStop(0, "#07070a"); fondo.addColorStop(0.55, "#0d0d12"); fondo.addColorStop(1, "#050507");
  g.fillStyle = fondo; g.fillRect(0, 0, c.width, c.height);
  for (const [x, y, r, a] of [[0.15, 0.78, 0.8, 0.55], [0.95, 0.25, 0.65, 0.35]]) {
    const rad = g.createRadialGradient(c.width * x, c.height * y, 0, c.width * x, c.height * y, c.width * r);
    rad.addColorStop(0, brillo + Math.round(a * 255).toString(16).padStart(2, "0"));
    rad.addColorStop(1, brillo + "00");
    g.fillStyle = rad; g.fillRect(0, 0, c.width, c.height);
  }
  g.restore();
  g.fillStyle = "#000";
  if (isla) {
    const iw = 0.29 * W * k, ih = 0.07 * W * k;
    g.beginPath(); g.roundRect((c.width - iw) / 2, 0.018 * H * k + m / 2, iw, ih, ih / 2); g.fill();
  } else {
    const nw = 0.36 * W * k, nh = 0.034 * H * k;
    g.beginPath(); g.roundRect((c.width - nw) / 2, m - 2, nw, nh, [0, 0, nh * 0.6, nh * 0.6]); g.fill();
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

export async function crearTelefono(canvas, modelo, colorId, opciones = {}) {
  const fotos = opciones.fotos || "assets/telefonos";
  const id = opciones.id;
  const d = modelo.tresd;
  const color = modelo.colores[colorId];
  const [W, H, D] = d.medidas;
  const b = d.bisel;
  const R = W * 0.165;

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NoToneMapping;

  const escena = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  escena.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const camara = new THREE.PerspectiveCamera(20, canvas.clientWidth / canvas.clientHeight, 10, 2000);
  camara.position.set(0, 0, opciones.distancia || 520);

  // luces: principal arriba a la izquierda, contraluz (por defecto del color del equipo) y una de relleno
  // ácida; opciones.contraluz / opciones.relleno las cambian por los colores de la marca
  const clave = new THREE.DirectionalLight(0xffffff, 1.6); clave.position.set(-160, 220, 260); escena.add(clave);
  const contra = new THREE.DirectionalLight(new THREE.Color(opciones.contraluz || color.brillo), 3.2); contra.position.set(260, 80, -220); escena.add(contra);
  const acido = new THREE.DirectionalLight(new THREE.Color(opciones.relleno || "#d4ff3a"), 0.9); acido.position.set(-260, -120, -60); escena.add(acido);
  const ambiente = new THREE.AmbientLight(0xffffff, 0.25); escena.add(ambiente);

  const texDorso = await cargarTextura(`${fotos}/${id}_${colorId}_dorso.webp`);
  const metal = d.material === "titanio"
    ? { metalness: 1, roughness: 0.42 }
    : { metalness: 0.85, roughness: 0.32 };
  const matMarco = new THREE.MeshPhysicalMaterial({ color: new THREE.Color(color.marco), ...metal, envMapIntensity: 1.25 });
  // dorso: la foto se ve tal cual (emisivo) y la luz suma brillo y reflejos encima
  const matDorso = new THREE.MeshPhysicalMaterial({
    map: texDorso, color: 0x2a2a2a, emissive: 0xffffff, emissiveMap: texDorso, emissiveIntensity: 0.86,
    roughness: d.material === "titanio" ? 0.5 : 0.3, metalness: 0, clearcoat: 0.6, clearcoatRoughness: 0.28,
  });
  const matPantalla = new THREE.MeshPhysicalMaterial({
    map: texturaPantalla(W, H, R, color.brillo, d.isla), color: 0x222222, emissive: 0xffffff,
    emissiveMap: null, emissiveIntensity: 0, roughness: 0.06, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.03,
  });
  matPantalla.emissiveMap = matPantalla.map; matPantalla.emissiveIntensity = 0.9;

  const telefono = new THREE.Group();
  const cuerpo = new THREE.Group();
  telefono.add(cuerpo);

  // cuerpo: perfil redondeado extruido, con canto curvo (bisel)
  const forma = rectRedondeado(W - 2 * b, H - 2 * b, R - b);
  const geoCuerpo = new THREE.ExtrudeGeometry(forma, {
    depth: D - 2 * b, bevelEnabled: true, bevelThickness: b, bevelSize: b, bevelSegments: 10, curveSegments: 36,
  });
  geoCuerpo.translate(0, 0, -(D - 2 * b) / 2);
  cuerpo.add(new THREE.Mesh(geoCuerpo, matMarco));

  // dorso (mira a +z, hacia la cámara en reposo) y frente
  const zCara = D / 2 + 0.02;
  const geoDorso = new THREE.ShapeGeometry(forma, 36);
  uvDesdePosicion(geoDorso, W, H);
  const dorso = new THREE.Mesh(geoDorso, matDorso);
  dorso.position.z = zCara;
  cuerpo.add(dorso);

  const geoFrente = new THREE.ShapeGeometry(forma, 36);
  uvDesdePosicion(geoFrente, W, H);
  const frente = new THREE.Mesh(geoFrente, matPantalla);
  frente.rotation.y = Math.PI;
  frente.position.z = -zCara;
  cuerpo.add(frente);

  // posición en mm a partir de fracciones del dorso
  const px = (u) => (u - 0.5) * W, py = (v) => (0.5 - v) * H;

  // módulo de cámara en relieve: la tapa lleva la misma foto, así coincide con el dorso
  const mod = d.modulo;
  const mx0 = px(mod.caja[0]), mx1 = px(mod.caja[2]), my0 = py(mod.caja[1]), my1 = py(mod.caja[3]);
  const mw = mx1 - mx0 - (mod.meseta ? 2 * b : 0), mh = my0 - my1 - (mod.meseta ? b : 0);
  const mcx = (mx0 + mx1) / 2, mcy = (my0 + my1) / 2 - (mod.meseta ? b / 2 : 0);
  const bm = Math.min(0.45, mod.alto * 0.4);
  const geoMod = new THREE.ExtrudeGeometry(rectRedondeado(mw, mh, Math.min(mod.radio * W, mw / 2, mh / 2)), {
    depth: mod.alto - bm, bevelEnabled: true, bevelThickness: bm, bevelSize: bm, bevelSegments: 6, curveSegments: 28,
  });
  uvDesdePosicion(geoMod, W, H, mcx, mcy);
  const modulo = new THREE.Mesh(geoMod, [matDorso, matMarco]);
  modulo.position.set(mcx, mcy, zCara);
  cuerpo.add(modulo);

  // lentes: cilindros que sobresalen del módulo, con anillo metálico
  const matAnillo = new THREE.MeshPhysicalMaterial({ color: new THREE.Color(color.marco), metalness: 1, roughness: 0.22 });
  for (const [u, v, r] of d.lentes.lista) {
    const rad = r * W, cx = px(u), cy = py(v), bl = 0.35;
    const circ = new THREE.Shape(); circ.absarc(0, 0, rad - bl, 0, Math.PI * 2, false);
    const geoL = new THREE.ExtrudeGeometry(circ, {
      depth: d.lentes.alto - bl, bevelEnabled: true, bevelThickness: bl, bevelSize: bl, bevelSegments: 4, curveSegments: 48,
    });
    uvDesdePosicion(geoL, W, H, cx, cy);
    const lente = new THREE.Mesh(geoL, [matDorso, matAnillo]);
    lente.position.set(cx, cy, zCara + mod.alto);
    cuerpo.add(lente);
  }

  // botones laterales (vistos desde el dorso: el de encendido queda a la izquierda)
  const boton = (largo, yCentro, lado, prof = 0.7) => {
    const g = new RoundedBoxGeometry(prof * 2, largo, D * 0.42, 3, 0.45);
    const m = new THREE.Mesh(g, matMarco);
    m.position.set(lado * (W / 2 + prof * 0.15), py(yCentro), 0);
    cuerpo.add(m);
  };
  boton(H * 0.105, 0.3, -1);                 // encendido
  boton(H * 0.06, 0.255, 1);                 // subir volumen
  boton(H * 0.06, 0.335, 1);                 // bajar volumen
  boton(H * (d.isla ? 0.045 : 0.03), 0.18, 1); // botón de acción / silencio
  if (d.control) {
    const g = new RoundedBoxGeometry(1.0, H * 0.065, D * 0.5, 3, 0.4);
    const cc = new THREE.Mesh(g, new THREE.MeshPhysicalMaterial({ color: 0x1b1b1e, metalness: 0.2, roughness: 0.08, clearcoat: 1 }));
    cc.position.set(-(W / 2 + 0.05), py(0.6), 0);
    cuerpo.add(cc);
  }

  escena.add(telefono);

  // valores de base para luz(): todo lo que se apaga cuando el equipo queda en silueta
  const materiales = [matMarco, matDorso, matPantalla, matAnillo];
  const base = new Map(materiales.map((m) => [m, { env: m.envMapIntensity ?? 1, emi: m.emissiveIntensity ?? 0 }]));

  return {
    // 0 = silueta (solo el contraluz dibuja el borde), 1 = iluminado normal
    luz(f = 1) {
      clave.intensity = 1.6 * f;
      ambiente.intensity = 0.25 * f;
      for (const m of materiales) {
        const v = base.get(m);
        m.envMapIntensity = v.env * (0.08 + 0.92 * f);
        m.emissiveIntensity = v.emi * f;
      }
    },
    pose({ giroY = 0, giroX = 0, giroZ = 0, subir = 0, correr = 0, escala = 1, acercar = 0 } = {}) {
      telefono.rotation.set(THREE.MathUtils.degToRad(giroX), THREE.MathUtils.degToRad(giroY), THREE.MathUtils.degToRad(giroZ), "YXZ");
      telefono.position.set(correr, subir, acercar);
      telefono.scale.setScalar(escala);
    },
    render() { renderer.render(escena, camara); },
  };
}

