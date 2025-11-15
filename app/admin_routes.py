"""
Rotas do painel administrativo
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from functools import wraps
import os
from pathlib import Path
from database import db
from models import Produto, Admin, Configuracao, Subcategoria
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
    """Dashboard principal do admin com métricas avançadas"""
    from datetime import datetime, timedelta
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
                         total_visualizacoes=total_visualizacoes)

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
        subcategoria = request.form.get('subcategoria')  # Feminino/Masculino
        tipo = request.form.get('tipo')  # Vestido, Camisa, etc.
        subcategoria_id = request.form.get('subcategoria_id')  # Legado
        tamanhos = request.form.getlist('tamanhos')
        ativo = request.form.get('ativo') == 'on'
        destaque = request.form.get('destaque') == 'on'
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
            subcategoria=subcategoria if subcategoria else None,
            tipo=tipo if tipo else None,
            subcategoria_id=int(subcategoria_id) if subcategoria_id else None,
            tamanhos=json.dumps(tamanhos),
            imagem=imagem_filename,
            ativo=ativo,
            destaque=destaque,
            ordem=ordem
        )

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
        # Atualizar dados
        produto.nome = request.form.get('nome')
        produto.descricao = request.form.get('descricao')
        produto.preco = float(request.form.get('preco'))
        produto.categoria = request.form.get('categoria')
        produto.subcategoria = request.form.get('subcategoria') or None
        produto.tipo = request.form.get('tipo') or None
        subcategoria_id = request.form.get('subcategoria_id')
        produto.subcategoria_id = int(subcategoria_id) if subcategoria_id else None
        produto.tamanhos = json.dumps(request.form.getlist('tamanhos'))
        produto.ativo = request.form.get('ativo') == 'on'
        produto.destaque = request.form.get('destaque') == 'on'
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