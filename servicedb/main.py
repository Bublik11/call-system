import crud, models, schemas
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/appeals/", response_model=list[schemas.Appeal])
def read_appeals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appeals = crud.get_appeals(db, skip=skip, limit=limit)
    return appeals


@app.get("/appeals/{appeal_id}", response_model=schemas.Appeal)
def read_appeal(appeal_id: int, db: Session = Depends(get_db)):
    db_appeal = crud.get_appeal(db, appeal_id=appeal_id)
    if db_appeal is None:
        raise HTTPException(status_code=404, detail="appeal not found")
    return db_appeal


@app.post("/appeals/", response_model=schemas.Appeal)
def create_appeal(
    appeal: schemas.AppealBase, db: Session = Depends(get_db)
):
    return crud.create_appeal(db=db, appeal=appeal)

