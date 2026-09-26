from app.core.security import hash_password, verify_password


def test_password_se_guarda_como_hash():
    password = "PruebaSegura@2026"

    hashed_password = hash_password(password)

    # La contraseña nunca debe quedar almacenada en texto plano.
    assert hashed_password != password

    # pwdlib está utilizando Argon2id.
    assert hashed_password.startswith("$argon2id$")


def test_password_correcta_es_valida():
    password = "PruebaSegura@2026"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_password_incorrecta_es_rechazada():
    password = "PruebaSegura@2026"
    hashed_password = hash_password(password)

    assert verify_password(
        "PasswordIncorrecta@2026",
        hashed_password
    ) is False


def test_mismo_password_genera_hashes_diferentes():
    password = "PruebaSegura@2026"

    hash_1 = hash_password(password)
    hash_2 = hash_password(password)

    # Argon2 utiliza salt aleatorio.
    assert hash_1 != hash_2

    # Ambos hashes deben seguir validando la contraseña original.
    assert verify_password(password, hash_1) is True
    assert verify_password(password, hash_2) is True