from databases import Database
from .models import appeals
 

async def get_appeal_by_id(database: Database, appeal_id: int):
    """Получить заявку по id"""
    query = appeals.select().where(appeals.c.id == appeal_id)
    return await database.fetch_one(query=query)

async def get_all_appeals(database: Database, skip: int = 0, limit: int = 100):
    """Получить все заявки"""
    query = appeals.select().limit(limit).offset(skip)
    return await database.fetch_all(query=query)

async def get_all_appeals_by_phone(database: Database, phone: str):
    """Получить все заявки по телефону"""
    query = appeals.select().where(appeals.c.phone_number == phone)
    return await database.fetch_all(query=query)

async def create_appeal(database: Database, surname: str,
            name: str,
            patronymic: str,
            phone_number: str,
            message: str):
    """Создать заявку"""
    values = {
        'surname' : surname,
        'name' : name,
        'patronymic' : patronymic,
        'phone_number' : phone_number,
        'message' : message
    }
    query = appeals.insert(inline=True)
    id = await database.execute(query=query, values=values)
    return await get_appeal_by_id(database=database, appeal_id=id)