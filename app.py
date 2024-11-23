from flask import Flask,redirect
from config import Config
from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity
from config import jwt,db
from routes.index import index
from routes.users import user
from routes.dish import admin
from routes.admin import admin_bp
from routes.profile import profile_bp
from routes.categories import category
from routes.reservations import reservations_bp


app = Flask(__name__)
app.config.from_object(Config)
Config.ensure_upload_folder_exists()


db.init_app(app)
jwt.init_app(app)

@jwt.invalid_token_loader
def invalid_token_loader(error):
    return redirect("/")

@jwt.unauthorized_loader
def unauthorized_loader(error):
    return redirect("/")

@jwt.expired_token_loader
def expired_token_loader(jwt_header,jwt_data):
    return redirect("/")



app.register_blueprint(index)
app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(profile_bp)
app.register_blueprint(reservations_bp, url_prefix='/reservations')
app.register_blueprint(category)
app.register_blueprint(admin_bp)


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


