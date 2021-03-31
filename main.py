import uvicorn
from fastapi import FastAPI, Depends
import os 
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from models import Event as ModelEvent
from schema import Event as SchemaEvent
from dotenv import load_dotenv
from database import SessionLocal, engine
import models
from admin import check_first_bill, check_feedback, alert_user


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/events/", response_model=SchemaEvent)
def root(event: SchemaEvent, database: Session = Depends(get_db)):
    db_event = ModelEvent(**event.dict())
    db.session.add(db_event)
    db.session.commit()

    userid = event.userid
    check_first_bill(database, userid)
    return db_event



@app.get("/admin/{userid}")
def admins(userid: str, db: Session = Depends(get_db)):
    check_feedback(db, userid)
    alert_user(db, userid)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
