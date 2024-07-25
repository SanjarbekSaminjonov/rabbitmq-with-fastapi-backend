from sqlalchemy import exists
from sqlalchemy.orm import Session

from . import models, schemas


def create_client(db: Session, client: schemas.Client) -> models.Client:
    db_client = models.Client(
        username=client.username,
        password=client.password,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_client(db: Session, id: int) -> models.Client:
    return db.query(models.Client).filter(models.Client.id == id).first()


def get_client_by_username(db: Session, username: str) -> models.Client:
    return db.query(models.Client).filter(models.Client.username == username).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> list[models.Client]:
    return db.query(models.Client).offset(skip).limit(limit).all()


def update_client(db: Session, id: int, client: schemas.Client) -> models.Client:
    _client = db.query(models.Client).filter(models.Client.id == id).first()
    _client.username = client.username
    _client.password = client.password
    db.commit()
    db.refresh(_client)
    return _client


def delete_client(db: Session, id: int) -> None:
    db.query(models.Client).filter(models.Client.id == id).delete()
    db.commit()


def check_client(db: Session, username: str, password: str) -> bool:
    return db.query(
        exists().where(
            models.Client.username == username, 
            models.Client.password == password
        )
    ).scalar()
