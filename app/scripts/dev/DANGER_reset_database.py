"""
🚨🚨🚨 PERIGO - SCRIPT DESTRUTIVO 🚨🚨🚨
=====================================
⚠️ ATENÇÃO: Este script APAGA TODOS os dados do banco de dados!

Execute APENAS em ambiente de DESENVOLVIMENTO ou na primeira instalação!
NUNCA execute em produção!

Execute: python scripts/dev/DANGER_reset_database.py

O que este script faz:
- ❌ APAGA todas as tabelas (db.drop_all)
- ✅ Recria todas as tabelas do zero
- ✅ Cria usuário admin padrão (admin/admin123)
- ✅ Adiciona configurações iniciais da loja
- ✅ Cria 6 produtos de exemplo

💡 Alternativas mais seguras:
- Para adicionar produtos: use populate_products.py
- Para atualizar schema: use scripts/maintenance/update_schema.py
"""

import sys
import os

# Adicionar diretório pai ao path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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
    print("\n" + "="*70)
    print("🚨🚨🚨 PERIGO - SCRIPT DESTRUTIVO 🚨🚨🚨")
    print("="*70)
    print("\n⚠️  ATENÇÃO: Isso vai APAGAR TODOS os dados existentes!")
    print("\n📋 O que será feito:")
    print("   - ❌ APAGAR todas as tabelas do banco (db.drop_all)")
    print("   - ✅ Recriar todas as tabelas do zero")
    print("   - ✅ Criar usuário admin padrão")
    print("   - ✅ Configurar informações da loja")
    print("   - ✅ Adicionar 6 produtos de exemplo")
    print("\n💡 Alternativas mais seguras:")
    print("   - Para adicionar produtos: python scripts/dev/populate_products.py")
    print("   - Para atualizar schema: python scripts/maintenance/update_schema.py")
    print("\n🔴 EXECUTE APENAS EM DESENVOLVIMENTO! NUNCA EM PRODUÇÃO!\n")

    resposta = input("🚨 Tem certeza que deseja APAGAR TUDO? Digite 'SIM APAGAR TUDO' para continuar: ")

    if resposta == 'SIM APAGAR TUDO':
        print("\n⚠️  Última chance! Este é um processo IRREVERSÍVEL!")
        confirmacao = input("Digite 'CONFIRMO' para prosseguir: ")

        if confirmacao == 'CONFIRMO':
            init_database()
            print("\n📝 Próximos passos:")
            print("   1. Execute: python scripts/dev/populate_products.py (para mais produtos)")
            print("   2. Inicie o servidor: python main.py")
            print("   3. Acesse http://localhost:5000/admin/login")
            print("   4. Login: admin / Senha: admin123")
            print("   5. ⚠️ TROQUE A SENHA IMEDIATAMENTE!")
        else:
            print("\n✅ Operação cancelada com segurança.")
    else:
        print("\n✅ Operação cancelada com segurança.")