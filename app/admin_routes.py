"""
Rotas do painel administrativo
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta
import os
import json
import zipfile
from pathlib import Path
from database import db
from models import Produto, Admin, Configuracao, Subcategoria, Cupom
from config import Config

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
    """Dashboard principal do admin com métricas avançadas"""
    from models import ProdutoVisualizacao

    # ===== ESTATÍSTICAS BÁSICAS =====
    total_produtos = Produto.query.count()
    produtos_ativos = Produto.query.filter_by(ativo=True).count()
    produtos_inativos = Produto.query.filter_by(ativo=False).count()
    produtos_sem_imagem = Produto.query.filter(
        (Produto.imagem == None) | (Produto.imagem == '')
    ).count()
    produtos_destaque = Produto.query.filter_by(destaque=True).count()

    # ===== ANÁLISE DE PREÇOS =====
    produto_mais_caro = Produto.query.order_by(Produto.preco.desc()).first()
    produto_mais_barato = Produto.query.filter(Produto.preco > 0).order_by(Produto.preco.asc()).first()
    preco_medio = db.session.query(db.func.avg(Produto.preco)).scalar() or 0

    # ===== PRODUTOS POR CATEGORIA (para gráfico de pizza) =====
    categorias_stats = db.session.query(
        Produto.categoria,
        db.func.count(Produto.id).label('total')
    ).group_by(Produto.categoria).all()

    # Formatar para Chart.js
    categorias_labels = [cat for cat, _ in categorias_stats]
    categorias_valores = [total for _, total in categorias_stats]

    # ===== PRODUTOS MAIS VISUALIZADOS (Top 10) =====
    produtos_mais_vistos = Produto.query.filter(
        Produto.visualizacoes > 0
    ).order_by(Produto.visualizacoes.desc()).limit(10).all()

    # ===== VISUALIZAÇÕES POR DIA (últimos 30 dias) =====
    trinta_dias_atras = datetime.utcnow() - timedelta(days=30)
    visualizacoes_por_dia = db.session.query(
        db.func.date(ProdutoVisualizacao.data_visualizacao).label('dia'),
        db.func.count(ProdutoVisualizacao.id).label('total')
    ).filter(
        ProdutoVisualizacao.data_visualizacao >= trinta_dias_atras
    ).group_by('dia').order_by('dia').all()

    # Formatar para Chart.js
    visualizacoes_labels = [dia.strftime('%d/%m') if hasattr(dia, 'strftime') else str(dia) for dia, _ in visualizacoes_por_dia]
    visualizacoes_valores = [total for _, total in visualizacoes_por_dia]

    # ===== ÚLTIMOS PRODUTOS ADICIONADOS =====
    ultimos_produtos = Produto.query.order_by(Produto.data_criacao.desc()).limit(5).all()

    # ===== TOTAL DE VISUALIZAÇÕES (últimos 30 dias) =====
    total_visualizacoes = db.session.query(
        db.func.count(ProdutoVisualizacao.id)
    ).filter(
        ProdutoVisualizacao.data_visualizacao >= trinta_dias_atras
    ).scalar() or 0

    # ===== ANALYTICS DE CUPONS =====
    total_cupons = Cupom.query.count()
    cupons_ativos = Cupom.query.filter_by(ativo=True).count()

    # Cupons mais usados (top 5)
    cupons_mais_usados = Cupom.query.filter(
        Cupom.quantidade_usada > 0
    ).order_by(Cupom.quantidade_usada.desc()).limit(5).all()

    # Total de descontos dados (estimativa)
    total_descontos_valor = 0
    for cupom in Cupom.query.filter(Cupom.quantidade_usada > 0).all():
        # Estimativa simples: quantidade_usada * valor médio de desconto
        if cupom.tipo_desconto == 'fixo':
            total_descontos_valor += cupom.valor_desconto * cupom.quantidade_usada
        else:
            # Para percentuais, usar preço médio como base de cálculo
            total_descontos_valor += (preco_medio * (cupom.valor_desconto / 100)) * cupom.quantidade_usada

    # ===== RANKING DE CATEGORIAS (por quantidade de produtos) =====
    categorias_ranking_raw = db.session.query(
        Produto.categoria,
        db.func.count(Produto.id).label('total'),
        db.func.sum(Produto.visualizacoes).label('views_total')
    ).group_by(Produto.categoria).order_by(db.text('total DESC')).all()

    # Converter Row objects para listas simples (JSON serializable)
    categorias_ranking = [[cat, total, views or 0] for cat, total, views in categorias_ranking_raw]

    return render_template('admin/dashboard.html',
                         # Estatísticas básicas
                         total_produtos=total_produtos,
                         produtos_ativos=produtos_ativos,
                         produtos_inativos=produtos_inativos,
                         produtos_sem_imagem=produtos_sem_imagem,
                         produtos_destaque=produtos_destaque,
                         # Análise de preços
                         produto_mais_caro=produto_mais_caro,
                         produto_mais_barato=produto_mais_barato,
                         preco_medio=preco_medio,
                         # Dados para gráficos
                         categorias_labels=categorias_labels,
                         categorias_valores=categorias_valores,
                         visualizacoes_labels=visualizacoes_labels,
                         visualizacoes_valores=visualizacoes_valores,
                         # Listas
                         produtos_mais_vistos=produtos_mais_vistos,
                         ultimos_produtos=ultimos_produtos,
                         # Analytics
                         total_visualizacoes=total_visualizacoes,
                         # Analytics de cupons
                         total_cupons=total_cupons,
                         cupons_ativos=cupons_ativos,
                         cupons_mais_usados=cupons_mais_usados,
                         total_descontos_valor=total_descontos_valor,
                         # Rankings
                         categorias_ranking=categorias_ranking)

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
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco_str = request.form.get('preco', '0')
        categoria = request.form.get('categoria', '').strip()
        subcategoria = request.form.get('subcategoria')  # Feminino/Masculino
        tipo = request.form.get('tipo')  # Vestido, Camisa, etc.
        subcategoria_id = request.form.get('subcategoria_id')  # Legado
        tamanhos = request.form.getlist('tamanhos')
        ativo = request.form.get('ativo') == 'on'
        destaque = request.form.get('destaque') == 'on'
        ordem_str = request.form.get('ordem', '0')

        # VALIDAÇÃO DE CAMPOS OBRIGATÓRIOS
        if not nome:
            flash('Nome do produto é obrigatório', 'danger')
            return redirect(url_for('admin.produto_novo'))

        if not categoria:
            flash('Categoria é obrigatória', 'danger')
            return redirect(url_for('admin.produto_novo'))

        # VALIDAÇÃO DE PREÇO
        try:
            preco = float(preco_str)
            if preco < 0:
                flash('Preço não pode ser negativo', 'danger')
                return redirect(url_for('admin.produto_novo'))
        except (ValueError, TypeError):
            flash('Preço inválido. Use apenas números (ex: 49.90)', 'danger')
            return redirect(url_for('admin.produto_novo'))

        # VALIDAÇÃO DE ORDEM
        try:
            ordem = int(ordem_str)
        except (ValueError, TypeError):
            ordem = 0

        # Upload de imagem principal
        imagem_file = request.files.get('imagem')
        imagem_filename = save_product_image(imagem_file) if imagem_file else None

        # Upload de imagens adicionais (galeria)
        imagens_adicionais_files = request.files.getlist('imagens_adicionais')
        imagens_adicionais_list = []
        for img_file in imagens_adicionais_files:
            if img_file and img_file.filename:
                filename = save_product_image(img_file)
                if filename:
                    imagens_adicionais_list.append(filename)

        # Criar produto
        produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            subcategoria=subcategoria if subcategoria else None,
            tipo=tipo if tipo else None,
            subcategoria_id=int(subcategoria_id) if subcategoria_id else None,
            tamanhos=json.dumps(tamanhos),
            imagem=imagem_filename,
            ativo=ativo,
            destaque=destaque,
            ordem=ordem
        )

        # Adicionar imagens adicionais ao produto
        if imagens_adicionais_list:
            produto.set_imagens_adicionais(imagens_adicionais_list)

        db.session.add(produto)
        db.session.commit()

        flash(f'Produto "{nome}" adicionado com sucesso!', 'success')
        return redirect(url_for('admin.produtos'))

    # Buscar todas as subcategorias para o formulário
    subcategorias = Subcategoria.query.filter_by(ativo=True).order_by(Subcategoria.categoria, Subcategoria.ordem).all()

    return render_template('admin/produto_form.html',
                         categorias=Config.CATEGORIES,
                         tamanhos_disponiveis=Config.SIZES,
                         subcategorias=subcategorias,
                         produto=None)

@admin_bp.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
@login_required
def produto_editar(produto_id):
    """Editar produto existente"""
    produto = Produto.query.get_or_404(produto_id)
    
    if request.method == 'POST':
        # Obter e validar dados
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco_str = request.form.get('preco', '0')
        categoria = request.form.get('categoria', '').strip()
        subcategoria = request.form.get('subcategoria') or None
        tipo = request.form.get('tipo') or None
        subcategoria_id = request.form.get('subcategoria_id')
        tamanhos = request.form.getlist('tamanhos')
        ativo = request.form.get('ativo') == 'on'
        destaque = request.form.get('destaque') == 'on'
        ordem_str = request.form.get('ordem', '0')

        # VALIDAÇÃO DE CAMPOS OBRIGATÓRIOS
        if not nome:
            flash('Nome do produto é obrigatório', 'danger')
            return redirect(url_for('admin.produto_editar', produto_id=produto_id))

        if not categoria:
            flash('Categoria é obrigatória', 'danger')
            return redirect(url_for('admin.produto_editar', produto_id=produto_id))

        # VALIDAÇÃO DE PREÇO
        try:
            preco = float(preco_str)
            if preco < 0:
                flash('Preço não pode ser negativo', 'danger')
                return redirect(url_for('admin.produto_editar', produto_id=produto_id))
        except (ValueError, TypeError):
            flash('Preço inválido. Use apenas números (ex: 49.90)', 'danger')
            return redirect(url_for('admin.produto_editar', produto_id=produto_id))

        # VALIDAÇÃO DE ORDEM
        try:
            ordem = int(ordem_str)
        except (ValueError, TypeError):
            ordem = 0

        # Atualizar dados do produto
        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco
        produto.categoria = categoria
        produto.subcategoria = subcategoria
        produto.tipo = tipo
        produto.subcategoria_id = int(subcategoria_id) if subcategoria_id else None
        produto.tamanhos = json.dumps(tamanhos)
        produto.ativo = ativo
        produto.destaque = destaque
        produto.ordem = ordem

        # Upload de nova imagem principal (opcional)
        imagem_file = request.files.get('imagem')
        if imagem_file and imagem_file.filename:
            # Deletar imagem antiga se existir
            if produto.imagem:
                old_image_path = Config.UPLOAD_FOLDER / produto.imagem
                if old_image_path.exists():
                    old_image_path.unlink()

            # Salvar nova imagem
            produto.imagem = save_product_image(imagem_file)

        # Upload de novas imagens adicionais (galeria) - opcional
        imagens_adicionais_files = request.files.getlist('imagens_adicionais')
        if imagens_adicionais_files and any(f.filename for f in imagens_adicionais_files):
            # Deletar imagens adicionais antigas se existir
            if produto.imagens_adicionais:
                try:
                    old_images = json.loads(produto.imagens_adicionais)
                    for old_img in old_images:
                        old_img_path = Config.UPLOAD_FOLDER / old_img
                        if old_img_path.exists():
                            old_img_path.unlink()
                except (json.JSONDecodeError, TypeError, OSError):
                    pass

            # Salvar novas imagens
            imagens_adicionais_list = []
            for img_file in imagens_adicionais_files:
                if img_file and img_file.filename:
                    filename = save_product_image(img_file)
                    if filename:
                        imagens_adicionais_list.append(filename)

            if imagens_adicionais_list:
                produto.set_imagens_adicionais(imagens_adicionais_list)
            else:
                produto.imagens_adicionais = None

        db.session.commit()

        flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.produtos'))

    # Converter tamanhos de JSON para lista
    tamanhos_produto = json.loads(produto.tamanhos) if produto.tamanhos else []

    # Buscar todas as subcategorias para o formulário
    subcategorias = Subcategoria.query.filter_by(ativo=True).order_by(Subcategoria.categoria, Subcategoria.ordem).all()

    return render_template('admin/produto_form.html',
                         categorias=Config.CATEGORIES,
                         tamanhos_disponiveis=Config.SIZES,
                         subcategorias=subcategorias,
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
            'loja_facebook',
            'loja_endereco'
        ]

        for config_key in configs:
            valor = request.form.get(config_key, '').strip()
            # Salvar mesmo se vazio (permite remover valores)
            Configuracao.set_valor(config_key, valor)

        # Configuração do Top Bar (checkbox)
        topbar_ativo = request.form.get('topbar_ativo') == 'on'
        Configuracao.set_valor('topbar_ativo', '1' if topbar_ativo else '0')

        flash('Configurações atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.configuracoes'))

    # Buscar configurações atuais
    configs = {
        'loja_nome': Configuracao.get_valor('loja_nome', 'Xodó da Preta'),
        'loja_telefone': Configuracao.get_valor('loja_telefone', ''),
        'loja_email': Configuracao.get_valor('loja_email', ''),
        'loja_instagram': Configuracao.get_valor('loja_instagram', ''),
        'loja_facebook': Configuracao.get_valor('loja_facebook', ''),
        'loja_endereco': Configuracao.get_valor('loja_endereco', ''),
        'topbar_ativo': Configuracao.get_valor('topbar_ativo', '1') == '1'
    }

    return render_template('admin/config.html', configs=configs)

# ========================================
# GERENCIAR SUBCATEGORIAS
# ========================================

@admin_bp.route('/subcategorias')
@login_required
def subcategorias():
    """Lista todas as subcategorias"""
    subcategorias = Subcategoria.query.order_by(Subcategoria.categoria, Subcategoria.ordem).all()

    # Agrupar por categoria
    subcategorias_por_categoria = {}
    for subcat in subcategorias:
        if subcat.categoria not in subcategorias_por_categoria:
            subcategorias_por_categoria[subcat.categoria] = []
        subcategorias_por_categoria[subcat.categoria].append(subcat)

    return render_template('admin/subcategorias.html',
                         subcategorias_por_categoria=subcategorias_por_categoria,
                         categorias=Config.CATEGORIES)

@admin_bp.route('/subcategorias/nova', methods=['GET', 'POST'])
@login_required
def subcategoria_nova():
    """Adicionar nova subcategoria"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        ativo = request.form.get('ativo') == 'on'
        ordem = int(request.form.get('ordem', 0))

        # Verificar se já existe
        existe = Subcategoria.query.filter_by(nome=nome, categoria=categoria).first()
        if existe:
            flash(f'Subcategoria "{nome}" já existe para a categoria "{categoria}".', 'warning')
            return redirect(url_for('admin.subcategoria_nova'))

        # Criar subcategoria
        subcategoria = Subcategoria(
            nome=nome,
            categoria=categoria,
            ativo=ativo,
            ordem=ordem
        )

        db.session.add(subcategoria)
        db.session.commit()

        flash(f'Subcategoria "{nome}" adicionada com sucesso!', 'success')
        return redirect(url_for('admin.subcategorias'))

    return render_template('admin/subcategoria_form.html',
                         categorias=Config.CATEGORIES,
                         subcategoria=None)

@admin_bp.route('/subcategorias/<int:subcategoria_id>/editar', methods=['GET', 'POST'])
@login_required
def subcategoria_editar(subcategoria_id):
    """Editar subcategoria existente"""
    subcategoria = Subcategoria.query.get_or_404(subcategoria_id)

    if request.method == 'POST':
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')

        # Verificar se já existe (exceto a atual)
        existe = Subcategoria.query.filter(
            Subcategoria.nome == nome,
            Subcategoria.categoria == categoria,
            Subcategoria.id != subcategoria_id
        ).first()

        if existe:
            flash(f'Subcategoria "{nome}" já existe para a categoria "{categoria}".', 'warning')
            return render_template('admin/subcategoria_form.html',
                                 categorias=Config.CATEGORIES,
                                 subcategoria=subcategoria)

        # Atualizar dados
        subcategoria.nome = nome
        subcategoria.categoria = categoria
        subcategoria.ativo = request.form.get('ativo') == 'on'
        subcategoria.ordem = int(request.form.get('ordem', 0))

        db.session.commit()

        flash(f'Subcategoria "{subcategoria.nome}" atualizada com sucesso!', 'success')
        return redirect(url_for('admin.subcategorias'))

    return render_template('admin/subcategoria_form.html',
                         categorias=Config.CATEGORIES,
                         subcategoria=subcategoria)

@admin_bp.route('/subcategorias/<int:subcategoria_id>/deletar', methods=['POST'])
@login_required
def subcategoria_deletar(subcategoria_id):
    """Deletar subcategoria"""
    subcategoria = Subcategoria.query.get_or_404(subcategoria_id)
    nome = subcategoria.nome

    # Verificar se há produtos usando esta subcategoria
    produtos_com_subcat = Produto.query.filter_by(subcategoria_id=subcategoria_id).count()
    if produtos_com_subcat > 0:
        flash(f'Não é possível deletar a subcategoria "{nome}" pois existem {produtos_com_subcat} produto(s) associado(s).', 'danger')
        return redirect(url_for('admin.subcategorias'))

    db.session.delete(subcategoria)
    db.session.commit()

    flash(f'Subcategoria "{nome}" deletada com sucesso!', 'success')
    return redirect(url_for('admin.subcategorias'))

@admin_bp.route('/api/subcategorias/<categoria>')
@login_required
def api_subcategorias_por_categoria(categoria):
    """API para buscar subcategorias por categoria (para uso em AJAX)"""
    subcategorias = Subcategoria.query.filter_by(categoria=categoria, ativo=True).order_by(Subcategoria.ordem).all()
    return {
        'subcategorias': [subcat.to_dict() for subcat in subcategorias]
    }


# ========================================
# ROTAS DO CMS (GERENCIAMENTO DE CONTEÚDO)
# ========================================

@admin_bp.route('/conteudo')
@login_required
def conteudo_listar():
    """Lista todo o conteúdo editável do site"""
    from models import ConteudoPagina

    # Agrupar conteúdo por página
    conteudos = ConteudoPagina.query.order_by(ConteudoPagina.pagina, ConteudoPagina.ordem).all()

    # Organizar por página
    conteudo_por_pagina = {}
    for item in conteudos:
        if item.pagina not in conteudo_por_pagina:
            conteudo_por_pagina[item.pagina] = []
        conteudo_por_pagina[item.pagina].append(item)

    return render_template('admin/conteudo_lista.html', conteudo_por_pagina=conteudo_por_pagina)


@admin_bp.route('/conteudo/editar/<pagina>')
@login_required
def conteudo_editar_pagina(pagina):
    """Edita todo o conteúdo de uma página específica"""
    from models import ConteudoPagina

    # Validar página
    paginas_validas = ['home', 'about', 'contact', 'footer']
    if pagina not in paginas_validas:
        flash('Página inválida', 'danger')
        return redirect(url_for('admin.conteudo_listar'))

    # Buscar conteúdo da página
    conteudos = ConteudoPagina.query.filter_by(pagina=pagina).order_by(ConteudoPagina.ordem).all()

    # Definir estrutura de campos por página
    estruturas = {
        'home': [
            {'secao': 'hero_titulo_1', 'label': 'Hero - Título Principal', 'tipo': 'texto', 'placeholder': 'Autenticidade e Inclusão'},
            {'secao': 'hero_titulo_2', 'label': 'Hero - Subtítulo', 'tipo': 'texto', 'placeholder': 'Identidade, Versatilidade e Representatividade'},
            {'secao': 'hero_texto', 'label': 'Hero - Texto Descritivo', 'tipo': 'textarea', 'placeholder': 'Desenvolvemos moda e acessórios...'},
            {'secao': 'hero_imagem', 'label': 'Hero - Imagem Principal', 'tipo': 'imagem'},
            {'secao': 'slide2_titulo', 'label': 'Slide 2 - Título', 'tipo': 'texto', 'placeholder': 'Uma História de Afeto'},
            {'secao': 'slide2_subtitulo', 'label': 'Slide 2 - Subtítulo', 'tipo': 'texto', 'placeholder': 'Xodó da Preta, criada pela minha mãe Marli'},
            {'secao': 'slide2_texto', 'label': 'Slide 2 - Texto', 'tipo': 'textarea'},
            {'secao': 'slide2_imagem', 'label': 'Slide 2 - Imagem', 'tipo': 'imagem'},
            {'secao': 'slide3_titulo', 'label': 'Slide 3 - Título', 'tipo': 'texto', 'placeholder': 'Produção Consciente'},
            {'secao': 'slide3_subtitulo', 'label': 'Slide 3 - Subtítulo', 'tipo': 'texto', 'placeholder': 'Sustentabilidade e Economia Circular'},
            {'secao': 'slide3_texto', 'label': 'Slide 3 - Texto', 'tipo': 'textarea'},
            {'secao': 'slide3_imagem', 'label': 'Slide 3 - Imagem', 'tipo': 'imagem'},
            {'secao': 'categorias_titulo', 'label': 'Categorias - Título', 'tipo': 'texto', 'placeholder': 'Categorias'},
            {'secao': 'categorias_subtitulo', 'label': 'Categorias - Subtítulo', 'tipo': 'texto', 'placeholder': 'Explore nossa coleção...'},
        ],
        'about': [
            {'secao': 'header_titulo', 'label': 'Cabeçalho - Título', 'tipo': 'texto', 'placeholder': 'Sobre Mim'},
            {'secao': 'header_texto', 'label': 'Cabeçalho - Texto', 'tipo': 'textarea', 'placeholder': 'Eu sou Teresa Cristina...'},
            {'secao': 'header_imagem', 'label': 'Cabeçalho - Imagem', 'tipo': 'imagem'},
            {'secao': 'servicos_titulo', 'label': 'Serviços - Título', 'tipo': 'texto', 'placeholder': 'Nossos Serviços'},
            {'secao': 'servicos_texto', 'label': 'Serviços - Texto', 'tipo': 'textarea'},
        ],
        'contact': [
            {'secao': 'header_titulo', 'label': 'Título Principal', 'tipo': 'texto', 'placeholder': 'Entre em Contato'},
            {'secao': 'header_subtitulo', 'label': 'Subtítulo', 'tipo': 'texto', 'placeholder': 'Ficou com alguma dúvida?...'},
            {'secao': 'telefone', 'label': 'Telefone/WhatsApp', 'tipo': 'texto', 'placeholder': '5511954375056'},
            {'secao': 'instagram', 'label': 'Instagram (usuário)', 'tipo': 'texto', 'placeholder': '@xododapreta'},
            {'secao': 'localizacao', 'label': 'Localização', 'tipo': 'texto', 'placeholder': 'São Paulo, SP'},
            {'secao': 'tempo_resposta', 'label': 'Tempo de Resposta', 'tipo': 'texto', 'placeholder': 'Respondemos em até 24 horas!'},
        ],
        'footer': [
            {'secao': 'sobre_texto', 'label': 'Texto "Sobre"', 'tipo': 'textarea', 'placeholder': 'Moda afro autoral...'},
            {'secao': 'direitos', 'label': 'Direitos Autorais', 'tipo': 'texto', 'placeholder': '© 2024 Xodó da Preta'},
        ]
    }

    estrutura_pagina = estruturas.get(pagina, [])

    # Criar dicionário de conteúdos existentes
    conteudo_dict = {item.secao: item for item in conteudos}

    return render_template(
        'admin/conteudo_editar.html',
        pagina=pagina,
        estrutura=estrutura_pagina,
        conteudo_dict=conteudo_dict
    )


@admin_bp.route('/conteudo/salvar/<pagina>', methods=['POST'])
@login_required
def conteudo_salvar(pagina):
    """Salva o conteúdo editado de uma página"""
    from models import ConteudoPagina

    try:
        # Processar todos os campos do formulário
        for key, value in request.form.items():
            if key.startswith('secao_'):
                secao = key.replace('secao_', '')

                # Verificar se é campo de imagem
                tipo = 'texto'
                if secao.endswith('_imagem'):
                    tipo = 'imagem'
                elif len(value) > 200:
                    tipo = 'textarea'

                # Atualizar ou criar conteúdo
                ConteudoPagina.set_conteudo(
                    pagina=pagina,
                    secao=secao,
                    conteudo=value if value else None,
                    tipo=tipo
                )

        # Processar upload de imagens
        for key in request.files:
            if key.startswith('imagem_'):
                secao = key.replace('imagem_', '')
                arquivo = request.files[key]

                if arquivo and arquivo.filename:
                    from werkzeug.utils import secure_filename
                    import os

                    # Salvar arquivo
                    filename = secure_filename(arquivo.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"

                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)

                    filepath = os.path.join(upload_folder, filename)
                    arquivo.save(filepath)

                    # Atualizar no banco
                    ConteudoPagina.set_conteudo(
                        pagina=pagina,
                        secao=secao,
                        imagem=filename,
                        tipo='imagem'
                    )

        flash(f'Conteúdo da página "{pagina}" atualizado com sucesso!', 'success')

    except Exception as e:
        flash(f'Erro ao salvar conteúdo: {str(e)}', 'danger')
        db.session.rollback()

    return redirect(url_for('admin.conteudo_editar_pagina', pagina=pagina))


# ==========================================
# BIBLIOTECA DE MÍDIA
# ==========================================

@admin_bp.route('/media')
@login_required
def media_biblioteca():
    """Biblioteca de mídia - todas as imagens do sistema"""
    from pathlib import Path
    import os

    upload_folder = Config.UPLOAD_FOLDER
    imagens = []

    if upload_folder.exists():
        # Carregar todos os produtos de uma vez (otimização N+1)
        todos_produtos = Produto.query.all()

        # Criar mapa de imagens para produtos
        imagem_para_produtos = {}
        for p in todos_produtos:
            # Verificar imagem principal
            if p.imagem:
                if p.imagem not in imagem_para_produtos:
                    imagem_para_produtos[p.imagem] = []
                imagem_para_produtos[p.imagem].append({'tipo': 'produto', 'nome': p.nome, 'id': p.id})

            # Verificar imagens adicionais
            if p.imagens_adicionais:
                try:
                    imgs_adicionais = json.loads(p.imagens_adicionais)
                    for img in imgs_adicionais:
                        if img not in imagem_para_produtos:
                            imagem_para_produtos[img] = []
                        imagem_para_produtos[img].append({'tipo': 'produto', 'nome': p.nome, 'id': p.id})
                except json.JSONDecodeError:
                    pass

        # Listar todos os arquivos de imagem
        extensoes_permitidas = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

        for arquivo in upload_folder.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in extensoes_permitidas:
                # Obter informações do arquivo
                stat = arquivo.stat()
                tamanho_kb = stat.st_size / 1024  # Converter para KB

                # Buscar no mapa (sem query adicional)
                usado_em = imagem_para_produtos.get(arquivo.name, [])

                imagens.append({
                    'nome': arquivo.name,
                    'tamanho_kb': round(tamanho_kb, 2),
                    'data_modificacao': datetime.fromtimestamp(stat.st_mtime),
                    'usado_em': usado_em,
                    'em_uso': len(usado_em) > 0
                })

        # Ordenar por data (mais recentes primeiro)
        imagens.sort(key=lambda x: x['data_modificacao'], reverse=True)

    return render_template('admin/media_biblioteca.html', imagens=imagens)


@admin_bp.route('/media/deletar/<filename>', methods=['POST'])
@login_required
def media_deletar(filename):
    """Deletar imagem da biblioteca"""
    from pathlib import Path

    # Verificar se a imagem está sendo usada
    produtos_usando = Produto.query.filter(
        (Produto.imagem == filename) |
        (Produto.imagens_adicionais.like(f'%{filename}%'))
    ).all()

    if produtos_usando:
        nomes = ', '.join([p.nome for p in produtos_usando[:3]])
        if len(produtos_usando) > 3:
            nomes += f' e mais {len(produtos_usando) - 3}'
        flash(f'Não é possível deletar. Imagem em uso em: {nomes}', 'danger')
        return redirect(url_for('admin.media_biblioteca'))

    # Deletar arquivo
    try:
        arquivo = Config.UPLOAD_FOLDER / filename
        if arquivo.exists():
            arquivo.unlink()
            flash(f'Imagem "{filename}" deletada com sucesso!', 'success')
        else:
            flash('Arquivo não encontrado.', 'warning')
    except Exception as e:
        flash(f'Erro ao deletar arquivo: {str(e)}', 'danger')

    return redirect(url_for('admin.media_biblioteca'))


# ==========================================
# SISTEMA DE BACKUP
# ==========================================

@admin_bp.route('/backup')
@login_required
def backup_painel():
    """Painel de backup e restore"""
    from pathlib import Path
    import os

    # Listar backups existentes
    backup_folder = Path(current_app.root_path).parent / 'backups'
    backups = []

    if backup_folder.exists():
        for arquivo in backup_folder.iterdir():
            if arquivo.is_file() and arquivo.suffix == '.zip':
                stat = arquivo.stat()
                backups.append({
                    'nome': arquivo.name,
                    'tamanho_mb': round(stat.st_size / (1024 * 1024), 2),
                    'data': datetime.fromtimestamp(stat.st_mtime)
                })

        backups.sort(key=lambda x: x['data'], reverse=True)

    return render_template('admin/backup.html', backups=backups)


@admin_bp.route('/backup/criar', methods=['POST'])
@login_required
def backup_criar():
    """Criar backup do banco de dados e uploads"""
    from pathlib import Path
    import shutil

    try:
        # Criar pasta de backups se não existir
        backup_folder = Path(current_app.root_path).parent / 'backups'
        backup_folder.mkdir(exist_ok=True)

        # Nome do backup com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}.zip'
        backup_path = backup_folder / backup_name

        # Criar arquivo ZIP
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Adicionar banco de dados
            db_path = Path(current_app.root_path) / 'loja.db'
            if db_path.exists():
                zipf.write(db_path, arcname='loja.db')

            # Adicionar pasta uploads
            uploads_folder = Config.UPLOAD_FOLDER
            if uploads_folder.exists():
                for arquivo in uploads_folder.rglob('*'):
                    if arquivo.is_file():
                        arcname = f'uploads/{arquivo.relative_to(uploads_folder)}'
                        zipf.write(arquivo, arcname=arcname)

        flash(f'Backup criado com sucesso: {backup_name}', 'success')

    except Exception as e:
        flash(f'Erro ao criar backup: {str(e)}', 'danger')

    return redirect(url_for('admin.backup_painel'))


@admin_bp.route('/backup/download/<filename>')
@login_required
def backup_download(filename):
    """Download de arquivo de backup"""
    from flask import send_file
    from pathlib import Path

    backup_folder = Path(current_app.root_path).parent / 'backups'
    backup_path = backup_folder / filename

    if not backup_path.exists():
        flash('Arquivo de backup não encontrado.', 'danger')
        return redirect(url_for('admin.backup_painel'))

    return send_file(backup_path, as_attachment=True)


@admin_bp.route('/backup/deletar/<filename>', methods=['POST'])
@login_required
def backup_deletar(filename):
    """Deletar arquivo de backup"""
    from pathlib import Path

    try:
        backup_folder = Path(current_app.root_path).parent / 'backups'
        backup_path = backup_folder / filename

        if backup_path.exists():
            backup_path.unlink()
            flash(f'Backup "{filename}" deletado com sucesso!', 'success')
        else:
            flash('Arquivo não encontrado.', 'warning')

    except Exception as e:
        flash(f'Erro ao deletar backup: {str(e)}', 'danger')

    return redirect(url_for('admin.backup_painel'))


# ==========================================
# CUPONS DE DESCONTO
# ==========================================

@admin_bp.route('/cupons')
@login_required
def cupons():
    """Lista todos os cupons"""
    cupons_lista = Cupom.query.order_by(Cupom.data_criacao.desc()).all()
    return render_template('admin/cupons.html', cupons=cupons_lista)


@admin_bp.route('/cupons/novo', methods=['GET', 'POST'])
@login_required
def cupom_novo():
    """Criar novo cupom"""
    if request.method == 'POST':
        # Obter e validar dados
        codigo = request.form.get('codigo', '').strip().upper()
        descricao = request.form.get('descricao', '').strip()
        tipo_desconto = request.form.get('tipo_desconto', 'percentual')
        valor_desconto_str = request.form.get('valor_desconto', '0')
        valor_minimo_str = request.form.get('valor_minimo', '0')
        quantidade_maxima_str = request.form.get('quantidade_maxima', '')
        data_inicio_str = request.form.get('data_inicio', '')
        data_fim_str = request.form.get('data_fim', '')
        ativo = request.form.get('ativo') == 'on'

        # VALIDAÇÕES
        if not codigo:
            flash('Código do cupom é obrigatório', 'danger')
            return redirect(url_for('admin.cupom_novo'))

        # Verificar se código já existe
        cupom_existente = Cupom.query.filter_by(codigo=codigo).first()
        if cupom_existente:
            flash(f'Cupom "{codigo}" já existe', 'danger')
            return redirect(url_for('admin.cupom_novo'))

        try:
            valor_desconto = float(valor_desconto_str)
            if valor_desconto <= 0:
                flash('Valor do desconto deve ser maior que zero', 'danger')
                return redirect(url_for('admin.cupom_novo'))
        except (ValueError, TypeError):
            flash('Valor do desconto inválido', 'danger')
            return redirect(url_for('admin.cupom_novo'))

        try:
            valor_minimo = float(valor_minimo_str) if valor_minimo_str else 0
        except (ValueError, TypeError):
            valor_minimo = 0

        try:
            quantidade_maxima = int(quantidade_maxima_str) if quantidade_maxima_str else None
        except (ValueError, TypeError):
            quantidade_maxima = None

        # Converter datas
        data_inicio = None
        data_fim = None

        if data_inicio_str:
            try:
                data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                data_inicio = datetime.utcnow()

        if data_fim_str:
            try:
                data_fim = datetime.strptime(data_fim_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                data_fim = None

        # Criar cupom
        cupom = Cupom(
            codigo=codigo,
            descricao=descricao,
            tipo_desconto=tipo_desconto,
            valor_desconto=valor_desconto,
            valor_minimo=valor_minimo,
            quantidade_maxima=quantidade_maxima,
            data_inicio=data_inicio or datetime.utcnow(),
            data_fim=data_fim,
            ativo=ativo
        )

        db.session.add(cupom)
        db.session.commit()

        flash(f'Cupom "{codigo}" criado com sucesso!', 'success')
        return redirect(url_for('admin.cupons'))

    return render_template('admin/cupom_form.html', cupom=None)


@admin_bp.route('/cupons/<int:cupom_id>/editar', methods=['GET', 'POST'])
@login_required
def cupom_editar(cupom_id):
    """Editar cupom existente"""
    cupom = Cupom.query.get_or_404(cupom_id)

    if request.method == 'POST':
        # Obter e validar dados
        codigo = request.form.get('codigo', '').strip().upper()
        descricao = request.form.get('descricao', '').strip()
        tipo_desconto = request.form.get('tipo_desconto', 'percentual')
        valor_desconto_str = request.form.get('valor_desconto', '0')
        valor_minimo_str = request.form.get('valor_minimo', '0')
        quantidade_maxima_str = request.form.get('quantidade_maxima', '')
        data_inicio_str = request.form.get('data_inicio', '')
        data_fim_str = request.form.get('data_fim', '')
        ativo = request.form.get('ativo') == 'on'

        # VALIDAÇÕES
        if not codigo:
            flash('Código do cupom é obrigatório', 'danger')
            return redirect(url_for('admin.cupom_editar', cupom_id=cupom_id))

        # Verificar se código já existe em outro cupom
        cupom_existente = Cupom.query.filter(Cupom.codigo == codigo, Cupom.id != cupom_id).first()
        if cupom_existente:
            flash(f'Cupom "{codigo}" já existe', 'danger')
            return redirect(url_for('admin.cupom_editar', cupom_id=cupom_id))

        try:
            valor_desconto = float(valor_desconto_str)
            if valor_desconto <= 0:
                flash('Valor do desconto deve ser maior que zero', 'danger')
                return redirect(url_for('admin.cupom_editar', cupom_id=cupom_id))
        except (ValueError, TypeError):
            flash('Valor do desconto inválido', 'danger')
            return redirect(url_for('admin.cupom_editar', cupom_id=cupom_id))

        try:
            valor_minimo = float(valor_minimo_str) if valor_minimo_str else 0
        except (ValueError, TypeError):
            valor_minimo = 0

        try:
            quantidade_maxima = int(quantidade_maxima_str) if quantidade_maxima_str else None
        except (ValueError, TypeError):
            quantidade_maxima = None

        # Converter datas
        data_inicio = cupom.data_inicio
        data_fim = None

        if data_inicio_str:
            try:
                data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                pass

        if data_fim_str:
            try:
                data_fim = datetime.strptime(data_fim_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                data_fim = None

        # Atualizar cupom
        cupom.codigo = codigo
        cupom.descricao = descricao
        cupom.tipo_desconto = tipo_desconto
        cupom.valor_desconto = valor_desconto
        cupom.valor_minimo = valor_minimo
        cupom.quantidade_maxima = quantidade_maxima
        cupom.data_inicio = data_inicio
        cupom.data_fim = data_fim
        cupom.ativo = ativo

        db.session.commit()

        flash(f'Cupom "{codigo}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.cupons'))

    return render_template('admin/cupom_form.html', cupom=cupom)


@admin_bp.route('/cupons/<int:cupom_id>/deletar', methods=['POST'])
@login_required
def cupom_deletar(cupom_id):
    """Deletar cupom"""
    cupom = Cupom.query.get_or_404(cupom_id)
    codigo = cupom.codigo

    db.session.delete(cupom)
    db.session.commit()

    flash(f'Cupom "{codigo}" deletado com sucesso!', 'success')
    return redirect(url_for('admin.cupons'))


# ==========================================
# DEBUG - TEMPORÁRIO
# ==========================================

@admin_bp.route('/debug/config')
@login_required
def debug_config():
    """Debug de configurações - TEMPORÁRIO"""
    from flask import Response

    output = []
    output.append("=== DEBUG DE CONFIGURAÇÕES ===\n\n")

    # Todas as configs
    output.append("TODAS AS CONFIGURAÇÕES NO BANCO:\n")
    all_configs = Configuracao.query.all()
    for c in all_configs:
        output.append(f"  {c.chave:25} = '{c.valor}' (type: {type(c.valor).__name__})\n")

    output.append("\n" + "="*50 + "\n\n")

    # Teste específico do topbar
    output.append("TESTE TOPBAR_ATIVO:\n")
    topbar_valor = Configuracao.get_valor('topbar_ativo', '1')
    output.append(f"  get_valor('topbar_ativo', '1') = '{topbar_valor}'\n")
    output.append(f"  type = {type(topbar_valor).__name__}\n")
    output.append(f"  '{topbar_valor}' == '1' ? {topbar_valor == '1'}\n")
    output.append(f"  bool('{topbar_valor}') = {bool(topbar_valor)}\n")

    output.append("\n" + "="*50 + "\n\n")

    # Context processor
    output.append("CONTEXT PROCESSOR:\n")
    result = topbar_valor == '1'
    output.append(f"  config_topbar_ativo = {result}\n")

    if result:
        output.append("\n✓ Top Bar DEVERIA APARECER\n")
    else:
        output.append("\n✗ Top Bar NÃO VAI APARECER\n")
        output.append("  Solução: Marcar checkbox em /admin/configuracoes\n")

    return Response(''.join(output), mimetype='text/plain')


@admin_bp.route('/debug/fix-topbar')
@login_required
def debug_fix_topbar():
    """Força topbar_ativo = 1"""
    Configuracao.set_valor('topbar_ativo', '1', 'Controla exibição do top bar')
    flash('topbar_ativo forçado para "1" (ativo)', 'success')
    return redirect(url_for('admin.debug_config'))