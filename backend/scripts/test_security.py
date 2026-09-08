from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


def main():

    password = "TestPassword123!"

    # Test password hashing
    hashed = hash_password(password)

    print("Original password:", password)
    print("Hashed password:", hashed)

    # Test password verification
    print(
        "Correct password:",
        verify_password(password, hashed),
    )

    print(
        "Wrong password:",
        verify_password("WrongPassword", hashed),
    )

    # Test JWT creation
    token = create_access_token(
        {
            "sub": "testuser",
            "role": "USER",
        }
    )

    print("\nJWT token:")
    print(token)

    # Test JWT decoding
    payload = decode_access_token(token)

    print("\nDecoded payload:")
    print(payload)


if __name__ == "__main__":
    main()
