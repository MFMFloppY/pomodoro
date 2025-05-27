from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    access_token: str


class YandexUserData(BaseModel):
    id: int
    default_email: str 
    access_token: str
    name: str = Field(alias="display_name")
