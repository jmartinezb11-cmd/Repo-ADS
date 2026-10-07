const cuerpoTabla = document.getElementById("cuerpoTabla");
const mensaje = document.getElementById("mensaje");

// OJO: usa el mismo puerto que el resto del proyecto haya
// acordado para el backend.
const API_BASE = "http://127.0.0.1:8000/api/usuarios";


function mostrarMensaje(texto, tipo) {
    mensaje.textContent = texto;
    mensaje.className = "mensaje " + tipo;
    mensaje.style.display = "block";
}


function obtenerToken() {
    const datosUsuario = sessionStorage.getItem("usuario");

    if (!datosUsuario) {
        return null;
    }

    return JSON.parse(datosUsuario).token;
}


async function cargarUsuarios() {

    const token = obtenerToken();

    if (!token) {
        mostrarMensaje(
            "Debes iniciar sesión como administrador para ver esta página.",
            "error"
        );

        cuerpoTabla.innerHTML = "";
        return;
    }

    try {

        const respuesta = await fetch(API_BASE + "/", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            mostrarMensaje(
                resultado.detail || "No fue posible cargar los usuarios.",
                "error"
            );

            cuerpoTabla.innerHTML = "";
            return;
        }

        dibujarTabla(resultado.usuarios);

    } catch (error) {

        console.error(error);

        mostrarMensaje(
            "No se pudo conectar con el servidor.",
            "error"
        );
    }
}


function dibujarTabla(usuarios) {

    if (usuarios.length === 0) {
        cuerpoTabla.innerHTML =
            "<tr><td colspan='5' class='cargando'>No hay usuarios registrados.</td></tr>";
        return;
    }

    cuerpoTabla.innerHTML = "";

    usuarios.forEach(function (usuario) {

        const fila = document.createElement("tr");

        const estadoSiguiente =
            usuario.estado_cuenta === "activo" ? "inactivo" : "activo";

        const textoBoton =
            usuario.estado_cuenta === "activo" ? "Desactivar" : "Activar";

        fila.innerHTML = `
            <td>${usuario.nombre_completo}</td>
            <td>${usuario.email}</td>
            <td>
                <span class="etiqueta-rol ${usuario.rol}">
                    ${usuario.rol}
                </span>
            </td>
            <td>
                <span class="etiqueta-estado ${usuario.estado_cuenta}">
                    ${usuario.estado_cuenta}
                </span>
            </td>
            <td>
                <button
                    class="boton-accion"
                    data-id="${usuario.id_estudiante}"
                    data-estado="${estadoSiguiente}"
                >
                    ${textoBoton}
                </button>
            </td>
        `;

        cuerpoTabla.appendChild(fila);
    });

    document.querySelectorAll(".boton-accion").forEach(function (boton) {
        boton.addEventListener("click", function () {
            cambiarEstado(
                boton.dataset.id,
                boton.dataset.estado
            );
        });
    });
}


async function cambiarEstado(idEstudiante, nuevoEstado) {

    const token = obtenerToken();

    try {

        const respuesta = await fetch(
            API_BASE + "/" + idEstudiante + "/estado",
            {
                method: "PATCH",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },

                body: JSON.stringify({ nuevo_estado: nuevoEstado })
            }
        );

        const resultado = await respuesta.json();

        if (respuesta.ok) {
            mostrarMensaje(resultado.mensaje, "exito");
            cargarUsuarios();
        } else {
            mostrarMensaje(
                resultado.detail || "No fue posible actualizar el estado.",
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
}


cargarUsuarios();