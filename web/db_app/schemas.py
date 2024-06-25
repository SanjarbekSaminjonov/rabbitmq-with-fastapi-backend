from pydantic import BaseModel


class Project(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ProjectRead(Project):
    id: int


class Topic(BaseModel):
    type: str
    key: str
    project_id: int

    class Config:
        from_attributes = True


class TopicRead(Topic):
    id: int


class TopicReadDetail(TopicRead):
    project: ProjectRead


class ClientUpdate(BaseModel):
    password: str
    is_admin: bool
    project_id: int

    class Config:
        from_attributes = True


class Client(ClientUpdate):
    username: str


class ClientReadDetail(Client):
    project: ProjectRead


class ProjectReadDetail(ProjectRead):
    topics: list[TopicRead]
    clients: list[Client]
