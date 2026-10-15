const API_EVALUACIONES = "http://127.0.0.1:8001/api/evaluaciones";

const formAsignar = document.getElementById("form-asignar");
const selectSolicitud = document.getElementById("select-solicitud");
const selectEvaluador = document.getElementById("select-evaluador");
const btnAsignar = document.getElementById("btn-asignar");
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


function mostrarMensaje(texto, tipo) {
    mensaje.textContent = texto;
    mensaje.className = `mensaje ${tipo}`;
}


function limpiarMensaje() {
    mensaje.textContent = "";
    mensaje.className = "mensaje oculto";
}


function cerrarSesion() {
    localStorage.removeItem("token");
    sessionStorage.removeItem("usuario");
    window.location.href = "login.html";
}


function textoDeError(resultado, textoPorDefecto) {
    // FastAPI devuelve "detail" como texto (400, 403) o como lista (422).
    if (typeof resultado.detail === "string") {
        return resultado.detail;
    }

    if (Array.isArray(resultado.detail)) {
        return resultado.detail.map((error) => error.msg).join(" ");
    }

    return textoPorDefecto;
}


async function obtenerLista(ruta) {
    const response = await fetch(
        `${API_EVALUACIONES}/${ruta}`,
        {
            headers: {
                "Authorization": `Bearer ${obtenerToken()}`
            }
        }
    );

    if (response.status === 401) {
        cerrarSesion();
        return null;
    }

    const resultado = await response.json();

    if (!response.ok) {
        throw new Error(
            textoDeError(resultado, "No se pudo cargar la información.")
        );
    }

    return resultado;
}


async function cargarDatos() {
    limpiarMensaje();

    // Basta con tener token: sessionStorage es propio de cada pestaña.
    // El backend valida de todos modos que seas administrador.
    if (!obtenerToken()) {
        window.location.href = "login.html";
        return;
    }

    const usuario = obtenerUsuario();

    if (usuario && usuario.rol !== "administrador") {
        mostrarMensaje(
            "Esta sección está disponible únicamente para administradores.",
            "error"
        );
        selectSolicitud.innerHTML = "";
        selectEvaluador.innerHTML = "";
        selectSolicitud.disabled = true;
        selectEvaluador.disabled = true;
        btnAsignar.disabled = true;
        return;
    }

    try {
        const [solicitudes, evaluadores] = await Promise.all([
            obtenerLista("solicitudes"),
            obtenerLista("evaluadores")
        ]);

        if (solicitudes === null || evaluadores === null) {
            return;
        }

        llenarSolicitudes(solicitudes);
        llenarEvaluadores(evaluadores);

    } catch (error) {
        selectSolicitud.innerHTML = "";
        selectEvaluador.innerHTML = "";
        selectSolicitud.disabled = true;
        selectEvaluador.disabled = true;
        btnAsignar.disabled = true;
        mostrarMensaje(error.message, "error");
    }
}


function crearOpcion(valor, texto) {
    const opcion = document.createElement("option");
    opcion.value = valor;
    opcion.textContent = texto;
    return opcion;
}


function llenarSolicitudes(solicitudes) {
    selectSolicitud.innerHTML = "";

    if (solicitudes.length === 0) {
        selectSolicitud.appendChild(
            crearOpcion("", "No hay solicitudes disponibles para asignar")
        );
        selectSolicitud.disabled = true;
        btnAsignar.disabled = true;
        return;
    }

    selectSolicitud.appendChild(
        crearOpcion("", "-- Selecciona una solicitud --")
    );

    solicitudes.forEach((solicitud) => {
        selectSolicitud.appendChild(
            crearOpcion(
                solicitud.id_solicitud,
                `Solicitud #${solicitud.id_solicitud} - ` +
                `${solicitud.estudiante} - ` +
                `${solicitud.convocatoria} (${solicitud.estado})`
            )
        );
    });
}


function llenarEvaluadores(evaluadores) {
    selectEvaluador.innerHTML = "";

    if (evaluadores.length === 0) {
        selectEvaluador.appendChild(
            crearOpcion("", "No hay evaluadores registrados")
        );
        selectEvaluador.disabled = true;
        btnAsignar.disabled = true;
        mostrarMensaje(
            "No hay usuarios con rol evaluador. Un usuario debe tener " +
            "el rol evaluador para poder recibir asignaciones.",
            "error"
        );
        return;
    }

    selectEvaluador.appendChild(
        crearOpcion("", "-- Selecciona un evaluador --")
    );

    evaluadores.forEach((evaluador) => {
        selectEvaluador.appendChild(
            crearOpcion(
                evaluador.id_evaluador,
                `${evaluador.nombre} (${evaluador.email})`
            )
        );
    });
}


async function asignarEvaluacion(evento) {
    evento.preventDefault();
    limpiarMensaje();

    const idSolicitud = selectSolicitud.value;
    const idEvaluador = selectEvaluador.value;

    if (!idSolicitud) {
        mostrarMensaje("Selecciona una solicitud.", "error");
        return;
    }

    if (!idEvaluador) {
        mostrarMensaje("Selecciona un evaluador.", "error");
        return;
    }

    const textoEvaluador =
        selectEvaluador.options[selectEvaluador.selectedIndex].textContent;

    btnAsignar.disabled = true;
    btnAsignar.textContent = "Asignando...";

    try {
        const response = await fetch(
            API_EVALUACIONES,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${obtenerToken()}`
                },
                body: JSON.stringify({
                    id_solicitud: Number(idSolicitud),
                    id_evaluador: Number(idEvaluador)
                })
            }
        );

        if (response.status === 401) {
            cerrarSesion();
            return;
        }

        const resultado = await response.json();

        if (!response.ok) {
            throw new Error(
                textoDeError(resultado, "No se pudo asignar la evaluación.")
            );
        }

        mostrarMensaje(
            `Solicitud #${resultado.id_solicitud} asignada a ` +
            `${textoEvaluador}.`,
            "exito"
        );

        selectSolicitud.value = "";
        selectEvaluador.value = "";

    } catch (error) {
        mostrarMensaje(error.message, "error");

    } finally {
        btnAsignar.disabled = false;
        btnAsignar.textContent = "Asignar evaluación";
    }
}


formAsignar.addEventListener("submit", asignarEvaluacion);

cargarDatos();