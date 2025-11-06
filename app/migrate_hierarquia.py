"""
Script de migração para adicionar hierarquia de 3 níveis (categoria > subcategoria > tipo)
Execute este script APENAS UMA VEZ para atualizar o banco de dados existente
"""
import sqlite3
from pathlib import Path

# Caminho do banco de dados
DB_PATH = Path(__file__).parent / 'loja.db'

def verificar_coluna_existe(cursor, tabela, coluna):
    """Verifica se uma coluna existe em uma tabela"""
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [row[1] for row in cursor.fetchall()]
    return coluna in colunas

def migrar_hierarquia():
    """Adiciona colunas subcategoria e tipo para hierarquia de 3 níveis"""

    if not DB_PATH.exists():
        print("❌ Banco de dados não encontrado!")
        print(f"   Esperado em: {DB_PATH}")
        return False

    print("=" * 70)
    print("🔄 MIGRAÇÃO - HIERARQUIA DE 3 NÍVEIS (Categoria > Subcategoria > Tipo)")
    print("=" * 70)
    print()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Adicionar coluna 'subcategoria' (Nível 2: Feminino/Masculino)
        if not verificar_coluna_existe(cursor, 'produtos', 'subcategoria'):
            print("📋 Adicionando coluna 'subcategoria' (Nível 2) na tabela 'produtos'...")
            cursor.execute('ALTER TABLE produtos ADD COLUMN subcategoria VARCHAR(50)')
            print("   ✅ Coluna 'subcategoria' adicionada com sucesso!")
        else:
            print("⏭️  Coluna 'subcategoria' já existe, pulando...")

        # Adicionar coluna 'tipo' (Nível 3: Vestido, Camisa, etc.)
        if not verificar_coluna_existe(cursor, 'produtos', 'tipo'):
            print("\n📋 Adicionando coluna 'tipo' (Nível 3) na tabela 'produtos'...")
            cursor.execute('ALTER TABLE produtos ADD COLUMN tipo VARCHAR(50)')
            print("   ✅ Coluna 'tipo' adicionada com sucesso!")
        else:
            print("\n⏭️  Coluna 'tipo' já existe, pulando...")

        conn.commit()

        print("\n" + "=" * 70)
        print("✨ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print("\n📊 Estrutura de 3 Níveis:")
        print("   📁 Nível 1: Categoria (ex: Roupas, Brincos, Colares)")
        print("   📂 Nível 2: Subcategoria (ex: Feminino, Masculino)")
        print("   📄 Nível 3: Tipo (ex: Vestido, Camisa, Saia)")
        print("\n🎯 Exemplo de Hierarquia:")
        print("   Roupas → Feminino → Vestido")
        print("   Roupas → Masculino → Camisa")
        print("\n💡 Produtos Antigos:")
        print("   ✅ Continuam funcionando (campos nullable)")
        print("   ✅ Aparecerão apenas no filtro de categoria")
        print("\n🚀 Próximos Passos:")
        print("   1. Execute: python main.py")
        print("   2. Acesse: /admin/produtos/novo")
        print("   3. Ao selecionar 'Roupas', verá os campos Subcategoria e Tipo")
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
    print("\n⚠️  Este script irá adicionar 2 novas colunas ao banco de dados:")
    print("    - subcategoria (VARCHAR 50, NULL)")
    print("    - tipo (VARCHAR 50, NULL)")
    print("\n✅ Produtos existentes NÃO serão afetados (colunas nullable)")
    print()

    resposta = input("Deseja continuar com a migração? (s/n): ")

    if resposta.lower() == 's':
        sucesso = migrar_hierarquia()
        if sucesso:
            print("\n✅ Banco de dados atualizado com sucesso!")
            print("   Agora você pode usar hierarquia de 3 níveis em Roupas.")
        else:
            print("\n❌ A migração falhou. Verifique os erros acima.")
    else:
        print("\n❌ Migração cancelada pelo usuário.")
