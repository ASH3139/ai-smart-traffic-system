from backend.app.database.session import SessionLocal
from backend.app.services.auth.service import AuthService


def main():

    db = SessionLocal()

    try:
        auth_service = AuthService(db)

        user = auth_service.authenticate_user(
            username="normaluser",
            password="TestPassword123!",
        )

        print("Authentication successful")
        print("ID:", user.id)
        print("Username:", user.username)
        print("Role:", user.role)
        print("Active:", user.is_active)

        token = auth_service.create_token(user)

        print("\nJWT created successfully")
        print(token)

    finally:
        db.close()


if __name__ == "__main__":
    main()
