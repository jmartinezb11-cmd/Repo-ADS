const formLogin = document.getElementById("formLogin");
const mensaje = document.getElementById("mensaje");

const API_URL = "http://127.0.0.1:8001/api/auth/login";

function mostrarMensaje(texto, tipo) {
  if (!mensaje) return;
  mensaje.textContent = texto;
  mensaje.className = "mensaje " + tipo;
  mensaje.style.display = "block";
}

if (formLogin) {
  formLogin.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    const datos = {
      email: email,
      password: password
    };

    try {
      const respuesta = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(datos)
      });

      const resultado = await respuesta.json();

      if (respuesta.ok) {
        mostrarMensaje("Inicio de sesión exitoso. Redirigiendo...", "exito");

        // Guarda el resultado que contiene id_estudiante: 1
        sessionStorage.setItem("usuario", JSON.stringify(resultado));

        setTimeout(function () {
          window.location.href = "perfil.html";
        }, 600);
      } else {
        let textoError = "No fue posible iniciar sesión.";
        if (typeof resultado.detail === "string") {
          textoError = resultado.detail;
        } else if (Array.isArray(resultado.detail)) {
          textoError = resultado.detail.map(error => error.msg).join(" ");
        }
        mostrarMensaje(textoError, "error");
      }
    } catch (error) {
      console.error(error);
      mostrarMensaje("No se pudo conectar con el servidor.", "error");
    }
  });
}