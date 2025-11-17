"""
Script para Popular Subcategorias Padrão
=========================================
Popula a tabela de subcategorias com valores padrão para a categoria Roupas.

Execute: python scripts/dev/popular_subcategorias.py

⚠️ IMPORTANTE: Este script permite resetar subcategorias.
Use com cuidado se já tiver subcategorias customizadas!

Subcategorias criadas:
- Roupas → Feminino
- Roupas → Masculino
- Roupas → Unissex
"""

import sys
import os

# Adicionar diretório pai ao path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database import db
from models import Subcategoria
from main import app

def popular_subcategorias():
    """Popula a tabela subcategorias com valores padrão"""

    with app.app_context():
        print("Populando subcategorias...")

        # Verificar se já existem subcategorias
        count = Subcategoria.query.count()
        if count > 0:
            print(f"Ja existem {count} subcategorias no banco.")
            resposta = input("Deseja apagar todas e recriar? (s/n): ")
            if resposta.lower() == 's':
                Subcategoria.query.delete()
                db.session.commit()
                print("Subcategorias antigas removidas.")
            else:
                print("Operacao cancelada.")
                return

        # Subcategorias de Roupas
        subcategorias_roupas = [
            {'nome': 'Feminino', 'categoria': 'Roupas', 'ordem': 1},
            {'nome': 'Masculino', 'categoria': 'Roupas', 'ordem': 2},
            {'nome': 'Unissex', 'categoria': 'Roupas', 'ordem': 3},
        ]

        for subcat_data in subcategorias_roupas:
            subcat = Subcategoria(
                nome=subcat_data['nome'],
                categoria=subcat_data['categoria'],
                ordem=subcat_data['ordem'],
                ativo=True
            )
            db.session.add(subcat)
            print(f"  + Adicionada: {subcat_data['categoria']} -> {subcat_data['nome']}")

        db.session.commit()
        print("\nSubcategorias populadas com sucesso!")
        print(f"Total: {Subcategoria.query.count()} subcategorias")

        # Listar subcategorias
        print("\nSubcategorias criadas:")
        for subcat in Subcategoria.query.order_by(Subcategoria.categoria, Subcategoria.ordem).all():
            print(f"  - {subcat.categoria} -> {subcat.nome} (ID: {subcat.id})")

if __name__ == '__main__':
    popular_subcategorias()
