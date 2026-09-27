const API_URL = "http://127.0.0.1:8001/api/convocatorias/";

const formulario = document.getElementById("formConvocatoria");
const mensaje = document.getElementById("mensaje");
const boton = document.getElementById("btnCrear");


formulario.addEventListener("submit", async function (event) {
    event.preventDefault();

    mensaje.textContent = "";

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

    const montoInput =
        document.getElementById("monto_beneficio").value;

    const cuposInput =
        document.getElementById("cupos_disponibles").value;

    const datos = {
        titulo: document.getElementById("titulo").value.trim(),

        descripcion:
            document.getElementById("descripcion").value.trim(),

        tipo_beca:
            document.getElementById("tipo_beca").value.trim(),

        institucion:
            document.getElementById("institucion").value.trim(),

        fecha_apertura: fechaApertura,

        fecha_cierre: fechaCierre,

        nivel_educativo:
            document.getElementById("nivel_educativo").value,

        requisitos:
            document.getElementById("requisitos").value.trim(),

        monto_beneficio:
            montoInput === "" ? null : Number(montoInput),

        cupos_disponibles:
            cuposInput === "" ? null : Number(cuposInput)
    };

    try {
        boton.disabled = true;
        boton.textContent = "Creando...";

        const respuesta = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            let detalle = resultado.detail;

            if (Array.isArray(detalle)) {
                detalle = detalle
                    .map(error => error.msg)
                    .join(" ");
            }

            throw new Error(
                detalle || "No se pudo crear la convocatoria."
            );
        }

        mostrarMensaje(
            `Convocatoria creada correctamente. ID: ${resultado.id_convocatoria}`,
            "exito"
        );

        formulario.reset();

    } catch (error) {

        mostrarMensaje(
            error.message || "No se pudo conectar con el servidor.",
            "error"
        );

    } finally {

        boton.disabled = false;
        boton.textContent = "Crear convocatoria";

    }
});


function mostrarMensaje(texto, tipo) {
    mensaje.textContent = texto;
    mensaje.className = tipo;
}