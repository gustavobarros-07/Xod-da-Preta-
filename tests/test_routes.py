"""
Testes para rotas públicas
"""
import pytest

def test_home_page(client):
    """Testa se a página inicial carrega"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'da Preta' in response.data

def test_shop_page(client):
    """Testa se a página da loja carrega"""
    response = client.get('/shop')
    assert response.status_code == 200

def test_shop_with_category(client):
    """Testa filtro por categoria"""
    response = client.get('/shop?categoria=Colares')
    assert response.status_code == 200

def test_product_detail(client):
    """Testa página de detalhes do produto"""
    response = client.get('/shop/1')
    assert response.status_code == 200
    assert b'Colar Teste' in response.data

def test_product_not_found(client):
    """Testa produto inexistente"""
    response = client.get('/shop/999')
    assert response.status_code == 404

def test_search_page(client):
    """Testa busca de produtos"""
    response = client.get('/busca?q=Colar')
    assert response.status_code == 200
    assert b'Colar Teste' in response.data

def test_search_empty(client):
    """Testa busca vazia"""
    response = client.get('/busca?q=')
    assert response.status_code == 200

def test_cart_page(client):
    """Testa página do carrinho"""
    response = client.get('/carrinho')
    assert response.status_code == 200

def test_about_page(client):
    """Testa página sobre"""
    response = client.get('/about')
    assert response.status_code == 200

def test_contact_page(client):
    """Testa página de contato"""
    response = client.get('/contact')
    assert response.status_code == 200

def test_404_page(client):
    """Testa página 404"""
    response = client.get('/pagina-inexistente')
    assert response.status_code == 404
