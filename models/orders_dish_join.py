from config import db

class orders_dish_join(db.Model):
    __tablename__ = 'orders_dish_join'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.id'), nullable=False)
    dish_id = db.Column(db.Integer(), db.ForeignKey('dishes.id'), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)

    order = db.relationship('orders', backref=db.backref('orders_dish_join'))
    dish = db.relationship('dishes', backref=db.backref('orders_dish_join'))

    def __init__ (self, order_id, dish_id, quantity):
        self.order_id = order_id
        self.dish_id = dish_id
        self.quantity = quantity

    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'dish_id': self.dish_id,
            'quiantity': self.quantity
        }
    
    def save(self):
        try:
            db.session.add(self)
            db.session.comit()
        except Exception as e:
            db.session.rollback()
            raise e