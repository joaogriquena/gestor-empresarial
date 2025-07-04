from app.extensoes import db
from datetime import datetime

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'

    id = db.Column(db.Integer, primary_key=True)
    ferramenta_id = db.Column(db.Integer, db.ForeignKey('ferramentas.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # saída ou devolucao
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos (opcional para exibir nomes)
    ferramenta = db.relationship('Ferramenta', backref='movimentacoes')
    funcionario = db.relationship('Funcionario', backref='movimentacoes')
