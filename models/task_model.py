from pydantic import BaseModel, model_validator


class TaskSchema(BaseModel):
    task_id: int | None = None
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int | None = None

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def chk_name_or_count_not_none(self):
        if self.name is None or self.pomodoro_count is None:
            raise ValueError("Error: No name or Pomodoro count. Enter again.")
        return self

