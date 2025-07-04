from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensoes import db
from app.models.almoxarifado.ferramentas import Ferramenta
from app.utils.auth import verificar_permissao

# Define o Blueprint com prefixo para a área do almoxarifado
ferramentas_bp = Blueprint('ferramentas', __name__, url_prefix='/almoxarifado')

# Rota para visualizar e cadastrar ferramentas
@ferramentas_bp.route('/ferramentas', methods=['GET', 'POST'])
@login_required
@verificar_permissao('almoxarifado')
def ferramentas():
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        quantidade = request.form.get('quantidade')

        # Validação simples
        if nome and quantidade:
            try:
                nova = Ferramenta(
                    nome=nome,
                    descricao=descricao,
                    quantidade_total=int(quantidade)
                )
                db.session.add(nova)
                db.session.commit()
                flash('✅ Ferramenta cadastrada com sucesso!', 'sucesso')
                return redirect(url_for('ferramentas.ferramentas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar: {str(e)}', 'erro')
        else:
            flash('⚠️ Preencha todos os campos obrigatórios.', 'erro')

    # Filtro de busca por nome
    filtro = request.args.get('filtro')
    if filtro:
        ferramentas = Ferramenta.query.filter(Ferramenta.nome.ilike(f'%{filtro}%')).all()
    else:
        ferramentas = Ferramenta.query.all()

    return render_template(
        'almoxarifado/ferramentas.html',
        ferramentas=ferramentas,
        filtro=filtro
    )
