from datetime import datetime
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Produto(db.Model):
    """Modelo para produtos da loja"""
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Brincos, Roupas, Colares
    tamanhos = db.Column(db.String(200), nullable=True)  # JSON string: ["P", "M", "G"]
    imagem = db.Column(db.String(200), nullable=True)  # Nome do arquivo
    ordem = db.Column(db.Integer, default=0)  # Para ordenação personalizada
    ativo = db.Column(db.Boolean, default=True)  # Produto visível ou não
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    def to_dict(self):
        """Converte o produto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'categoria': self.categoria,
            'tamanhos': self.tamanhos,
            'imagem': self.imagem,
            'ordem': self.ordem,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y') if self.data_criacao else None
        }


class Admin(db.Model):
    """Modelo para administradores do sistema"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        """Define a senha (com hash)"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'


class Configuracao(db.Model):
    """Modelo para configurações da loja"""
    __tablename__ = 'configuracoes'

    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.Text, nullable=True)
    descricao = db.Column(db.String(200), nullable=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Configuracao {self.chave}>'

    @staticmethod
    def get_valor(chave, default=None):
        """Obtém o valor de uma configuração"""
        config = Configuracao.query.filter_by(chave=chave).first()
        return config.valor if config else default

    @staticmethod
    def set_valor(chave, valor, descricao=None):
        """Define o valor de uma configuração"""
        config = Configuracao.query.filter_by(chave=chave).first()
        if config:
            config.valor = valor
            if descricao:
                config.descricao = descricao
        else:
            config = Configuracao(chave=chave, valor=valor, descricao=descricao)
            db.session.add(config)
        db.session.commit()
        return config


class ItemCarrinho(db.Model):
    """Modelo para itens do carrinho de compras"""
    __tablename__ = 'itens_carrinho'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)  # ID da sessão do usuário
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    tamanho = db.Column(db.String(10), nullable=True)  # Tamanho selecionado (se aplicável)
    data_adicao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com Produto
    produto = db.relationship('Produto', backref='itens_carrinho')

    def __repr__(self):
        return f'<ItemCarrinho produto_id={self.produto_id} qtd={self.quantidade}>'

    def to_dict(self):
        """Converte o item do carrinho para dicionário"""
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome,
            'produto_preco': self.produto.preco,
            'produto_imagem': self.produto.imagem,
            'quantidade': self.quantidade,
            'tamanho': self.tamanho,
            'subtotal': self.produto.preco * self.quantidade
        }
