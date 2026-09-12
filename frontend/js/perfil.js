const API_URL = "http://127.0.0.1:8001";

let datosActuales = {};

const form = document.getElementById("perfil-form");
const btnEditar = document.getElementById("btn-editar");
const btnGuardar = document.getElementById("btn-guardar");
const btnCancelar = document.getElementById("btn-cancelar");
const alertBox = document.getElementById("alert-box");

function cargarDatos(datos) {
  Object.keys(datos).forEach(key => {
    const field = document.getElementById(key);
    if (field) {
      field.value = datos[key] !== null && datos[key] !== undefined ? datos[key] : "";
    }
  });
}

function alternarModoEdicion(editable) {
  if (!form) return;
  const inputs = form.querySelectorAll("input, select");
  inputs.forEach(input => {
    if (!input.classList.contains("readonly") && input.id !== "cui" && input.id !== "fechaNacimiento") {
      input.disabled = !editable;
    }
  });

  if (editable) {
    btnEditar?.classList.add("hidden");
    btnGuardar?.classList.remove("hidden");
    btnCancelar?.classList.remove("hidden");
  } else {
    btnEditar?.classList.remove("hidden");
    btnGuardar?.classList.add("hidden");
    btnCancelar?.classList.add("hidden");
  }
}

function mostrarMensaje(texto, tipo) {
  if (!alertBox) return;
  alertBox.className = `alert alert-${tipo}`;
  alertBox.textContent = texto;
  alertBox.classList.remove("hidden");
  setTimeout(() => alertBox.classList.add("hidden"), 5000);
}

async function obtenerPerfil() {
  const sesionRaw = sessionStorage.getItem("usuario");

  if (!sesionRaw) {
    window.location.href = "login.html";
    return;
  }

  const sesion = JSON.parse(sesionRaw);
  const idEstudiante = sesion.id_estudiante || 1;

  try {
    const res = await fetch(`${API_URL}/api/estudiantes/${idEstudiante}`);

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Código ${res.status}`);
    }

    const data = await res.json();

    datosActuales = {
      nombres: `${data.primer_nombre || ""} ${data.primer_apellido || ""}`.trim(),
      segundoNombre: `${data.segundo_nombre || ""} ${data.segundo_apellido || ""}`.trim(),
      cui: data.cui || "",
      fechaNacimiento: data.fecha_nacimiento ? String(data.fecha_nacimiento).split("T")[0] : "",
      genero: data.genero === "Masculino" ? "M" : (data.genero === "Femenino" ? "F" : data.genero || "M"),
      nacionalidad: data.nacionalidad || "Guatemalteca",
      telefono: data.telefono || "",
      direccion: data.direccion_exacta || "",
      nivelEducativo: data.nivel_educativo || "Universitario",
      institucion: data.institucion || "",
      carrera: data.carrera || "",
      promedio: data.promedio ?? "",
      ingresoFamiliar: data.ingreso_familiar_mensual ?? "",
      miembrosFamilia: data.numero_miembros_nucleo ?? "",
      ocupacionEncargado: data.ocupacion_encargado || "",
      tipoVivienda: data.tipo_vivienda || "Propia",
      dependientes: data.dependientes_economicos ?? "",
      contactoEmergencia: data.telefono_emergencia || ""
    };

    cargarDatos(datosActuales);
    mostrarMensaje(`Perfil cargado desde PostgreSQL: ${datosActuales.nombres}`, "success");

  } catch (error) {
    console.error("Error al obtener datos:", error);
    mostrarMensaje(`Error al cargar perfil: ${error.message}`, "error");
  }
}

btnEditar?.addEventListener("click", () => alternarModoEdicion(true));

btnCancelar?.addEventListener("click", () => {
  cargarDatos(datosActuales);
  alternarModoEdicion(false);
});

form?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const sesionRaw = sessionStorage.getItem("usuario");
  const idEstudiante = sesionRaw ? JSON.parse(sesionRaw).id_estudiante : 1;

  const formData = new FormData(form);
  const datosForm = Object.fromEntries(formData.entries());

  if (!datosForm.telefono || datosForm.telefono.trim().length < 8) {
    mostrarMensaje("El teléfono debe contener al menos 8 dígitos.", "error");
    return;
  }

  const payload = {
    telefono: datosForm.telefono || null,
    direccion: datosForm.direccion || null,
    nivelEducativo: datosForm.nivelEducativo || null,
    institucion: datosForm.institucion || null,
    carrera: datosForm.carrera || null,
    promedio: datosForm.promedio ? parseFloat(datosForm.promedio) : null,
    ingresoFamiliar: datosForm.ingresoFamiliar ? parseFloat(datosForm.ingresoFamiliar) : null,
    miembrosFamilia: datosForm.miembrosFamilia ? parseInt(datosForm.miembrosFamilia) : null,
    ocupacionEncargado: datosForm.ocupacionEncargado || null,
    tipoVivienda: datosForm.tipoVivienda || null,
    dependientes: datosForm.dependientes ? parseInt(datosForm.dependientes) : null,
    contactoEmergencia: datosForm.contactoEmergencia || null
  };

  try {
    const res = await fetch(`${API_URL}/api/estudiantes/${idEstudiante}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Fallo al actualizar en base de datos");
    }

    datosActuales = { ...datosActuales, ...datosForm };
    alternarModoEdicion(false);
    mostrarMensaje("¡Perfil actualizado con éxito en PostgreSQL!", "success");

  } catch (err) {
    mostrarMensaje(err.message, "error");
  }
});

document.addEventListener("DOMContentLoaded", obtenerPerfil);