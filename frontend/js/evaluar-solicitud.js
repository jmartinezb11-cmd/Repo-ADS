const API_EVALUACIONES = "http://127.0.0.1:8001/api/evaluaciones";
const API_DOCUMENTOS = "http://127.0.0.1:8001/api/documentos";

const listaAsignaciones = document.getElementById("lista-asignaciones");
const seccionDetalle = document.getElementById("seccion-detalle");
const tituloDetalle = document.getElementById("titulo-detalle");
const resumenSolicitud = document.getElementById("resumen-solicitud");
const informacionSolicitud = document.getElementById("informacion-solicitud");
const listaDocumentos = document.getElementById("lista-documentos");
const resultadoEvaluacion = document.getElementById("resultado-evaluacion");
const formEvaluar = document.getElementById("form-evaluar");
const inputPuntaje = document.getElementById("input-puntaje");
const selectRecomendacion = document.getElementById("select-recomendacion");
const btnEvaluar = document.getElementById("btn-evaluar");
const btnCerrarDetalle = document.getElementById("btn-cerrar-detalle");
const mensaje = document.getElementById("mensaje");

// Evaluación que se está mostrando en el detalle
let idEvaluacionActual = null;


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


function formatearFecha(fecha) {
    if (!fecha) {
        return "No disponible";
    }

    return new Date(fecha).toLocaleString("es-GT");
}


function textoDeError(resultado, textoPorDefecto) {
    // FastAPI devuelve "detail" como texto (400, 403, 404) o lista (422).
    if (typeof resultado.detail === "string") {
        return resultado.detail;
    }

    if (Array.isArray(resultado.detail)) {
        return resultado.detail.map((error) => error.msg).join(" ");
    }

    return textoPorDefecto;
}


async function pedir(url, opciones = {}) {
    const response = await fetch(url, {
        ...opciones,
        headers: {
            ...(opciones.headers || {}),
            "Authorization": `Bearer ${obtenerToken()}`
        }
    });

    if (response.status === 401) {
        cerrarSesion();
        return null;
    }

    return response;
}


async function pedirJson(url, opciones, textoPorDefecto) {
    const response = await pedir(url, opciones);

    if (response === null) {
        return null;
    }

    const resultado = await response.json();

    if (!response.ok) {
        throw new Error(textoDeError(resultado, textoPorDefecto));
    }

    return resultado;
}


function crearElemento(etiqueta, clase, texto) {
    const elemento = document.createElement(etiqueta);

    if (clase) {
        elemento.className = clase;
    }

    if (texto !== undefined) {
        elemento.textContent = texto;
    }

    return elemento;
}


function agregarFila(contenedor, etiqueta, valor) {
    const fila = crearElemento("p", "fila");
    const negrita = crearElemento("strong", null, `${etiqueta}:`);

    fila.appendChild(negrita);
    // textContent evita que texto escrito por el estudiante
    // se interprete como HTML.
    fila.appendChild(document.createTextNode(
        valor === null || valor === undefined ? "No disponible" : valor
    ));

    contenedor.appendChild(fila);
}


// ---------- Lista de asignaciones ----------

async function cargarAsignaciones() {
    limpiarMensaje();

    // Basta con tener token: sessionStorage es propio de cada pestaña.
    // El backend valida de todos modos que seas evaluador.
    if (!obtenerToken()) {
        window.location.href = "login.html";
        return;
    }

    const usuario = obtenerUsuario();

    if (usuario && usuario.rol !== "evaluador") {
        mostrarMensaje(
            "Esta sección está disponible únicamente para evaluadores.",
            "error"
        );
        listaAsignaciones.innerHTML = "";
        return;
    }

    try {
        const asignaciones = await pedirJson(
            `${API_EVALUACIONES}/mis-asignaciones`,
            {},
            "No se pudieron consultar tus asignaciones."
        );

        if (asignaciones === null) {
            return;
        }

        mostrarAsignaciones(asignaciones);

    } catch (error) {
        listaAsignaciones.innerHTML = "";
        mostrarMensaje(error.message, "error");
    }
}


function mostrarAsignaciones(asignaciones) {
    listaAsignaciones.innerHTML = "";

    if (asignaciones.length === 0) {
        listaAsignaciones.appendChild(
            crearElemento("p", null, "No tienes solicitudes asignadas.")
        );
        return;
    }

    asignaciones.forEach((asignacion) => {
        const tarjeta = crearElemento("article", "tarjeta");
        const datos = crearElemento("div");

        datos.appendChild(
            crearElemento("h3", null, asignacion.convocatoria)
        );
        datos.appendChild(
            crearElemento(
                "p", null, `Solicitud #${asignacion.id_solicitud}`
            )
        );
        datos.appendChild(
            crearElemento(
                "p", null,
                `Asignada: ${formatearFecha(asignacion.fecha_asignacion)}`
            )
        );

        const estado = crearElemento(
            "span", `etiqueta ${asignacion.estado}`, asignacion.estado
        );
        datos.appendChild(estado);

        const boton = crearElemento(
            "button",
            "btn-principal btn-pequeno",
            asignacion.estado === "evaluada" ? "Ver resultado" : "Evaluar"
        );
        boton.type = "button";
        boton.addEventListener("click", () => {
            abrirEvaluacion(asignacion.id_evaluacion);
        });

        tarjeta.appendChild(datos);
        tarjeta.appendChild(boton);
        listaAsignaciones.appendChild(tarjeta);
    });
}


// ---------- Detalle de la solicitud ----------

async function abrirEvaluacion(idEvaluacion) {
    limpiarMensaje();

    try {
        const resultado = await pedirJson(
            `${API_EVALUACIONES}/${idEvaluacion}`,
            {},
            "No se pudo consultar la evaluación."
        );

        if (resultado === null) {
            return;
        }

        idEvaluacionActual = idEvaluacion;

        mostrarResumen(resultado.solicitud);
        mostrarInformacion(resultado.detalle);
        mostrarFormulario(resultado.evaluacion);

        seccionDetalle.classList.remove("oculto");
        seccionDetalle.scrollIntoView({ behavior: "smooth" });

        cargarDocumentos(resultado.solicitud.id_solicitud);

    } catch (error) {
        mostrarMensaje(error.message, "error");
    }
}


function mostrarResumen(solicitud) {
    tituloDetalle.textContent = `Solicitud #${solicitud.id_solicitud}`;
    resumenSolicitud.innerHTML = "";

    agregarFila(resumenSolicitud, "Estudiante", solicitud.estudiante);
    agregarFila(resumenSolicitud, "Convocatoria", solicitud.convocatoria);
    agregarFila(resumenSolicitud, "Estado de la solicitud", solicitud.estado);
}


function mostrarInformacion(detalle) {
    informacionSolicitud.innerHTML = "";

    if (!detalle) {
        const aviso = crearElemento("div", "grupo");
        aviso.appendChild(
            crearElemento(
                "p", null,
                "El estudiante todavía no completó la información " +
                "de la solicitud."
            )
        );
        informacionSolicitud.appendChild(aviso);
        return;
    }

    const grupos = [
        {
            titulo: "Información socioeconómica",
            filas: [
                ["Situación económica", detalle.situacion_economica],
                ["Ingresos familiares", `Q${detalle.ingresos_familiares}`],
                ["Integrantes del hogar", detalle.integrantes_hogar],
                ["Dependientes económicos", detalle.dependientes_economicos],
                ["Ocupación del responsable", detalle.ocupacion_responsable]
            ]
        },
        {
            titulo: "Información académica",
            filas: [
                ["Institución", detalle.institucion_educativa],
                ["Carrera o área", detalle.carrera_area],
                ["Grado/Semestre", detalle.grado_semestre],
                ["Promedio", detalle.promedio_academico]
            ]
        },
        {
            titulo: "Motivación y metas",
            filas: [
                ["Motivación", detalle.motivacion],
                ["Meta académica", detalle.meta_academica]
            ]
        }
    ];

    grupos.forEach((grupo) => {
        const contenedor = crearElemento("div", "grupo");
        contenedor.appendChild(crearElemento("h3", null, grupo.titulo));

        grupo.filas.forEach(([etiqueta, valor]) => {
            agregarFila(contenedor, etiqueta, valor);
        });

        informacionSolicitud.appendChild(contenedor);
    });
}


// ---------- Documentos ----------

async function cargarDocumentos(idSolicitud) {
    listaDocumentos.innerHTML = "";
    listaDocumentos.appendChild(crearElemento("p", null, "Cargando..."));

    try {
        const documentos = await pedirJson(
            `${API_DOCUMENTOS}/revision/solicitud/${idSolicitud}`,
            {},
            "No se pudieron consultar los documentos."
        );

        if (documentos === null) {
            return;
        }

        mostrarDocumentos(documentos);

    } catch (error) {
        listaDocumentos.innerHTML = "";
        listaDocumentos.appendChild(
            crearElemento("p", null, error.message)
        );
    }
}


function mostrarDocumentos(documentos) {
    listaDocumentos.innerHTML = "";

    if (documentos.length === 0) {
        listaDocumentos.appendChild(
            crearElemento("p", null, "La solicitud no tiene documentos.")
        );
        return;
    }

    documentos.forEach((documento) => {
        const fila = crearElemento("div", "documento");
        const datos = crearElemento("div");

        datos.appendChild(crearElemento("strong", null, documento.nombre_archivo));

        const detalle = crearElemento(
            "p", null, `Cargado: ${formatearFecha(documento.fecha_carga)} `
        );
        detalle.appendChild(
            crearElemento(
                "span",
                `etiqueta ${documento.estado_validacion}`,
                documento.estado_validacion
            )
        );
        datos.appendChild(detalle);

        if (documento.comentario_validacion) {
            datos.appendChild(
                crearElemento(
                    "p", null, `Comentario: ${documento.comentario_validacion}`
                )
            );
        }

        const boton = crearElemento(
            "button", "btn-principal btn-pequeno", "Abrir PDF"
        );
        boton.type = "button";
        boton.addEventListener("click", () => {
            abrirDocumento(documento.id_documento);
        });

        fila.appendChild(datos);
        fila.appendChild(boton);
        listaDocumentos.appendChild(fila);
    });
}


async function abrirDocumento(idDocumento) {
    limpiarMensaje();

    // Se abre la pestaña antes de la petición para que el navegador
    // no la bloquee como ventana emergente.
    const ventana = window.open("", "_blank");

    try {
        const response = await pedir(`${API_DOCUMENTOS}/${idDocumento}/archivo`);

        if (response === null) {
            if (ventana) {
                ventana.close();
            }
            return;
        }

        if (!response.ok) {
            const resultado = await response.json();
            throw new Error(
                textoDeError(resultado, "No se pudo abrir el documento.")
            );
        }

        const archivo = await response.blob();
        const direccion = URL.createObjectURL(archivo);

        if (ventana) {
            ventana.location = direccion;
        } else {
            window.location.href = direccion;
        }

    } catch (error) {
        if (ventana) {
            ventana.close();
        }
        mostrarMensaje(error.message, "error");
    }
}


// ---------- Evaluación ----------

function mostrarFormulario(evaluacion) {
    resultadoEvaluacion.innerHTML = "";

    if (evaluacion.estado === "evaluada") {
        resultadoEvaluacion.appendChild(
            crearElemento("strong", null, "Evaluación registrada")
        );
        agregarFila(resultadoEvaluacion, "Puntaje", evaluacion.puntaje);
        agregarFila(
            resultadoEvaluacion, "Recomendación", evaluacion.recomendacion
        );
        agregarFila(
            resultadoEvaluacion, "Fecha",
            formatearFecha(evaluacion.fecha_evaluacion)
        );
        resultadoEvaluacion.classList.remove("oculto");

        inputPuntaje.value = evaluacion.puntaje;
        selectRecomendacion.value = evaluacion.recomendacion;

        inputPuntaje.disabled = true;
        selectRecomendacion.disabled = true;
        btnEvaluar.disabled = true;
        return;
    }

    resultadoEvaluacion.classList.add("oculto");

    formEvaluar.reset();
    inputPuntaje.disabled = false;
    selectRecomendacion.disabled = false;
    btnEvaluar.disabled = false;
}


async function registrarEvaluacion(evento) {
    evento.preventDefault();
    limpiarMensaje();

    const textoPuntaje = inputPuntaje.value.trim();
    const recomendacion = selectRecomendacion.value;

    if (textoPuntaje === "") {
        mostrarMensaje("Escribe un puntaje.", "error");
        return;
    }

    const puntaje = Number(textoPuntaje);

    if (!Number.isInteger(puntaje) || puntaje < 0 || puntaje > 100) {
        mostrarMensaje(
            "El puntaje debe ser un número entero entre 0 y 100.",
            "error"
        );
        return;
    }

    if (!recomendacion) {
        mostrarMensaje("Selecciona una recomendación.", "error");
        return;
    }

    btnEvaluar.disabled = true;
    btnEvaluar.textContent = "Registrando...";

    try {
        const resultado = await pedirJson(
            `${API_EVALUACIONES}/${idEvaluacionActual}/evaluar`,
            {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ puntaje, recomendacion })
            },
            "No se pudo registrar la evaluación."
        );

        if (resultado === null) {
            return;
        }

        // Primero se refresca la lista (esto limpia mensajes)
        // y después se muestra el mensaje de éxito.
        cargarAsignaciones();
        mostrarMensaje("Evaluación registrada correctamente.", "exito");
        mostrarFormulario(resultado);

    } catch (error) {
        mostrarMensaje(error.message, "error");
        btnEvaluar.disabled = false;

    } finally {
        btnEvaluar.textContent = "Registrar evaluación";
    }
}


btnCerrarDetalle.addEventListener("click", () => {
    seccionDetalle.classList.add("oculto");
    idEvaluacionActual = null;
});

formEvaluar.addEventListener("submit", registrarEvaluacion);

cargarAsignaciones();