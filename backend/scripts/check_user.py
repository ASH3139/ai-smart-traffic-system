from sqlalchemy import select

from backend.app.database.session import SessionLocal
from backend.app.database.tables.user import User
from backend.app.core.security import verify_password


def main():

    db = SessionLocal()

    try:
        username = "normaluser"
        password = "TestPassword123!"

        user = db.scalar(select(User).where(User.username == username))

        if user is None:
            print("USER NOT FOUND")
            return

        print("User found")
        print("ID:", user.id)
        print("Username:", user.username)
        print("Role:", user.role)
        print("Active:", user.is_active)

        password_valid = verify_password(
            password,
            user.password_hash,
        )

        print("Password valid:", password_valid)

    finally:
        db.close()


if __name__ == "__main__":
    main()
