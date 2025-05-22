from repository import TaskRepository, TaskCache
from models.task_model import TaskSchema, TaskCreateSchema
from dataclasses import dataclass
from exeption import TaskNotFound

@dataclass
class TaskService:
    def __init__(self, task_repositiory: TaskRepository, task_cache: TaskCache):
        self.task_repository = task_repositiory
        self.task_cache = task_cache


    def get_tasks(self) -> list[TaskSchema]:

        if cache_task := self.task_cache.get_tasks():
            return cache_task
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)

            return tasks_schema
    

    def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = self.task_repository.create_task(body, user_id)
        new_task = self.task_repository.get_task(task_id)
        return TaskSchema.model_validate(new_task)
    

    def update_task_name(self, task_id, name, user_id) -> TaskSchema:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        task = self.task_repository.update_task_name(task_id=task_id, name=name)
        return TaskSchema.model_validate(task)
    

    def delete_task(self, task_id, user_id) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)