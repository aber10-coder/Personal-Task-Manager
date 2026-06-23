from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user

from db import (
    create_task,
    get_tasks_by_owner,
    get_task_by_id,
    delete_task,
    update_task
)

from schemas import TaskCreate,TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/")
def add_task(
    task: TaskCreate,
    current_user=Depends(get_current_user)
):
    return create_task(
        task.title,
        task.description,
        task.priority,
        "pending",
        task.due_date,
        current_user
    )


@router.get("/")
def get_tasks(
    current_user=Depends(get_current_user)
):
    return get_tasks_by_owner(
        current_user
    )


@router.get("/{task_id}")
def get_task(
    task_id: int,
    current_user=Depends(get_current_user)
):
    task = get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task["owner_email"] != current_user:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    return task


@router.delete("/{task_id}")
def remove_task(
    task_id: int,
    current_user=Depends(get_current_user)
):
    task = get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task["owner_email"] != current_user:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    delete_task(task_id)

    return {
        "message": "Task deleted"
    }

@router.put("/{task_id}")
def edit_task(
    task_id: int,
    task: TaskUpdate,
    current_user=Depends(get_current_user)
):
    existing_task = get_task_by_id(
        task_id
    )

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if existing_task["owner_email"] != current_user:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    return update_task(
        task_id,
        task.title,
        task.description,
        task.priority,
        task.status,
        task.due_date
    )