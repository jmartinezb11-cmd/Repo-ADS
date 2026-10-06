-- US-011 - Completar solicitud
-- Información adicional requerida para completar una solicitud.

CREATE TABLE IF NOT EXISTS detalle_solicitudes (
    id_detalle SERIAL PRIMARY KEY,

    id_solicitud INTEGER NOT NULL UNIQUE
        REFERENCES solicitudes(id_solicitud)
        ON DELETE CASCADE,

    motivacion TEXT NOT NULL,
    situacion_economica TEXT NOT NULL,

    ingresos_familiares DECIMAL(10,2) NOT NULL
        CHECK (ingresos_familiares >= 0),

    integrantes_hogar INTEGER NOT NULL
        CHECK (integrantes_hogar > 0),

    dependientes_economicos INTEGER NOT NULL
        CHECK (dependientes_economicos >= 0),

    ocupacion_responsable VARCHAR(150) NOT NULL,

    institucion_educativa VARCHAR(200) NOT NULL,
    carrera_area VARCHAR(200) NOT NULL,
    grado_semestre VARCHAR(100) NOT NULL,

    promedio_academico DECIMAL(5,2) NOT NULL
        CHECK (promedio_academico >= 0 AND promedio_academico <= 100),

    meta_academica TEXT NOT NULL,

    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);