from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(Config):
    from .auth import auth
    from .file_manager import file_manager

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(auth)
    app.register_blueprint(file_manager)

    @login_manager.user_loader
    def load_user(user_id):
        from FileManager.models import User
        return User.query.get(int(user_id))
        
    return app