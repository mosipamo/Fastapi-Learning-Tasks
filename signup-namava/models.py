from pydantic import BaseModel


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    age: int | None = None
    roles: list[str] = []


class LoginRequest(BaseModel):
    username: str
    password: str
