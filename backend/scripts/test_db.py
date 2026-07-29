from sqlalchemy import text

from backend.app.database.connection import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    print(result.fetchone())
