from app.extensoes import db

class Ferramenta(db.Model):
    __tablename__ = 'ferramentas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    quantidade_total = db.Column(db.Integer, default=0)
