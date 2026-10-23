# Plan y Casos de Prueba - Sprint 4 (ADS)

**Responsable de QA / Calidad:** Luis  
**Objetivo:** Validar el funcionamiento, reglas de negocio y restricciones de rol para las historias de usuario del Sprint 4 (US-017 a US-027).

---

## 1. Matriz de Casos de Prueba

| ID Caso | Historia | Rol / Usuario | Precondición | Pasos / Acción | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-017-01** | US-017 (Asignar evaluación) | Administrador / Comité | Solicitud pendiente | 1. Seleccionar solicitud.<br>2. Seleccionar evaluador.<br>3. Confirmar asignación. | La solicitud cambia a estado "En Evaluación" y asignada al evaluador. | ⏳ Pendiente |
| **TC-017-02** | US-017 (Asignar evaluación) | Estudiante | Ninguna | Intentar acceder al módulo de asignación. | Acceso denegado (Error 403 / Redirección). | ⏳ Pendiente |
| **TC-018-01** | US-018 (Evaluar solicitud) | Evaluador | Solicitud asignada | 1. Abrir solicitud asignada.<br>2. Llenar criterios de evaluación.<br>3. Guardar. | Se registra la evaluación y puntuación en el sistema. | ⏳ Pendiente |
| **TC-019-01** | US-019 (Registrar observaciones) | Evaluador | Evaluación en proceso | 1. Ingresar observaciones detalladas.<br>2. Guardar observaciones. | Las observaciones se vinculan correctamente a la evaluación. | ⏳ Pendiente |
| **TC-020-01** | US-020 (Consultar evaluación) | Comité / Admin | Solicitud evaluada | 1. Ir a consulta de evaluaciones.<br>2. Seleccionar solicitud evaluada. | Se muestra el detalle de nota y observaciones del evaluador. | ⏳ Pendiente |
| **TC-024-01** | US-024 (Aprobar/Rechazar) | Comité | Evaluación completada | 1. Revisar dictamen.<br>2. Seleccionar "Aprobar" o "Rechazar".<br>3. Confirmar. | El estado final de la solicitud se actualiza formalmente. | ⏳ Pendiente |
| **TC-025-01** | US-025 (Consultar estado) | Estudiante | Solicitud enviada | 1. Iniciar sesión.<br>2. Ir a "Mis Solicitudes". | Se visualiza la etapa y estado actual en tiempo real. | ⏳ Pendiente |
| **TC-026-01** | US-026 (Reporte solicitudes) | Administrador | Datos registrados | 1. Acceder a Reportes.<br>2. Aplicar filtros (fecha/estado).<br>3. Generar reporte. | Se despliega o descarga la lista correspondiente. | ⏳ Pendiente |
| **TC-027-01** | US-027 (Reporte resultados) | Administrador | Solicitudes dictaminadas | 1. Seleccionar "Reporte de Resultados".<br>2. Generar resúmenes. | Genera consolidado de resultados generales del proceso. | ⏳ Pendiente |

---

## 2. Registro de Incidencias (Bugs Encontrados)

| Bug ID | Historia | Descripción del Error | Pasos para Reproducir | Responsable | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| *Sin registros aún* | - | - | - | - | - |