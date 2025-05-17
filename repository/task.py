from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from db_models import Tasks, Categories

from models.task_model import TaskSchema



class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_tasks(self) -> list[Tasks]:

        with self.db_session() as session:
            tasks: list[Tasks] = session.execute(select(Tasks)).scalars().all()

        return tasks
    

    def get_task(self, task_id: int) -> Tasks | None:

        with self.db_session() as session:
            task: Tasks = session.execute(select(Tasks).where(Tasks.task_id == task_id)).scalar_one_or_none()

            return task


    def create_task(self, task: TaskSchema) -> None:
        task_model = Tasks(name = task.name, pomodoro_count = task.pomodoro_count, category_id = task.category_id)
        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.task_id

    
    def delete_task(self, task_id: int) -> None:
        with self.db_session() as session:
            session.execute(delete(Tasks).where(Tasks.task_id == task_id))
            session.commit()
    
    
    def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.db_session() as session:
            tasks: list[Tasks] = session.execute(query).scalars().all()

            return tasks
    

    def update_task(self, task_id: int, name: str, pomodoro_count: int, category_id: int) -> Tasks:
        query = update(Tasks).where(Tasks.task_id == task_id).values(name = name, pomodoro_count = pomodoro_count, category_id = category_id).returning(Tasks.task_id)
        with self.db_session() as session:
            updated_tasks_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(updated_tasks_id)


