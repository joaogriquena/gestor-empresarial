from app import criar_app
from app.extensoes import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

# Criar app e contexto
app = criar_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Usuário admin
    admin = Usuario(
        usuario='admin',
        senha=generate_password_hash('admin123'),
        nome='Administrador Geral',
        tipo='admin'
    )

    # Usuário almoxarife
    almoxarife = Usuario(
        usuario='joao',
        senha=generate_password_hash('123456'),
        nome='João Almoxarife',
        tipo='almoxarife'
    )

    db.session.add(admin)
    db.session.add(almoxarife)
    db.session.commit()

    print("✅ Banco de dados criado com sucesso e usuários inseridos.")
