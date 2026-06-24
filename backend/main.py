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


