document.addEventListener("DOMContentLoaded", () => {
    // Consultamos el comité con ID 1 (puedes ajustar el ID)
    consultarComite(1);
});

async function consultarComite(idComite) {
    const loadingEl = document.getElementById("loading");
    const containerEl = document.getElementById("integrantes-container");
    const infoEl = document.getElementById("comite-info");

    try {
        const response = await fetch(`http://127.0.0.1:8000/comite/${idComite}`);
        
        if (!response.ok) {
            throw new Error(`Error en la petición: ${response.status}`);
        }

        const data = await response.json();
        
        loadingEl.style.display = "none";
        infoEl.style.display = "block";
        containerEl.innerHTML = "";

        // Renderizamos cada integrante devuelto por la API
        if (data.integrantes && data.integrantes.length > 0) {
            data.integrantes.forEach(integrante => {
                const card = document.createElement("div");
                card.className = "card";
                card.innerHTML = `
                    <h3>${integrante.nombre}</h3>
                    <p><strong>Rol:</strong> ${integrante.rol}</p>
                    <p><strong>Asignaciones:</strong> ${integrante.asignaciones ? integrante.asignaciones.join(", ") : "Sin asignaciones"}</p>
                `;
                containerEl.appendChild(card);
            });
        } else {
            containerEl.innerHTML = "<p>No se encontraron integrantes en este comité.</p>";
        }

    } catch (error) {
        console.error("Error al obtener los datos del comité:", error);
        loadingEl.innerHTML = "<p style='color: red;'>Error al cargar los datos del comité.</p>";
    }
}