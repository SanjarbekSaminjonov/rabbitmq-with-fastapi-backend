from sqlalchemy.orm import Session

from . import models, schemas


def create_project(db: Session, project: schemas.Project) -> models.Project:
    db_project = models.Project(name=project.name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, id: int) -> models.Project | None:
    return db.query(models.Project).filter(models.Project.id == id).first()


def get_project_by_name(db: Session, name: str) -> models.Project | None:
    return db.query(models.Project).filter(models.Project.name == name).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> list[models.Project]:
    return db.query(models.Project).offset(skip).limit(limit).all()


def update_project(db: Session, id: int, project: schemas.Project) -> models.Project:
    db_project = db.query(models.Project).filter(models.Project.id == id).first()
    db_project.name = project.name
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, id: int) -> None:
    db.query(models.Project).filter(models.Project.id == id).delete()
    db.commit()


def create_topic(db: Session, topic: schemas.Topic) -> models.Topic:
    db_topic = models.Topic(type=topic.type, key=topic.key, project_id=topic.project_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_topic(db: Session, id: int) -> models.Topic | None:
    return db.query(models.Topic).filter(models.Topic.id == id).first()

def get_topic_by_key(db: Session, key: str) -> models.Topic | None:
    return db.query(models.Topic).filter(models.Topic.key == key).first()

def get_topics(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Topic]:
    return db.query(models.Topic).offset(skip).limit(limit).all()


def update_topic(db: Session, id: int, topic: schemas.Topic) -> models.Topic:
    db_topic = db.query(models.Topic).filter(models.Topic.id == id).first()
    db_topic.type = topic.type
    db_topic.key = topic.key
    db_topic.project_id = topic.project_id
    db.commit()
    db.refresh(db_topic)
    return db_topic


def delete_topic(db: Session, id: int) -> None:
    db.query(models.Topic).filter(models.Topic.id == id).delete()
    db.commit()


def create_client(db: Session, client: schemas.Client) -> models.Client:
    db_client = models.Client(
        username=client.username,
        password=client.password,
        is_admin=client.is_admin,
        project_id=client.project_id,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_client(db: Session, username: str) -> models.Client:
    return db.query(models.Client).filter(models.Client.username == username).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> list[models.Client]:
    return db.query(models.Client).offset(skip).limit(limit).all()


def update_client(
    db: Session, username: str, client: schemas.ClientUpdate
) -> models.Client:
    db_client = (
        db.query(models.Client).filter(models.Client.username == username).first()
    )
    db_client.password = client.password
    db_client.is_admin = client.is_admin
    db_client.project_id = client.project_id
    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, username: str) -> None:
    db.query(models.Client).filter(models.Client.username == username).delete()
    db.commit()
