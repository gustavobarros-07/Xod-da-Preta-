from flask import Flask, render_template, request
from pathlib import Path
from config import Config
from database import db, init_db
from admin_routes import admin_bp

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
    db.create_all()

# Registrar Blueprint do Admin
app.register_blueprint(admin_bp)

# ========================================
# ROTAS DO SITE
# ========================================

@app.route("/")
def home():
    """Página inicial"""
    return render_template("index.html")

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
    """Página da loja com filtros"""
    from models import Produto
    
    # Filtros da URL
    categoria_filtro = request.args.get('categoria')
    preco_filtro = request.args.get('preco')
    
    # Query base: produtos ativos
    query = Produto.query.filter_by(ativo=True)
    
    # Aplicar filtro de categoria
    if categoria_filtro:
        query = query.filter_by(categoria=categoria_filtro)
    
    # Aplicar filtro de preço
    if preco_filtro:
        if preco_filtro == '0-50':
            query = query.filter(Produto.preco <= 50)
        elif preco_filtro == '50-100':
            query = query.filter(Produto.preco > 50, Produto.preco <= 100)
        elif preco_filtro == '100-200':
            query = query.filter(Produto.preco > 100, Produto.preco <= 200)
        elif preco_filtro == '200+':
            query = query.filter(Produto.preco > 200)
    
    # Ordenar e buscar
    produtos = query.order_by(Produto.ordem).all()
    
    return render_template("shop.html", produtos=produtos)

@app.route("/shop/<int:produto_id>")
def shop_single(produto_id):
    """Página de produto individual"""
    from models import Produto
    
    # Buscar produto pelo ID
    produto = Produto.query.get_or_404(produto_id)
    
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
# EXECUTAR APLICAÇÃO
# ========================================

if __name__ == "__main__":
    app.run(debug=True) 