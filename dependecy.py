from fastapi import Depends
from repository import TaskRepository, TaskCache, UserRepository
from database import get_db_session
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from sqlalchemy.orm import Session


def get_tasks_repo(db_session: Session = Depends(get_db_session)) -> TaskRepository:

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


def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository: 

    return UserRepository(db_session=db_session)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:

    return UserService(user_repository=user_repository)


def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository)