const API_URL = "http://127.0.0.1:8001/api/convocatorias";

const form = document.getElementById("form-editar-convocatoria");
const alertBox = document.getElementById("alert-box");
const btnCancelar = document.getElementById("btn-cancelar");
const btnGuardar = document.getElementById("btn-guardar");

let convocatoriaActual = null;

// Mostrar mensajes

function mostrarMensaje(texto, tipo) {
    alertBox.className = `alert alert-${tipo}`;
    alertBox.textContent = texto;
    alertBox.classList.remove("hidden");
}

// Obtener ID desde la URL
// Ejemplo:
// editar-convocatoria.html?id=3

function obtenerIdConvocatoria() {
    const parametros = new URLSearchParams(window.location.search);
    return parametros.get("id");
}
// Obtener token JWT

function obtenerToken() {
    return (
        localStorage.getItem("access_token") ||
        localStorage.getItem("token")
    );
}
// Cargar datos en formulario

function cargarFormulario(datos) {

    document.getElementById("id_convocatoria").value =
        datos.id_convocatoria;

    document.getElementById("titulo").value =
        datos.titulo;

    document.getElementById("descripcion").value =
        datos.descripcion;

    document.getElementById("tipo_beca").value =
        datos.tipo_beca;

    document.getElementById("institucion").value =
        datos.institucion;

    document.getElementById("fecha_apertura").value =
        datos.fecha_apertura;

    document.getElementById("fecha_cierre").value =
        datos.fecha_cierre;

    document.getElementById("nivel_educativo").value =
        datos.nivel_educativo;

    document.getElementById("requisitos").value =
        datos.requisitos;

    document.getElementById("monto_beneficio").value =
        datos.monto_beneficio ?? "";

    document.getElementById("cupos_disponibles").value =
        datos.cupos_disponibles ?? "";

    document.getElementById("estado").value =
        datos.estado;
}
// Consultar convocatoria real

async function cargarConvocatoria() {

    const id = obtenerIdConvocatoria();

    if (!id) {
        mostrarMensaje(
            "No se indicó el ID de la convocatoria.",
            "error"
        );

        btnGuardar.disabled = true;
        return;
    }

    try {

        const respuesta = await fetch(
            `${API_URL}/${id}`
        );

        if (!respuesta.ok) {

            if (respuesta.status === 404) {
                throw new Error(
                    "La convocatoria no existe."
                );
            }

            throw new Error(
                `Error al consultar la convocatoria (${respuesta.status}).`
            );
        }

        convocatoriaActual = await respuesta.json();

        cargarFormulario(convocatoriaActual);

        // Una convocatoria publicada o cerrada
        // ya no puede editarse.
        if (convocatoriaActual.estado !== "borrador") {

            btnGuardar.disabled = true;

            mostrarMensaje(
                `La convocatoria está en estado "${convocatoriaActual.estado}" y ya no puede editarse.`,
                "error"
            );
        }

    } catch (error) {

        console.error(error);

        mostrarMensaje(
            error.message,
            "error"
        );

        btnGuardar.disabled = true;
    }
}

// Guardar cambios

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    if (!convocatoriaActual) {
        mostrarMensaje(
            "No hay una convocatoria cargada.",
            "error"
        );
        return;
    }

    const fechaApertura =
        document.getElementById("fecha_apertura").value;

    const fechaCierre =
        document.getElementById("fecha_cierre").value;

    if (fechaCierre <= fechaApertura) {

        mostrarMensaje(
            "La fecha de cierre debe ser posterior a la fecha de apertura.",
            "error"
        );

        return;
    }

    const token = obtenerToken();

    if (!token) {

        mostrarMensaje(
            "Debes iniciar sesión como administrador para editar una convocatoria.",
            "error"
        );

        return;
    }

    const monto =
        document.getElementById("monto_beneficio").value;

    const cupos =
        document.getElementById("cupos_disponibles").value;

    const datosModificados = {

        titulo:
            document.getElementById("titulo").value.trim(),

        descripcion:
            document.getElementById("descripcion").value.trim(),

        tipo_beca:
            document.getElementById("tipo_beca").value.trim(),

        institucion:
            document.getElementById("institucion").value.trim(),

        fecha_apertura:
            fechaApertura,

        fecha_cierre:
            fechaCierre,

        nivel_educativo:
            document.getElementById("nivel_educativo").value.trim(),

        requisitos:
            document.getElementById("requisitos").value.trim(),

        monto_beneficio:
            monto === "" ? null : Number(monto),

        cupos_disponibles:
            cupos === "" ? null : Number(cupos)
    };


    try {

        btnGuardar.disabled = true;

        const respuesta = await fetch(
            `${API_URL}/${convocatoriaActual.id_convocatoria}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify(datosModificados)
            }
        );


        const resultado = await respuesta.json();


        if (!respuesta.ok) {

            let mensaje = "No se pudo actualizar la convocatoria.";

            if (resultado.detail) {

                if (typeof resultado.detail === "string") {
                    mensaje = resultado.detail;
                } else {
                    mensaje = JSON.stringify(resultado.detail);
                }
            }

            throw new Error(mensaje);
        }


        convocatoriaActual = resultado.convocatoria;

        cargarFormulario(convocatoriaActual);

        mostrarMensaje(
            "Convocatoria actualizada correctamente.",
            "success"
        );

    } catch (error) {

        console.error(error);

        mostrarMensaje(
            error.message,
            "error"
        );

    } finally {

        if (
            convocatoriaActual &&
            convocatoriaActual.estado === "borrador"
        ) {
            btnGuardar.disabled = false;
        }
    }
});

// Cancelar cambios

btnCancelar.addEventListener("click", () => {

    if (!convocatoriaActual) {
        return;
    }

    cargarFormulario(convocatoriaActual);

    mostrarMensaje(
        "Cambios descartados.",
        "error"
    );
});

// Inicio

document.addEventListener(
    "DOMContentLoaded",
    cargarConvocatoria
);