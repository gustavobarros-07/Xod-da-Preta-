"""Script para debugar configurações"""
from app.main import app
from app.models import Configuracao

with app.app_context():
    print("\n=== CONFIGURAÇÕES NO BANCO ===\n")
    configs = Configuracao.query.all()
    for c in configs:
        print(f"{c.chave:20} = {repr(c.valor):30} (type: {type(c.valor).__name__})")

    print("\n=== TESTE DE GET_VALOR ===\n")
    topbar = Configuracao.get_valor('topbar_ativo', '1')
    print(f"topbar_ativo = {repr(topbar)} (type: {type(topbar).__name__})")
    print(f"topbar == '1': {topbar == '1'}")
    print(f"topbar == '0': {topbar == '0'}")
    print(f"bool(topbar): {bool(topbar)}")

    print("\n=== TESTE DE CONTEXT PROCESSOR ===\n")
    result = topbar == '1'
    print(f"config_topbar_ativo = {result}")
