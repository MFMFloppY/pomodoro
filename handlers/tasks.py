from fastapi import APIRouter, status, Depends
from models.task_model import TaskSchema
from typing import Annotated
from repository import TaskRepository
from dependecy import get_tasks_repo, get_tasks_service, get_request_user_id
from service import TaskService


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

def Create_new_task(new_task: TaskSchema, task_repository: Annotated[TaskRepository, Depends(get_tasks_repo)], user_id: int = Depends(get_request_user_id)):
    """Создает новую задачу."""
    
    taskid = task_repository.create_task(new_task)
    new_task.task_id = taskid
    return new_task


@router.patch(
    "/update_task",
    status_code=status.HTTP_202_ACCEPTED
    )

def Update_task(task_id: int, name: str, pomodoro_count: int, category_id: int,
                task_repository: Annotated[TaskRepository, Depends(get_tasks_repo)]
                ):
    """Обновляет параметры текущей задачи."""
    
    return task_repository.update_task(task_id, name, pomodoro_count, category_id)
    

@router.delete(
    "/delete_task"
    )

def delete_task(task_id: int,
                 task_repository: Annotated[TaskRepository, Depends(get_tasks_repo)]
                 ):
    """Удаляет задачу с заданным id."""

    task_repository.delete_task(task_id)

    return f"Task {task_id} sucsessfully deleted."

    