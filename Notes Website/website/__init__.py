from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from .constants import *;

db = SQLAlchemy()

def _read_from_env(key):
    return os.environ.get(key)

def create_tables(app):
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = _read_from_env(SECRET_KEY)
    
    DB_URL = _read_from_env(MYSQL_DB_URL)
    DBNAME = _read_from_env(DB_NAME)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_URL}/{DBNAME}'
    db.init_app(app)
    
    from .views import views;
    from .auth import auth;
    
    from .models import User, Note
    create_tables(app)
    
    
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app