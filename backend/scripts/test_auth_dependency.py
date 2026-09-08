from backend.app.core.security import create_access_token
from backend.app.database.session import SessionLocal
from backend.app.dependencies.auth import get_current_user


def main():

    db = SessionLocal()

    try:
        # Create a token for the existing test user.
        token = create_access_token(
            {
                "sub": "1",
                "username": "testuser",
                "role": "USER",
            }
        )

        print("Token created:")
        print(token)

        # Validate token and retrieve user.
        user = get_current_user(
            token=token,
            db=db,
        )

        print("\nJWT validation successful")
        print("User ID:", user.id)
        print("Username:", user.username)
        print("Role:", user.role)
        print("Active:", user.is_active)

    finally:
        db.close()


if __name__ == "__main__":
    main()
