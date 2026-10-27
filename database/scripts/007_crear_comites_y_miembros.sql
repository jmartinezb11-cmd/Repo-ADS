-- US-021: Crear comites
CREATE TABLE IF NOT EXISTS comites (
    id_comite SERIAL PRIMARY KEY,
    nombre_comite VARCHAR(150) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_estado_comite
        CHECK (estado IN ('ACTIVO', 'INACTIVO'))
);

-- US-022: Asignar miembros al comite
CREATE TABLE IF NOT EXISTS miembros_comite (
    id_miembro SERIAL PRIMARY KEY,
    id_comite INTEGER NOT NULL,
    id_estudiante INTEGER NOT NULL,
    rol_comite VARCHAR(30) NOT NULL DEFAULT 'EVALUADOR',
    fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_miembro_comite
        FOREIGN KEY (id_comite)
        REFERENCES comites(id_comite)
        ON DELETE CASCADE,

    CONSTRAINT fk_miembro_estudiante
        FOREIGN KEY (id_estudiante)
        REFERENCES estudiantes(id_estudiante),

    CONSTRAINT uq_miembro_comite
        UNIQUE (id_comite, id_estudiante),

    CONSTRAINT chk_rol_comite
        CHECK (rol_comite IN (
            'PRESIDENTE',
            'EVALUADOR',
            'SECRETARIO'
        ))
);