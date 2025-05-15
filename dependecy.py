from fastapi import Depends
from repository import TaskRepository, TaskCache
from database import get_db_session
from cache import get_redis_connection
from service import TaskService

def get_tasks_repo() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_tasks_cacherepository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)
    

def get_tasks_service(task_repository: TaskRepository = Depends(get_tasks_repo), 
                      task_cache: TaskCache = Depends(get_tasks_cacherepository)
                      ) -> TaskService:
    return TaskService(
        task_repositiory=task_repository,
        task_cache=task_cache
        )