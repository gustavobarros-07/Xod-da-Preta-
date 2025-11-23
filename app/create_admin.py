"""
Script para criar usuario administrador
Executar: python create_admin.py
"""
from main import app
from database import db
from models import Admin
from config import Config


def create_admin_user():
    """Cria ou confirma o usuario administrador usando credenciais do .env"""
    with app.app_context():
        username = Config.ADMIN_USERNAME
        password = Config.ADMIN_PASSWORD
        email = f"{username}@xododapreta.com"

        # Verificar se ja existe admin com esse username
        existing_admin = Admin.query.filter_by(username=username).first()

        if existing_admin:
            print(f"[ERRO] Usuario '{username}' ja existe no banco de dados!")
            print(f"   Email: {existing_admin.email}")
            print("\n[AVISO] Se esqueceu a senha, voce pode redefinir manualmente no banco.")
            return

        # Criar novo admin
        print("Criando usuario administrador...")
        admin = Admin(
            username=username,
            email=email
        )
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        print("\n[OK] Usuario administrador criado com sucesso!")
        print("\n" + "="*50)
        print("CREDENCIAIS DE ACESSO")
        print("="*50)
        print(f"URL: http://localhost:5000/admin/login")
        print(f"Usuario: {username}")
        print(f"Senha: {password}")
        print("="*50)
        print("\n[IMPORTANTE] Altere a senha apos o primeiro login!")
        print("   (Menu: Admin -> Configuracoes -> Alterar Senha)\n")


if __name__ == '__main__':
    create_admin_user()
