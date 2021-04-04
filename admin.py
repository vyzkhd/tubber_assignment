from models import Event
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import logging


logging.basicConfig(filename='tubber.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def check_first_bill(db: Session, userid: int):
    counts = db.query(Event).filter(Event.userid == userid, Event.noun == "bill").count()

    if counts == 1:
        logging.info(f"first bill pay for user {userid}")
        return True 
    else:
        return False 


def alert_user(db: Session, userid: int):
    now = datetime.now()
    five_mins_ago = now - timedelta(minutes=5)

    #nums_over_20000 = db.query(Event).filter(Event.userid == userid, Event.properties.value >= 20000, Event.ts > five_mins_ago).count()
    total = db.query(func.sum(Event.properties.value)).filter(Event.userid == userid, datetime.strptime(Event.ts, '%Y%m%d %H%M%S')  > five_mins_ago).order_by(datetime.strptime(Event.ts, '%Y%m%d %H%M%S') ).limit(5).all()
    if total > 20000:
        logging.info(f"notifying user {userid}")

def check_feedback(db: Session, userid: int):
      
    bill_pay_time = datetime.now() - timedelta(minutes=15)

    if db.query(Event).filter(Event.userid == userid, Event.noun == "fdfk").count() > 0:
        ts_fdbk = db.query(Event).filter(Event.userid == userid, Event.noun == "fdfk").first().ts
        fdbk_time = datetime.strptime(ts_fdbk, '%Y%m%d %H%M%S') 
        if fdbk_time < bill_pay_time:
            logging.info("notifying Tubber engineer")

      
