
(() => {
  "use strict";

  const RUTAS_PUBLICAS = new Set([
    "index.html",
    "login.html"
  ]);

  const MODULOS = {
    "admin.html": ["administrador"],
    "crear-convocatoria.html": ["administrador"],
    "editar-convocatoria.html": ["administrador"],
    "gestion-comites.html": ["administrador"],
    "asignar-evaluacion.html": ["administrador"],

    "mis-solicitudes.html": ["estudiante"],
    "completar-solicitud.html": ["estudiante"],
    "enviar-solicitud.html": ["estudiante"],
    "documentos.html": ["estudiante"],
    "perfil.html": ["estudiante"],

    "evaluacion.html": ["evaluador"],
    "evaluar-solicitud.html": ["evaluador"],

    "convocatorias.html": ["estudiante", "administrador"],
    "comite.html": ["administrador", "evaluador"]
  };

  const pagina = location.pathname.split("/").pop() || "index.html";

  if (RUTAS_PUBLICAS.has(pagina) || pagina === "dashboard.html") {
    return;
  }

  const token = localStorage.getItem("token");

  let usuario = null;

  try {
    usuario = JSON.parse(sessionStorage.getItem("usuario") || "null");
  } catch {
    usuario = null;
  }

  const rol = String(usuario?.rol || "").trim().toLowerCase();

  function cerrarSesion() {
    localStorage.removeItem("token");
    sessionStorage.removeItem("usuario");
    location.replace("login.html");
  }

  if (!token || !usuario) {
    location.replace("login.html");
    return;
  }

  const rolesPermitidos = MODULOS[pagina];

  if (rolesPermitidos && !rolesPermitidos.includes(rol)) {
    location.replace("dashboard.html");
    return;
  }

  function crearBoton(texto, accion, clase) {
    const boton = document.createElement("button");
    boton.type = "button";
    boton.className = clase;
    boton.textContent = texto;
    boton.addEventListener("click", accion);
    return boton;
  }

  function construirNavegacion() {
    const barra = document.createElement("nav");
    barra.className = "ads-navegacion";
    barra.setAttribute("aria-label", "Navegación del sistema");

    const izquierda = document.createElement("div");
    izquierda.className = "ads-nav-izquierda";

    const marca = document.createElement("strong");
    marca.className = "ads-nav-marca";
    marca.textContent = "🎓 ADS Becas";

    const volver = crearBoton(
      "← Volver al panel",
      () => location.href = "dashboard.html",
      "ads-btn-volver"
    );

    izquierda.append(marca, volver);

    const derecha = document.createElement("div");
    derecha.className = "ads-nav-derecha";

    const usuarioTexto = document.createElement("span");
    usuarioTexto.className = "ads-nav-usuario";
    usuarioTexto.textContent =
      usuario.nombre_completo || usuario.email || "Usuario";

    const salir = crearBoton(
      "Cerrar sesión",
      cerrarSesion,
      "ads-btn-salir"
    );

    derecha.append(usuarioTexto, salir);
    barra.append(izquierda, derecha);

    document.body.prepend(barra);

    
    
    // Ocultar los botones antiguos de regreso duplicados y evitar trabajo.
    document.querySelectorAll("a, button").forEach((elemento) => {
      if (elemento.closest(".ads-navegacion")) {
        return;
      }

      const texto = elemento.textContent
        .trim()
        .toLowerCase()
        .replace(/\s+/g, " ");

      const esBotonRegreso =
        /^(←\s*)?(volver|regresar)\s+(al|a la|a)\s+(inicio|panel|perfil)$/.test(texto);

      if (esBotonRegreso) {
        elemento.hidden = true;
        elemento.setAttribute("aria-hidden", "true");
      }
    });

  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", construirNavegacion);
  } else {
    construirNavegacion();
  }
})();
