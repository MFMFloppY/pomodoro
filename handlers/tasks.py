from fastapi import APIRouter, status, Depends, HTTPException
from models import TaskSchema, TaskCreateSchema
from typing import Annotated
from repository import TaskRepository
from dependecy import get_tasks_service, get_request_user_id
from service import TaskService
from exeption import TaskNotFound


router = APIRouter(prefix="/tasks)",tags=["tasks"])


@router.get(
        "/get_tasks",
        response_model=list[TaskSchema]
        )

def Get_all_tasks(task_service: Annotated[TaskService, Depends(get_tasks_service)]):
    """Возвращает список задач."""

    return task_service.get_tasks()

@router.post(
        "/create_task",
        response_model=TaskSchema,
        status_code=status.HTTP_201_CREATED
        )

def Create_new_task(body: TaskCreateSchema,
                    task_service: Annotated[TaskService, Depends(get_tasks_service)],
                    user_id: int = Depends(get_request_user_id)):
    """Создает новую задачу."""
    
    new_task = task_service.create_task(body, user_id)
    return new_task


@router.patch(
    "/update_task",
    status_code=status.HTTP_202_ACCEPTED
    )

def Update_task(task_id: int, 
                name: str, 
                task_service: Annotated[TaskService, Depends(get_tasks_service)],
                user_id: int = Depends(get_request_user_id)
                ):
    """Обновляет параметры текущей задачи."""
    try:
        return task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    

@router.delete(
    "/delete_task"
    )

def delete_task(task_id: int,
                 task_service: Annotated[TaskRepository, Depends(get_tasks_service)],
                 user_id: int = Depends(get_request_user_id)):
    """Удаляет задачу с заданным id."""

    try:
        task_service.delete_task(task_id=task_id, user_id=user_id)
        return f"Task {task_id} sucsessfully deleted."
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)

    