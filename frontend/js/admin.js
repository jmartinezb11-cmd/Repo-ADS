const cuerpoTabla = document.getElementById("cuerpoTabla");
const mensaje = document.getElementById("mensaje");

// OJO: usa el mismo puerto que el resto del proyecto haya
// acordado para el backend.
const API_BASE = "http://127.0.0.1:8001/api/usuarios";


function mostrarMensaje(texto, tipo) {
    mensaje.textContent = texto;
    mensaje.className = "mensaje " + tipo;
    mensaje.style.display = "block";
}


function obtenerToken() {
    return localStorage.getItem("token");
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
    <div class="acciones-usuario">
        <button
            class="boton-accion"
            data-id="${usuario.id_estudiante}"
            data-estado="${estadoSiguiente}"
        >
            ${textoBoton}
        </button>

        ${usuario.rol !== "administrador" ? `
            <select
                class="selector-rol"
                data-id="${usuario.id_estudiante}"
                aria-label="Nuevo rol del usuario"
            >
                <option value="estudiante"
                    ${usuario.rol === "estudiante" ? "selected" : ""}>
                    Estudiante
                </option>
                <option value="evaluador"
                    ${usuario.rol === "evaluador" ? "selected" : ""}>
                    Evaluador
                </option>
            </select>

            <button
                class="boton-cambiar-rol"
                data-id="${usuario.id_estudiante}"
            >
                Guardar rol
            </button>
        ` : ""}
    </div>
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
    
document.querySelectorAll(".boton-cambiar-rol").forEach(function (boton) {
    boton.addEventListener("click", function () {
        const id = boton.dataset.id;

        const selector = document.querySelector(
            `.selector-rol[data-id="${id}"]`
        );

        if (selector) {
            cambiarRol(id, selector.value);
        }
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


async function cambiarRol(idEstudiante, nuevoRol) {
    const token = obtenerToken();

    if (!token) {
        mostrarMensaje("Debes iniciar sesión nuevamente.", "error");
        return;
    }

    const confirmado = confirm(
        `¿Confirmas cambiar el rol del usuario a ${nuevoRol}?`
    );

    if (!confirmado) return;

    try {
        const respuesta = await fetch(
            `${API_BASE}/${idEstudiante}/rol`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    nuevo_rol: nuevoRol
                })
            }
        );

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            mostrarMensaje(
                typeof resultado.detail === "string"
                    ? resultado.detail
                    : "No fue posible cambiar el rol.",
                "error"
            );
            return;
        }

        mostrarMensaje(
            "Rol actualizado correctamente.",
            "exito"
        );

        await cargarUsuarios();

    } catch (error) {
        console.error(error);
        mostrarMensaje(
            "No se pudo conectar con el servidor.",
            "error"
        );
    }
}
