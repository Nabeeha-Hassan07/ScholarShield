import hashlib
import hmac
import secrets

from database.database import get_connection


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):
    """
    Create a secure salted password hash.
    """

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


# =========================================================
# PASSWORD VERIFICATION
# =========================================================

def verify_password(password, stored_hash):
    """
    Verify a password against the stored salted hash.
    """

    try:
        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return hmac.compare_digest(
            new_hash.hex(),
            hash_hex
        )

    except (ValueError, TypeError):
        return False


# =========================================================
# REGISTER USER
# =========================================================

def register_user(name, email, password):
    """
    Register a new user in the database.

    Returns:
        (True, message)  → successful
        (False, message) → unsuccessful
    """

    name = name.strip()
    email = email.strip().lower()

    connection = get_connection()

    cursor = connection.cursor()

    # Check whether email already exists
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        connection.close()

        return False, "An account with this email already exists."

    password_hash = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users
        (
            name,
            email,
            password_hash
        )
        VALUES (?, ?, ?)
        """,
        (
            name,
            email,
            password_hash
        )
    )

    connection.commit()
    connection.close()

    return True, "Account created successfully."


# =========================================================
# LOGIN USER
# =========================================================

def authenticate_user(email, password):
    """
    Authenticate a user using email and password.

    Returns:
        User row if successful.
        None if authentication fails.
    """

    email = email.strip().lower()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            password_hash,
            created_at
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    if verify_password(
        password,
        user["password_hash"]
    ):
        return user

    return None