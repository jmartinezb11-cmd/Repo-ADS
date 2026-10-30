
const API_COMITES = "http://127.0.0.1:8001/comite";

const mensaje = document.getElementById("mensaje");
const resultado = document.getElementById("resultado-comite");

function mostrarMensaje(texto, tipo = "exito") {
    mensaje.textContent = texto;
    mensaje.className = `mensaje ${tipo}`;
}

function obtenerToken() {
    return localStorage.getItem("token");
}


async function peticion(url, opciones = {}) {
    const token = obtenerToken();

    if (!token) {
        throw new Error(
            "Tu sesión no está disponible. Inicia sesión nuevamente."
        );
    }

    const headers = {
        "Content-Type": "application/json",
        ...opciones.headers,
        Authorization: `Bearer ${token}`
    };

    let respuesta;

    try {
        respuesta = await fetch(url, {
            ...opciones,
            headers
        });
    } catch (error) {
        console.error("Error de conexión:", error);

        throw new Error(
            "No se pudo conectar con el servidor. " +
            "Verifica que FastAPI esté ejecutándose en el puerto 8001 " +
            "y revisa la consola del navegador."
        );
    }

    const datos = await respuesta.json().catch(() => ({}));

    if (!respuesta.ok) {
        let detalle = datos.detail || "No se pudo completar la operación.";

        if (Array.isArray(detalle)) {
            detalle = detalle
                .map(error => error.msg || "Dato inválido")
                .join(", ");
        }

        if (respuesta.status === 401) {
            throw new Error(
                "Tu sesión expiró o no es válida. Inicia sesión nuevamente."
            );
        }

        if (respuesta.status === 403) {
            throw new Error(
                "No tienes permisos para realizar esta operación."
            );
        }

        if (respuesta.status === 404) {
            throw new Error(
                `No se encontró el recurso solicitado. ${detalle}`
            );
        }

        throw new Error(
            typeof detalle === "string"
                ? detalle
                : "El servidor devolvió un error."
        );
    }

    return datos;
}


document.getElementById("form-crear").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const boton = evento.currentTarget.querySelector("button");
    boton.disabled = true;

    try {
        const datos = await peticion(API_COMITES, {
            method: "POST",
            body: JSON.stringify({
                nombre_comite: document.getElementById("nombre").value.trim(),
                descripcion: document.getElementById("descripcion").value.trim()
            })
        });

        mostrarMensaje(`Comité creado correctamente. ID: ${datos.id_comite}`);

        document.getElementById("form-crear").reset();
        await cargarComites();

        document.getElementById("id-comite").value =
            String(datos.id_comite);

        document.getElementById("id-consulta").value =
            String(datos.id_comite);

    } catch (error) {
        mostrarMensaje(error.message, "error");
    } finally {
        boton.disabled = false;
    }
});

document.getElementById("form-asignar").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const boton = evento.currentTarget.querySelector("button");
    boton.disabled = true;

    try {
        const idComite = Number(document.getElementById("id-comite").value);

        await peticion(`${API_COMITES}/${idComite}/miembros`, {
            method: "POST",
            body: JSON.stringify({
                id_estudiante: Number(document.getElementById("id-usuario").value),
                rol_comite: document.getElementById("rol").value
            })
        });

        mostrarMensaje("Integrante asignado correctamente.");
        document.getElementById("id-consulta").value = idComite;
        await consultarComite(idComite);

    } catch (error) {
        mostrarMensaje(error.message, "error");
    } finally {
        boton.disabled = false;
    }
});

document.getElementById("form-consultar").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const idComite = Number(document.getElementById("id-consulta").value);
    await consultarComite(idComite);
});

async function consultarComite(idComite) {
    resultado.textContent = "Consultando integrantes...";

    try {
        const datos = await peticion(`${API_COMITES}/${idComite}`);

        resultado.replaceChildren();

        const titulo = document.createElement("h3");
        titulo.textContent = datos.nombre_comite;
        resultado.appendChild(titulo);

        if (!datos.integrantes.length) {
            const vacio = document.createElement("p");
            vacio.textContent = "Este comité todavía no tiene integrantes.";
            resultado.appendChild(vacio);
            return;
        }

        datos.integrantes.forEach(integrante => {
            const tarjeta = document.createElement("div");
            tarjeta.className = "integrante";

            const nombre = document.createElement("h3");
            nombre.textContent = integrante.nombre;

            const rol = document.createElement("p");
            rol.textContent = `Rol: ${integrante.rol}`;

            const asignaciones = document.createElement("p");
            asignaciones.textContent = `Asignaciones: ${
                integrante.asignaciones?.length
                    ? integrante.asignaciones.join(", ")
                    : "Sin asignaciones"
            }`;

            tarjeta.append(nombre, rol, asignaciones);
            resultado.appendChild(tarjeta);
        });

    } catch (error) {
        resultado.textContent = error.message;
        mostrarMensaje(error.message, "error");
    }
}

consultarComite(1);


const API_USUARIOS = "http://127.0.0.1:8001/api/usuarios";

let usuariosDisponibles = [];

function mostrarUsuarios(filtro = "") {
    const selector = document.getElementById("id-usuario");
    const valorAnterior = selector.value;

    selector.replaceChildren();

    const opcionInicial = new Option(
        "Selecciona un integrante",
        ""
    );

    selector.add(opcionInicial);

    const texto = filtro.trim().toLowerCase();

    const usuariosFiltrados = usuariosDisponibles.filter(usuario => {
        return (
            usuario.nombre_completo.toLowerCase().includes(texto) ||
            usuario.email.toLowerCase().includes(texto)
        );
    });

    usuariosFiltrados.forEach(usuario => {
        const etiqueta =
            `${usuario.nombre_completo} — ${usuario.email} (${usuario.rol})`;

        selector.add(
            new Option(etiqueta, String(usuario.id_estudiante))
        );
    });

    if (
        usuariosFiltrados.some(
            usuario => String(usuario.id_estudiante) === valorAnterior
        )
    ) {
        selector.value = valorAnterior;
    }
}

async function cargarUsuariosDisponibles() {
    const selector = document.getElementById("id-usuario");

    try {
        const datos = await peticion(`${API_USUARIOS}/`);

        usuariosDisponibles = datos.usuarios.filter(usuario =>
            usuario.rol === "evaluador" ||
            usuario.rol === "administrador"
        );

        mostrarUsuarios();

        if (!usuariosDisponibles.length) {
            selector.options[0].textContent =
                "No hay integrantes disponibles";
        }

    } catch (error) {
        console.error(error);

        selector.replaceChildren(
            new Option("No se pudieron cargar los usuarios", "")
        );

        mostrarMensaje(error.message, "error");
    }
}

document.getElementById("buscar-usuario")
    .addEventListener("input", evento => {
        mostrarUsuarios(evento.target.value);
    });

cargarUsuariosDisponibles();


async function cargarComites() {
    const selectorAsignar = document.getElementById("id-comite");
    const selectorConsultar = document.getElementById("id-consulta");

    try {
        const datos = await peticion(API_COMITES);

        const comites = datos.comites || [];

        selectorAsignar.replaceChildren(
            new Option("Selecciona un comité", "")
        );

        selectorConsultar.replaceChildren(
            new Option("Selecciona un comité", "")
        );

        comites.forEach(comite => {
            const etiqueta = `${comite.nombre_comite} (${comite.estado})`;
            const valor = String(comite.id_comite);

            selectorAsignar.add(new Option(etiqueta, valor));
            selectorConsultar.add(new Option(etiqueta, valor));
        });

        if (!comites.length) {
            mostrarMensaje(
                "Todavía no hay comités registrados.",
                "error"
            );
        }

    } catch (error) {
        console.error(error);
        mostrarMensaje(error.message, "error");
    }
}

cargarComites();

