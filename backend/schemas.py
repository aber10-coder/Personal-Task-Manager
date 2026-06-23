from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str


class TokenResponse(BaseModel):
    token: str


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: str


class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
    due_date: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    due_date: str
    owner_email: str