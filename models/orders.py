from config import db

class orders (db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    special_request = db.Column(db.Text())

    def __init__(self, special_request=None):
        self.especial.request = special_request

    def serialize (self):
        return {
            'id': self.id,
            'special_request': self.special_request
        }
    
    def save (self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e