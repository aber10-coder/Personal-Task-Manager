from fastapi import FastAPI
from db import init_db

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Task Manager API"}


@app.post("/auth/register")
def register():
    return {"message": "register"}


@app.post("/auth/login")
def login():
    return {"message": "login"}


@app.get("/auth/me")
def me():
    return {"message": "me"}


@app.post("/tasks")
def create_task():
    return {"message": "create task"}


@app.get("/tasks")
def get_tasks():
    return {"message": "get tasks"}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"message": f"task {task_id}"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    return {"message": f"update {task_id}"}


@app.patch("/tasks/{task_id}/status")
def update_status(task_id: int):
    return {"message": f"status {task_id}"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return {"message": f"delete {task_id}"}


@app.get("/tasks/summary")
def summary():
    return {"message": "summary"}