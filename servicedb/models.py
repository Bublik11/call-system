import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime, func

from database import Base


class Appeal(Base):
    __tablename__ = "appeal"

    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    phone_number = Column(String)
    message = Column(String)
    checked = Column(Boolean, default=False)
    update_at = Column(DateTime, nullable=True, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, server_default=func.now())
