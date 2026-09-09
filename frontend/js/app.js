const form = document.getElementById("formRegistro");

const nivelEducativo = document.getElementById("nivel_educativo");
const camposSecundaria = document.getElementById("camposSecundaria");
const camposUniversidad = document.getElementById("camposUniversidad");
const contenedorEspecialidad = document.getElementById("contenedorEspecialidad");

const discapacidad = document.getElementById("discapacidad");
const contenedorTipoDiscapacidad = document.getElementById(
    "contenedorTipoDiscapacidad"
);

const mensaje = document.getElementById("mensaje");


function obtenerValor(id) {
    const valor = document.getElementById(id).value.trim();

    return valor === "" ? null : valor;
}


function obtenerNumero(id) {
    const valor = document.getElementById(id).value;

    return valor === "" ? null : Number(valor);
}


/* ======================================
   MOSTRAR CAMPOS SEGÚN NIVEL EDUCATIVO
====================================== */

nivelEducativo.addEventListener("change", function () {

    const nivel = nivelEducativo.value;

    camposSecundaria.style.display = "none";
    camposUniversidad.style.display = "none";
    contenedorEspecialidad.style.display = "none";

    if (
        nivel === "basico" ||
        nivel === "bachillerato" ||
        nivel === "perito"
    ) {
        camposSecundaria.style.display = "grid";
    }

    if (nivel === "perito") {
        contenedorEspecialidad.style.display = "flex";
    }

    if (nivel === "universitario") {
        camposUniversidad.style.display = "grid";
    }
});


/* ======================================
   MOSTRAR TIPO DE DISCAPACIDAD
====================================== */

discapacidad.addEventListener("change", function () {

    if (discapacidad.checked) {
        contenedorTipoDiscapacidad.style.display = "flex";
    } else {
        contenedorTipoDiscapacidad.style.display = "none";

        document.getElementById("tipo_discapacidad").value = "";
    }
});


/* ======================================
   MOSTRAR MENSAJES
====================================== */

function mostrarMensaje(texto, tipo) {

    mensaje.textContent = texto;
    mensaje.className = "mensaje " + tipo;
    mensaje.style.display = "block";
}


/* ======================================
   ENVÍO DEL FORMULARIO
====================================== */

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    mensaje.style.display = "none";

    const password = document.getElementById("password").value;
    const confirmarPassword = document.getElementById(
        "confirmar_password"
    ).value;

    if (password !== confirmarPassword) {
        mostrarMensaje(
            "Las contraseñas no coinciden.",
            "error"
        );

        return;
    }

    const datos = {

        primer_nombre: obtenerValor("primer_nombre"),
        segundo_nombre: obtenerValor("segundo_nombre"),
        primer_apellido: obtenerValor("primer_apellido"),
        segundo_apellido: obtenerValor("segundo_apellido"),

        cui: obtenerValor("cui"),
        fecha_nacimiento: obtenerValor("fecha_nacimiento"),

        genero: obtenerValor("genero"),
        nacionalidad: obtenerValor("nacionalidad"),

        telefono: obtenerValor("telefono"),
        telefono_alternativo: obtenerValor(
            "telefono_alternativo"
        ),

        departamento: obtenerValor("departamento"),
        municipio: obtenerValor("municipio"),
        zona_aldea: obtenerValor("zona_aldea"),
        direccion_exacta: obtenerValor(
            "direccion_exacta"
        ),

        discapacidad: discapacidad.checked,

        tipo_discapacidad: discapacidad.checked
            ? obtenerValor("tipo_discapacidad")
            : null,

        pueblo_pertenencia: obtenerValor(
            "pueblo_pertenencia"
        ),

        email: obtenerValor("email"),
        password: password,

        datos_academicos: {

            nivel_educativo: obtenerValor(
                "nivel_educativo"
            ),

            establecimiento_educativo:
                obtenerValor(
                    "establecimiento_educativo"
                ),

            grado_actual:
                obtenerValor("grado_actual"),

            jornada:
                obtenerValor("jornada"),

            sector:
                obtenerValor("sector"),

            promedio_notas:
                obtenerNumero("promedio_notas"),

            especialidad:
                obtenerValor("especialidad"),

            universidad:
                obtenerValor("universidad"),

            facultad_escuela:
                obtenerValor("facultad_escuela"),

            carrera:
                obtenerValor("carrera"),

            anio_semestre_actual:
                obtenerValor(
                    "anio_semestre_actual"
                ),

            carnet_universitario:
                obtenerValor(
                    "carnet_universitario"
                ),

            cum:
                obtenerNumero("cum"),

            creditos_aprobados:
                obtenerNumero(
                    "creditos_aprobados"
                ),

            modalidad:
                obtenerValor("modalidad")
        },

        datos_socioeconomicos: {

            ingreso_familiar_mensual:
                obtenerNumero(
                    "ingreso_familiar_mensual"
                ),

            numero_miembros_nucleo:
                obtenerNumero(
                    "numero_miembros_nucleo"
                ),

            ocupacion_padre:
                obtenerValor("ocupacion_padre"),

            ocupacion_madre:
                obtenerValor("ocupacion_madre"),

            ocupacion_encargado:
                obtenerValor(
                    "ocupacion_encargado"
                ),

            tipo_vivienda:
                obtenerValor("tipo_vivienda"),

            dependientes_economicos:
                obtenerNumero(
                    "dependientes_economicos"
                )
        },

        contacto_emergencia: {

            nombre_encargado:
                obtenerValor("nombre_encargado"),

            parentesco:
                obtenerValor("parentesco"),

            telefono_emergencia:
                obtenerValor(
                    "telefono_emergencia"
                )
        }
    };

    try {

        const respuesta = await fetch(
            "http://127.0.0.1:8001/api/estudiantes/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(datos)
            }
        );

        const resultado = await respuesta.json();

        if (respuesta.ok) {

            mostrarMensaje(
                resultado.mensaje,
                "exito"
            );

            form.reset();

            camposSecundaria.style.display = "none";
            camposUniversidad.style.display = "none";
            contenedorEspecialidad.style.display = "none";
            contenedorTipoDiscapacidad.style.display = "none";

        } else {

            let textoError = "No fue posible realizar el registro.";

            if (typeof resultado.detail === "string") {

                textoError = resultado.detail;

            } else if (Array.isArray(resultado.detail)) {

                textoError = resultado.detail
                    .map(error => error.msg)
                    .join(" ");

            }

            mostrarMensaje(
                textoError,
                "error"
            );
        }

    } catch (error) {

        console.error(error);

        mostrarMensaje(
            "No se pudo conectar con el servidor.",
            "error"
        );
    }
});