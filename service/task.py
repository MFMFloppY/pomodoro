from repository import TaskRepository, TaskCache
from models.task_model import TaskSchema
from dataclasses import dataclass

@dataclass
class TaskService:
    def __init__(self, task_repositiory: TaskRepository, task_cache: TaskCache):
        self.task_repository = task_repositiory
        self.task_cache = task_cache


    def get_tasks(self):

        if cache_task := self.task_cache.get_tasks():
            return cache_task
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)

            return tasks_schema