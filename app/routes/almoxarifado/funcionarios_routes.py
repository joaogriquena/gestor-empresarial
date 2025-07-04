from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensoes import db
from app.models.almoxarifado.funcionario import Funcionario
from app.utils.auth import verificar_permissao

funcionarios_bp = Blueprint('funcionarios', __name__, url_prefix='/almoxarifado')

@funcionarios_bp.route('/funcionarios', methods=['GET', 'POST'])
@login_required
@verificar_permissao('almoxarifado')
def funcionarios():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cargo = request.form.get('cargo')
        matricula = request.form.get('matricula')

        if nome and matricula:
            try:
                novo = Funcionario(
                    nome=nome.strip(),
                    cargo=cargo.strip() if cargo else None,
                    matricula=matricula.strip()
                )
                db.session.add(novo)
                db.session.commit()
                flash('✅ Funcionário cadastrado com sucesso!', 'sucesso')
                return redirect(url_for('funcionarios.funcionarios'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar funcionário: {str(e)}', 'erro')
        else:
            flash('⚠️ Nome e matrícula são obrigatórios.', 'erro')

    filtro = request.args.get('filtro')
    if filtro:
        funcionarios = Funcionario.query.filter(Funcionario.nome.ilike(f'%{filtro}%')).all()
    else:
        funcionarios = Funcionario.query.all()

    return render_template('almoxarifado/funcionarios.html', funcionarios=funcionarios, filtro=filtro)
