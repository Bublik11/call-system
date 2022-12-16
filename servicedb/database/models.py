from sqlalchemy import (Table, Column, Integer, String, DateTime, func)
from .config import metadata

appeals = Table(
    "appeals",
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True, index=True),
    Column('surname', String),
    Column('name', String),
    Column('patronymic', String),
    Column('phone_number', String),
    Column('message', String),
    Column('created_at', DateTime, server_default=func.now()),
)
