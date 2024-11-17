from config import db

class Table (db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    code = db.Column(db.Integer(), unique=True, nullable=False)
    capacity = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Enum("interior","exterior",name='type_enum'),nullable=False)
    availabillity = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, code, capacity, type,availabillity):
        self.code = code
        self.capacity = capacity
        self.type = type
        self.availabillity = availabillity
    
    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'capacity': self.capacity,
            'type':self.type,
            'availabillity': self.availabillity
        }
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    def deactivate(self):
        try:
            self.availabillity=False
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e