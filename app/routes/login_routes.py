from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models.usuario import Usuario
from app.extensoes import db
from app.utils.auth import verificar_permissao

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def home():
    return redirect(url_for('login.login'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_input = request.form['usuario']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(usuario=usuario_input).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            session['tipo'] = usuario.tipo
            return redirect(url_for('login.selecao_area'))
        else:
            flash('Usuário ou senha inválidos')
    
    return render_template('login.html')

@login_bp.route('/selecionar-area')
def selecao_area():
    return render_template('selecao_area.html')
