const API_URL = "http://127.0.0.1:8001/api";

let solicitudMock = {
  id_solicitud: 1,
  convocatoria: "Beca Universitaria de Grado 2026",
  estudiante: "Kenneth Alexander Vides García",
  estado: "borrador",
  formularioCompleto: true,
  documentosCargados: true
};

const checklistEl = document.getElementById("checklist-requisitos");
const btnEnviar = document.getElementById("btn-enviar-solicitud");
const modal = document.getElementById("modal-confirmacion");
const btnConfirmar = document.getElementById("btn-confirmar-envio");
const btnCancelar = document.getElementById("btn-cancelar-modal");
const alertBox = document.getElementById("alert-box");

function mostrarMensaje(texto, tipo) {
  alertBox.className = `alert alert-${tipo}`;
  alertBox.textContent = texto;
  alertBox.classList.remove("hidden");
  setTimeout(() => alertBox.classList.add("hidden"), 4500);
}

function renderizarSolicitud(datos) {
  document.getElementById("info-id").textContent = `#${datos.id_solicitud}`;
  document.getElementById("info-convocatoria").textContent = datos.convocatoria;
  document.getElementById("info-estudiante").textContent = datos.estudiante;

  const estadoBadge = document.getElementById("info-estado");
  estadoBadge.textContent = datos.estado.toUpperCase();
  if (datos.estado === "enviada") {
    estadoBadge.className = "badge badge-enviada";
  }

  checklistEl.innerHTML = `
    <li class="${datos.formularioCompleto ? 'item-completo' : 'item-incompleto'}">
      <span>1. Formulario socioeconómico y académico completo (US-011)</span>
      <strong>${datos.formularioCompleto ? 'COMPLETO' : 'PENDIENTE'}</strong>
    </li>
    <li class="${datos.documentosCargados ? 'item-completo' : 'item-incompleto'}">
      <span>2. Expediente de documentación cargado (US-014)</span>
      <strong>${datos.documentosCargados ? 'COMPLETO' : 'PENDIENTE'}</strong>
    </li>
  `;

  const listoParaEnviar = datos.formularioCompleto && datos.documentosCargados && datos.estado === "borrador";
  btnEnviar.disabled = !listoParaEnviar;

  if (datos.estado === "enviada") {
    btnEnviar.textContent = "Solicitud Enviada (Bloqueada)";
    btnEnviar.disabled = true;
  }
}

btnEnviar.addEventListener("click", () => {
  modal.classList.remove("hidden");
});

btnCancelar.addEventListener("click", () => {
  modal.classList.add("hidden");
});

btnConfirmar.addEventListener("click", async () => {
  modal.classList.add("hidden");

  try {
    const token = localStorage.getItem("token") || localStorage.getItem("access_token");

    const respuesta = await fetch(`${API_URL}/solicitudes/${solicitudMock.id_solicitud}/enviar`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { "Authorization": `Bearer ${token}` } : {})
      }
    });

    if (respuesta.ok) {
      solicitudMock.estado = "enviada";
      renderizarSolicitud(solicitudMock);
      mostrarMensaje("Solicitud enviada formalmente al comité evaluador.", "success");
    } else {
      solicitudMock.estado = "enviada";
      renderizarSolicitud(solicitudMock);
      mostrarMensaje("Envío procesado en modo local (Mock activo). Edición bloqueada.", "success");
    }
  } catch (err) {
    solicitudMock.estado = "enviada";
    renderizarSolicitud(solicitudMock);
    mostrarMensaje("Envío registrado localmente. La solicitud no admitirá modificaciones.", "success");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  renderizarSolicitud(solicitudMock);
});