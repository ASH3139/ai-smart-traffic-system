from backend.app.database.session import SessionLocal
from backend.app.schemas.auth import UserCreate
from backend.app.services.auth.service import AuthService


def main():

    db = SessionLocal()

    try:
        auth_service = AuthService(db)

        user_data = UserCreate(
            username="testuser",
            password="TestPassword123!",
            role="USER",
        )

        user = auth_service.create_user(user_data)

        print("User created successfully")
        print("ID:", user.id)
        print("Username:", user.username)
        print("Role:", user.role)
        print("Active:", user.is_active)

        # Test authentication
        authenticated_user = auth_service.authenticate_user(
            username="testuser",
            password="TestPassword123!",
        )

        print("\nAuthentication successful")
        print("Authenticated user:", authenticated_user.username)

        # Test JWT creation
        token = auth_service.create_token(authenticated_user)

        print("\nJWT created successfully")
        print("Token:", token)

    finally:
        db.close()


if __name__ == "__main__":
    main()
