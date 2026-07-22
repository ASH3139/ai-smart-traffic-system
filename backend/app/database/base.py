from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.
    Every table in the project will inherit from this class.
    """
    pass