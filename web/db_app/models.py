from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    def __repr__(self):
        return f"Client(username={self.username}, is_admin={self.is_admin}"
