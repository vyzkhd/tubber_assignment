import uvicorn
from fastapi import FastAPI, Depends, BackgroundTasks
import os 
import sched, time 
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
async def root(event: SchemaEvent, background_tasks: BackgroundTasks, database: Session = Depends(get_db)):
    db_event = ModelEvent(**event.dict())
    db.session.add(db_event)
    db.session.commit()

    userid = event.userid
    if event.noun == 'bill':
        check_first_bill(database, userid)
       
        s = sched.scheduler(time.time, time.sleep)
        s.enter(5*60, 1, alert_user, (database, userid))
        s.enter(15*60, 2, check_feedback, (database, userid))
        background_tasks.add_task(s.run)
    return db_event



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
