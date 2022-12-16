from fastapi import FastAPI, HTTPException
from database import crud
from database import engine, metadata, database  
from schemas import AppealDB, AppealBase
from rmq_consumer import consume

metadata.create_all(bind=engine)

app = FastAPI(debug=True, title='Appeals')

@app.on_event('startup')
async def startup():
    await consume()
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@app.get('/appeals/all', response_model=list[AppealDB | None])
async def read_all_appeals(skip: int = 0, limit: int = 100):
    appeals = await crud.get_all_appeals(database=database, skip=skip, limit=limit)
    return appeals

@app.get('/appeals', response_model=list[AppealDB]) 
async def read_appeal_by_phone(phone: str):
    appeals = await crud.get_all_appeals_by_phone(database=database, phone=phone)
    return appeals

@app.get('/appeals/{appeal_id}', response_model=AppealDB) 
async def read_appeal_by_id(appeal_id: int):
    one_appeal = await crud.get_appeal_by_id(database=database, appeal_id=appeal_id)
    if not one_appeal:
        raise HTTPException(status_code=404, detail='appeal not found')
    return one_appeal

@app.post('/appeals/', response_model=AppealDB)
async def create_appeal(appeal: AppealBase):
    return await crud.create_appeal(database=database, **appeal.dict())
