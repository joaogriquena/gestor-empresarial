from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.auth import verificar_permissao
from app.extensoes import db
from app.models.almoxarifado.ferramenta import Ferramenta
from app.models.almoxarifado.movimentacao import Movimentacao
from sqlalchemy import func

estoque_bp = Blueprint('estoque', __name__, url_prefix='/almoxarifado')

@estoque_bp.route('/estoque')
@login_required
@verificar_permissao('almoxarifado')
def estoque():
    ferramentas = Ferramenta.query.all()

    dados_estoque = []
    for f in ferramentas:
        saidas = (
            db.session.query(func.sum(Movimentacao.quantidade))
            .filter_by(ferramenta_id=f.id, tipo='saida')
            .scalar()
        ) or 0

        devolucoes = (
            db.session.query(func.sum(Movimentacao.quantidade))
            .filter_by(ferramenta_id=f.id, tipo='devolucao')
            .scalar()
        ) or 0

        retiradas = saidas - devolucoes
        atual = f.quantidade_total - retiradas

        dados_estoque.append({
            'nome': f.nome,
            'descricao': f.descricao or '-',
            'total': f.quantidade_total,
            'retiradas': retiradas,
            'disponivel': atual
        })

    return render_template('almoxarifado/estoque.html', dados=dados_estoque)
