ALTER TABLE estudiantes
    ADD COLUMN rol VARCHAR(20) NOT NULL DEFAULT 'estudiante';

ALTER TABLE estudiantes
    ADD CONSTRAINT chk_rol
        CHECK (rol IN ('estudiante', 'evaluador', 'administrador'));