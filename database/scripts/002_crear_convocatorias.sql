
 --US-005: Crear convocatoria
-- Sistema de Gestion de Becas


CREATE TABLE convocatorias (
    id_convocatoria SERIAL PRIMARY KEY,

    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,

    tipo_beca VARCHAR(100) NOT NULL,
    institucion VARCHAR(150) NOT NULL,

    fecha_apertura DATE NOT NULL,
    fecha_cierre DATE NOT NULL,

    nivel_educativo VARCHAR(50) NOT NULL,
    requisitos TEXT NOT NULL,

    monto_beneficio NUMERIC(12, 2),
    cupos_disponibles INTEGER,

    estado VARCHAR(20) NOT NULL DEFAULT 'borrador',

    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_ultima_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_fechas_convocatoria
        CHECK (fecha_cierre > fecha_apertura),

    CONSTRAINT chk_monto_beneficio
        CHECK (
            monto_beneficio IS NULL
            OR monto_beneficio >= 0
        ),

    CONSTRAINT chk_cupos_disponibles
        CHECK (
            cupos_disponibles IS NULL
            OR cupos_disponibles >= 0
        ),

    CONSTRAINT chk_estado_convocatoria
        CHECK (
            estado IN (
                'borrador',
                'publicada',
                'cerrada'
            )
        )
);