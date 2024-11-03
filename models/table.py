from config import db

class Table (db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, number, capacity, availability):
        self.number = number
        self.capacity = capacity
        self.availability = availability
    
    def serialize(self):
        return {
            'id': self.id,
            'number': self.number,
            'capacity': self.capacity,
            'availability': self.availability
        }
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
