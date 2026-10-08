ALTER TABLE documentos
    ADD COLUMN IF NOT EXISTS estado_validacion VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    ADD COLUMN IF NOT EXISTS comentario_validacion TEXT,
    ADD COLUMN IF NOT EXISTS id_validador INTEGER REFERENCES estudiantes(id_estudiante),
    ADD COLUMN IF NOT EXISTS fecha_validacion TIMESTAMP;
