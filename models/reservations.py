from config import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = "Reservations"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("Users.id"), nullable=False)
    order_id = db.Column(db.Integer(), db.ForeignKey("orders.id"), nullable=False)
    table_id = db.Column(db.Integer(), db.ForeignKey("tables.id"), nullable=False)
    reservation_date = db.Column(db.DateTime(), nullable=False)
    num_people = db.Column(db.Integer(), nullable=False)
    special_requests = db.Column(db.Text(), nullable=True)  
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    terms_and_conditions_accepted = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self,user_id,order_id,table_id,reservation_date,num_people,special_requests,created_at,terms_and_conditions_accepted):
        self.user_id = user_id
        self.order_id = order_id
        self.table_id = table_id
        self.reservation_date = reservation_date
        self.num_people = num_people
        self.special_requests = special_requests
        self.created_at = created_at
        self.terms_and_conditions_accepted = terms_and_conditions_accepted

    def serialize(self):
        return {
            'reservation_id': self.reservation_id,
            'user_id': self.user_id,
            'order_id':self.order_id,
            'table_id':self.table_id,
            'reservation_date': self.reservation_date.strftime("%Y-%m-%d %H:%M:%S"),
            'num_people': self.num_people,
            'special_requests': self.special_requests,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'reservation_confirmation': self.reservation_confirmation,
            'terms_and_conditions_accepted': self.terms_and_conditions_accepted,
        }
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
            

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
