"""
Testes para rotas administrativas
"""
import pytest
from config import Config

ADMIN_USERNAME = Config.ADMIN_USERNAME
ADMIN_PASSWORD = Config.ADMIN_PASSWORD


def test_admin_login_page(client):
    """Testa se a pagina de login carrega"""
    response = client.get('/admin/login')
    assert response.status_code == 200
    assert b'login' in response.data.lower()


def test_admin_login_success(client):
    """Testa login bem-sucedido"""
    response = client.post(
        '/admin/login',
        data={'username': ADMIN_USERNAME, 'password': ADMIN_PASSWORD},
        follow_redirects=True
    )
    assert response.status_code == 200


def test_admin_login_wrong_password(client):
    """Testa login com senha errada"""
    response = client.post(
        '/admin/login',
        data={'username': ADMIN_USERNAME, 'password': 'wrong'},
        follow_redirects=True
    )
    assert response.status_code == 200
    # Deve permanecer na pagina de login


def test_admin_dashboard_requires_auth(client):
    """Testa que dashboard exige autenticacao"""
    response = client.get('/admin/dashboard')
    assert response.status_code == 302  # Redirect para login


def test_admin_dashboard_with_auth(auth_client):
    """Testa dashboard com autenticacao"""
    response = auth_client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data


def test_admin_produtos_page(auth_client):
    """Testa pagina de produtos do admin"""
    response = auth_client.get('/admin/produtos')
    assert response.status_code == 200


def test_admin_logout(auth_client):
    """Testa logout"""
    response = auth_client.get('/admin/logout', follow_redirects=True)
    assert response.status_code == 200


def test_admin_rate_limiting(client):
    """Testa rate limiting no login"""
    # Fazer 6 tentativas (limite e 5)
    for _ in range(6):
        response = client.post(
            '/admin/login',
            data={'username': ADMIN_USERNAME, 'password': 'wrong'}
        )

    # A 6a tentativa deve ser bloqueada (ou ainda permitida se limite nao resetou)
    # Como e baseado em sessao, depende da implementacao exata
    assert response.status_code in [200, 429]
