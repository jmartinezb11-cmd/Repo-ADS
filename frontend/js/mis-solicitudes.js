const API_URL = "http://127.0.0.1:8001/api/solicitudes";

const listaSolicitudes = document.getElementById("lista-solicitudes");
const seccionDetalle = document.getElementById("seccion-detalle");
const contenidoDetalle = document.getElementById("contenido-detalle");
const btnCerrarDetalle = document.getElementById("btn-cerrar-detalle");
const mensaje = document.getElementById("mensaje");


function obtenerToken() {
    return localStorage.getItem("token");
}


function obtenerUsuario() {
    try {
        return JSON.parse(sessionStorage.getItem("usuario"));
    } catch {
        return null;
    }
}


function mostrarError(texto) {
    mensaje.textContent = texto;
    mensaje.classList.remove("oculto");
}


function limpiarError() {
    mensaje.textContent = "";
    mensaje.classList.add("oculto");
}


function formatearFecha(fecha) {
    if (!fecha) {
        return "No disponible";
    }

    return new Date(fecha).toLocaleString("es-GT");
}


async function cargarSolicitudes() {
    limpiarError();

    const token = obtenerToken();
    const usuario = obtenerUsuario();

    if (!token || !usuario) {
        window.location.href = "login.html";
        return;
    }

    if (usuario.rol !== "estudiante") {
        mostrarError(
            "Esta sección está disponible únicamente para estudiantes."
        );
        listaSolicitudes.innerHTML = "";
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/mis-solicitudes`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {
            localStorage.removeItem("token");
            sessionStorage.removeItem("usuario");
            window.location.href = "login.html";
            return;
        }

        const resultado = await response.json();

        if (!response.ok) {
            throw new Error(
                resultado.detail ||
                "No se pudieron consultar las solicitudes."
            );
        }

        mostrarSolicitudes(resultado.solicitudes);

    } catch (error) {
        listaSolicitudes.innerHTML = "";
        mostrarError(error.message);
    }
}


function mostrarSolicitudes(solicitudes) {
    listaSolicitudes.innerHTML = "";

    if (!solicitudes || solicitudes.length === 0) {
        listaSolicitudes.innerHTML =
            "<p>No tienes solicitudes registradas.</p>";
        return;
    }

    solicitudes.forEach((solicitud) => {
        const tarjeta = document.createElement("article");
        tarjeta.className = "tarjeta-solicitud";

        tarjeta.innerHTML = `
            <h3>${solicitud.convocatoria}</h3>

            <p>
                <strong>Solicitud:</strong>
                #${solicitud.id_solicitud}
            </p>

            <p>
                <strong>Estado:</strong>
                <span class="estado">
                    ${solicitud.estado}
                </span>
            </p>

            <p>
                <strong>Creada:</strong>
                ${formatearFecha(solicitud.fecha_creacion)}
            </p>

            <p>
                <strong>Última actualización:</strong>
                ${formatearFecha(
                    solicitud.fecha_ultima_actualizacion
                )}
            </p>

            <button
                class="btn-detalle"
                data-id="${solicitud.id_solicitud}"
                type="button"
            >
                Ver detalle
            </button>
        `;

        listaSolicitudes.appendChild(tarjeta);
    });

    document.querySelectorAll(".btn-detalle").forEach((boton) => {
        boton.addEventListener("click", () => {
            cargarDetalle(boton.dataset.id);
        });
    });
}


async function cargarDetalle(idSolicitud) {
    limpiarError();

    const token = obtenerToken();

    try {
        const response = await fetch(
            `${API_URL}/${idSolicitud}`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const resultado = await response.json();

        if (!response.ok) {
            throw new Error(
                resultado.detail ||
                "No se pudo consultar la solicitud."
            );
        }

        mostrarDetalle(resultado);

    } catch (error) {
        mostrarError(error.message);
    }
}


function mostrarDetalle(resultado) {
    const solicitud = resultado.solicitud;
    const detalle = resultado.detalle;

    let html = `
        <div class="grupo-detalle">
            <h3>Información general</h3>

            <p class="fila">
                <strong>ID:</strong>
                ${solicitud.id_solicitud}
            </p>

            <p class="fila">
                <strong>Estado:</strong>
                ${solicitud.estado}
            </p>

            <p class="fila">
                <strong>Fecha de creación:</strong>
                ${formatearFecha(solicitud.fecha_creacion)}
            </p>
        </div>
    `;

    if (!detalle) {
        html += `
            <p>
                Esta solicitud todavía no tiene información
                complementaria registrada.
            </p>
        `;
    } else {
        html += `
            <div class="grupo-detalle">
                <h3>Información socioeconómica</h3>

                <p class="fila">
                    <strong>Situación económica:</strong>
                    ${detalle.situacion_economica}
                </p>

                <p class="fila">
                    <strong>Ingresos familiares:</strong>
                    Q${detalle.ingresos_familiares}
                </p>

                <p class="fila">
                    <strong>Integrantes del hogar:</strong>
                    ${detalle.integrantes_hogar}
                </p>

                <p class="fila">
                    <strong>Dependientes económicos:</strong>
                    ${detalle.dependientes_economicos}
                </p>

                <p class="fila">
                    <strong>Ocupación del responsable:</strong>
                    ${detalle.ocupacion_responsable}
                </p>
            </div>

            <div class="grupo-detalle">
                <h3>Información académica</h3>

                <p class="fila">
                    <strong>Institución:</strong>
                    ${detalle.institucion_educativa}
                </p>

                <p class="fila">
                    <strong>Carrera o área:</strong>
                    ${detalle.carrera_area}
                </p>

                <p class="fila">
                    <strong>Grado/Semestre:</strong>
                    ${detalle.grado_semestre}
                </p>

                <p class="fila">
                    <strong>Promedio:</strong>
                    ${detalle.promedio_academico}
                </p>
            </div>

            <div class="grupo-detalle">
                <h3>Motivación</h3>

                <p>${detalle.motivacion}</p>

                <h3>Meta académica</h3>

                <p>${detalle.meta_academica}</p>
            </div>
        `;
    }

    contenidoDetalle.innerHTML = html;
    seccionDetalle.classList.remove("oculto");

    seccionDetalle.scrollIntoView({
        behavior: "smooth"
    });
}


btnCerrarDetalle.addEventListener("click", () => {
    seccionDetalle.classList.add("oculto");
});


cargarSolicitudes();