from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensoes import db
from app.models.almoxarifado.ferramenta import Ferramenta
from app.models.almoxarifado.funcionario import Funcionario
from app.models.almoxarifado.movimentacao import Movimentacao
from app.utils.auth import verificar_permissao

movimentacoes_bp = Blueprint('movimentacoes', __name__, url_prefix='/almoxarifado')

@movimentacoes_bp.route('/movimentacoes', methods=['GET', 'POST'])
@login_required
@verificar_permissao('almoxarifado')
def movimentacoes():
    if request.method == 'POST':
        ferramenta_id = request.form.get('ferramenta_id')
        matricula = request.form.get('matricula')
        quantidade = request.form.get('quantidade')

        funcionario = Funcionario.query.filter_by(matricula=matricula).first()

        if not funcionario:
            flash('Matrícula inválida!', 'erro')
        elif not ferramenta_id or not quantidade:
            flash('Campos obrigatórios faltando.', 'erro')
        else:
            nova = Movimentacao(
                ferramenta_id=ferramenta_id,
                funcionario_id=funcionario.id,
                tipo='saida',
                quantidade=int(quantidade)
            )
            db.session.add(nova)
            db.session.commit()
            flash('✅ Saída registrada com sucesso!', 'sucesso')
            return redirect(url_for('movimentacoes.movimentacoes'))

    ferramentas = Ferramenta.query.all()
    filtro_tipo = request.args.get('filtro_tipo')
    movimentacoes = Movimentacao.query

    if filtro_tipo:
        movimentacoes = movimentacoes.filter_by(tipo=filtro_tipo)

    movimentacoes = movimentacoes.order_by(Movimentacao.data.desc()).all()

    return render_template(
        'almoxarifado/movimentacoes.html',
        movimentacoes=movimentacoes,
        ferramentas=ferramentas,
        filtro_tipo=filtro_tipo
    )
