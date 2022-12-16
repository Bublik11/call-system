from datetime import date
from pydantic import BaseModel


class AppealBase(BaseModel):
    surname: str
    name: str
    patronymic: str
    phone_number: str
    message: str


class AppealDB(AppealBase):
    id: int
    created_at: date

    class Config:
        orm_mode = True
