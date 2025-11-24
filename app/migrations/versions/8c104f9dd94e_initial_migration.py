"""Initial migration

Revision ID: 8c104f9dd94e
Revises: 
Create Date: 2025-11-17 19:39:57.997312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c104f9dd94e'
down_revision = None
branch_labels = None
depends_on = None


def _has_table(insp, name):
    return name in insp.get_table_names()


def _ensure_index(insp, name, table, columns, unique=False):
    if not _has_table(insp, table):
        return
    existing = {ix['name'] for ix in insp.get_indexes(table)}
    if name not in existing:
        op.create_index(name, table, columns, unique=unique)


def upgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # subcategorias
    if not _has_table(insp, 'subcategorias'):
        op.create_table(
            'subcategorias',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('nome', sa.String(length=50), nullable=False),
            sa.Column('categoria', sa.String(length=50), nullable=False),
            sa.Column('parent_id', sa.Integer(), sa.ForeignKey('subcategorias.id', ondelete='CASCADE'), nullable=True),
            sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('1')),
            sa.Column('ordem', sa.Integer(), nullable=False, server_default=sa.text('0')),
            sa.Column('data_criacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        )
    insp = sa.inspect(bind)
    _ensure_index(insp, 'ix_subcategorias_categoria', 'subcategorias', ['categoria'])

    # produtos
    if not _has_table(insp, 'produtos'):
        op.create_table(
            'produtos',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('nome', sa.String(length=100), nullable=False),
            sa.Column('descricao', sa.Text(), nullable=True),
            sa.Column('preco', sa.Float(), nullable=False),
            sa.Column('categoria', sa.String(length=50), nullable=False),
            sa.Column('subcategoria', sa.String(length=50), nullable=True),
            sa.Column('tipo', sa.String(length=50), nullable=True),
            sa.Column('subcategoria_id', sa.Integer(), sa.ForeignKey('subcategorias.id', ondelete='SET NULL'), nullable=True),
            sa.Column('tamanhos', sa.String(length=200), nullable=True),
            sa.Column('imagem', sa.String(length=200), nullable=True),
            sa.Column('imagens_adicionais', sa.Text(), nullable=True),
            sa.Column('ordem', sa.Integer(), nullable=False, server_default=sa.text('0')),
            sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('1')),
            sa.Column('destaque', sa.Boolean(), nullable=False, server_default=sa.text('0')),
            sa.Column('visualizacoes', sa.Integer(), nullable=False, server_default=sa.text('0')),
            sa.Column('data_criacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.Column('data_atualizacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        )
    insp = sa.inspect(bind)
    _ensure_index(insp, 'ix_produtos_nome', 'produtos', ['nome'])
    _ensure_index(insp, 'ix_produtos_categoria', 'produtos', ['categoria'])
    _ensure_index(insp, 'ix_produtos_subcategoria_id', 'produtos', ['subcategoria_id'])

    # admins
    if not _has_table(insp, 'admins'):
        op.create_table(
            'admins',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('username', sa.String(length=80), nullable=False, unique=True),
            sa.Column('password_hash', sa.String(length=200), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=True, unique=True),
            sa.Column('data_criacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.Column('ultimo_login', sa.DateTime(), nullable=True),
        )

    # configuracoes
    if not _has_table(insp, 'configuracoes'):
        op.create_table(
            'configuracoes',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('chave', sa.String(length=50), nullable=False, unique=True),
            sa.Column('valor', sa.Text(), nullable=True),
            sa.Column('descricao', sa.String(length=200), nullable=True),
            sa.Column('data_atualizacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        )

    # itens_carrinho
    if not _has_table(insp, 'itens_carrinho'):
        op.create_table(
            'itens_carrinho',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('session_id', sa.String(length=100), nullable=False),
            sa.Column('produto_id', sa.Integer(), sa.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False),
            sa.Column('quantidade', sa.Integer(), nullable=False, server_default=sa.text('1')),
            sa.Column('tamanho', sa.String(length=10), nullable=True),
            sa.Column('data_adicao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        )
    insp = sa.inspect(bind)
    _ensure_index(insp, 'ix_itens_carrinho_session_id', 'itens_carrinho', ['session_id'])
    _ensure_index(insp, 'ix_itens_carrinho_produto_id', 'itens_carrinho', ['produto_id'])

    # produto_visualizacoes
    if not _has_table(insp, 'produto_visualizacoes'):
        op.create_table(
            'produto_visualizacoes',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('produto_id', sa.Integer(), sa.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False),
            sa.Column('data_visualizacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        )
    insp = sa.inspect(bind)
    _ensure_index(insp, 'idx_produto_data', 'produto_visualizacoes', ['produto_id', 'data_visualizacao'])
    _ensure_index(insp, 'ix_produto_visualizacoes_produto_id', 'produto_visualizacoes', ['produto_id'])
    _ensure_index(insp, 'ix_produto_visualizacoes_data_visualizacao', 'produto_visualizacoes', ['data_visualizacao'])

    # cupons
    if not _has_table(insp, 'cupons'):
        op.create_table(
            'cupons',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('codigo', sa.String(length=50), nullable=False, unique=True),
            sa.Column('descricao', sa.String(length=200), nullable=True),
            sa.Column('tipo_desconto', sa.String(length=20), nullable=False, server_default=sa.text("'percentual'")),
            sa.Column('valor_desconto', sa.Float(), nullable=False),
            sa.Column('valor_minimo', sa.Float(), nullable=False, server_default=sa.text('0')),
            sa.Column('quantidade_maxima', sa.Integer(), nullable=True),
            sa.Column('quantidade_usada', sa.Integer(), nullable=False, server_default=sa.text('0')),
            sa.Column('data_inicio', sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.Column('data_fim', sa.DateTime(), nullable=True),
            sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('1')),
            sa.Column('data_criacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.Column('data_atualizacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        )

    # conteudo_pagina
    if not _has_table(insp, 'conteudo_pagina'):
        op.create_table(
            'conteudo_pagina',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('pagina', sa.String(length=50), nullable=False),
            sa.Column('secao', sa.String(length=100), nullable=False),
            sa.Column('tipo', sa.String(length=20), nullable=False, server_default=sa.text("'texto'")),
            sa.Column('conteudo', sa.Text(), nullable=True),
            sa.Column('imagem', sa.String(length=200), nullable=True),
            sa.Column('ordem', sa.Integer(), nullable=False, server_default=sa.text('0')),
            sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('1')),
            sa.Column('data_atualizacao', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        )


def downgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    for table in [
        'conteudo_pagina',
        'cupons',
        'produto_visualizacoes',
        'itens_carrinho',
        'configuracoes',
        'admins',
        'produtos',
        'subcategorias',
    ]:
        if _has_table(insp, table):
            op.drop_table(table)
