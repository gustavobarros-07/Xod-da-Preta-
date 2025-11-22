"""
Script para LIMPAR TODAS as subcategorias do banco de dados.
Execute este script para resetar o sistema de subcategorias.

USO: python limpar_subcategorias.py

ATENÇÃO: Este script irá:
1. Remover TODAS as subcategorias existentes
2. Limpar a referência subcategoria_id de todos os produtos
3. Permitir recomeçar do zero com o novo sistema hierárquico
"""

import sys
from pathlib import Path

# Adicionar diretório do app ao path
app_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(app_dir))

from database import db
from models import Subcategoria, Produto
from main import app


def limpar_subcategorias():
    """Remove todas as subcategorias e limpa referências nos produtos"""

    with app.app_context():
        print("=" * 60)
        print("LIMPEZA DE SUBCATEGORIAS - Xodó da Preta")
        print("=" * 60)

        # Contar subcategorias existentes
        total_subcategorias = Subcategoria.query.count()
        print(f"\n📊 Subcategorias encontradas: {total_subcategorias}")

        # Contar produtos com subcategoria_id
        produtos_com_subcat = Produto.query.filter(Produto.subcategoria_id.isnot(None)).count()
        print(f"📦 Produtos com subcategoria associada: {produtos_com_subcat}")

        if total_subcategorias == 0:
            print("\n✅ Não há subcategorias para limpar. Banco já está limpo!")
            return

        # Confirmar ação
        print("\n⚠️  ATENÇÃO: Esta ação é IRREVERSÍVEL!")
        print("   Todas as subcategorias serão deletadas permanentemente.")
        confirmacao = input("\nDeseja continuar? Digite 'SIM' para confirmar: ")

        if confirmacao.strip().upper() != 'SIM':
            print("\n❌ Operação cancelada pelo usuário.")
            return

        try:
            print("\n🔄 Iniciando limpeza...")

            # Passo 1: Limpar subcategoria_id de todos os produtos
            print(f"\n1️⃣  Limpando referências em {produtos_com_subcat} produto(s)...")
            Produto.query.update({
                Produto.subcategoria_id: None,
                Produto.subcategoria: None,
                Produto.tipo: None
            })
            db.session.commit()
            print("   ✅ Referências de produtos limpas com sucesso!")

            # Passo 2: Deletar todas as subcategorias
            print(f"\n2️⃣  Removendo {total_subcategorias} subcategoria(s)...")
            Subcategoria.query.delete()
            db.session.commit()
            print("   ✅ Subcategorias removidas com sucesso!")

            print("\n" + "=" * 60)
            print("✨ LIMPEZA CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print("\n📋 Próximos passos:")
            print("   1. Acesse o painel admin: /admin/subcategorias")
            print("   2. Crie suas subcategorias (máximo 2 níveis):")
            print("      - Nível 1 (Subcategoria): Ex: Feminino, Masculino")
            print("      - Nível 2 (Sub-subcategoria): Ex: Vestido, Camisa, Bata")
            print("   3. Ao adicionar produtos, as subcategorias aparecerão automaticamente!")
            print("\n💡 Exemplo de hierarquia (máximo 2 níveis):")
            print("   Categoria: Roupas")
            print("   ├─ Feminino (Subcategoria - Nível 1)")
            print("   │  ├─ Vestido (Sub-subcategoria - Nível 2)")
            print("   │  └─ Saia (Sub-subcategoria - Nível 2)")
            print("   └─ Masculino (Subcategoria - Nível 1)")
            print("      ├─ Camisa (Sub-subcategoria - Nível 2)")
            print("      └─ Bata (Sub-subcategoria - Nível 2)")
            print("\n⚠️  IMPORTANTE: O sistema não permite criar um terceiro nível!")
            print()

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERRO durante a limpeza: {e}")
            print("   O banco de dados foi revertido ao estado anterior.")
            sys.exit(1)


if __name__ == '__main__':
    limpar_subcategorias()
