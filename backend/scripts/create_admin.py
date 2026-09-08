from backend.app.database.session import SessionLocal
from backend.app.database.tables.user import User
from backend.app.core.security import hash_password
from sqlalchemy import select


def main():

    db = SessionLocal()

    try:
        username = "admin"
        password = "AdminPassword123!"

        existing_user = db.scalar(select(User).where(User.username == username))

        if existing_user:
            existing_user.role = "ADMIN"
            existing_user.is_active = True
            db.commit()

            print("Existing user promoted to ADMIN.")
            print("Username:", existing_user.username)
            print("Role:", existing_user.role)

        else:
            admin = User(
                username=username,
                password_hash=hash_password(password),
                role="ADMIN",
                is_active=True,
            )

            db.add(admin)
            db.commit()
            db.refresh(admin)

            print("Admin user created successfully.")
            print("ID:", admin.id)
            print("Username:", admin.username)
            print("Role:", admin.role)

    finally:
        db.close()


if __name__ == "__main__":
    main()
