from config import db

class orders_dish_join(db.Model):
    __tablename__ = 'orders_dish_join'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    quantity = db.Column(db.Integer, db.ForeignKey ('quantity'), nullable=False)

    order = db.relationship('orders', backref=db.backref('orders_dish'), cascade ='all, delete-orphan')
    dish = db.relationship('dish', backref=db.backref('orders_dish'), cascade ='all, delete-orphan')