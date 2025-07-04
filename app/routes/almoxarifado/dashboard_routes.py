from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.auth import verificar_permissao

dashboard_almoxarifado = Blueprint('dashboard_almoxarifado', __name__, url_prefix='/almoxarifado')

@dashboard_almoxarifado.route('/dashboard')
@login_required
@verificar_permissao('almoxarifado')
def index():
    return render_template('almoxarifado/dashboard.html')
