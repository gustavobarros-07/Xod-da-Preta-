"""
Script para criar usuário administrador
Executar: python create_admin.py
"""
from main import app
from database import db
from models import Admin

def create_admin_user():
    """Cria o usuário administrador no banco de dados existente"""
    with app.app_context():
        # Verificar se já existe admin
        existing_admin = Admin.query.filter_by(username='admin').first()

        if existing_admin:
            print("[ERRO] Usuario 'admin' ja existe no banco de dados!")
            print(f"   Email: {existing_admin.email}")
            print("\n[AVISO] Se esqueceu a senha, voce pode redefinir manualmente no banco.")
            return

        # Criar novo admin
        print("Criando usuario administrador...")
        admin = Admin(
            username='admin',
            email='admin@xododapreta.com'
        )
        admin.set_password('admin123')

        db.session.add(admin)
        db.session.commit()

        print("\n[OK] Usuario administrador criado com sucesso!")
        print("\n" + "="*50)
        print("CREDENCIAIS DE ACESSO")
        print("="*50)
        print(f"URL: http://localhost:5000/admin/login")
        print(f"Usuario: admin")
        print(f"Senha: admin123")
        print("="*50)
        print("\n[IMPORTANTE] Altere a senha apos o primeiro login!")
        print("   (Menu: Admin -> Configuracoes -> Alterar Senha)\n")

if __name__ == '__main__':
    create_admin_user()
