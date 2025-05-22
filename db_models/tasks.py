from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from typing import Optional
from sqlalchemy import ForeignKey


class Tasks(Base):

    task_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfile.id"), nullable=False )

class Categories(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Optional[str]]
    name: Mapped[str]