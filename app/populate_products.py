"""
Script para popular o banco de dados com produtos de exemplo
Execute: python populate_products.py
"""

from main import app
from database import db
from models import Produto
import json

def limpar_produtos_exemplo():
    """Remove produtos de exemplo anteriores"""
    print("Removendo produtos de exemplo anteriores...")
    Produto.query.filter(Produto.descricao.like('%[Produto de exemplo]%')).delete()
    db.session.commit()
    print("✓ Produtos de exemplo removidos")

def criar_produtos_exemplo():
    """Cria produtos de exemplo para todas as categorias"""

    produtos_exemplo = [
        # COLARES
        {
            'nome': 'Colar Africano Ouro',
            'descricao': 'Colar artesanal com design africano em tons de ouro, perfeito para ocasiões especiais. [Produto de exemplo]',
            'preco': 89.90,
            'categoria': 'Colares',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 1
        },
        {
            'nome': 'Colar Afro Miçangas Coloridas',
            'descricao': 'Colar vibrante com miçangas coloridas, celebrando a cultura afro. [Produto de exemplo]',
            'preco': 65.00,
            'categoria': 'Colares',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 2
        },
        {
            'nome': 'Colar Étnico Madeira',
            'descricao': 'Colar étnico confeccionado em madeira nobre com acabamento artesanal. [Produto de exemplo]',
            'preco': 75.50,
            'categoria': 'Colares',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 3
        },

        # ANÉIS
        {
            'nome': 'Anel Africano Dourado',
            'descricao': 'Anel com símbolos africanos em acabamento dourado, design exclusivo. [Produto de exemplo]',
            'preco': 45.00,
            'categoria': 'Anéis',
            'tamanhos': json.dumps(['P', 'M', 'G']),
            'ativo': True,
            'ordem': 1
        },
        {
            'nome': 'Anel Afro Prata',
            'descricao': 'Anel em prata com detalhes afro, elegante e versátil. [Produto de exemplo]',
            'preco': 55.00,
            'categoria': 'Anéis',
            'tamanhos': json.dumps(['P', 'M', 'G']),
            'ativo': True,
            'ordem': 2
        },
        {
            'nome': 'Anel Tribal Bronze',
            'descricao': 'Anel tribal em bronze com gravações manuais, peça única. [Produto de exemplo]',
            'preco': 38.90,
            'categoria': 'Anéis',
            'tamanhos': json.dumps(['P', 'M', 'G', 'GG']),
            'ativo': True,
            'ordem': 3
        },
        {
            'nome': 'Anel Geométrico Afro',
            'descricao': 'Anel com padrões geométricos africanos, moderno e autêntico. [Produto de exemplo]',
            'preco': 42.00,
            'categoria': 'Anéis',
            'tamanhos': json.dumps(['P', 'M', 'G']),
            'ativo': True,
            'ordem': 4
        },

        # PULSEIRAS
        {
            'nome': 'Pulseira Afro Colorida',
            'descricao': 'Pulseira vibrante com cores que celebram a identidade afro. [Produto de exemplo]',
            'preco': 35.00,
            'categoria': 'Pulseiras',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 1
        },
        {
            'nome': 'Pulseira Tribal Couro',
            'descricao': 'Pulseira tribal em couro legítimo com detalhes em metal. [Produto de exemplo]',
            'preco': 48.50,
            'categoria': 'Pulseiras',
            'tamanhos': json.dumps(['P', 'M', 'G']),
            'ativo': True,
            'ordem': 2
        },
        {
            'nome': 'Pulseira Miçangas Africanas',
            'descricao': 'Pulseira artesanal com miçangas africanas tradicionais. [Produto de exemplo]',
            'preco': 29.90,
            'categoria': 'Pulseiras',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 3
        },
        {
            'nome': 'Pulseira Étnica Dourada',
            'descricao': 'Pulseira étnica com acabamento dourado, sofisticada e elegante. [Produto de exemplo]',
            'preco': 52.00,
            'categoria': 'Pulseiras',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 4
        },
        {
            'nome': 'Pulseira Afro Mix',
            'descricao': 'Conjunto de pulseiras afro com mix de cores e materiais. [Produto de exemplo]',
            'preco': 39.90,
            'categoria': 'Pulseiras',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 5
        },

        # BRINCOS
        {
            'nome': 'Brincos Afro Argola Grande',
            'descricao': 'Brincos em formato de argola com design africano, statement piece. [Produto de exemplo]',
            'preco': 58.00,
            'categoria': 'Brincos',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 1
        },
        {
            'nome': 'Brincos Tribal Colorido',
            'descricao': 'Brincos tribais com cores vibrantes, perfeitos para o dia a dia. [Produto de exemplo]',
            'preco': 42.50,
            'categoria': 'Brincos',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 2
        },
        {
            'nome': 'Brincos Étnico Madeira',
            'descricao': 'Brincos étnicos confeccionados em madeira pintada à mão. [Produto de exemplo]',
            'preco': 36.00,
            'categoria': 'Brincos',
            'tamanhos': json.dumps(['Único']),
            'ativo': True,
            'ordem': 3
        },

        # ROUPAS
        {
            'nome': 'Vestido Africano Estampado',
            'descricao': 'Vestido longo com estampas africanas autênticas, versátil e elegante. [Produto de exemplo]',
            'preco': 159.90,
            'categoria': 'Roupas',
            'tamanhos': json.dumps(['PP', 'P', 'M', 'G', 'GG']),
            'ativo': True,
            'ordem': 1
        },
        {
            'nome': 'Camisa Afro Print',
            'descricao': 'Camisa unissex com print afro exclusivo, confortável e estilosa. [Produto de exemplo]',
            'preco': 98.00,
            'categoria': 'Roupas',
            'tamanhos': json.dumps(['P', 'M', 'G', 'GG']),
            'ativo': True,
            'ordem': 2
        },
        {
            'nome': 'Saia Midi Afro',
            'descricao': 'Saia midi com estampa afro vibrante, perfeita para todas as ocasiões. [Produto de exemplo]',
            'preco': 89.90,
            'categoria': 'Roupas',
            'tamanhos': json.dumps(['PP', 'P', 'M', 'G', 'GG']),
            'ativo': True,
            'ordem': 3
        },
        {
            'nome': 'Calça Africana Wide Leg',
            'descricao': 'Calça wide leg com estampa africana, conforto e estilo em uma peça. [Produto de exemplo]',
            'preco': 125.00,
            'categoria': 'Roupas',
            'tamanhos': json.dumps(['P', 'M', 'G', 'GG']),
            'ativo': True,
            'ordem': 4
        },
    ]

    print(f"\nCriando {len(produtos_exemplo)} produtos de exemplo...")

    for produto_data in produtos_exemplo:
        produto = Produto(**produto_data)
        db.session.add(produto)
        print(f"  ✓ {produto_data['categoria']}: {produto_data['nome']}")

    db.session.commit()
    print(f"\n✓ {len(produtos_exemplo)} produtos criados com sucesso!")

def mostrar_estatisticas():
    """Mostra estatísticas dos produtos no banco"""
    print("\n" + "="*60)
    print("ESTATÍSTICAS DO BANCO DE DADOS")
    print("="*60)

    total = Produto.query.count()
    ativos = Produto.query.filter_by(ativo=True).count()

    print(f"\nTotal de produtos: {total}")
    print(f"Produtos ativos: {ativos}")
    print(f"\nProdutos por categoria:")

    categorias = ['Colares', 'Anéis', 'Pulseiras', 'Brincos', 'Roupas']
    for categoria in categorias:
        count = Produto.query.filter_by(categoria=categoria).count()
        print(f"  • {categoria}: {count} produtos")

    print("\n" + "="*60)

if __name__ == '__main__':
    print("="*60)
    print("SCRIPT DE POPULAÇÃO DO BANCO DE DADOS")
    print("Xodó da Preta - Produtos de Exemplo")
    print("="*60)

    with app.app_context():
        # Pergunta se deseja limpar produtos anteriores
        resposta = input("\nDeseja remover produtos de exemplo anteriores? (s/n): ").lower()
        if resposta == 's':
            limpar_produtos_exemplo()

        # Cria novos produtos
        criar_produtos_exemplo()

        # Mostra estatísticas
        mostrar_estatisticas()

        print("\n✓ Script concluído com sucesso!")
        print("\nVocê pode agora:")
        print("  1. Acessar a loja em: http://localhost:5000/shop")
        print("  2. Testar os filtros por categoria")
        print("  3. Gerenciar produtos no painel admin em: http://localhost:5000/admin/login")
