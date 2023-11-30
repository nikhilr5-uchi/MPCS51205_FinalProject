from flask import Flask
from flask_mongoengine import MongoEngine
from flask.json import jsonify
from flask_login import LoginManager
from bson import ObjectId


db = MongoEngine()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    app.config['MONGODB_SETTINGS'] = {
        'db': 'users',
        'host': 'mongodb://appUser:appPassword@localhost:27017/users',
    }

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        print(User.objects(id=ObjectId(user_id)).first())
        return User.objects(id=ObjectId(user_id)).first()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app