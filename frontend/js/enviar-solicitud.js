
const API_URL = "http://127.0.0.1:8001/api";

const checklistEl = document.getElementById("checklist-requisitos");
const btnEnviar = document.getElementById("btn-enviar-solicitud");
const modal = document.getElementById("modal-confirmacion");
const btnConfirmar = document.getElementById("btn-confirmar-envio");
const btnCancelar = document.getElementById("btn-cancelar-modal");
const alertBox = document.getElementById("alert-box");

let solicitudSeleccionada = null;

function mostrarMensaje(texto, tipo) {
    alertBox.textContent = texto;
    alertBox.className = `alert alert-${tipo}`;
    alertBox.classList.remove("hidden");
}

async function consultarAPI(ruta, opciones = {}) {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "login.html";
        throw new Error("Debes iniciar sesión.");
    }

    const respuesta = await fetch(`${API_URL}${ruta}`, {
        ...opciones,
        headers: {
            Authorization: `Bearer ${token}`,
            ...(opciones.headers || {})
        }
    });

    const datos = await respuesta.json();

    if (!respuesta.ok) {
        const detalle = datos.detail;
        throw new Error(
            typeof detalle === "string"
                ? detalle
                : "No se pudo completar la operación."
        );
    }

    return datos;
}

function agregarRequisito(texto, completo) {
    const item = document.createElement("li");
    item.className = completo ? "item-completo" : "item-incompleto";

    const descripcion = document.createElement("span");
    descripcion.textContent = texto;

    const estado = document.createElement("strong");
    estado.textContent = completo ? "COMPLETO" : "PENDIENTE";

    item.append(descripcion, estado);
    checklistEl.appendChild(item);
}

async function cargarSolicitud() {
    btnEnviar.disabled = true;
    checklistEl.innerHTML = "";

    try {
        const parametros = new URLSearchParams(window.location.search);
        const idSolicitado = Number(parametros.get("solicitud"));

        const resultado = await consultarAPI("/solicitudes/mis-solicitudes");
        const solicitudes = resultado.solicitudes || [];

        if (solicitudes.length === 0) {
            mostrarMensaje("No tienes solicitudes registradas.", "error");
            return;
        }

        const solicitud = idSolicitado
            ? solicitudes.find(s => s.id_solicitud === idSolicitado)
            : solicitudes.length === 1 ? solicitudes[0] : null;

        if (!solicitud) {
            mostrarMensaje(
                "Selecciona una solicitud desde Mis solicitudes.",
                "error"
            );
            return;
        }

        solicitudSeleccionada = solicitud;

        document.getElementById("info-id").textContent =
            `#${solicitud.id_solicitud}`;

        document.getElementById("info-convocatoria").textContent =
            solicitud.convocatoria;

        const usuario = JSON.parse(
            sessionStorage.getItem("usuario") || "null"
        );

        document.getElementById("info-estudiante").textContent =
            usuario?.nombre || usuario?.correo || `Estudiante #${solicitud.id_estudiante}`;

        document.getElementById("info-estado").textContent =
            solicitud.estado.toUpperCase();

        const [expediente, documentos] = await Promise.all([
            consultarAPI(`/solicitudes/${solicitud.id_solicitud}`),
            consultarAPI(`/documentos/solicitud/${solicitud.id_solicitud}`)
        ]);

        const formularioCompleto = expediente.detalle !== null;
        const documentosCargados = documentos.length > 0;

        agregarRequisito(
            "Formulario socioeconómico y académico completo (US-011)",
            formularioCompleto
        );

        agregarRequisito(
            "Expediente de documentación cargado (US-014)",
            documentosCargados
        );

        const puedeEnviar =
            solicitud.estado === "pendiente" &&
            formularioCompleto &&
            documentosCargados;

        btnEnviar.disabled = !puedeEnviar;

        if (solicitud.estado === "enviada") {
            btnEnviar.textContent = "Solicitud enviada";
        } else if (["aprobada", "rechazada"].includes(solicitud.estado)) {
            btnEnviar.textContent = "Solicitud resuelta";
        } else {
            btnEnviar.textContent = "Enviar Solicitud Definitiva";
        }

    } catch (error) {
        mostrarMensaje(error.message, "error");
    }
}

btnEnviar.addEventListener("click", () => {
    if (solicitudSeleccionada && !btnEnviar.disabled) {
        modal.classList.remove("hidden");
    }
});

btnCancelar.addEventListener("click", () => {
    modal.classList.add("hidden");
});

btnConfirmar.addEventListener("click", async () => {
    modal.classList.add("hidden");

    if (!solicitudSeleccionada) return;

    btnConfirmar.disabled = true;
    btnEnviar.disabled = true;

    try {
        const resultado = await consultarAPI(
            `/solicitudes/${solicitudSeleccionada.id_solicitud}/enviar`,
            { method: "POST" }
        );

        mostrarMensaje(resultado.mensaje, "success");
        await cargarSolicitud();

    } catch (error) {
        mostrarMensaje(error.message, "error");
        await cargarSolicitud();
    } finally {
        btnConfirmar.disabled = false;
    }
});

document.addEventListener("DOMContentLoaded", cargarSolicitud);
