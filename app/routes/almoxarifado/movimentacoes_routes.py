from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensoes import db
from app.models.almoxarifado.funcionario import Funcionario
from app.models.almoxarifado.ferramenta import Ferramenta
from app.models.almoxarifado.movimentacao import Movimentacao
from app.utils.auth import verificar_permissao
from datetime import datetime

movimentacoes_bp = Blueprint('movimentacoes', __name__, url_prefix='/almoxarifado')

@movimentacoes_bp.route('/movimentacoes', methods=['GET', 'POST'])
@login_required
@verificar_permissao('almoxarifado')
def movimentacoes():
    if request.method == 'POST':
        funcionario_id = request.form.get('funcionario_id')
        ferramenta_id = request.form.get('ferramenta_id')
        quantidade = request.form.get('quantidade')

        if funcionario_id and ferramenta_id and quantidade:
            try:
                nova = Movimentacao(
                    funcionario_id=int(funcionario_id),
                    ferramenta_id=int(ferramenta_id),
                    quantidade=int(quantidade),
                    tipo='saida',
                    data_hora=datetime.now()
                )
                db.session.add(nova)
                db.session.commit()
                flash('✅ Movimentação registrada com sucesso!', 'sucesso')
                return redirect(url_for('movimentacoes.movimentacoes'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentação: {str(e)}', 'erro')
        else:
            flash('⚠️ Todos os campos são obrigatórios.', 'erro')

    filtro = request.args.get('filtro')
    query = db.session.query(Movimentacao).join(Funcionario).join(Ferramenta)

    if filtro:
        query = query.filter(
            db.or_(
                Funcionario.nome.ilike(f'%{filtro}%'),
                Ferramenta.nome.ilike(f'%{filtro}%')
            )
        )

    movimentacoes = query.order_by(Movimentacao.data_hora.desc()).all()
    funcionarios = Funcionario.query.order_by(Funcionario.nome).all()
    ferramentas = Ferramenta.query.order_by(Ferramenta.nome).all()

    return render_template(
        'almoxarifado/movimentacoes.html',
        movimentacoes=movimentacoes,
        funcionarios=funcionarios,
        ferramentas=ferramentas,
        filtro=filtro
    )
