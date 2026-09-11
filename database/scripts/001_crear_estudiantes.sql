-- =========================================================
-- US-001: Registro de estudiante
-- Sistema de Gestión de Becas
-- =========================================================

-- =========================
-- TABLA: estudiantes
-- =========================

CREATE TABLE estudiantes (
    id_estudiante SERIAL PRIMARY KEY,

    -- Datos personales
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50),

    cui VARCHAR(20) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(20) NOT NULL,
    nacionalidad VARCHAR(50) NOT NULL,

    telefono VARCHAR(20) NOT NULL,
    telefono_alternativo VARCHAR(20),

    departamento VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    zona_aldea VARCHAR(100),
    direccion_exacta VARCHAR(255) NOT NULL,

    discapacidad BOOLEAN NOT NULL DEFAULT FALSE,
    tipo_discapacidad VARCHAR(100),

    pueblo_pertenencia VARCHAR(50),

    -- Cuenta / estado
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,

    estado_cuenta VARCHAR(30) NOT NULL DEFAULT 'pendiente_verificacion',

    email_verificado BOOLEAN NOT NULL DEFAULT FALSE,

    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_ultima_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Validaciones
    CONSTRAINT chk_estado_cuenta
        CHECK (estado_cuenta IN (
            'activo',
            'inactivo',
            'pendiente_verificacion'
        )),

    CONSTRAINT chk_discapacidad
        CHECK (
            discapacidad = TRUE
            OR tipo_discapacidad IS NULL
        )
);


-- =========================
-- TABLA: datos_academicos
-- =========================

CREATE TABLE datos_academicos (
    id_academico SERIAL PRIMARY KEY,

    id_estudiante INTEGER NOT NULL UNIQUE,

    nivel_educativo VARCHAR(30) NOT NULL,

    -- Secundaria / diversificado
    establecimiento_educativo VARCHAR(150),
    grado_actual VARCHAR(50),
    jornada VARCHAR(30),
    sector VARCHAR(30),
    promedio_notas NUMERIC(5,2),
    especialidad VARCHAR(100),

    -- Universidad
    universidad VARCHAR(150),
    facultad_escuela VARCHAR(150),
    carrera VARCHAR(150),
    anio_semestre_actual VARCHAR(50),
    carnet_universitario VARCHAR(50),
    cum NUMERIC(5,2),
    creditos_aprobados INTEGER,
    modalidad VARCHAR(30),

    CONSTRAINT fk_academico_estudiante
        FOREIGN KEY (id_estudiante)
        REFERENCES estudiantes(id_estudiante)
        ON DELETE CASCADE
);


-- =========================
-- TABLA: datos_socioeconomicos
-- =========================

CREATE TABLE datos_socioeconomicos (
    id_socioeconomico SERIAL PRIMARY KEY,

    id_estudiante INTEGER NOT NULL UNIQUE,

    ingreso_familiar_mensual NUMERIC(10,2),
    numero_miembros_nucleo INTEGER,

    ocupacion_padre VARCHAR(150),
    ocupacion_madre VARCHAR(150),
    ocupacion_encargado VARCHAR(150),

    tipo_vivienda VARCHAR(30),

    dependientes_economicos INTEGER,

    CONSTRAINT fk_socio_estudiante
        FOREIGN KEY (id_estudiante)
        REFERENCES estudiantes(id_estudiante)
        ON DELETE CASCADE
);


-- =========================
-- TABLA: contacto_emergencia
-- =========================

CREATE TABLE contacto_emergencia (
    id_contacto SERIAL PRIMARY KEY,

    id_estudiante INTEGER NOT NULL UNIQUE,

    nombre_encargado VARCHAR(150) NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    telefono_emergencia VARCHAR(20) NOT NULL,

    CONSTRAINT fk_contacto_estudiante
        FOREIGN KEY (id_estudiante)
        REFERENCES estudiantes(id_estudiante)
        ON DELETE CASCADE
);