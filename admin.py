from models import Event
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging


logging.basicConfig(filename='tubber.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def check_first_bill(db: Session, userid: int):
    counts = db.query(Event).filter(Event.userid == userid, Event.noun == "bill").count()

    if counts > 0:
        logging.info(f"first bill pay for user {userid}")


def alert_user(db: Session, userid: int):
    now = datetime.now()
    five_mins_ago = now - timedelta(minutes=5)

    nums_over_20000 = db.query(Event).filter(Event.userid == userid, Event.properties.value >= 20000, Event.ts > five_mins_ago).count()

    if nums_over_20000 > 5:
        logging.info(f"notifying user {userid}")

def check_feedback(db: Session, userid: int):
    

    if db.query(Event).filter(Event.userid == userid, Event.noun == "bill").count() > 0:
        bill_pay_event = db.query(Event).filter(Event.userid == userid, Event.noun == "bill").first().ts 
        fifteen_mins_later = datetime.strptime(bill_pay_event, '%Y%m%d %H%M%S') + timedelta(minutes=15)
        
        if db.query(Event).filter(Event.userid == userid, Event.noun == "fdfk").count() > 0:
            ts_fdbk = db.query(Event).filter(Event.userid == userid, Event.noun == "fdfk").first().ts
            if ts_fdbk > fifteen_mins_later:
                logging.info("notifying Tubber engineer")
    
      
