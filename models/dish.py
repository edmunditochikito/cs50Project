from config import db
# Importa la clase Category correctamente

class Dish(db.Model):
    __tablename__ = "dishes"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)
    categories_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    # Relación con Category
    

    def __init__(self, name, price, description, categories_id, image=None):
        self.name = name
        self.price = price
        self.description = description
        self.categories_id = categories_id
        self.image = image

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),  # Convertir a float si es Decimal
            "description": self.description,
            "image": self.image,
            "categories_id":self.categories_id
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
