from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./appdb.db'
    upload_folder = 'uploads'
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.secret_key = 'mysecretkey'

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    from routes import register_routes

    from models import User
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)

    register_routes(app, bcrypt, db, socketio)

    migrate = Migrate(app, db)

    return app