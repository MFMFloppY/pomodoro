from pydantic import BaseModel, model_validator


class Category(BaseModel):
    id: int | None = None
    name: str | None = None

    @model_validator(mode="after")
    def chk_name_not_none(self):
        if self.name is None :
            raise ValueError("Error: No name. Enter again.")
        return self