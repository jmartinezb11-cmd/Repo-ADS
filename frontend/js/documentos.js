const API_SOLICITUDES = "http://127.0.0.1:8001/api/solicitudes";
const API_DOCUMENTOS = "http://127.0.0.1:8001/api/documentos";

const TAMANIO_MAXIMO_BYTES = 5 * 1024 * 1024; // 5 MB

const selectSolicitud = document.getElementById("select-solicitud");
const seccionSubir = document.getElementById("seccion-subir");
const seccionLista = document.getElementById("seccion-lista");
const formSubir = document.getElementById("form-subir");
const inputArchivo = document.getElementById("input-archivo");
const btnSubir = document.getElementById("btn-subir");
const listaDocumentos = document.getElementById("lista-documentos");
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


function formatearFecha(fecha) {
    if (!fecha) {
        return "No disponible";
    }

    return new Date(fecha).toLocaleString("es-GT");
}


function cerrarSesion() {
    localStorage.removeItem("token");
    sessionStorage.removeItem("usuario");
    window.location.href = "login.html";
}


async function cargarSolicitudes() {
    limpiarMensaje();

    const token = obtenerToken();
    const usuario = obtenerUsuario();

    // Basta con tener token: sessionStorage es propio de cada pestaña,
    // así que "usuario" puede faltar si se abrió esta página en otra
    // pestaña. El backend valida el rol de todos modos.
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    if (usuario && usuario.rol !== "estudiante") {
        mostrarMensaje(
            "Esta sección está disponible únicamente para estudiantes.",
            "error"
        );
        selectSolicitud.innerHTML = "";
        selectSolicitud.disabled = true;
        return;
    }

    try {
        const response = await fetch(
            `${API_SOLICITUDES}/mis-solicitudes`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {
            cerrarSesion();
            return;
        }

        const resultado = await response.json();

        if (!response.ok) {
            throw new Error(
                resultado.detail ||
                "No se pudieron consultar tus solicitudes."
            );
        }

        llenarSelect(resultado.solicitudes);

    } catch (error) {
        selectSolicitud.innerHTML = "";
        mostrarMensaje(error.message, "error");
    }
}


function llenarSelect(solicitudes) {
    selectSolicitud.innerHTML = "";

    if (!solicitudes || solicitudes.length === 0) {
        selectSolicitud.innerHTML =
            "<option value=''>No tienes solicitudes registradas</option>";
        return;
    }

    const opcionInicial = document.createElement("option");
    opcionInicial.value = "";
    opcionInicial.textContent = "-- Selecciona una solicitud --";
    selectSolicitud.appendChild(opcionInicial);

    solicitudes.forEach((solicitud) => {
        const opcion = document.createElement("option");
        opcion.value = solicitud.id_solicitud;
        opcion.textContent =
            `Solicitud #${solicitud.id_solicitud} - ` +
            `${solicitud.convocatoria} (${solicitud.estado})`;
        selectSolicitud.appendChild(opcion);
    });

    // Permite abrir la página con ?solicitud=ID ya seleccionada
    const parametros = new URLSearchParams(window.location.search);
    const idPreseleccionado = parametros.get("solicitud");

    if (idPreseleccionado) {
        selectSolicitud.value = idPreseleccionado;

        if (selectSolicitud.value === idPreseleccionado) {
            alCambiarSolicitud();
        }
    }
}


function alCambiarSolicitud() {
    limpiarMensaje();

    const idSolicitud = selectSolicitud.value;

    if (!idSolicitud) {
        seccionSubir.classList.add("oculto");
        seccionLista.classList.add("oculto");
        return;
    }

    seccionSubir.classList.remove("oculto");
    seccionLista.classList.remove("oculto");

    cargarDocumentos(idSolicitud);
}


// US-015 - Consultar documentos
async function cargarDocumentos(idSolicitud) {
    listaDocumentos.innerHTML = "<p>Cargando documentos...</p>";

    try {
        const response = await fetch(
            `${API_DOCUMENTOS}/solicitud/${idSolicitud}`,
            {
                headers: {
                    "Authorization": `Bearer ${obtenerToken()}`
                }
            }
        );

        if (response.status === 401) {
            cerrarSesion();
            return;
        }

        const resultado = await response.json();

        if (!response.ok) {
            throw new Error(
                resultado.detail ||
                "No se pudieron consultar los documentos."
            );
        }

        mostrarDocumentos(resultado);

    } catch (error) {
        listaDocumentos.innerHTML = "";
        mostrarMensaje(error.message, "error");
    }
}


function mostrarDocumentos(documentos) {
    listaDocumentos.innerHTML = "";

    if (!documentos || documentos.length === 0) {
        listaDocumentos.innerHTML =
            "<p>Esta solicitud todavía no tiene documentos cargados.</p>";
        return;
    }

    const tabla = document.createElement("table");
    tabla.className = "tabla";

    tabla.innerHTML = `
        <thead>
            <tr>
                <th>Nombre del archivo</th>
                <th>Tipo</th>
                <th>Fecha de carga</th>
            </tr>
        </thead>
    `;

    const cuerpo = document.createElement("tbody");

    documentos.forEach((documento) => {
        const fila = document.createElement("tr");

        // textContent evita que un nombre de archivo malicioso
        // se interprete como HTML.
        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = documento.nombre_archivo;

        const celdaTipo = document.createElement("td");
        const etiqueta = document.createElement("span");
        etiqueta.className = "etiqueta";
        etiqueta.textContent = documento.tipo_archivo;
        celdaTipo.appendChild(etiqueta);

        const celdaFecha = document.createElement("td");
        celdaFecha.textContent = formatearFecha(documento.fecha_carga);

        fila.appendChild(celdaNombre);
        fila.appendChild(celdaTipo);
        fila.appendChild(celdaFecha);
        cuerpo.appendChild(fila);
    });

    tabla.appendChild(cuerpo);
    listaDocumentos.appendChild(tabla);
}


// US-014 - Cargar documentación
async function subirDocumento(evento) {
    evento.preventDefault();
    limpiarMensaje();

    const idSolicitud = selectSolicitud.value;
    const archivo = inputArchivo.files[0];

    if (!idSolicitud) {
        mostrarMensaje("Selecciona una solicitud.", "error");
        return;
    }

    if (!archivo) {
        mostrarMensaje("Selecciona un archivo PDF.", "error");
        return;
    }

    if (!archivo.name.toLowerCase().endsWith(".pdf")) {
        mostrarMensaje("Solo se permiten archivos en formato PDF.", "error");
        return;
    }

    if (archivo.size > TAMANIO_MAXIMO_BYTES) {
        mostrarMensaje("El archivo no puede superar los 5 MB.", "error");
        return;
    }

    const datos = new FormData();
    datos.append("archivo", archivo);

    btnSubir.disabled = true;
    btnSubir.textContent = "Subiendo...";

    try {
        const response = await fetch(
            `${API_DOCUMENTOS}/solicitud/${idSolicitud}`,
            {
                method: "POST",
                headers: {
                    // No se define Content-Type: el navegador lo hace
                    // solo y agrega el "boundary" que necesita FormData.
                    "Authorization": `Bearer ${obtenerToken()}`
                },
                body: datos
            }
        );

        if (response.status === 401) {
            cerrarSesion();
            return;
        }

        const resultado = await response.json();

        if (!response.ok) {
            throw new Error(
                resultado.detail ||
                "No se pudo cargar el documento."
            );
        }

        mostrarMensaje("Documento cargado correctamente.", "exito");
        formSubir.reset();
        cargarDocumentos(idSolicitud);

    } catch (error) {
        mostrarMensaje(error.message, "error");

    } finally {
        btnSubir.disabled = false;
        btnSubir.textContent = "Subir documento";
    }
}


selectSolicitud.addEventListener("change", alCambiarSolicitud);
formSubir.addEventListener("submit", subirDocumento);

cargarSolicitudes();