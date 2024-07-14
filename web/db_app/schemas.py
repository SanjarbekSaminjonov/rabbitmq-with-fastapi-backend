from pydantic import BaseModel


class Client(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class ClientRead(Client):
    id: int
