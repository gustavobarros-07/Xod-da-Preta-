"""
Script para inicializar o banco de dados
Execute: python init_db.py
"""

from main import app
from database import db
from models import Produto, Admin, Configuracao
import json

def init_database():
    """Inicializa o banco de dados com dados padrão"""
    
    with app.app_context():
        # Remover todas as tabelas existentes
        print("🗑️  Removendo tabelas antigas...")
        db.drop_all()
        
        # Criar todas as tabelas
        print("📦 Criando tabelas...")
        db.create_all()
        
        # Criar admin padrão
        print("👤 Criando administrador padrão...")
        admin = Admin(
            username='admin',
            email='admin@xododapreta.com'
        )
        admin.set_password('admin123')  # Senha padrão (trocar depois!)
        db.session.add(admin)
        
        # Criar configurações da loja
        print("⚙️  Criando configurações da loja...")
        configs = [
            ('loja_nome', 'Xodó da Preta', 'Nome da loja'),
            ('loja_telefone', '55 11 954375056', 'Telefone do WhatsApp'),
            ('loja_email', 'contato@xododapreta.com', 'Email de contato'),
            ('loja_instagram', '@xododapreta', 'Instagram'),
            ('loja_endereco', 'São Paulo, SP', 'Endereço da loja'),
        ]
        
        for chave, valor, descricao in configs:
            config = Configuracao(chave=chave, valor=valor, descricao=descricao)
            db.session.add(config)
        
        # Criar produtos de exemplo
        print("🛍️  Criando produtos de exemplo...")
        produtos_exemplo = [
            {
                'nome': 'Brinco Dourado Clássico',
                'descricao': 'Brinco elegante folheado a ouro, perfeito para qualquer ocasião.',
                'preco': 45.90,
                'categoria': 'Brincos',
                'tamanhos': json.dumps(['Único']),
                'imagem': 'brinco_01.jpg',
                'ordem': 1,
                'ativo': True
            },
            {
                'nome': 'Brinco Argola Grande',
                'descricao': 'Argola moderna e estilosa, ideal para looks despojados.',
                'preco': 39.90,
                'categoria': 'Brincos',
                'tamanhos': json.dumps(['Único']),
                'imagem': 'brinco_02.jpg',
                'ordem': 2,
                'ativo': True
            },
            {
                'nome': 'Vestido Estampado Afro',
                'descricao': 'Vestido com estampas africanas vibrantes, confortável e estiloso.',
                'preco': 129.90,
                'categoria': 'Roupas',
                'tamanhos': json.dumps(['P', 'M', 'G', 'GG']),
                'imagem': 'vestido_01.jpg',
                'ordem': 3,
                'ativo': True
            },
            {
                'nome': 'Blusa Cropped Dourada',
                'descricao': 'Blusa cropped com detalhes dourados, moderna e versátil.',
                'preco': 79.90,
                'categoria': 'Roupas',
                'tamanhos': json.dumps(['PP', 'P', 'M', 'G']),
                'imagem': 'blusa_01.jpg',
                'ordem': 4,
                'ativo': True
            },
            {
                'nome': 'Colar Gargantilha Étnico',
                'descricao': 'Colar gargantilha com design étnico africano, peça única.',
                'preco': 89.90,
                'categoria': 'Colares',
                'tamanhos': json.dumps(['Único']),
                'imagem': 'colar_01.jpg',
                'ordem': 5,
                'ativo': True
            },
            {
                'nome': 'Colar Longo Contas',
                'descricao': 'Colar longo com contas coloridas, perfeito para festas.',
                'preco': 69.90,
                'categoria': 'Colares',
                'tamanhos': json.dumps(['Único']),
                'imagem': 'colar_02.jpg',
                'ordem': 6,
                'ativo': True
            },
        ]
        
        for prod_data in produtos_exemplo:
            produto = Produto(**prod_data)
            db.session.add(produto)
        
        # Salvar tudo no banco
        print("💾 Salvando no banco de dados...")
        db.session.commit()
        
        print("\n✅ Banco de dados inicializado com sucesso!")
        print("\n📊 Dados criados:")
        print(f"   - 1 administrador (username: admin, senha: admin123)")
        print(f"   - {len(produtos_exemplo)} produtos de exemplo")
        print(f"   - {len(configs)} configurações da loja")
        print("\n🔐 IMPORTANTE: Troque a senha do admin após o primeiro login!")
        print("\n🚀 Inicie o servidor com: python main.py")

if __name__ == '__main__':
    print("\n🎯 INICIALIZANDO BANCO DE DADOS - XODÓ DA PRETA\n")
    print("⚠️  ATENÇÃO: Isso vai APAGAR todos os dados existentes!")
    resposta = input("Deseja continuar? (s/n): ")
    
    if resposta.lower() == 's':
        init_database()
    else:
        print("❌ Operação cancelada.")