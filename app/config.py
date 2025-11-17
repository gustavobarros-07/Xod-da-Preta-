import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Diretório base do projeto (pasta app/)
BASE_DIR = Path(__file__).resolve().parent
# Diretório raiz do projeto (pasta acima de app/)
PROJECT_ROOT = BASE_DIR.parent

class Config:
    """Configurações da aplicação Flask"""

    # Chave secreta (vem do .env) - OBRIGATÓRIO em produção
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY não definida no arquivo .env\n"
            "Gere uma chave com: python -c \"import secrets; print(secrets.token_hex(32))\""
        )

    # Banco de dados SQLite (agora em instance/)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(PROJECT_ROOT / 'instance' / 'loja.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload de imagens
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Configurações do admin (vem do .env) - OBRIGATÓRIO
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        raise RuntimeError(
            "ADMIN_USERNAME e ADMIN_PASSWORD devem estar definidos no arquivo .env\n"
            "Use uma senha forte com letras, números e símbolos"
        )
    
    # Paginação
    PRODUCTS_PER_PAGE = 9
    
    # Categorias disponíveis
    CATEGORIES = ['Brincos', 'Roupas', 'Colares', 'Anéis', 'Pulseiras']

    # Hierarquia de Categorias (3 níveis)
    CATEGORY_HIERARCHY = {
        'Roupas': {
            'Feminino': ['Vestido', 'Saia', 'Macacão', 'Jaqueta'],
            'Masculino': ['Camisa', 'Bata', 'Conjunto', 'Jaqueta']
        }
        # Outras categorias não têm hierarquia (apenas 1 nível)
    }

    # Tamanhos disponíveis
    SIZES = ['PP', 'P', 'M', 'G', 'GG', 'GG1', 'GG2', 'GG3', 'Único']
    
    @staticmethod
    def init_app(app):
        """Inicializa a aplicação com as configurações"""
        # Criar pasta de uploads se não existir
        upload_folder = Config.UPLOAD_FOLDER
        upload_folder.mkdir(parents=True, exist_ok=True)

        # Criar pasta instance se não existir (para banco de dados)
        instance_folder = PROJECT_ROOT / 'instance'
        instance_folder.mkdir(exist_ok=True)