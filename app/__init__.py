from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from jinja2 import ChoiceLoader, FileSystemLoader
import os

db = SQLAlchemy()
login_manager = LoginManager()

def criar_app():
    app = Flask(__name__)
    app.secret_key = 'sua_chave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema.db'

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.login_routes import login_bp
    app.register_blueprint(login_bp)

    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(os.path.join(app.root_path, 'templates'))
    ])

    from app.models.usuario import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app
