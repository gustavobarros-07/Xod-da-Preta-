"""
Script para garantir que a configuração topbar_ativo existe no banco
Execute: python -m app.fix_topbar
"""
from main import app
from models import Configuracao

with app.app_context():
    print("\n=== VERIFICANDO CONFIGURAÇÃO TOPBAR ===\n")

    # Verificar se topbar_ativo existe
    topbar_config = Configuracao.query.filter_by(chave='topbar_ativo').first()

    if topbar_config:
        print(f"✓ topbar_ativo existe no banco: valor = '{topbar_config.valor}'")
    else:
        print("✗ topbar_ativo NÃO existe no banco")
        print("  Criando com valor padrão '1' (ativo)...")
        Configuracao.set_valor('topbar_ativo', '1', 'Controla se o top bar aparece no site')
        print("✓ Criado com sucesso!")

    print("\n=== VERIFICANDO TODAS AS CONFIGURAÇÕES ===\n")
    all_configs = Configuracao.query.all()
    for c in all_configs:
        print(f"  {c.chave:25} = '{c.valor}'")

    print("\n=== TESTE DO CONTEXT PROCESSOR ===\n")
    valor = Configuracao.get_valor('topbar_ativo', '1')
    resultado = valor == '1'
    print(f"  Configuracao.get_valor('topbar_ativo', '1') = '{valor}'")
    print(f"  '{valor}' == '1' ? {resultado}")
    print(f"  config_topbar_ativo (bool) = {resultado}")

    if resultado:
        print("\n✓ Top Bar deveria APARECER no site")
    else:
        print("\n✗ Top Bar NÃO vai aparecer no site")
        print("  SOLUÇÃO: Vá em /admin/config e marque o checkbox 'Exibir Top Bar'")
