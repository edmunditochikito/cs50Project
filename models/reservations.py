from config import db
from datetime import datetime, timezone

class Reservation(db.Model):
    __tablename__ = 'Reservations'
    
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)  # Relación con la tabla Users
    reservation_date = db.Column(db.DateTime, nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    table_type = db.Column(db.String(8), nullable=False)  # Solo acepta "exterior" o "interior"
    reservation_confirmation = db.Column(db.Boolean, default=False, nullable=False)  # Confirmación de reserva
    terms_and_conditions_accepted = db.Column(db.Boolean, default=False, nullable=False)  # Términos y condiciones
    table_number = db.Column(db.Integer, nullable=False)  # Número de mesa
    
    # Relación con User
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))

    def __init__(self, user_id, reservation_date, num_people, table_number, special_requests=None, table_type='interior', reservation_confirmation=False, terms_and_conditions_accepted=False):
        self.user_id = user_id
        self.reservation_date = reservation_date
        self.num_people = num_people
        self.table_number = table_number
        self.special_requests = special_requests
        self.table_type = table_type
        self.reservation_confirmation = reservation_confirmation
        self.terms_and_conditions_accepted = terms_and_conditions_accepted

    def serialize(self):
        return {
            'reservation_id': self.reservation_id,
            'user_id': self.user_id,
            'reservation_date': self.reservation_date.strftime("%Y-%m-%d %H:%M:%S"),
            'num_people': self.num_people,
            'table_number': self.table_number,
            'special_requests': self.special_requests,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'table_type': self.table_type,
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
