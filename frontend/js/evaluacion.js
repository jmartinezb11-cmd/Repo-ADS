const API_URL = "http://127.0.0.1:8001/api";

// Datos simulados (Mock) para autonomía total mientras se integran los endpoints
let mockEvaluacion = {
  id_solicitud: 1,
  estudiante: "Kenneth Alexander Vides García",
  convocatoria: "Beca Universitaria a la Excelencia Académica 2026",
  puntaje: 85,
  estado: "En Proceso",
  observaciones: [
    {
      id: 1,
      tipo: "DOCUMENTACION",
      comentario: "Constancia de ingresos legible, pendiente verificar sello institucional.",
      fecha: "2026-10-15 14:30"
    }
  ]
};

const solicituIdEl = document.getElementById("eval-solicitud-id");
const estudianteEl = document.getElementById("eval-estudiante");
const convocatoriaEl = document.getElementById("eval-convocatoria");
const puntajeEl = document.getElementById("eval-puntaje");
const badgeEstadoEl = document.getElementById("badge-estado-eval");
const listaObsEl = document.getElementById("lista-observaciones");
const formObs = document.getElementById("form-observacion");
const alertBox = document.getElementById("alert-box");

function mostrarMensaje(texto, tipo = "success") {
  if (!alertBox) return;
  alertBox.className = `alert alert-${tipo}`;
  alertBox.textContent = texto;
  alertBox.classList.remove("hidden");
  setTimeout(() => alertBox.classList.add("hidden"), 4000);
}

// US-020: Consultar y renderizar datos del expediente
async function cargarEvaluacion() {
  const token = localStorage.getItem("token") || localStorage.getItem("access_token");

  try {
    const res = await fetch(`${API_URL}/evaluaciones/solicitud/1`, {
      headers: {
        ...(token ? { "Authorization": `Bearer ${token}` } : {})
      }
    });

    if (res.ok) {
      const data = await res.json();
      renderizarDatos(data);
      return;
    }
  } catch (err) {
    console.warn("Backend no disponible. Cargando datos mock unificados (US-019 / US-020).");
  }

  renderizarDatos(mockEvaluacion);
}

function renderizarDatos(datos) {
  if (solicituIdEl) solicituIdEl.textContent = `#${datos.id_solicitud}`;
  if (estudianteEl) estudianteEl.textContent = datos.estudiante;
  if (convocatoriaEl) convocatoriaEl.textContent = datos.convocatoria;
  if (puntajeEl) puntajeEl.textContent = datos.puntaje;
  if (badgeEstadoEl) {
    badgeEstadoEl.textContent = datos.estado;
    badgeEstadoEl.className = datos.estado.toLowerCase() === "aprobada" 
      ? "badge badge-evaluado" 
      : "badge badge-pendiente";
  }

  renderizarObservaciones(datos.observaciones || []);
}

function renderizarObservaciones(lista) {
  if (!listaObsEl) return;
  listaObsEl.innerHTML = "";

  if (lista.length === 0) {
    listaObsEl.innerHTML = `<p style="color: #64748b;">No hay observaciones registradas aún.</p>`;
    return;
  }

  lista.forEach(obs => {
    const item = document.createElement("div");
    item.className = "item-obs";
    item.innerHTML = `
      <div class="item-obs-header">
        <strong>${obs.tipo}</strong>
        <small>${obs.fecha}</small>
      </div>
      <p style="margin: 0;">${obs.comentario}</p>
    `;
    listaObsEl.appendChild(item);
  });
}

// US-019: Registrar nueva observación
formObs?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const tipo = document.getElementById("tipo-obs").value;
  const comentario = document.getElementById("texto-obs").value.trim();

  if (!comentario) return;

  const payload = {
    id_solicitud: mockEvaluacion.id_solicitud,
    tipo: tipo,
    comentario: comentario
  };

  const token = localStorage.getItem("token") || localStorage.getItem("access_token");

  try {
    const res = await fetch(`${API_URL}/evaluaciones/observaciones`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { "Authorization": `Bearer ${token}` } : {})
      },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      mostrarMensaje("Observación registrada con éxito en backend.");
      formObs.reset();
      cargarEvaluacion();
      return;
    }
  } catch (err) {
    console.warn("Backend no disponible. Guardando observación localmente en mock.");
  }

  // Guardado local reactivo
  const nuevaObs = {
    id: mockEvaluacion.observaciones.length + 1,
    tipo: tipo,
    comentario: comentario,
    fecha: new Date().toISOString().replace("T", " ").substring(0, 16)
  };

  mockEvaluacion.observaciones.unshift(nuevaObs);
  renderizarObservaciones(mockEvaluacion.observaciones);
  formObs.reset();
  mostrarMensaje("Observación agregada con éxito (Mock activo).");
});

document.addEventListener("DOMContentLoaded", cargarEvaluacion);