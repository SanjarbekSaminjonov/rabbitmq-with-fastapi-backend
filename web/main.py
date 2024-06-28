from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from settings import env
from db_app import crud, models, schemas
from db_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="RabbitMQ Broker Connections Controller",
    description="This API is used to manage RabbitMQ connections.",
    version="1.0.0",
    docs_url=env.str("DOCS_URL"),
    redoc_url=env.str("REDOC_URL"),
    openapi_url=env.str("OPENAPI_URL"),
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/projects/create/", response_model=schemas.ProjectReadDetail, tags=["projects"]
)
async def create_project(project: schemas.Project, db: Session = Depends(get_db)):
    if crud.get_project_by_name(db, project.name):
        raise HTTPException(status_code=400, detail="Project already registered")
    return crud.create_project(db, project)


@app.get("/projects/", response_model=list[schemas.ProjectRead], tags=["projects"])
async def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit)


@app.get("/projects/{id}/", response_model=schemas.ProjectReadDetail, tags=["projects"])
async def get_project(id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.put("/projects/{id}/", response_model=schemas.ProjectReadDetail, tags=["projects"])
async def update_project(
    id: int, project: schemas.Project, db: Session = Depends(get_db)
):
    db_project = crud.get_project(db, id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.update_project(db, id, project)


@app.delete("/projects/{id}/", tags=["projects"])
async def delete_project(id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if len(db_project.topics) > 0:
        raise HTTPException(status_code=400, detail="Project has topics")
    if len(db_project.clients) > 0:
        raise HTTPException(status_code=400, detail="Project has clients")
    crud.delete_project(db, id)


@app.post("/topics/create/", response_model=schemas.TopicReadDetail, tags=["topics"])
async def create_topic(topic: schemas.Topic, db: Session = Depends(get_db)):
    if crud.get_topic_by_key(db, topic.key):
        raise HTTPException(status_code=400, detail="Topic already registered")
    project = crud.get_project(db, topic.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.create_topic(db, topic)


@app.get("/topics/", response_model=list[schemas.TopicRead], tags=["topics"])
async def get_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_topics(db, skip=skip, limit=limit)


@app.get("/topics/{id}/", response_model=schemas.TopicReadDetail, tags=["topics"])
async def get_topic(id: int, db: Session = Depends(get_db)):
    db_topic = crud.get_topic(db, id)
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic


@app.put("/topics/{id}/", response_model=schemas.TopicRead, tags=["topics"])
async def update_topic(id: int, topic: schemas.Topic, db: Session = Depends(get_db)):
    db_topic = crud.get_topic(db, id)
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    project = crud.get_project(db, topic.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.update_topic(db, id, topic)


@app.delete("/topics/{id}/", tags=["topics"])
async def delete_topic(id: int, db: Session = Depends(get_db)):
    db_topic = crud.get_topic(db, id)
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    crud.delete_topic(db, id)


@app.post("/clients/create/", response_model=schemas.ClientReadDetail, tags=["clients"])
async def create_client(client: schemas.Client, db: Session = Depends(get_db)):
    if crud.get_client(db, client.username):
        raise HTTPException(status_code=400, detail="Client already registered")
    project = crud.get_project(db, client.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.create_client(db, client)


@app.get("/clients/", response_model=list[schemas.Client], tags=["clients"])
async def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clients(db, skip=skip, limit=limit)


@app.get(
    "/clients/{username}/", response_model=schemas.ClientReadDetail, tags=["clients"]
)
async def get_client(username: str, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, username)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@app.put(
    "/clients/{username}/", response_model=schemas.ClientReadDetail, tags=["clients"]
)
async def update_client(
    username: str, client: schemas.ClientUpdate, db: Session = Depends(get_db)
):
    db_client = crud.get_client(db, username)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    project = crud.get_project(db, client.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.update_client(db, username, client)


@app.delete("/clients/{username}/", tags=["clients"])
async def delete_client(username: str, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, username)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    crud.delete_client(db, username)


@app.post("/broker/check_user/", tags=["broker"])
async def check_user(request: Request, db: Session = Depends(get_db)) -> str:
    data = await request.form()
    username: str = data.get("username") or ""
    password: str = data.get("password") or ""
    if username == env.str("BROKER_USER") and password == env.str("BROKER_PASSWORD"):
        return PlainTextResponse("allow administrator")
    if username.startswith("websocket/") and password == "saminjonov.uz":
        client = crud.get_client(db, username.replace("websocket/", ""))
        return PlainTextResponse("allow" if client else "deny")
    client = crud.get_client(db, username)
    if client and client.password == data.get("password"):
        return PlainTextResponse("allow")
    return PlainTextResponse("deny")


@app.post("/broker/check_vhost/", tags=["broker"])
async def check_vhost(request: Request) -> str:
    data = await request.form()
    if data.get("username") == env.str("BROKER_USER"):
        return PlainTextResponse("allow")
    if data.get("vhost") == "/":
        return PlainTextResponse("allow")
    return PlainTextResponse("deny")


@app.post("/broker/check_resource/", tags=["broker"])
async def check_resource(request: Request) -> str:
    return PlainTextResponse("allow")


@app.post("/broker/check_topic/", tags=["broker"])
async def check_topic(request: Request, db: Session = Depends(get_db)) -> str:
    data = await request.form()
    username: str = data.get("username") or ""
    if (
        username.startswith("websocket/")
        and data.get("permission") == "read"
        and data.get("routing_key") == username.replace("/", ".")
    ):
        return PlainTextResponse("allow")
    if username == env.str("BROKER_USER"):
        return PlainTextResponse("allow")
    client = crud.get_client(db, username)
    if client and client.is_admin:
        return PlainTextResponse("allow")
    for topic in client.project.topics:
        if (
            data.get("permission") == topic.type
            and data.get("routing_key") == f"{topic.key}.{username}"
        ):
            return PlainTextResponse("allow")
    return PlainTextResponse("deny")
