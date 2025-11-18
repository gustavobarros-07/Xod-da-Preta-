"""
Testes para models
"""
import pytest
from models import Produto, Admin, Configuracao

def test_produto_creation(app):
    """Testa criação de produto"""
    with app.app_context():
        produto = Produto(
            nome='Teste',
            preco=50.0,
            categoria='Brincos',
            ativo=True
        )
        assert produto.nome == 'Teste'
        assert produto.preco == 50.0
        assert produto.ativo is True

def test_produto_to_dict(app):
    """Testa conversão de produto para dict"""
    with app.app_context():
        produto = Produto.query.first()
        produto_dict = produto.to_dict()
        assert 'id' in produto_dict
        assert 'nome' in produto_dict
        assert 'preco' in produto_dict

def test_admin_password_hashing(app):
    """Testa hash de senha do admin"""
    with app.app_context():
        admin = Admin(username='test', email='test@test.com')
        admin.set_password('senha123')

        assert admin.password_hash is not None
        assert admin.password_hash != 'senha123'
        assert admin.check_password('senha123') is True
        assert admin.check_password('errado') is False

def test_configuracao_get_valor(app):
    """Testa obter valor de configuração"""
    with app.app_context():
        valor = Configuracao.get_valor('loja_nome', 'Default')
        assert valor == 'Xodó da Preta Test'

def test_configuracao_get_valor_default(app):
    """Testa obter valor padrão quando não existe"""
    with app.app_context():
        valor = Configuracao.get_valor('chave_inexistente', 'Padrão')
        assert valor == 'Padrão'

def test_produto_imagens_adicionais(app):
    """Testa manipulação de imagens adicionais"""
    with app.app_context():
        produto = Produto.query.first()
        imagens = ['img1.jpg', 'img2.jpg']
        produto.set_imagens_adicionais(imagens)

        assert produto.get_imagens_adicionais() == imagens
