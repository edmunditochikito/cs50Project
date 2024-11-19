from flask import Flask
from config import Config
from routes.index import index
from routes.users import user
from routes.dish import admin
from routes.profile import profile_bp
from config import jwt,db
from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity
from routes.reservations import reservations_bp


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
jwt.init_app(app)


app.register_blueprint(index)
app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(profile_bp)
app.register_blueprint(reservations_bp)


@app.context_processor
def inject_user():
    try:
        verify_jwt_in_request(optional=True)
        current_user = get_jwt_identity()
    except Exception:
        current_user = None

    return {'user_logged_in': current_user is not None, 'current_user': current_user}


if __name__ == '__main__':
    app.run(debug=True, port=3000)


