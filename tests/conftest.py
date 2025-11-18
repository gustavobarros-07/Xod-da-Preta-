"""
Configuração de fixtures para pytest
"""
import pytest
import sys
from pathlib import Path

# Adicionar diretório app ao path
app_dir = Path(__file__).parent.parent / 'app'
sys.path.insert(0, str(app_dir))

from main import app as flask_app
from database import db
from models import Admin, Produto, Configuracao, Subcategoria

@pytest.fixture
def app():
    """Cria aplicação Flask para testes"""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,  # Desabilitar CSRF nos testes
        'SECRET_KEY': 'test-secret-key'
    })

    with flask_app.app_context():
        db.create_all()

        # Criar admin de teste
        admin = Admin(username='admin', email='admin@test.com')
        admin.set_password('admin123')
        db.session.add(admin)

        # Criar configurações básicas
        configs = [
            Configuracao(chave='loja_nome', valor='Xodó da Preta Test'),
            Configuracao(chave='loja_telefone', valor='11 99999-9999'),
            Configuracao(chave='topbar_ativo', valor='1')
        ]
        db.session.add_all(configs)

        # Criar produtos de teste
        produto1 = Produto(
            nome='Colar Teste',
            descricao='Produto de teste',
            preco=99.90,
            categoria='Colares',
            ativo=True,
            destaque=True,
            ordem=1
        )
        produto2 = Produto(
            nome='Brinco Teste',
            descricao='Produto de teste 2',
            preco=49.90,
            categoria='Brincos',
            ativo=True,
            destaque=False,
            ordem=2
        )
        db.session.add_all([produto1, produto2])
        db.session.commit()

        yield flask_app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de teste Flask"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner para testes"""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """Cliente autenticado como admin"""
    with client.session_transaction() as session:
        session['admin_logged_in'] = True
        session['admin_id'] = 1
        session['admin_username'] = 'admin'
    return client
