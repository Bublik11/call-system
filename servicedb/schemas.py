from datetime import date
from pydantic import BaseModel


class AppealBase(BaseModel):
    surname: str
    name: str
    patronymic: str
    phone_number: str
    message: str


class Appeal(AppealBase):
    id: int
    checked: bool = False
    created_at: date
    update_at: date

    class Config:
        orm_mode = True
