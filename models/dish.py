from config import db

class dish(db.Model):
    __tablename__ = "dishes"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(), nullable=False)
    description = db.Column(db.Text(),nullable=False)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description
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