"""
Rotas do painel administrativo
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from functools import wraps
import os
from pathlib import Path
from database import db
from models import Produto, Admin, Configuracao
from config import Config
import json

# Criar Blueprint para rotas do admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator para proteger rotas (só admin logado acessa)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# Função auxiliar para upload de imagens
def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_product_image(file):
    """Salva imagem do produto e retorna o nome do arquivo"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Adicionar timestamp para evitar conflitos
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        filepath = Config.UPLOAD_FOLDER / filename
        file.save(filepath)
        return filename
    return None

# ========================================
# ROTAS DE AUTENTICAÇÃO
# ========================================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login do admin"""
    # Se já estiver logado, redireciona para dashboard
    if 'admin_logged_in' in session:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Buscar admin no banco
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            # Login bem-sucedido
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            
            # Atualizar último login
            from datetime import datetime
            admin.ultimo_login = datetime.utcnow()
            db.session.commit()
            
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Logout do admin"""
    session.clear()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('admin.login'))

# ========================================
# DASHBOARD
# ========================================

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do admin"""
    # Estatísticas
    total_produtos = Produto.query.count()
    produtos_ativos = Produto.query.filter_by(ativo=True).count()
    produtos_inativos = Produto.query.filter_by(ativo=False).count()
    
    # Produtos por categoria
    categorias = {}
    for categoria in Config.CATEGORIES:
        count = Produto.query.filter_by(categoria=categoria).count()
        categorias[categoria] = count
    
    # Últimos produtos adicionados
    ultimos_produtos = Produto.query.order_by(Produto.data_criacao.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_produtos=total_produtos,
                         produtos_ativos=produtos_ativos,
                         produtos_inativos=produtos_inativos,
                         categorias=categorias,
                         ultimos_produtos=ultimos_produtos)

# ========================================
# GERENCIAR PRODUTOS
# ========================================

@admin_bp.route('/produtos')
@login_required
def produtos():
    """Lista todos os produtos"""
    produtos = Produto.query.order_by(Produto.ordem, Produto.id.desc()).all()
    return render_template('admin/produtos.html', produtos=produtos)

@admin_bp.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def produto_novo():
    """Adicionar novo produto"""
    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        categoria = request.form.get('categoria')
        tamanhos = request.form.getlist('tamanhos')
        ativo = request.form.get('ativo') == 'on'
        ordem = int(request.form.get('ordem', 0))
        
        # Upload de imagem
        imagem_file = request.files.get('imagem')
        imagem_filename = save_product_image(imagem_file) if imagem_file else None
        
        # Criar produto
        produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            tamanhos=json.dumps(tamanhos),
            imagem=imagem_filename,
            ativo=ativo,
            ordem=ordem
        )
        
        db.session.add(produto)
        db.session.commit()
        
        flash(f'Produto "{nome}" adicionado com sucesso!', 'success')
        return redirect(url_for('admin.produtos'))
    
    return render_template('admin/produto_form.html',
                         categorias=Config.CATEGORIES,
                         tamanhos_disponiveis=Config.SIZES,
                         produto=None)

@admin_bp.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
@login_required
def produto_editar(produto_id):
    """Editar produto existente"""
    produto = Produto.query.get_or_404(produto_id)
    
    if request.method == 'POST':
        # Atualizar dados
        produto.nome = request.form.get('nome')
        produto.descricao = request.form.get('descricao')
        produto.preco = float(request.form.get('preco'))
        produto.categoria = request.form.get('categoria')
        produto.tamanhos = json.dumps(request.form.getlist('tamanhos'))
        produto.ativo = request.form.get('ativo') == 'on'
        produto.ordem = int(request.form.get('ordem', 0))
        
        # Upload de nova imagem (opcional)
        imagem_file = request.files.get('imagem')
        if imagem_file and imagem_file.filename:
            # Deletar imagem antiga se existir
            if produto.imagem:
                old_image_path = Config.UPLOAD_FOLDER / produto.imagem
                if old_image_path.exists():
                    old_image_path.unlink()
            
            # Salvar nova imagem
            produto.imagem = save_product_image(imagem_file)
        
        db.session.commit()
        
        flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.produtos'))
    
    # Converter tamanhos de JSON para lista
    tamanhos_produto = json.loads(produto.tamanhos) if produto.tamanhos else []
    
    return render_template('admin/produto_form.html',
                         categorias=Config.CATEGORIES,
                         tamanhos_disponiveis=Config.SIZES,
                         produto=produto,
                         tamanhos_produto=tamanhos_produto)

@admin_bp.route('/produtos/<int:produto_id>/deletar', methods=['POST'])
@login_required
def produto_deletar(produto_id):
    """Deletar produto"""
    produto = Produto.query.get_or_404(produto_id)
    nome = produto.nome
    
    # Deletar imagem se existir
    if produto.imagem:
        image_path = Config.UPLOAD_FOLDER / produto.imagem
        if image_path.exists():
            image_path.unlink()
    
    db.session.delete(produto)
    db.session.commit()
    
    flash(f'Produto "{nome}" deletado com sucesso!', 'success')
    return redirect(url_for('admin.produtos'))

# ========================================
# CONFIGURAÇÕES
# ========================================

@admin_bp.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    """Configurações da loja"""
    if request.method == 'POST':
        # Atualizar configurações
        configs = [
            'loja_nome',
            'loja_telefone',
            'loja_email',
            'loja_instagram',
            'loja_endereco'
        ]
        
        for config_key in configs:
            valor = request.form.get(config_key)
            if valor:
                Configuracao.set_valor(config_key, valor)
        
        flash('Configurações atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.configuracoes'))
    
    # Buscar configurações atuais
    configs = {
        'loja_nome': Configuracao.get_valor('loja_nome', 'Xodó da Preta'),
        'loja_telefone': Configuracao.get_valor('loja_telefone', ''),
        'loja_email': Configuracao.get_valor('loja_email', ''),
        'loja_instagram': Configuracao.get_valor('loja_instagram', ''),
        'loja_endereco': Configuracao.get_valor('loja_endereco', '')
    }
    
    return render_template('admin/config.html', configs=configs)