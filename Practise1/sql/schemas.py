from pydantic import BaseModel

class User(BaseModel):

    id: int
    name: str
    age: int
    country: str


class Login(BaseModel):
    username: str
    password: str
    email: str