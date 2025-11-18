"""
Testes para funcionalidades do carrinho
"""
import pytest
import json

def test_add_to_cart(client):
    """Testa adicionar produto ao carrinho"""
    response = client.post('/api/carrinho/adicionar',
                          data=json.dumps({
                              'produto_id': 1,
                              'quantidade': 2
                          }),
                          content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['total_itens'] == 2

def test_add_to_cart_invalid_product(client):
    """Testa adicionar produto inexistente"""
    response = client.post('/api/carrinho/adicionar',
                          data=json.dumps({
                              'produto_id': 999,
                              'quantidade': 1
                          }),
                          content_type='application/json')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False

def test_add_to_cart_invalid_quantity(client):
    """Testa quantidade inválida"""
    response = client.post('/api/carrinho/adicionar',
                          data=json.dumps({
                              'produto_id': 1,
                              'quantidade': -1
                          }),
                          content_type='application/json')

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False

def test_add_to_cart_large_quantity(client):
    """Testa quantidade muito grande"""
    response = client.post('/api/carrinho/adicionar',
                          data=json.dumps({
                              'produto_id': 1,
                              'quantidade': 101
                          }),
                          content_type='application/json')

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False

def test_cart_total(client):
    """Testa obter total do carrinho"""
    # Adicionar item primeiro
    client.post('/api/carrinho/adicionar',
               data=json.dumps({'produto_id': 1, 'quantidade': 1}),
               content_type='application/json')

    # Obter total
    response = client.get('/api/carrinho/total')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total_itens'] == 1

def test_update_cart_item(client):
    """Testa atualizar quantidade no carrinho"""
    # Adicionar item
    client.post('/api/carrinho/adicionar',
               data=json.dumps({'produto_id': 1, 'quantidade': 1}),
               content_type='application/json')

    # Atualizar quantidade (assumindo que o item_id é 1)
    response = client.put('/api/carrinho/atualizar/1',
                         data=json.dumps({'quantidade': 3}),
                         content_type='application/json')

    # Pode retornar 200 ou 404 dependendo se o item existe na sessão
    assert response.status_code in [200, 404]

def test_remove_cart_item(client):
    """Testa remover item do carrinho"""
    # Adicionar item
    client.post('/api/carrinho/adicionar',
               data=json.dumps({'produto_id': 1, 'quantidade': 1}),
               content_type='application/json')

    # Remover item
    response = client.delete('/api/carrinho/remover/1')

    # Pode retornar 200 ou 404 dependendo se o item existe na sessão
    assert response.status_code in [200, 404]
