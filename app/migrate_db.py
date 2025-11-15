"""
Script para migrar o banco de dados
Adiciona campos 'destaque' e 'visualizacoes' a tabela Produto
Cria tabelas ProdutoVisualizacao e ConteudoPagina
"""

from main import app, db
from models import Produto, ProdutoVisualizacao, ConteudoPagina
from sqlalchemy import inspect

def migrate_database():
    """Executa migracao do banco de dados"""

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

        print("\n[SUCESSO] Migracao concluida!")

if __name__ == '__main__':
    migrate_database()
