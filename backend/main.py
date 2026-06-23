from fastapi import FastAPI
from db import init_db
from routers.auth_router import router as auth_router
from routers.tasks_router import router as tasks_router
app = FastAPI()
app.include_router(auth_router)
app.include_router(tasks_router)

@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Task Manager API"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    return {"message": f"update {task_id}"}


@app.patch("/tasks/{task_id}/status")
def update_status(task_id: int):
    return {"message": f"status {task_id}"}

@app.get("/tasks/summary")
def summary():
    return {"message": "summary"}