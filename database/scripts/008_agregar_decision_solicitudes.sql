ALTER TABLE solicitudes
    ADD COLUMN IF NOT EXISTS comentario_decision TEXT,
    ADD COLUMN IF NOT EXISTS id_decisor INTEGER REFERENCES estudiantes(id_estudiante),
    ADD COLUMN IF NOT EXISTS fecha_decision TIMESTAMP;
