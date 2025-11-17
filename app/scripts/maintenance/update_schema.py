"""
Script de Atualização de Schema do Banco de Dados
===================================================
Adiciona novos campos e tabelas ao banco de dados existente (NON-DESTRUCTIVE)

Execute este script quando precisar adicionar novos recursos ao banco:
    python scripts/maintenance/update_schema.py

⚠️ IMPORTANTE: Este script NÃO apaga dados! Ele apenas adiciona novos campos/tabelas.

O que este script faz:
- Adiciona campos 'destaque', 'visualizacoes', 'imagens_adicionais' à tabela produtos
- Adiciona campo 'parent_id' à tabela subcategorias (para hierarquia)
- Cria tabela 'produto_visualizacoes' (analytics)
- Cria tabela 'conteudo_pagina' (CMS)
- Cria tabela 'cupons' (sistema de cupons de desconto)
"""

import sys
import os

# Adicionar diretório pai ao path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app, db
from models import Produto, ProdutoVisualizacao, ConteudoPagina, Cupom
from sqlalchemy import inspect

def update_schema():
    """Atualiza o schema do banco de dados adicionando novos campos e tabelas"""

    with app.app_context():
        inspector = inspect(db.engine)

        # Verificar se a tabela produtos existe
        if 'produtos' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('produtos')]

            # Adicionar campo 'destaque' se nao existir
            if 'destaque' not in columns:
                print("Adicionando campo 'destaque' a tabela produtos...")
                db.session.execute(db.text('ALTER TABLE produtos ADD COLUMN destaque BOOLEAN DEFAULT 0'))
                db.session.commit()
                print("[OK] Campo 'destaque' adicionado")
            else:
                print("[OK] Campo 'destaque' ja existe")

            # Adicionar campo 'visualizacoes' se nao existir
            if 'visualizacoes' not in columns:
                print("Adicionando campo 'visualizacoes' a tabela produtos...")
                db.session.execute(db.text('ALTER TABLE produtos ADD COLUMN visualizacoes INTEGER DEFAULT 0'))
                db.session.commit()
                print("[OK] Campo 'visualizacoes' adicionado")
            else:
                print("[OK] Campo 'visualizacoes' ja existe")

            # Adicionar campo 'imagens_adicionais' se nao existir
            if 'imagens_adicionais' not in columns:
                print("Adicionando campo 'imagens_adicionais' a tabela produtos...")
                db.session.execute(db.text('ALTER TABLE produtos ADD COLUMN imagens_adicionais TEXT'))
                db.session.commit()
                print("[OK] Campo 'imagens_adicionais' adicionado (galeria de imagens)")
            else:
                print("[OK] Campo 'imagens_adicionais' ja existe")

        # Criar tabela produto_visualizacoes se nao existir
        if 'produto_visualizacoes' not in inspector.get_table_names():
            print("Criando tabela 'produto_visualizacoes'...")
            db.create_all()
            print("[OK] Tabela 'produto_visualizacoes' criada")
        else:
            print("[OK] Tabela 'produto_visualizacoes' ja existe")

        # Criar tabela conteudo_pagina se nao existir
        if 'conteudo_pagina' not in inspector.get_table_names():
            print("Criando tabela 'conteudo_pagina'...")
            db.create_all()
            print("[OK] Tabela 'conteudo_pagina' criada (CMS)")
        else:
            print("[OK] Tabela 'conteudo_pagina' ja existe")

        # Criar tabela cupons se nao existir
        if 'cupons' not in inspector.get_table_names():
            print("Criando tabela 'cupons'...")
            db.create_all()
            print("[OK] Tabela 'cupons' criada (Sistema de Cupons)")
        else:
            print("[OK] Tabela 'cupons' ja existe")

        # Adicionar campo 'parent_id' na tabela subcategorias
        if 'subcategorias' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('subcategorias')]

            if 'parent_id' not in columns:
                print("Adicionando campo 'parent_id' a tabela subcategorias...")
                db.session.execute(db.text('ALTER TABLE subcategorias ADD COLUMN parent_id INTEGER REFERENCES subcategorias(id)'))
                db.session.commit()
                print("[OK] Campo 'parent_id' adicionado (hierarquia de subcategorias)")
            else:
                print("[OK] Campo 'parent_id' ja existe")

        print("\n[SUCESSO] Schema atualizado com sucesso!")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🔧 ATUALIZAÇÃO DE SCHEMA - XODÓ DA PRETA")
    print("="*70)
    print("\n📋 Este script irá:")
    print("   - Adicionar novos campos às tabelas existentes")
    print("   - Criar novas tabelas se não existirem")
    print("   - PRESERVAR todos os dados existentes (não-destrutivo)")
    print("\n✅ É seguro executar este script múltiplas vezes.\n")

    update_schema()
