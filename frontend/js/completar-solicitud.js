const API_SOLICITUDES =
  "http://127.0.0.1:8001/api/solicitudes";

const formulario =
  document.getElementById("form-solicitud");

const btnGuardar =
  document.getElementById("btn-guardar");

const alertBox =
  document.getElementById("alert-box");


function obtenerToken() {
  return localStorage.getItem("token");
}


function obtenerIdSolicitud() {
  const parametros =
    new URLSearchParams(window.location.search);

  return parametros.get("id");
}


function mostrarAlerta(mensaje, tipo) {
  alertBox.textContent = mensaje;

  alertBox.className =
    `alert alert-${tipo}`;

  alertBox.classList.remove("hidden");
}


document.addEventListener("DOMContentLoaded", () => {
  const token = obtenerToken();
  const idSolicitud = obtenerIdSolicitud();

  if (!token) {
    alert("Debes iniciar sesión para completar una solicitud.");

    window.location.href = "login.html";
    return;
  }

  if (!idSolicitud) {
    mostrarAlerta(
      "No se encontró el identificador de la solicitud.",
      "error"
    );

    formulario.classList.add("hidden");
  }
});


formulario.addEventListener("submit", async (event) => {
  event.preventDefault();

  const token = obtenerToken();
  const idSolicitud = obtenerIdSolicitud();

  if (!token || !idSolicitud) {
    mostrarAlerta(
      "No fue posible identificar la solicitud.",
      "error"
    );

    return;
  }


  const integrantesHogar =
    Number(document.getElementById("integrantes_hogar").value);

  const dependientesEconomicos =
    Number(document.getElementById("dependientes_economicos").value);


  if (dependientesEconomicos > integrantesHogar) {
    mostrarAlerta(
      "Los dependientes económicos no pueden superar " +
      "el número de integrantes del hogar.",
      "error"
    );

    return;
  }


  const datos = {
    motivacion:
      document.getElementById("motivacion").value.trim(),

    situacion_economica:
      document.getElementById("situacion_economica").value.trim(),

    ingresos_familiares:
      Number(document.getElementById("ingresos_familiares").value),

    integrantes_hogar:
      integrantesHogar,

    dependientes_economicos:
      dependientesEconomicos,

    ocupacion_responsable:
      document.getElementById("ocupacion_responsable").value.trim(),

    institucion_educativa:
      document.getElementById("institucion_educativa").value.trim(),

    carrera_area:
      document.getElementById("carrera_area").value.trim(),

    grado_semestre:
      document.getElementById("grado_semestre").value.trim(),

    promedio_academico:
      Number(document.getElementById("promedio_academico").value),

    meta_academica:
      document.getElementById("meta_academica").value.trim()
  };


  try {
    btnGuardar.disabled = true;
    btnGuardar.textContent = "Guardando...";

    const respuesta = await fetch(
      `${API_SOLICITUDES}/${idSolicitud}/completar`,
      {
        method: "PUT",

        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify(datos)
      }
    );


    const resultado = await respuesta.json();


    if (!respuesta.ok) {
      mostrarAlerta(
        resultado.detail ||
        "No fue posible completar la solicitud.",
        "error"
      );

      return;
    }


    mostrarAlerta(
      "Solicitud completada correctamente.",
      "success"
    );


  } catch (error) {
    console.error(error);

    mostrarAlerta(
      "No se pudo conectar con el servidor.",
      "error"
    );

  } finally {
    btnGuardar.disabled = false;
    btnGuardar.textContent = "Guardar información";
  }
});