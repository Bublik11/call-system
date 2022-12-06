from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import models, schemas


async def get_appeal(session: AsyncSession, appeal_id: int) -> models.Appeal | None:
    """Получить заявку по id"""
    query = select(models.Appeal).where(models.Appeal.id == appeal_id)
    return await session.execute(query).scalars().first()

async def get_appeals(session: AsyncSession, skip: int = 0, limit: int = 100, ) -> list[models.Appeal] | None:
    """Получить все заявки по телефону"""
    query = select(models.Appeal).offset(skip).limit(100)
    return await session.execute(query).scalars().all()   

async def get_all_appeals_by_phone(session: AsyncSession, phone: str) -> models.Appeal | list[models.Appeal] | None:
    """Получить все заявки по телефону"""
    query = select(models.Appeal).where(models.Appeal.phone_number == phone)
    return await session.execute(query).scalars().all()

async def get_all_unchecked_appeals(session: AsyncSession) -> models.Appeal | list[models.Appeal] | None:
    """Получить заявку все непроверенные заявки"""
    query = select(models.Appeal).where(models.Appeal.checked == False)
    return await session.execute(query).scalars().all()

async def create_appeal(session: AsyncSession, appeal: schemas.Appeal) -> models.Appeal:
    """Создать заявку"""
    db_appeal = models.Appeal(**appeal)
    await session.add(db_appeal)
    await session.refresh(db_appeal)
    return await db_appeal
