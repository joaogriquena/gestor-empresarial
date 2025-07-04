from flask import Flask
from app.extensoes import db, login_manager
from jinja2 import ChoiceLoader, FileSystemLoader
import os

def criar_app():
    app = Flask(__name__)
    app.secret_key = 'sua_chave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'

    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(os.path.join(app.root_path, 'templates'))
    ])

    from app.routes.login_routes import login_bp
    from app.routes.almoxarifado.dashboard_routes import dashboard_almoxarifado
    from app.routes.almoxarifado.ferramentas_routes import ferramentas_bp
    from app.routes.almoxarifado.funcionarios_routes import funcionarios_bp
    
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_almoxarifado)
    app.register_blueprint(ferramentas_bp)
    app.register_blueprint(funcionarios_bp)
    

    from app.models.usuario import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app
