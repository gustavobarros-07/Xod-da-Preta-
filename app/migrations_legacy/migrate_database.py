"""
Script de migração do banco de dados para adicionar suporte a subcategorias
Execute este script APENAS UMA VEZ para atualizar o banco de dados existente
"""
import sqlite3
import os
from pathlib import Path

# Caminho do banco de dados
DB_PATH = Path(__file__).parent / 'loja.db'

def verificar_coluna_existe(cursor, tabela, coluna):
    """Verifica se uma coluna existe em uma tabela"""
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [row[1] for row in cursor.fetchall()]
    return coluna in colunas

def verificar_tabela_existe(cursor, tabela):
    """Verifica se uma tabela existe"""
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabela}'")
    return cursor.fetchone() is not None

def migrar_banco_dados():
    """Executa a migração do banco de dados"""

    if not DB_PATH.exists():
        print("❌ Banco de dados não encontrado!")
        print(f"   Esperado em: {DB_PATH}")
        print("\n💡 Execute primeiro: python setup_inicial.py")
        return False

    print("=" * 60)
    print("🔄 MIGRAÇÃO DO BANCO DE DADOS - SUBCATEGORIAS")
    print("=" * 60)
    print()

    # Conectar ao banco de dados
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. Criar tabela de subcategorias (se não existir)
        if not verificar_tabela_existe(cursor, 'subcategorias'):
            print("📋 Criando tabela 'subcategorias'...")
            cursor.execute('''
                CREATE TABLE subcategorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(50) NOT NULL,
                    categoria VARCHAR(50) NOT NULL,
                    ativo BOOLEAN DEFAULT 1,
                    ordem INTEGER DEFAULT 0,
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("   ✅ Tabela 'subcategorias' criada com sucesso!")
        else:
            print("⏭️  Tabela 'subcategorias' já existe, pulando...")

        # 2. Adicionar coluna subcategoria_id na tabela produtos (se não existir)
        if not verificar_coluna_existe(cursor, 'produtos', 'subcategoria_id'):
            print("\n📋 Adicionando coluna 'subcategoria_id' na tabela 'produtos'...")
            cursor.execute('''
                ALTER TABLE produtos
                ADD COLUMN subcategoria_id INTEGER
            ''')
            print("   ✅ Coluna 'subcategoria_id' adicionada com sucesso!")
        else:
            print("\n⏭️  Coluna 'subcategoria_id' já existe, pulando...")

        # 3. Inserir subcategorias iniciais (se não existirem)
        cursor.execute("SELECT COUNT(*) FROM subcategorias")
        count = cursor.fetchone()[0]

        if count == 0:
            print("\n📋 Inserindo subcategorias iniciais para Roupas...")

            subcategorias_iniciais = [
                ('Vestido', 'Roupas', 1, 1),
                ('Saia', 'Roupas', 1, 2),
                ('Macacão', 'Roupas', 1, 3),
                ('Jaqueta Feminina', 'Roupas', 1, 4),
                ('Camisa', 'Roupas', 1, 5),
                ('Bata', 'Roupas', 1, 6),
                ('Conjunto', 'Roupas', 1, 7),
                ('Jaqueta Masculina', 'Roupas', 1, 8),
            ]

            cursor.executemany(
                'INSERT INTO subcategorias (nome, categoria, ativo, ordem) VALUES (?, ?, ?, ?)',
                subcategorias_iniciais
            )

            print("   ✅ 8 subcategorias inseridas com sucesso!")
            print("\n   📝 Subcategorias criadas:")
            print("      🎀 FEMININO:")
            print("         - Vestido")
            print("         - Saia")
            print("         - Macacão")
            print("         - Jaqueta Feminina")
            print("\n      👔 MASCULINO:")
            print("         - Camisa")
            print("         - Bata")
            print("         - Conjunto")
            print("         - Jaqueta Masculina")
        else:
            print(f"\n⏭️  Já existem {count} subcategoria(s) no banco, pulando inserção...")

        # Commit das alterações
        conn.commit()

        print("\n" + "=" * 60)
        print("✨ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("\n📊 Resumo:")
        print(f"   ✅ Tabela 'subcategorias': OK")
        print(f"   ✅ Coluna 'subcategoria_id' em produtos: OK")

        cursor.execute("SELECT COUNT(*) FROM subcategorias")
        total_subcats = cursor.fetchone()[0]
        print(f"   ✅ Total de subcategorias: {total_subcats}")

        print("\n🚀 Próximos passos:")
        print("   1. Execute: python main.py")
        print("   2. Acesse: http://localhost:5000/admin/login")
        print("   3. Vá em: Admin → Subcategorias")
        print("   4. Gerencie as subcategorias conforme necessário")
        print()

        return True

    except sqlite3.Error as e:
        print(f"\n❌ Erro durante a migração: {e}")
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("\n⚠️  ATENÇÃO: Este script irá modificar o banco de dados!")
    print("    Certifique-se de ter um backup antes de continuar.\n")

    resposta = input("Deseja continuar com a migração? (s/n): ")

    if resposta.lower() == 's':
        sucesso = migrar_banco_dados()

        if sucesso:
            print("\n✅ Tudo pronto! Seu banco de dados foi atualizado.")
        else:
            print("\n❌ A migração falhou. Verifique os erros acima.")
    else:
        print("\n❌ Migração cancelada pelo usuário.")
