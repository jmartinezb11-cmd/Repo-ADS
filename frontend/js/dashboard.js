
const token = localStorage.getItem("token");

let usuario = null;

try {
  usuario = JSON.parse(sessionStorage.getItem("usuario") || "null");
} catch {
  usuario = null;
}

const rolesPermitidos = ["estudiante", "administrador", "evaluador"];
const rol = String(usuario?.rol || "").trim().toLowerCase();

if (!token || !rolesPermitidos.includes(rol)) {
  window.location.replace("login.html");
} else {
  iniciarDashboard();
}

function iniciarDashboard() {
  const modulos = {
    estudiante: [
      ["Convocatorias", "convocatorias.html", "📢"],
      ["Mis solicitudes", "mis-solicitudes.html", "📋"],
      ["Mi perfil", "perfil.html", "👤"],
      ["Documentos", "documentos.html", "📁"]
    ],
    administrador: [
      ["Gestión de usuarios", "admin.html", "👥"],
      ["Convocatorias", "convocatorias.html", "📢"],
      ["Crear convocatoria", "crear-convocatoria.html", "➕"],
      ["Gestión de comités", "gestion-comites.html", "🏛️"],
      ["Asignar evaluaciones", "asignar-evaluacion.html", "📝"]
    ],
    evaluador: [
    ["Mis evaluaciones", "evaluar-solicitud.html", "📋"]
  ]
  };

  const titulos = {
    estudiante: "Panel del estudiante",
    administrador: "Panel de administración",
    evaluador: "Panel del evaluador"
  };

  document.getElementById("tituloPanel").textContent = titulos[rol];
  document.getElementById("nombreUsuario").textContent =
    usuario.nombre_completo || usuario.email || "Usuario";
  document.getElementById("rolUsuario").textContent = rol;

  const menu = document.getElementById("menu");
  const tarjetas = document.getElementById("tarjetas");

  modulos[rol].forEach(([nombre, ruta, icono]) => {
    const enlace = document.createElement("a");
    enlace.href = ruta;
    enlace.className = "enlace-menu";
    enlace.textContent = `${icono} ${nombre}`;
    menu.appendChild(enlace);

    const tarjeta = document.createElement("a");
    tarjeta.href = ruta;
    tarjeta.className = "tarjeta";
    tarjeta.innerHTML = `
      <span class="tarjeta-icono">${icono}</span>
      <h3>${nombre}</h3>
      <p>Abrir módulo</p>
    `;
    tarjetas.appendChild(tarjeta);
  });
}

document.getElementById("cerrarSesion").addEventListener("click", () => {
  localStorage.removeItem("token");
  sessionStorage.removeItem("usuario");
  window.location.replace("login.html");
});


const btnMenu = document.getElementById("btnMenu");
const sidebar = document.getElementById("sidebar");

if (btnMenu && sidebar) {
  btnMenu.addEventListener("click", () => {
    const abierto = sidebar.classList.toggle("sidebar-abierto");

    btnMenu.setAttribute("aria-expanded", String(abierto));
    btnMenu.setAttribute(
      "aria-label",
      abierto ? "Cerrar menú de navegación" : "Abrir menú de navegación"
    );
  });

  sidebar.querySelectorAll("a").forEach((enlace) => {
    enlace.addEventListener("click", () => {
      sidebar.classList.remove("sidebar-abierto");
      btnMenu.setAttribute("aria-expanded", "false");
      btnMenu.setAttribute("aria-label", "Abrir menú de navegación");
    });
  });
}
