CREATE TABLE IF NOT EXISTS evaluaciones (
    id_evaluacion SERIAL PRIMARY KEY,

    id_solicitud INTEGER NOT NULL
        REFERENCES solicitudes(id_solicitud),

    id_evaluador INTEGER NOT NULL
        REFERENCES estudiantes(id_estudiante),

    id_asignador INTEGER NOT NULL
        REFERENCES estudiantes(id_estudiante),

    estado VARCHAR(20) NOT NULL DEFAULT 'asignada',

    fecha_asignacion TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    puntaje INTEGER,
    recomendacion TEXT,
    fecha_evaluacion TIMESTAMP,

    CONSTRAINT uq_evaluacion_solicitud_evaluador
        UNIQUE (id_solicitud, id_evaluador)
);