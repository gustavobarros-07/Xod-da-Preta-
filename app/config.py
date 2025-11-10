import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Configurações da aplicação Flask"""
    
    # Chave secreta (vem do .env)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'loja.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload de imagens
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Configurações do admin (vem do .env)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'change-me'
    
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
        
        # Criar pasta instance se não existir
        instance_folder = BASE_DIR / 'instance'
        instance_folder.mkdir(exist_ok=True)