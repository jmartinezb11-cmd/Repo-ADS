ALTER TABLE evaluaciones
    ADD COLUMN IF NOT EXISTS puntaje INTEGER
        CHECK (puntaje >= 0 AND puntaje <= 100),
    ADD COLUMN IF NOT EXISTS recomendacion VARCHAR(20)
        CHECK (recomendacion IN ('aprobar', 'rechazar')),
    ADD COLUMN IF NOT EXISTS fecha_evaluacion TIMESTAMP;