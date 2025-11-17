from datetime import datetime
import json
from database import db
from werkzeug.security import generate_password_hash, check_password_hash


class Subcategoria(db.Model):
    """Modelo para subcategorias de produtos"""
    __tablename__ = 'subcategorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Categoria pai
    parent_id = db.Column(db.Integer, db.ForeignKey('subcategorias.id'), nullable=True)  # Subcategoria pai (para hierarquia)
    ativo = db.Column(db.Boolean, default=True)
    ordem = db.Column(db.Integer, default=0)  # Para ordenação
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com produtos
    produtos = db.relationship('Produto', backref='subcategoria_obj', lazy=True)

    # Relacionamento hierárquico (subcategorias filhas)
    filhas = db.relationship('Subcategoria', backref=db.backref('parent', remote_side=[id]), lazy=True)

    def __repr__(self):
        return f'<Subcategoria {self.categoria} - {self.nome}>'

    def to_dict(self):
        """Converte a subcategoria para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria,
            'parent_id': self.parent_id,
            'parent_nome': self.parent.nome if self.parent else None,
            'ativo': self.ativo,
            'ordem': self.ordem
        }


class Produto(db.Model):
    """Modelo para produtos da loja"""
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Nível 1: Brincos, Roupas, Colares, etc.
    subcategoria = db.Column(db.String(50), nullable=True)  # Nível 2: Feminino, Masculino (para Roupas)
    tipo = db.Column(db.String(50), nullable=True)  # Nível 3: Vestido, Camisa, Saia, etc.
    subcategoria_id = db.Column(db.Integer, db.ForeignKey('subcategorias.id'), nullable=True)  # Legado - manter por compatibilidade
    tamanhos = db.Column(db.String(200), nullable=True)  # JSON string: ["P", "M", "G"]
    imagem = db.Column(db.String(200), nullable=True)  # Nome do arquivo (imagem principal)
    imagens_adicionais = db.Column(db.Text, nullable=True)  # JSON string: ["img1.jpg", "img2.jpg", "img3.jpg"]
    ordem = db.Column(db.Integer, default=0)  # Para ordenação personalizada
    ativo = db.Column(db.Boolean, default=True)  # Produto visível ou não
    destaque = db.Column(db.Boolean, default=False)  # Produto em destaque na home
    visualizacoes = db.Column(db.Integer, default=0)  # Contador de visualizações
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
            'subcategoria': self.subcategoria,
            'tipo': self.tipo,
            'subcategoria_id': self.subcategoria_id,
            'subcategoria_nome': self.subcategoria_obj.nome if self.subcategoria_obj else None,
            'tamanhos': self.tamanhos,
            'imagem': self.imagem,
            'ordem': self.ordem,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y') if isinstance(self.data_criacao, datetime) else (self.data_criacao if self.data_criacao else None)
        }

    def get_todas_imagens(self):
        """Retorna lista com todas as imagens (principal + adicionais)"""
        imagens = []
        if self.imagem:
            imagens.append(self.imagem)
        if self.imagens_adicionais:
            try:
                imagens.extend(json.loads(self.imagens_adicionais))
            except json.JSONDecodeError:
                pass
        return imagens

    def set_imagens_adicionais(self, lista_imagens):
        """Define imagens adicionais a partir de uma lista"""
        self.imagens_adicionais = json.dumps(lista_imagens) if lista_imagens else None


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


class ProdutoVisualizacao(db.Model):
    """Modelo para rastreamento de visualizações de produtos (Analytics)"""
    __tablename__ = 'produto_visualizacoes'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    data_visualizacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    produto = db.relationship('Produto', backref='visualizacoes_registro')

    def __repr__(self):
        return f'<ProdutoVisualizacao produto_id={self.produto_id} em {self.data_visualizacao}>'


class Cupom(db.Model):
    """Modelo para cupons de desconto"""
    __tablename__ = 'cupons'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)  # Ex: PRIMEIRACOMPRA10
    descricao = db.Column(db.String(200), nullable=True)  # Descrição do cupom

    # Tipo de desconto
    tipo_desconto = db.Column(db.String(20), nullable=False, default='percentual')  # 'percentual' ou 'fixo'
    valor_desconto = db.Column(db.Float, nullable=False)  # 10 (para 10%) ou 50 (para R$ 50)

    # Condições
    valor_minimo = db.Column(db.Float, default=0)  # Valor mínimo do carrinho para usar
    quantidade_maxima = db.Column(db.Integer, nullable=True)  # Máximo de usos (None = ilimitado)
    quantidade_usada = db.Column(db.Integer, default=0)  # Quantas vezes foi usado

    # Validade
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime, nullable=True)  # None = sem data de expiração

    # Status
    ativo = db.Column(db.Boolean, default=True)

    # Auditoria
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Cupom {self.codigo}>'

    def is_valido(self):
        """Verifica se o cupom está válido para uso"""
        if not self.ativo:
            return False, "Cupom inativo"

        # Verificar data de início
        if self.data_inicio and datetime.utcnow() < self.data_inicio:
            return False, "Cupom ainda não está disponível"

        # Verificar data de expiração
        if self.data_fim and datetime.utcnow() > self.data_fim:
            return False, "Cupom expirado"

        # Verificar quantidade máxima
        if self.quantidade_maxima and self.quantidade_usada >= self.quantidade_maxima:
            return False, "Cupom esgotado"

        return True, "Cupom válido"

    def calcular_desconto(self, valor_carrinho):
        """Calcula o valor do desconto para um determinado valor de carrinho"""
        valido, mensagem = self.is_valido()
        if not valido:
            return 0, mensagem

        # Verificar valor mínimo
        if valor_carrinho < self.valor_minimo:
            return 0, f"Valor mínimo do carrinho deve ser R$ {self.valor_minimo:.2f}"

        # Calcular desconto
        if self.tipo_desconto == 'percentual':
            desconto = valor_carrinho * (self.valor_desconto / 100)
        else:  # fixo
            desconto = self.valor_desconto

        # Desconto não pode ser maior que o valor do carrinho
        desconto = min(desconto, valor_carrinho)

        return desconto, "Desconto aplicado com sucesso!"

    def usar(self):
        """Incrementa o contador de uso do cupom"""
        self.quantidade_usada += 1
        db.session.commit()

    def to_dict(self):
        """Converte o cupom para dicionário"""
        return {
            'id': self.id,
            'codigo': self.codigo,
            'descricao': self.descricao,
            'tipo_desconto': self.tipo_desconto,
            'valor_desconto': self.valor_desconto,
            'valor_minimo': self.valor_minimo,
            'quantidade_maxima': self.quantidade_maxima,
            'quantidade_usada': self.quantidade_usada,
            'ativo': self.ativo,
            'valido': self.is_valido()[0]
        }


class ConteudoPagina(db.Model):
    """Modelo para conteúdo editável das páginas (CMS)"""
    __tablename__ = 'conteudo_pagina'

    id = db.Column(db.Integer, primary_key=True)
    pagina = db.Column(db.String(50), nullable=False)  # 'home', 'about', 'contact', 'footer'
    secao = db.Column(db.String(100), nullable=False)  # Ex: 'hero_titulo', 'sobre_texto', etc.
    tipo = db.Column(db.String(20), default='texto')  # 'texto', 'imagem', 'html'
    conteudo = db.Column(db.Text, nullable=True)  # Conteúdo textual
    imagem = db.Column(db.String(200), nullable=True)  # Nome do arquivo de imagem
    ordem = db.Column(db.Integer, default=0)  # Para ordenação
    ativo = db.Column(db.Boolean, default=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ConteudoPagina {self.pagina}.{self.secao}>'

    @staticmethod
    def get_conteudo(pagina, secao, default=None):
        """Obtém conteúdo de uma seção específica"""
        item = ConteudoPagina.query.filter_by(
            pagina=pagina,
            secao=secao,
            ativo=True
        ).first()

        if item:
            return item.imagem if item.tipo == 'imagem' else item.conteudo
        return default

    @staticmethod
    def set_conteudo(pagina, secao, conteudo=None, imagem=None, tipo='texto'):
        """Define ou atualiza conteúdo de uma seção"""
        item = ConteudoPagina.query.filter_by(pagina=pagina, secao=secao).first()

        if item:
            if conteudo is not None:
                item.conteudo = conteudo
            if imagem is not None:
                item.imagem = imagem
            item.tipo = tipo
        else:
            item = ConteudoPagina(
                pagina=pagina,
                secao=secao,
                conteudo=conteudo,
                imagem=imagem,
                tipo=tipo
            )
            db.session.add(item)

        db.session.commit()
        return item

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'pagina': self.pagina,
            'secao': self.secao,
            'tipo': self.tipo,
            'conteudo': self.conteudo,
            'imagem': self.imagem,
            'ordem': self.ordem,
            'ativo': self.ativo
        }
