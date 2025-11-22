"""
Script para CRIAR subcategorias de exemplo com hierarquia de 2 níveis.
Execute este script após limpar as subcategorias antigas.

USO: python criar_subcategorias_exemplo.py

Este script cria a seguinte estrutura (máximo 2 níveis):
- Categoria: Roupas
  ├─ Feminino (Subcategoria - Nível 1)
  │  ├─ Vestido (Sub-subcategoria - Nível 2)
  │  ├─ Saia (Sub-subcategoria - Nível 2)
  │  └─ Macacão (Sub-subcategoria - Nível 2)
  └─ Masculino (Subcategoria - Nível 1)
     ├─ Camisa (Sub-subcategoria - Nível 2)
     └─ Bata (Sub-subcategoria - Nível 2)

- Categoria: Brincos
  ├─ Argola (Subcategoria - Nível 1)
  └─ Pêndulo (Subcategoria - Nível 1)
"""

import sys
from pathlib import Path

# Adicionar diretório do app ao path
app_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(app_dir))

from database import db
from models import Subcategoria
from main import app


def criar_subcategorias_exemplo():
    """Cria estrutura de exemplo de subcategorias hierárquicas"""

    with app.app_context():
        print("=" * 70)
        print("CRIAÇÃO DE SUBCATEGORIAS DE EXEMPLO - Xodó da Preta")
        print("=" * 70)

        # Verificar se já existem subcategorias
        total_existentes = Subcategoria.query.count()
        if total_existentes > 0:
            print(f"\n⚠️  ATENÇÃO: Já existem {total_existentes} subcategoria(s) no banco!")
            print("   Recomendamos executar 'limpar_subcategorias.py' primeiro.")
            confirmacao = input("\nDeseja continuar mesmo assim? Digite 'SIM': ")
            if confirmacao.strip().upper() != 'SIM':
                print("\n❌ Operação cancelada.")
                return

        try:
            print("\n🔄 Criando subcategorias de exemplo...\n")

            # ==========================================
            # CATEGORIA: ROUPAS
            # ==========================================
            print("👗 Categoria: ROUPAS")

            # Nível 1: Feminino
            feminino = Subcategoria(
                nome='Feminino',
                categoria='Roupas',
                parent_id=None,
                ativo=True,
                ordem=1
            )
            db.session.add(feminino)
            db.session.flush()  # Para obter o ID
            print(f"   ├─ [Nível 1] Feminino (ID: {feminino.id})")

            # Nível 2 (Filhos de Feminino)
            vestido = Subcategoria(
                nome='Vestido',
                categoria='Roupas',
                parent_id=feminino.id,
                ativo=True,
                ordem=1
            )
            db.session.add(vestido)
            print(f"   │  ├─ [Nível 2] Vestido")

            saia = Subcategoria(
                nome='Saia',
                categoria='Roupas',
                parent_id=feminino.id,
                ativo=True,
                ordem=2
            )
            db.session.add(saia)
            print(f"   │  ├─ [Nível 2] Saia")

            macacao = Subcategoria(
                nome='Macacão',
                categoria='Roupas',
                parent_id=feminino.id,
                ativo=True,
                ordem=3
            )
            db.session.add(macacao)
            print(f"   │  └─ [Nível 2] Macacão")

            # Nível 1: Masculino
            masculino = Subcategoria(
                nome='Masculino',
                categoria='Roupas',
                parent_id=None,
                ativo=True,
                ordem=2
            )
            db.session.add(masculino)
            db.session.flush()
            print(f"   └─ [Nível 1] Masculino (ID: {masculino.id})")

            # Nível 2 (Filhos de Masculino)
            camisa = Subcategoria(
                nome='Camisa',
                categoria='Roupas',
                parent_id=masculino.id,
                ativo=True,
                ordem=1
            )
            db.session.add(camisa)
            print(f"      ├─ [Nível 2] Camisa")

            bata = Subcategoria(
                nome='Bata',
                categoria='Roupas',
                parent_id=masculino.id,
                ativo=True,
                ordem=2
            )
            db.session.add(bata)
            print(f"      └─ [Nível 2] Bata")

            # ==========================================
            # CATEGORIA: BRINCOS
            # ==========================================
            print("\n💍 Categoria: BRINCOS")

            argola = Subcategoria(
                nome='Argola',
                categoria='Brincos',
                parent_id=None,
                ativo=True,
                ordem=1
            )
            db.session.add(argola)
            print(f"   ├─ [Nível 1] Argola")

            pendulo = Subcategoria(
                nome='Pêndulo',
                categoria='Brincos',
                parent_id=None,
                ativo=True,
                ordem=2
            )
            db.session.add(pendulo)
            print(f"   └─ [Nível 1] Pêndulo")

            # ==========================================
            # CATEGORIA: COLARES
            # ==========================================
            print("\n📿 Categoria: COLARES")

            colar_curto = Subcategoria(
                nome='Colar Curto',
                categoria='Colares',
                parent_id=None,
                ativo=True,
                ordem=1
            )
            db.session.add(colar_curto)
            print(f"   ├─ [Nível 1] Colar Curto")

            colar_longo = Subcategoria(
                nome='Colar Longo',
                categoria='Colares',
                parent_id=None,
                ativo=True,
                ordem=2
            )
            db.session.add(colar_longo)
            print(f"   └─ [Nível 1] Colar Longo")

            # Salvar tudo
            db.session.commit()

            print("\n" + "=" * 70)
            print("✨ SUBCATEGORIAS CRIADAS COM SUCESSO!")
            print("=" * 70)

            # Resumo
            total_criadas = Subcategoria.query.count()
            nivel1 = Subcategoria.query.filter_by(parent_id=None).count()
            nivel2 = Subcategoria.query.filter(
                Subcategoria.parent_id.isnot(None)
            ).count()

            print(f"\n📊 RESUMO:")
            print(f"   Total de subcategorias: {total_criadas}")
            print(f"   Nível 1 (subcategorias): {nivel1}")
            print(f"   Nível 2 (sub-subcategorias): {nivel2}")

            print("\n📋 PRÓXIMOS PASSOS:")
            print("   1. Acesse o painel admin: http://localhost:5000/admin")
            print("   2. Vá em 'Subcategorias' para visualizar a hierarquia")
            print("   3. Adicione um novo produto e veja as subcategorias aparecendo!")
            print("   4. Teste a hierarquia de 2 níveis:")
            print("      - Selecione 'Roupas' → 'Masculino' → 'Camisa'")
            print("\n💡 As subcategorias funcionam com 2 níveis de forma 100% dinâmica!")
            print()

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERRO ao criar subcategorias: {e}")
            print("   O banco de dados foi revertido.")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == '__main__':
    criar_subcategorias_exemplo()
