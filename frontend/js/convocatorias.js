const API_URL = "http://127.0.0.1:8001/api/convocatorias";

const contenedor = document.getElementById("lista-convocatorias");
const modal = document.getElementById("modal-detalle");
const btnCerrarModal = document.getElementById("btn-cerrar-modal");
const btnVolverModal = document.getElementById("btn-volver-modal");
const alertBox = document.getElementById("alert-box");

let convocatoriasDisponibles = [];


function mostrarError(mensaje) {
    if (alertBox) {
        alertBox.textContent = mensaje;
        alertBox.className = "alert alert-error";
        alertBox.classList.remove("hidden");
    }

    console.error(mensaje);
}


async function obtenerConvocatorias() {
    try {
        const respuesta = await fetch(`${API_URL}/`);

        if (!respuesta.ok) {
            throw new Error(
                `Error HTTP ${respuesta.status}`
            );
        }

        const datos = await respuesta.json();

        // US-008 muestra únicamente convocatorias publicadas
        return datos.filter(
            convocatoria => convocatoria.estado === "publicada"
        );

    } catch (error) {
        console.error(
            "Error al consultar convocatorias:",
            error
        );

        mostrarError(
            "No se pudieron cargar las convocatorias. Intenta nuevamente."
        );

        return [];
    }
}


function renderizarTarjetas(convocatorias) {
    contenedor.innerHTML = "";

    if (!convocatorias.length) {
        contenedor.innerHTML =
            "<p>No hay convocatorias publicadas en este momento.</p>";
        return;
    }

    convocatorias.forEach(convocatoria => {
        const card = document.createElement("article");

        card.className = "convocatoria-card";

        card.innerHTML = `
            <div>
                <h3 class="card-title">
                    ${convocatoria.titulo}
                </h3>

                <span class="badge badge-publicada">
                    ${convocatoria.estado}
                </span>

                <p class="fechas-info">
                    <strong>Apertura:</strong>
                    ${convocatoria.fecha_apertura}
                </p>

                <p class="fechas-info">
                    <strong>Cierre:</strong>
                    ${convocatoria.fecha_cierre}
                </p>

                <p class="card-desc">
                    ${convocatoria.descripcion}
                </p>
            </div>

            <button
                class="btn-primary"
                onclick="abrirDetalle(${convocatoria.id_convocatoria})"
            >
                Ver Detalles
            </button>
        `;

        contenedor.appendChild(card);
    });
}


window.abrirDetalle = function(id) {
    const convocatoria = convocatoriasDisponibles.find(
        item => item.id_convocatoria === id
    );

    if (!convocatoria) {
        mostrarError(
            "No se encontró la convocatoria seleccionada."
        );
        return;
    }

    document.getElementById("modal-titulo").textContent =
        convocatoria.titulo;

    document.getElementById("modal-estado").textContent =
        convocatoria.estado;

    document.getElementById("modal-fechas").textContent =
        `Del ${convocatoria.fecha_apertura} al ${convocatoria.fecha_cierre}`;

    document.getElementById("modal-descripcion").textContent =
        convocatoria.descripcion;

    document.getElementById("modal-requisitos").textContent =
        convocatoria.requisitos;

    modal.classList.remove("hidden");
};


function cerrarModal() {
    modal.classList.add("hidden");
}


btnCerrarModal.addEventListener(
    "click",
    cerrarModal
);

btnVolverModal.addEventListener(
    "click",
    cerrarModal
);


document.addEventListener(
    "DOMContentLoaded",
    async () => {
        convocatoriasDisponibles =
            await obtenerConvocatorias();

        renderizarTarjetas(
            convocatoriasDisponibles
        );
    }
);