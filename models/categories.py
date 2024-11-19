from config import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Enum('entradas', 'platos principales', 'postres', 'bebidas'), nullable=False)

    # Relación con Dish
  

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
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
