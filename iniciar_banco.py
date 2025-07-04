from app import criar_app
from app.extensoes import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

app = criar_app()

with app.app_context():  # ✅ Contexto do app necessário
    print("⏳ Criando banco de dados...")
    db.drop_all()
    db.create_all()

    admin = Usuario(
        usuario='admin',
        senha=generate_password_hash('admin123'),
        nome='Administrador Geral',
        tipo='admin'
    )

    almoxarife = Usuario(
        usuario='joao',
        senha=generate_password_hash('123456'),
        nome='João Almoxarifado',
        tipo='almoxarifado'
    )

    db.session.add_all([admin, almoxarife])
    db.session.commit()

    print("✅ Banco de dados criado com sucesso!")
    print("✅ Usuários padrão criados: admin e almoxarife")