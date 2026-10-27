
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

    const headers = {
        "Content-Type": "application/json",
        ...opciones.headers
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const respuesta = await fetch(url, {
        ...opciones,
        headers
    });

    const datos = await respuesta.json();

    if (!respuesta.ok) {
        let detalle = datos.detail || "Error en la solicitud.";

        if (Array.isArray(detalle)) {
            detalle = detalle
                .map(error => error.msg)
                .join(", ");
        }

        throw new Error(detalle);
    }

    return datos;
}

document.getElementById("form-crear").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const boton = evento.currentTarget.querySelector("button");
    boton.disabled = true;

    try {
        const datos = await peticion(`${API_COMITES}/`, {
            method: "POST",
            body: JSON.stringify({
                nombre_comite: document.getElementById("nombre").value.trim(),
                descripcion: document.getElementById("descripcion").value.trim()
            })
        });

        mostrarMensaje(`Comité creado correctamente. ID: ${datos.id_comite}`);

        document.getElementById("form-crear").reset();
        document.getElementById("id-comite").value = datos.id_comite;
        document.getElementById("id-consulta").value = datos.id_comite;

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
