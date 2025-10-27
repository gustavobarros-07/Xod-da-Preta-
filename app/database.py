from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Classe base para os modelos do SQLAlchemy"""
    pass

# Instância do SQLAlchemy
db = SQLAlchemy(model_class=Base)

def init_db(app):
    """
    Inicializa o banco de dados com a aplicação Flask
    
    Args:
        app: Instância da aplicação Flask
    """
    # Configurar o banco de dados
    db.init_app(app)
    
    with app.app_context():
        # Importar modelos aqui para evitar importação circular
        from models import Produto, Admin, Configuracao
        
        # Criar todas as tabelas
        db.create_all()
        
        print("✅ Banco de dados inicializado com sucesso!")

def get_db():
    """
    Retorna a instância do banco de dados
    
    Returns:
        db: Instância do SQLAlchemy
    """
    return db