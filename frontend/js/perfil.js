// Mock temporal mientras US-002 (Login/Auth) se integra
const mockEstudiante = {
  nombres: "Kenneth Alexander",
  segundoNombre: "Vides Garcia",
  cui: "3000123450101",
  fechaNacimiento: "2003-05-14",
  genero: "M",
  nacionalidad: "Guatemalteca",
  telefono: "55551234",
  direccion: "Antigua Guatemala, Sacatepéquez",
  nivelEducativo: "Universitario",
  institucion: "Universidad Mariano Gálvez",
  carrera: "Ingeniería en Sistemas",
  promedio: 88.5,
  ingresoFamiliar: 6500,
  miembrosFamilia: 4,
  ocupacionEncargado: "Comerciante",
  tipoVivienda: "Propia",
  dependientes: 2,
  contactoEmergencia: "55554321"
};

let datosActuales = { ...mockEstudiante };

// Elementos del DOM
const form = document.getElementById("perfil-form");
const btnEditar = document.getElementById("btn-editar");
const btnGuardar = document.getElementById("btn-guardar");
const btnCancelar = document.getElementById("btn-cancelar");
const alertBox = document.getElementById("alert-box");

// Cargar datos en los inputs
function cargarDatos(datos) {
  Object.keys(datos).forEach(key => {
    const field = document.getElementById(key);
    if (field) field.value = datos[key];
  });
}

// Activar o desactivar modo edición (CUI y Fecha de Nacimiento quedan bloqueados por integridad)
function alternarModoEdicion(editable) {
  const inputs = form.querySelectorAll("input, select");
  inputs.forEach(input => {
    if (!input.classList.contains("readonly")) {
      input.disabled = !editable;
    }
  });

  if (editable) {
    btnEditar.classList.add("hidden");
    btnGuardar.classList.remove("hidden");
    btnCancelar.classList.remove("hidden");
  } else {
    btnEditar.classList.remove("hidden");
    btnGuardar.classList.add("hidden");
    btnCancelar.classList.add("hidden");
  }
}

function mostrarMensaje(texto, tipo) {
  alertBox.className = `alert alert-${tipo}`;
  alertBox.textContent = texto;
  alertBox.classList.remove("hidden");
  setTimeout(() => alertBox.classList.add("hidden"), 4000);
}

// Eventos
btnEditar.addEventListener("click", () => alternarModoEdicion(true));

btnCancelar.addEventListener("click", () => {
  cargarDatos(datosActuales);
  alternarModoEdicion(false);
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);
  const datosActualizados = {};
  formData.forEach((value, key) => {
    datosActualizados[key] = value;
  });

  try {
    // SIMULACIÓN DE PUT /perfil
    // Cuando el backend esté listo se usará:
    // await fetch('/perfil', { method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(datosActualizados) });
    
    // Validaciones básicas de campos
    if (!datosActualizados.telefono || datosActualizados.telefono.trim().length < 8) {
      throw new Error("El teléfono debe tener un formato válido de 8 dígitos.");
    }

    datosActuales = { ...datosActuales, ...datosActualizados };
    alternarModoEdicion(false);
    mostrarMensaje("¡Perfil actualizado con éxito!", "success");
  } catch (error) {
    mostrarMensaje(error.message || "Error al actualizar el perfil", "error");
  }
});

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
  cargarDatos(datosActuales);
});