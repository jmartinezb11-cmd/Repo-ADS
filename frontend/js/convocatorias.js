const API_URL = "http://127.0.0.1:8001/api/convocatorias";

// Mocks de prueba acordados con el equipo para US-008
const mockConvocatorias = [
  {
    id_convocatoria: 1,
    titulo: "Beca a la Excelencia Universitaria 2026",
    descripcion: "Dirigida a estudiantes con promedios sobresalientes para apoyo de colegiatura.",
    fecha_inicio: "2026-02-01",
    fecha_fin: "2026-03-31",
    requisitos: "Promedio mínimo de 85 puntos, estar inscrito legalmente y no tener sanciones.",
    estado: "publicada"
  },
  {
    id_convocatoria: 2,
    titulo: "Beca de Apoyo Socioeconómico Regional",
    descripcion: "Fondo especial destinado a estudiantes con limitaciones económicas comprobables.",
    fecha_inicio: "2026-02-15",
    fecha_fin: "2026-04-10",
    requisitos: "Constancia de ingresos familiares, estudio socioeconómico y formulario completo.",
    estado: "publicada"
  }
];

const contenedor = document.getElementById("lista-convocatorias");
const modal = document.getElementById("modal-detalle");
const btnCerrarModal = document.getElementById("btn-cerrar-modal");
const btnVolverModal = document.getElementById("btn-volver-modal");

async function obtenerConvocatorias() {
  try {
    const respuesta = await fetch(`${API_URL}/`);
    if (respuesta.ok) {
      const datos = await respuesta.json();
      return datos.filter(c => c.estado === "publicada");
    }
  } catch (error) {
    console.warn("Backend no disponible. Utilizando datos mock.");
  }
  return mockConvocatorias;
}

function renderizarTarjetas(convocatorias) {
  contenedor.innerHTML = "";
  if (!convocatorias.length) {
    contenedor.innerHTML = "<p>No hay convocatorias publicadas en este momento.</p>";
    return;
  }

  convocatorias.forEach(item => {
    const card = document.createElement("article");
    card.className = "convocatoria-card";
    card.innerHTML = `
      <div>
        <h3 class="card-title">${item.titulo}</h3>
        <span class="badge badge-publicada">${item.estado}</span>
        <p class="fechas-info"><strong>Cierre:</strong> ${item.fecha_fin}</p>
        <p class="card-desc">${item.descripcion}</p>
      </div>
      <button class="btn-primary" onclick="abrirDetalle(${item.id_convocatoria})">Ver Detalles</button>
    `;
    contenedor.appendChild(card);
  });
}

window.abrirDetalle = async function(id) {
  const convocatorias = await obtenerConvocatorias();
  const conv = convocatorias.find(c => c.id_convocatoria === id);
  if (!conv) return;

  document.getElementById("modal-titulo").textContent = conv.titulo;
  document.getElementById("modal-estado").textContent = conv.estado;
  document.getElementById("modal-fechas").textContent = `Del ${conv.fecha_inicio} al ${conv.fecha_fin}`;
  document.getElementById("modal-descripcion").textContent = conv.descripcion;
  document.getElementById("modal-requisitos").textContent = conv.requisitos;

  modal.classList.remove("hidden");
};

function cerrarModal() {
  modal.classList.add("hidden");
}

btnCerrarModal.addEventListener("click", cerrarModal);
btnVolverModal.addEventListener("click", cerrarModal);

document.addEventListener("DOMContentLoaded", async () => {
  const data = await obtenerConvocatorias();
  renderizarTarjetas(data);
});