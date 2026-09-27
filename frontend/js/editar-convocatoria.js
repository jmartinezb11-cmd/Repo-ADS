const API_URL = "http://127.0.0.1:8001/api/convocatorias";

// Mock de convocatoria para trabajar en paralelo respetando US-005
let convocatoriaActual = {
  id_convocatoria: 1,
  titulo: "Beca Universitaria de Grado 2026",
  descripcion: "Programa de apoyo económico para estudiantes universitarios con rendimiento destacado.",
  fecha_inicio: "2026-02-01",
  fecha_fin: "2026-03-15",
  requisitos: "Promedio mínimo de 85 puntos, constancia de inscripción activa, no contar con otra beca.",
  estado: "borrador"
};

const form = document.getElementById("form-editar-convocatoria");
const alertBox = document.getElementById("alert-box");
const btnCancelar = document.getElementById("btn-cancelar");

function mostrarMensaje(texto, tipo) {
  alertBox.className = `alert alert-${tipo}`;
  alertBox.textContent = texto;
  alertBox.classList.remove("hidden");
  setTimeout(() => alertBox.classList.add("hidden"), 4000);
}

function cargarFormulario(datos) {
  document.getElementById("id_convocatoria").value = datos.id_convocatoria;
  document.getElementById("titulo").value = datos.titulo;
  document.getElementById("descripcion").value = datos.descripcion;
  document.getElementById("fecha_inicio").value = datos.fecha_inicio;
  document.getElementById("fecha_fin").value = datos.fecha_fin;
  document.getElementById("requisitos").value = datos.requisitos;
  document.getElementById("estado").value = datos.estado;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const fechaInicio = new Date(document.getElementById("fecha_inicio").value);
  const fechaFin = new Date(document.getElementById("fecha_fin").value);

  // Validación: la fecha final debe ser posterior a la de inicio
  if (fechaFin <= fechaInicio) {
    mostrarMensaje("La fecha de finalización debe ser posterior a la fecha de inicio.", "error");
    return;
  }

  const formData = new FormData(form);
  const datosModificados = Object.fromEntries(formData.entries());

  try {
    const token = localStorage.getItem("token") || localStorage.getItem("access_token");

    const respuesta = await fetch(`${API_URL}/${datosModificados.id_convocatoria}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { "Authorization": `Bearer ${token}` } : {})
      },
      body: JSON.stringify(datosModificados)
    });

    if (respuesta.ok) {
      convocatoriaActual = { ...convocatoriaActual, ...datosModificados };
      mostrarMensaje("Convocatoria actualizada con éxito en el servidor.", "success");
    } else {
      // Modo Mock mientras US-005 concluye en backend
      convocatoriaActual = { ...convocatoriaActual, ...datosModificados };
      mostrarMensaje("Cambios guardados localmente (Modo Mock / Integración US-005 pendiente).", "success");
    }
  } catch (error) {
    convocatoriaActual = { ...convocatoriaActual, ...datosModificados };
    mostrarMensaje("Cambios guardados localmente (Modo Mock).", "success");
  }
});

btnCancelar.addEventListener("click", () => {
  cargarFormulario(convocatoriaActual);
  mostrarMensaje("Cambios descartados. Se restauraron los datos iniciales.", "error");
});

document.addEventListener("DOMContentLoaded", () => {
  cargarFormulario(convocatoriaActual);
});