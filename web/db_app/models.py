from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    topics = relationship("Topic", back_populates="project")
    clients = relationship("Client", back_populates="project")

    def __repr__(self):
        return f"Project(name={self.name})"


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    key = Column(String)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="topics")

    def __repr__(self):
        return f"Topic(key={self.key})"


class Client(Base):
    __tablename__ = "clients"

    username = Column(String, primary_key=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="clients")

    def __repr__(self):
        return f"Client(username={self.username}, is_admin={self.is_admin}, project_id={self.project_id})"
