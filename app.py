from flask import Flask
from config import Config
from routes.index import index
from  models import db
app=Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(index)

with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True,port=3000)