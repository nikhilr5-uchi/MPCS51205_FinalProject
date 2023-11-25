from flask import Flask
# from flask_mongoengine import MongoEngine

# db = MongoEngine()

def create_app():
    app = Flask(__name__)

    # app.config['SECRET_KEY'] = 'secret-key-goes-here'
    
    # app.config['MONGODB_SETTINGS'] = {
    #     'db': 'users',
    #     'host': 'mongodb://username:password@localhost/db_name'
    # }

    # db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
