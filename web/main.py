# from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi import Depends, FastAPI, Request
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


"""
@app.post("/clients/create/", response_model=schemas.ClientRead, tags=["clients"])
async def create_client(
    client: schemas.Client, db: Session = Depends(get_db)
) -> schemas.ClientRead:
    if crud.get_client_by_username(db, client.username):
        raise HTTPException(status_code=400, detail="Client already registered")
    return crud.create_client(db, client)


@app.get("/clients/", response_model=list[schemas.ClientRead], tags=["clients"])
async def get_clients(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schemas.ClientRead]:
    return crud.get_clients(db, skip=skip, limit=limit)


@app.get("/clients/{id}/", response_model=schemas.ClientRead, tags=["clients"])
async def get_client_by_username(
    id: int, db: Session = Depends(get_db)
) -> schemas.ClientRead:
    db_client = crud.get_client(db, id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@app.get(
    "/clients/username/{username}/", response_model=schemas.ClientRead, tags=["clients"]
)
async def get_client_by_username(username: str, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_username(db, username)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@app.put("/clients/{id}/", response_model=schemas.ClientRead, tags=["clients"])
async def update_client(
    id: str, client: schemas.Client, db: Session = Depends(get_db)
) -> schemas.ClientRead:
    db_client = crud.get_client(db, id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return crud.update_client(db, id, client)


@app.delete("/clients/{id}/", tags=["clients"])
async def delete_client(id: int, db: Session = Depends(get_db)) -> dict[str, bool]:
    db_client = crud.get_client(db, id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    crud.delete_client(db, id)
    return {"deleted": True}
"""


@app.post("/broker/check_user/", tags=["broker"])
async def check_user(request: Request, db: Session = Depends(get_db)) -> str:
    data = await request.form()
    username: str = data.get("username") or ""
    password: str = data.get("password") or ""
    if username == env.str("BROKER_USER") and password == env.str("BROKER_PASSWORD"):
        return PlainTextResponse("allow administrator")
    if username == env.str("SUPERUSER") and password == env.str("SUPERUSER_PASSWORD"):
        return PlainTextResponse("allow")
    if env.bool("CREATE_CLIENT_AUTOMATICALLY"):
        client = crud.get_client_by_username(db, username)
        if client:
            if client.password == password:
                return PlainTextResponse("allow")
            return PlainTextResponse("deny")
        crud.create_client(db, schemas.Client(username=username, password=password))
        return PlainTextResponse("allow")
    if crud.check_client(db, username, password):
        return PlainTextResponse("allow")
    return PlainTextResponse("deny")


@app.post("/broker/check_vhost/", tags=["broker"])
async def check_vhost(request: Request) -> str:
    data = await request.form()
    if data.get("username") in [env.str("BROKER_USER"), env.str("SUPERUSER")]:
        return PlainTextResponse("allow")
    if data.get("vhost") == "/":
        return PlainTextResponse("allow")
    return PlainTextResponse("deny")


@app.post("/broker/check_resource/", tags=["broker"])
async def check_resource(request: Request) -> str:
    return PlainTextResponse("allow")


@app.post("/broker/check_topic/", tags=["broker"])
async def check_topic(request: Request) -> str:
    data = await request.form()
    username: str = data.get("username") or ""
    if username in [env.str("BROKER_USER"), env.str("SUPERUSER")]:
        return PlainTextResponse("allow")
    if data.get("permission") == "read":
        for topic in env.list("CLIENT_READ_TOPICS"):
            if data.get("routing_key") == f"{topic}.{username}":
                return PlainTextResponse("allow")
        return PlainTextResponse("deny")
    if data.get("permission") == "write":
        for topic in env.list("CLIENT_WRITE_TOPICS"):
            if data.get("routing_key") == f"{topic}.{username}":
                return PlainTextResponse("allow")
        return PlainTextResponse("deny")
    return PlainTextResponse("deny")
