const API_URL = "http://127.0.0.1:8001/api/convocatorias";

// MOCK: Datos simulados de respaldo si el backend está apagado o en pruebas
const MOCK_CONVOCATORIAS = [
  {
    id_convocatoria: 1,
    titulo: "Beca Universitaria a la Excelencia Académica 2026",
    descripcion: "Programa de financiamiento total de colegiatura y apoyo mensual para estudiantes con rendimiento académico destacado.",
    fecha_inicio: "2026-02-01",
    fecha_fin: "2026-03-31",
    requisitos: "Promedio general mínimo de 85 puntos; Estar legalmente inscrito en el ciclo 2026; Constancia de carencia de sanciones disciplinarias; Comprobante de ingresos familiares.",
    estado: "publicada"
  },
  {
    id_convocatoria: 2,
    titulo: "Beca de Apoyo Socioeconómico y Transporte",
    descripcion: "Subsidio destinado a estudiantes de departamentos con dificultades de cobertura de traslados y materiales de estudio.",
    fecha_inicio: "2026-02-15",
    fecha_fin: "2026-04-15",
    requisitos: "Estudio socioeconómico completado; Constancia de residencia comunitaria; Fotocopia legible de DPI; No contar con otra beca activa.",
    estado: "publicada"
  }
];

let convocatoriasCargadas = [];
let convocatoriaSeleccionada = null;

// Referencias del DOM
const contenedor = document.getElementById("lista-convocatorias");
const contadorEl = document.getElementById("contador-convocatorias");
const modal = document.getElementById("modal-detalle");
const btnCerrarModal = document.getElementById("btn-cerrar-modal");
const btnVolverModal = document.getElementById("btn-volver-modal");
const btnSolicitar = document.getElementById("btn-solicitar");

// Obtener convocatorias (intenta API real, si falla recurre al Mock)
async function obtenerConvocatorias() {
  try {
    const res = await fetch(`${API_URL}/`);
    if (res.ok) {
      const data = await res.json();
      return data.filter(c => c.estado?.toLowerCase() === "publicada");
    }
  } catch (error) {
    console.warn("Backend no disponible en el puerto 8001. Cargando datos simulados (Mock).");
  }
  return MOCK_CONVOCATORIAS;
}

// Renderizar tarjetas en pantalla
function renderizarTarjetas(lista) {
  convocatoriasCargadas = lista;
  contenedor.innerHTML = "";
  if (contadorEl) {
    contadorEl.textContent = `${lista.length} convocatoria(s) activa(s)`;
  }

  if (!lista.length) {
    contenedor.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; background: white; border-radius: 12px; color: #64748b;">
        No hay convocatorias publicadas en este momento.
      </div>
    `;
    return;
  }

  lista.forEach(item => {
    const card = document.createElement("article");
    card.className = "convocatoria-card";
    card.innerHTML = `
      <div>
        <div class="card-top">
          <h3 class="card-title">${item.titulo}</h3>
          <span class="badge badge-publicada">${item.estado}</span>
        </div>
        <div class="card-meta">
          <span>📅 <strong>Cierre:</strong> ${item.fecha_fin}</span>
        </div>
        <p class="card-desc">${item.descripcion}</p>
      </div>
      <button type="button" class="btn-primary" onclick="abrirDetalle(${item.id_convocatoria})">
        Ver Detalles y Requisitos
      </button>
    `;
    contenedor.appendChild(card);
  });
}

// Abrir modal con detalle
window.abrirDetalle = function(id) {
  const conv = convocatoriasCargadas.find(c => c.id_convocatoria === id);
  if (!conv) return;

  convocatoriaSeleccionada = conv;

  const modalTitulo = document.getElementById("modal-titulo");
  const modalEstado = document.getElementById("modal-estado");
  const modalFechas = document.getElementById("modal-fechas");
  const modalDesc = document.getElementById("modal-descripcion");
  const listaReq = document.getElementById("modal-requisitos");

  if (modalTitulo) modalTitulo.textContent = conv.titulo;
  if (modalEstado) {
    modalEstado.textContent = conv.estado;
    modalEstado.className = `badge badge-${conv.estado.toLowerCase()}`;
  }
  if (modalFechas) modalFechas.textContent = `Plazo: del ${conv.fecha_inicio} al ${conv.fecha_fin}`;
  if (modalDesc) modalDesc.textContent = conv.descripcion;

  if (listaReq) {
    const requisitosArray = conv.requisitos ? conv.requisitos.split(/;|\n/) : [];
    listaReq.innerHTML = requisitosArray
      .map(r => r.trim())
      .filter(r => r.length > 0)
      .map(r => `<li>${r}</li>`)
      .join("");
  }

  if (modal) modal.classList.remove("hidden");
};

function cerrarModal() {
  if (modal) modal.classList.add("hidden");
  convocatoriaSeleccionada = null;
}

if (btnCerrarModal) btnCerrarModal.addEventListener("click", cerrarModal);
if (btnVolverModal) btnVolverModal.addEventListener("click", cerrarModal);

// Redirigir a US-010 / US-011
if (btnSolicitar) {
  btnSolicitar.addEventListener("click", () => {
    if (!convocatoriaSeleccionada) return;
    window.location.href = `completar-solicitud.html?convocatoria_id=${convocatoriaSeleccionada.id_convocatoria}`;
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  const data = await obtenerConvocatorias();
  renderizarTarjetas(data);
});