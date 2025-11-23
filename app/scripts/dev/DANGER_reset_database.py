"""
!!! PERIGO - SCRIPT DESTRUTIVO !!!
=================================
ATENCAO: Este script APAGA TODOS os dados do banco de dados!

Execute APENAS em ambiente de DESENVOLVIMENTO ou na primeira instalacao.
NUNCA execute em producao!

Execute: python scripts/dev/DANGER_reset_database.py

O que este script faz:
- APAGA todas as tabelas (db.drop_all)
- Recria todas as tabelas do zero
- Cria usuario admin padrao usando ADMIN_USERNAME/ADMIN_PASSWORD do .env
- Adiciona configuracoes iniciais da loja
- Cria 6 produtos de exemplo

Alternativas mais seguras:
- Para adicionar produtos: use populate_products.py
- Para atualizar schema: use scripts/maintenance/update_schema.py
"""

import sys
import os
import json

# Adicionar diretorio pai ao path para importar modulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from database import db
from models import Produto, Admin, Configuracao
from config import Config

ADMIN_USERNAME = Config.ADMIN_USERNAME
ADMIN_PASSWORD = Config.ADMIN_PASSWORD
ADMIN_EMAIL = f"{ADMIN_USERNAME}@xododapreta.com"


def init_database():
    """Inicializa o banco de dados com dados padrao."""
    with app.app_context():
        # Remover todas as tabelas existentes
        print("Removendo tabelas antigas...")
        db.drop_all()

        # Criar todas as tabelas
        print("Criando tabelas...")
        db.create_all()

        # Criar admin padrao
        print("Criando administrador padrao...")
        admin = Admin(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL
        )
        admin.set_password(ADMIN_PASSWORD)  # Senha definida no .env
        db.session.add(admin)

        # Criar configuracoes da loja
        print("Criando configuracoes da loja...")
        configs = [
            ('loja_nome', 'Xodo da Preta', 'Nome da loja'),
            ('loja_telefone', '55 11 954375056', 'Telefone do WhatsApp'),
            ('loja_email', 'contato@xododapreta.com', 'Email de contato'),
            ('loja_instagram', '@xododapreta', 'Instagram'),
            ('loja_endereco', 'Sao Paulo, SP', 'Endereco da loja'),
        ]

        for chave, valor, descricao in configs:
            config = Configuracao(chave=chave, valor=valor, descricao=descricao)
            db.session.add(config)

        # Criar produtos de exemplo
        print("Criando produtos de exemplo...")
        produtos_exemplo = [
            {
                'nome': 'Brinco Dourado Classico',
                'descricao': 'Brinco elegante folheado a ouro, perfeito para qualquer ocasiao.',
                'preco': 45.90,
                'categoria': 'Brincos',
                'tamanhos': json.dumps(['Unico']),
                'imagem': 'brinco_01.jpg',
                'ordem': 1,
                'ativo': True
            },
            {
                'nome': 'Brinco Argola Grande',
                'descricao': 'Argola moderna e estilosa, ideal para looks despojados.',
                'preco': 39.90,
                'categoria': 'Brincos',
                'tamanhos': json.dumps(['Unico']),
                'imagem': 'brinco_02.jpg',
                'ordem': 2,
                'ativo': True
            },
            {
                'nome': 'Vestido Estampado Afro',
                'descricao': 'Vestido com estampas africanas vibrantes, confortavel e estiloso.',
                'preco': 129.90,
                'categoria': 'Roupas',
                'tamanhos': json.dumps(['P', 'M', 'G', 'GG']),
                'imagem': 'vestido_01.jpg',
                'ordem': 3,
                'ativo': True
            },
            {
                'nome': 'Blusa Cropped Dourada',
                'descricao': 'Blusa cropped com detalhes dourados, moderna e versatil.',
                'preco': 79.90,
                'categoria': 'Roupas',
                'tamanhos': json.dumps(['PP', 'P', 'M', 'G']),
                'imagem': 'blusa_01.jpg',
                'ordem': 4,
                'ativo': True
            },
            {
                'nome': 'Colar Gargantilha Etnico',
                'descricao': 'Colar gargantilha com design etnico africano, peca unica.',
                'preco': 89.90,
                'categoria': 'Colares',
                'tamanhos': json.dumps(['Unico']),
                'imagem': 'colar_01.jpg',
                'ordem': 5,
                'ativo': True
            },
            {
                'nome': 'Colar Longo Contas',
                'descricao': 'Colar longo com contas coloridas, perfeito para festas.',
                'preco': 69.90,
                'categoria': 'Colares',
                'tamanhos': json.dumps(['Unico']),
                'imagem': 'colar_02.jpg',
                'ordem': 6,
                'ativo': True
            },
        ]

        for prod_data in produtos_exemplo:
            produto = Produto(**prod_data)
            db.session.add(produto)

        # Salvar tudo no banco
        print("Salvando no banco de dados...")
        db.session.commit()

        print("\nBanco de dados inicializado com sucesso!")
        print("\nDados criados:")
        print(f"   - 1 administrador (username: {ADMIN_USERNAME}, senha: {ADMIN_PASSWORD})")
        print(f"   - {len(produtos_exemplo)} produtos de exemplo")
        print(f"   - {len(configs)} configuracoes da loja")
        print("\nIMPORTANTE: Troque a senha do admin apos o primeiro login!")
        print("\nInicie o servidor com: python main.py")


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("!!! PERIGO - SCRIPT DESTRUTIVO !!!")
    print("=" * 70)
    print("\nATENCAO: Isso vai APAGAR TODOS os dados existentes!")
    print("\nO que sera feito:")
    print("   - APAGAR todas as tabelas do banco (db.drop_all)")
    print("   - Recriar todas as tabelas do zero")
    print("   - Criar usuario admin padrao")
    print("   - Configurar informacoes da loja")
    print("   - Adicionar 6 produtos de exemplo")
    print("\nAlternativas mais seguras:")
    print("   - Para adicionar produtos: python scripts/dev/populate_products.py")
    print("   - Para atualizar schema: python scripts/maintenance/update_schema.py")
    print("\nEXECUTE APENAS EM DESENVOLVIMENTO! NUNCA EM PRODUCAO!\n")

    resposta = input("Tem certeza que deseja APAGAR TUDO? Digite 'SIM APAGAR TUDO' para continuar: ")

    if resposta == 'SIM APAGAR TUDO':
        print("\nUltima chance! Este e um processo IRREVERSIVEL!")
        confirmacao = input("Digite 'CONFIRMO' para prosseguir: ")

        if confirmacao == 'CONFIRMO':
            init_database()
            print("\nProximos passos:")
            print("   1. Execute: python scripts/dev/populate_products.py (para mais produtos)")
            print("   2. Inicie o servidor: python main.py")
            print("   3. Acesse http://localhost:5000/admin/login")
            print(f"   4. Login: {ADMIN_USERNAME} / Senha: {ADMIN_PASSWORD}")
            print("   5. TROQUE A SENHA IMEDIATAMENTE!")
        else:
            print("\nOperacao cancelada com seguranca.")
    else:
        print("\nOperacao cancelada com seguranca.")
