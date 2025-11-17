from flask import Flask, render_template, request, session, jsonify
from pathlib import Path
from config import Config
from database import db
from admin_routes import admin_bp
import uuid

# Diretório base
BASE_DIR = Path(__file__).resolve().parent

# Criar aplicação Flask
app = Flask(
    __name__, 
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

# Carregar configurações
app.config.from_object(Config)
Config.init_app(app)

# Inicializar banco de dados
db.init_app(app)

# Criar tabelas se não existirem
with app.app_context():
    # Importar modelos para garantir que sejam registrados
    from models import Produto, Admin, Configuracao, Subcategoria, ConteudoPagina
    db.create_all()

# Registrar Blueprint do Admin
app.register_blueprint(admin_bp)

# ========================================
# CONTEXT PROCESSOR - Configurações globais
# ========================================

@app.context_processor
def inject_configuracoes():
    """Injeta configurações da loja em todos os templates"""
    from models import Configuracao

    return {
        'config_loja_nome': Configuracao.get_valor('loja_nome', 'Xodó da Preta'),
        'config_loja_telefone': Configuracao.get_valor('loja_telefone', '55 11 95437-5056'),
        'config_loja_email': Configuracao.get_valor('loja_email', ''),
        'config_loja_instagram': Configuracao.get_valor('loja_instagram', '@xododapreta'),
        'config_loja_facebook': Configuracao.get_valor('loja_facebook', ''),
        'config_loja_endereco': Configuracao.get_valor('loja_endereco', 'São Paulo, SP'),
        'config_topbar_ativo': Configuracao.get_valor('topbar_ativo', '1') == '1',
    }

# ========================================
# ROTAS DO SITE
# ========================================

@app.route("/")
def home():
    """Página inicial"""
    from models import Produto

    # Buscar produtos em destaque (máximo 4)
    produtos_destaque = Produto.query.filter_by(
        ativo=True,
        destaque=True
    ).order_by(Produto.ordem).limit(4).all()

    return render_template("index.html", produtos_destaque=produtos_destaque)

@app.route("/about")
def about():
    """Página sobre"""
    return render_template("about.html")

@app.route("/contact")
def contact():
    """Página de contato"""
    return render_template("contact.html")

@app.route("/shop")
def shop():
    """Página da loja com filtros hierárquicos (3 níveis)"""
    from models import Produto, Subcategoria
    from config import Config

    # Filtros da URL (3 níveis)
    categoria_filtro = request.args.get('categoria')  # Nível 1: Roupas, Brincos, etc.
    subcategoria_filtro = request.args.get('subcategoria')  # Nível 2: Feminino, Masculino
    tipo_filtro = request.args.get('tipo')  # Nível 3: Vestido, Camisa, etc.
    preco_filtro = request.args.get('preco')
    preco_min = request.args.get('preco_min', type=int)
    preco_max = request.args.get('preco_max', type=int)
    ordenar = request.args.get('ordenar', 'padrao')  # Ordenação

    # Query base: produtos ativos
    query = Produto.query.filter_by(ativo=True)

    # Aplicar filtro de categoria (Nível 1)
    if categoria_filtro:
        query = query.filter_by(categoria=categoria_filtro)

    # Aplicar filtro de subcategoria (Nível 2 - Feminino/Masculino)
    if subcategoria_filtro:
        query = query.filter_by(subcategoria=subcategoria_filtro)

    # Aplicar filtro de tipo (Nível 3 - Vestido/Camisa/etc.)
    if tipo_filtro:
        query = query.filter_by(tipo=tipo_filtro)

    # Aplicar filtro de preço por faixas rápidas
    if preco_filtro:
        if preco_filtro == '0-50':
            query = query.filter(Produto.preco <= 50)
        elif preco_filtro == '50-100':
            query = query.filter(Produto.preco > 50, Produto.preco <= 100)
        elif preco_filtro == '100-200':
            query = query.filter(Produto.preco > 100, Produto.preco <= 200)
        elif preco_filtro == '100+':
            query = query.filter(Produto.preco > 100)
        elif preco_filtro == '200+':
            query = query.filter(Produto.preco > 200)

    # Aplicar filtro de preço customizado (slider)
    if preco_min is not None and preco_max is not None:
        query = query.filter(Produto.preco >= preco_min, Produto.preco <= preco_max)

    # Aplicar ordenação
    if ordenar == 'preco_asc':
        query = query.order_by(Produto.preco.asc())
    elif ordenar == 'preco_desc':
        query = query.order_by(Produto.preco.desc())
    elif ordenar == 'nome':
        query = query.order_by(Produto.nome.asc())
    elif ordenar == 'recentes':
        query = query.order_by(Produto.data_criacao.desc())
    elif ordenar == 'visualizacoes':
        query = query.order_by(Produto.visualizacoes.desc())
    else:  # padrao
        query = query.order_by(Produto.ordem, Produto.id.desc())

    # Buscar produtos
    produtos = query.all()

    # Buscar subcategorias antigas (legado - manter compatibilidade)
    subcategorias_legado = Subcategoria.query.filter_by(ativo=True).order_by(Subcategoria.categoria, Subcategoria.ordem).all()

    return render_template(
        "shop.html",
        produtos=produtos,
        categoria_filtro=categoria_filtro,
        subcategoria_filtro=subcategoria_filtro,
        tipo_filtro=tipo_filtro,
        preco_filtro=preco_filtro,
        subcategorias=subcategorias_legado,  # Legado
        hierarchy=Config.CATEGORY_HIERARCHY
    )

@app.route("/shop/<int:produto_id>")
def shop_single(produto_id):
    """Página de produto individual"""
    from models import Produto, ProdutoVisualizacao

    # Buscar produto pelo ID
    produto = Produto.query.get_or_404(produto_id)

    # Registrar visualização (analytics)
    visualizacao = ProdutoVisualizacao()
    visualizacao.produto_id = produto_id
    db.session.add(visualizacao)

    # Incrementar contador de visualizações
    produto.visualizacoes += 1
    db.session.commit()

    # Buscar produtos relacionados (mesma categoria)
    produtos_relacionados = Produto.query.filter(
        Produto.categoria == produto.categoria,
        Produto.id != produto.id,
        Produto.ativo == True
    ).limit(4).all()

    return render_template(
        "shop-single.html",
        produto=produto,
        produtos_relacionados=produtos_relacionados
    )

# ========================================
# ROTAS DO CARRINHO
# ========================================

def get_session_id():
    """Obtém ou cria um ID de sessão único para o carrinho"""
    if 'cart_session_id' not in session:
        session['cart_session_id'] = str(uuid.uuid4())
    return session['cart_session_id']

@app.route("/carrinho")
def carrinho():
    """Página do carrinho de compras"""
    from models import ItemCarrinho

    session_id = get_session_id()
    itens = ItemCarrinho.query.filter_by(session_id=session_id).all()

    # Calcular total
    total = sum(item.produto.preco * item.quantidade for item in itens)

    return render_template("carrinho.html", itens=itens, total=total)

@app.route("/api/carrinho/adicionar", methods=['POST'])
def adicionar_ao_carrinho():
    """Adiciona um produto ao carrinho"""
    from models import ItemCarrinho, Produto

    try:
        data = request.get_json()
        produto_id = data.get('produto_id')
        quantidade = data.get('quantidade', 1)
        tamanho = data.get('tamanho')

        if not produto_id:
            return jsonify({'success': False, 'message': 'Produto não especificado'}), 400

        # Verificar se o produto existe
        produto = Produto.query.get(produto_id)
        if not produto or not produto.ativo:
            return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404

        session_id = get_session_id()

        # Verificar se o item já existe no carrinho
        item_existente = ItemCarrinho.query.filter_by(
            session_id=session_id,
            produto_id=produto_id,
            tamanho=tamanho
        ).first()

        if item_existente:
            # Atualizar quantidade
            item_existente.quantidade += quantidade
        else:
            # Criar novo item
            novo_item = ItemCarrinho(
                session_id=session_id,
                produto_id=produto_id,
                quantidade=quantidade,
                tamanho=tamanho
            )
            db.session.add(novo_item)

        db.session.commit()

        # Contar total de itens no carrinho
        total_itens = db.session.query(db.func.sum(ItemCarrinho.quantidade)).filter_by(
            session_id=session_id
        ).scalar() or 0

        return jsonify({
            'success': True,
            'message': 'Produto adicionado ao carrinho',
            'total_itens': total_itens
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/api/carrinho/remover/<int:item_id>", methods=['DELETE'])
def remover_do_carrinho(item_id):
    """Remove um item do carrinho"""
    from models import ItemCarrinho

    try:
        session_id = get_session_id()
        item = ItemCarrinho.query.filter_by(id=item_id, session_id=session_id).first()

        if not item:
            return jsonify({'success': False, 'message': 'Item não encontrado'}), 404

        db.session.delete(item)
        db.session.commit()

        # Contar total de itens no carrinho
        total_itens = db.session.query(db.func.sum(ItemCarrinho.quantidade)).filter_by(
            session_id=session_id
        ).scalar() or 0

        return jsonify({
            'success': True,
            'message': 'Item removido do carrinho',
            'total_itens': total_itens
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/api/carrinho/atualizar/<int:item_id>", methods=['PUT'])
def atualizar_carrinho(item_id):
    """Atualiza a quantidade de um item no carrinho"""
    from models import ItemCarrinho

    try:
        data = request.get_json()
        quantidade = data.get('quantidade', 1)

        if quantidade < 1:
            return jsonify({'success': False, 'message': 'Quantidade inválida'}), 400

        session_id = get_session_id()
        item = ItemCarrinho.query.filter_by(id=item_id, session_id=session_id).first()

        if not item:
            return jsonify({'success': False, 'message': 'Item não encontrado'}), 404

        item.quantidade = quantidade
        db.session.commit()

        # Contar total de itens no carrinho
        total_itens = db.session.query(db.func.sum(ItemCarrinho.quantidade)).filter_by(
            session_id=session_id
        ).scalar() or 0

        subtotal = item.produto.preco * item.quantidade

        return jsonify({
            'success': True,
            'message': 'Carrinho atualizado',
            'subtotal': subtotal,
            'total_itens': total_itens
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/api/carrinho/total")
def carrinho_total():
    """Retorna o total de itens no carrinho"""
    from models import ItemCarrinho

    session_id = get_session_id()
    total_itens = db.session.query(db.func.sum(ItemCarrinho.quantidade)).filter_by(
        session_id=session_id
    ).scalar() or 0

    return jsonify({'total_itens': total_itens})

# ========================================
# CUPONS
# ========================================

@app.route("/api/cupom/validar", methods=['POST'])
def validar_cupom():
    """Valida um cupom de desconto"""
    from models import Cupom

    try:
        data = request.get_json()
        codigo = data.get('codigo', '').upper().strip()
        valor_carrinho = float(data.get('valor_carrinho', 0))

        if not codigo:
            return jsonify({'success': False, 'message': 'Código do cupom não informado'}), 400

        # Buscar cupom
        cupom = Cupom.query.filter_by(codigo=codigo).first()

        if not cupom:
            return jsonify({'success': False, 'message': f'Cupom "{codigo}" não encontrado. Verifique o código e tente novamente.'}), 404

        # Validar cupom
        valido, mensagem = cupom.is_valido()
        if not valido:
            return jsonify({'success': False, 'message': mensagem}), 400

        # Verificar valor mínimo
        if cupom.valor_minimo and valor_carrinho < cupom.valor_minimo:
            return jsonify({
                'success': False,
                'message': f'Valor mínimo do carrinho: R$ {cupom.valor_minimo:.2f}'
            }), 400

        # Calcular desconto
        valor_desconto, mensagem_desconto = cupom.calcular_desconto(valor_carrinho)

        if valor_desconto == 0:
            return jsonify({
                'success': False,
                'message': mensagem_desconto
            }), 400

        return jsonify({
            'success': True,
            'cupom': {
                'id': cupom.id,
                'codigo': cupom.codigo,
                'tipo_desconto': cupom.tipo_desconto,
                'valor_desconto': cupom.valor_desconto
            },
            'valor_desconto': valor_desconto,
            'message': 'Cupom aplicado com sucesso!'
        })

    except Exception as e:
        print(f"Erro ao validar cupom: {e}")
        return jsonify({'success': False, 'message': 'Erro ao validar cupom'}), 500

# ========================================
# BUSCA
# ========================================

@app.route("/busca")
def busca():
    """Busca de produtos"""
    from models import Produto

    # Termo de busca
    termo = request.args.get('q', '').strip()

    if not termo:
        return render_template("busca.html", produtos=[], termo='')

    # Buscar produtos por nome ou descrição
    produtos = Produto.query.filter(
        Produto.ativo == True,
        db.or_(
            Produto.nome.ilike(f'%{termo}%'),
            Produto.descricao.ilike(f'%{termo}%'),
            Produto.categoria.ilike(f'%{termo}%')
        )
    ).order_by(Produto.ordem).all()

    return render_template("busca.html", produtos=produtos, termo=termo)

# ========================================
# FILTROS JINJA2 PERSONALIZADOS
# ========================================

@app.template_filter('currency')
def currency_filter(value):
    """Formata valor como moeda brasileira"""
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ 0,00"

@app.template_filter('from_json')
def from_json_filter(value):
    """Converte string JSON para lista Python"""
    import json
    try:
        return json.loads(value) if value else []
    except (ValueError, TypeError):
        return []

# ========================================
# CONTEXTO GLOBAL (disponível em todos os templates)
# ========================================

@app.context_processor
def inject_global_vars():
    """Injeta variáveis globais em todos os templates"""
    from models import Configuracao
    
    return {
        'loja_nome': Configuracao.get_valor('loja_nome', 'Xodó da Preta'),
        'loja_telefone': Configuracao.get_valor('loja_telefone', '55 11 954375056'),
        'loja_email': Configuracao.get_valor('loja_email', 'contato@xododapreta.com'),
        'loja_instagram': Configuracao.get_valor('loja_instagram', '@xododapreta'),
    }

# ========================================
# ROTA DE CSS DINÂMICO (CORES PERSONALIZÁVEIS)
# ========================================

@app.route('/static/css/custom-colors.css')
def custom_colors_css():
    """Gera CSS dinâmico com cores personalizadas do painel admin"""
    from models import Configuracao
    from flask import Response

    # Buscar cores do banco
    cor_primaria = Configuracao.get_valor('cor_primaria', '#ffc107')
    cor_secundaria = Configuracao.get_valor('cor_secundaria', '#000000')
    cor_destaque = Configuracao.get_valor('cor_destaque', '#ff9800')

    # Gerar CSS dinâmico
    css_content = f"""
/* ========================================
   CORES PERSONALIZADAS - XODÓ DA PRETA
   Gerado automaticamente pelo painel admin
   ======================================== */

:root {{
    --cor-dourada: {cor_primaria};
    --cor-preta: {cor_secundaria};
    --cor-laranja: {cor_destaque};
    --cor-hover: {cor_destaque};
    --cor-sucesso: {cor_primaria};
}}

/* Aplicar cores personalizadas */
.btn-success {{
    background-color: {cor_primaria} !important;
    border-color: {cor_primaria} !important;
}}

.btn-success:hover {{
    background-color: {cor_destaque} !important;
    border-color: {cor_destaque} !important;
}}

.text-success,
.text-warning {{
    color: {cor_primaria} !important;
}}

.bg-success,
.bg-warning {{
    background-color: {cor_primaria} !important;
}}

#templatemo_nav_top {{
    background-color: {cor_secundaria} !important;
}}

#templatemo_nav_top a {{
    color: {cor_primaria} !important;
}}

#templatemo_main_nav a:hover {{
    color: {cor_primaria} !important;
}}

.navbar-brand {{
    color: {cor_secundaria} !important;
}}

.product-price {{
    color: {cor_primaria} !important;
}}

.badge.bg-warning {{
    background-color: {cor_destaque} !important;
}}

.input-group-text.bg-warning {{
    background-color: {cor_primaria} !important;
}}

#tempaltemo_footer {{
    background-color: {cor_secundaria} !important;
}}

#tempaltemo_footer h2 {{
    color: {cor_primaria} !important;
    border-bottom-color: {cor_primaria} !important;
}}

#tempaltemo_footer a:hover {{
    color: {cor_primaria} !important;
}}

.form-control:focus {{
    border-color: {cor_primaria};
    box-shadow: 0 0 0 0.2rem rgba(255, 193, 7, 0.25);
}}
"""

    return Response(css_content, mimetype='text/css')

# ========================================
# EXECUTAR APLICAÇÃO
# ========================================

if __name__ == "__main__":
    app.run(debug=True) 