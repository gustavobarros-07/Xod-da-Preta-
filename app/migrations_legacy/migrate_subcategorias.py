"""
Script de migração para popular as subcategorias iniciais
Execute este script após atualizar o banco de dados
"""
import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import Subcategoria


def criar_subcategorias_iniciais():
    """Cria as subcategorias iniciais baseadas no pedido da cliente"""

    # Subcategorias para Roupas
    subcategorias_roupas = [
        # Feminino
        {'nome': 'Vestido', 'categoria': 'Roupas', 'ordem': 1},
        {'nome': 'Saia', 'categoria': 'Roupas', 'ordem': 2},
        {'nome': 'Macacão', 'categoria': 'Roupas', 'ordem': 3},
        {'nome': 'Jaqueta Feminina', 'categoria': 'Roupas', 'ordem': 4},
        # Masculino
        {'nome': 'Camisa', 'categoria': 'Roupas', 'ordem': 5},
        {'nome': 'Bata', 'categoria': 'Roupas', 'ordem': 6},
        {'nome': 'Conjunto', 'categoria': 'Roupas', 'ordem': 7},
        {'nome': 'Jaqueta Masculina', 'categoria': 'Roupas', 'ordem': 8},
    ]

    print("🔄 Iniciando criação de subcategorias...")

    for subcat_data in subcategorias_roupas:
        # Verificar se a subcategoria já existe
        existe = Subcategoria.query.filter_by(
            nome=subcat_data['nome'],
            categoria=subcat_data['categoria']
        ).first()

        if not existe:
            subcategoria = Subcategoria(
                nome=subcat_data['nome'],
                categoria=subcat_data['categoria'],
                ordem=subcat_data['ordem'],
                ativo=True
            )
            db.session.add(subcategoria)
            print(f"✅ Criada: {subcat_data['categoria']} > {subcat_data['nome']}")
        else:
            print(f"⏭️  Já existe: {subcat_data['categoria']} > {subcat_data['nome']}")

    db.session.commit()
    print("\n✨ Migração de subcategorias concluída com sucesso!")
    print("\n📋 Resumo das subcategorias criadas:")
    print("\n🎀 FEMININO:")
    print("  - Vestido")
    print("  - Saia")
    print("  - Macacão")
    print("  - Jaqueta Feminina")
    print("\n👔 MASCULINO:")
    print("  - Camisa")
    print("  - Bata")
    print("  - Conjunto")
    print("  - Jaqueta Masculina")


if __name__ == '__main__':
    # Importar a aplicação Flask para ter acesso ao contexto
    from main import app

    with app.app_context():
        criar_subcategorias_iniciais()
