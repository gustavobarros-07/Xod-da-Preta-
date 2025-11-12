Descrição linha a linha dos arquivos .py do projeto

Observação: Em trechos óbvios e blocos repetitivos, linhas consecutivas podem ser descritas em conjunto para manter a leitura objetiva. Comentários com acentuação corrompida foram mantidos com a intenção inferida pelo contexto.


# Xod-da-Preta-/app/models.py

- Linha 1: Importa `datetime` para registrar datas/hora em colunas.
- Linha 2: Importa a instância `db` (SQLAlchemy) do módulo `database`.
- Linha 3: Importa utilitários para gerar e verificar hash de senha.
- Linha 4: Linha em branco (organização).
- Linha 5: Linha em branco (organização).
- Linha 6: Define a classe `Subcategoria`, herda de `db.Model` (tabela ORM).
- Linha 7: Docstring do modelo `Subcategoria`.
- Linha 8: Define o nome da tabela como `subcategorias`.
- Linha 9: Linha em branco (separação).
- Linha 10: Coluna `id` (chave primária, inteiro).
- Linha 11: Coluna `nome` (string até 50, obrigatório).
- Linha 12: Coluna `categoria` (string até 50, obrigatório) — categoria pai.
- Linha 13: Coluna `ativo` (booleano, padrão True).
- Linha 14: Coluna `ordem` (inteiro, padrão 0) — ordenação personalizada.
- Linha 15: Coluna `data_criacao` (DateTime, padrão agora em UTC).
- Linha 16: Linha em branco.
- Linha 17: Comentário sobre relacionamento com produtos.
- Linha 18: Relacionamento ORM: uma `Subcategoria` tem muitos `Produto`; cria `backref` `subcategoria_obj`.
- Linha 19: Linha em branco.
- Linha 20: Início de `__repr__` para representação legível.
- Linha 21: Retorna representação textual contendo `categoria` e `nome`.
- Linha 22: Linha em branco.
- Linha 23: Início de `to_dict` (serialização para dicionário).
- Linha 24: Docstring do método `to_dict`.
- Linhas 25–31: Retorna dicionário com campos principais da subcategoria.
- Linha 32: Linha em branco.
- Linha 33: Linha em branco.
- Linha 34: Define a classe `Produto`, herda de `db.Model` (tabela ORM).
- Linha 35: Docstring do modelo `Produto`.
- Linha 36: Define o nome da tabela como `produtos`.
- Linha 37: Linha em branco.
- Linha 38: Coluna `id` (chave primária, inteiro).
- Linha 39: Coluna `nome` (string até 100, obrigatório).
- Linha 40: Coluna `descricao` (texto, opcional).
- Linha 41: Coluna `preco` (float, obrigatório).
- Linha 42: Coluna `categoria` (string até 50, obrigatório) — nível 1.
- Linha 43: Coluna `subcategoria` (string até 50, opcional) — nível 2.
- Linha 44: Coluna `tipo` (string até 50, opcional) — nível 3.
- Linha 45: Coluna `subcategoria_id` (FK para `subcategorias.id`, opcional) — legado.
- Linha 46: Coluna `tamanhos` (string até 200) contendo JSON textual de tamanhos.
- Linha 47: Coluna `imagem` (string até 200) com nome do arquivo.
- Linha 48: Coluna `ordem` (inteiro, padrão 0) — ordenação personalizada.
- Linha 49: Coluna `ativo` (booleano, padrão True) — controle de visibilidade.
- Linha 50: Coluna `data_criacao` (DateTime, padrão agora em UTC).
- Linha 51: Coluna `data_atualizacao` (DateTime, padrão agora + atualiza em updates).
- Linha 52: Linha em branco.
- Linha 53: Início de `__repr__` do produto.
- Linha 54: Retorna representação textual com o nome do produto.
- Linha 55: Linha em branco.
- Linha 56: Início de `to_dict` (serialização do produto).
- Linha 57: Docstring de `to_dict`.
- Linhas 58–73: Constrói dicionário com todos os campos relevantes; inclui `subcategoria_nome` via `backref` e formata `data_criacao`.
- Linha 74: Linha em branco.
- Linha 75: Linha em branco.
- Linha 76: Define a classe `Admin`, herda de `db.Model` (tabela ORM).
- Linha 77: Docstring do modelo `Admin`.
- Linha 78: Define o nome da tabela como `admins`.
- Linha 79: Linha em branco.
- Linha 80: Coluna `id` (chave primária, inteiro).
- Linha 81: Coluna `username` (string até 80, único, obrigatório).
- Linha 82: Coluna `password_hash` (string até 200, obrigatório).
- Linha 83: Coluna `email` (string até 120, único, opcional).
- Linha 84: Coluna `data_criacao` (DateTime, padrão agora em UTC).
- Linha 85: Coluna `ultimo_login` (DateTime, opcional).
- Linha 86: Linha em branco.
- Linha 87: Início de `set_password` (aplica hash à senha em texto puro).
- Linha 88: Docstring de `set_password`.
- Linha 89: Gera o hash e armazena em `password_hash`.
- Linha 90: Linha em branco.
- Linha 91: Início de `check_password` (valida senha informada).
- Linha 92: Docstring de `check_password`.
- Linha 93: Verifica o hash com a senha fornecida.
- Linha 94: Linha em branco.
- Linha 95: Início de `__repr__` do admin.
- Linha 96: Retorna representação textual com `username`.
- Linha 97: Linha em branco.
- Linha 98: Linha em branco.
- Linha 99: Define a classe `Configuracao`, herda de `db.Model`.
- Linha 100: Docstring do modelo `Configuracao`.
- Linha 101: Define nome da tabela `configuracoes`.
- Linha 102: Linha em branco.
- Linha 103: Coluna `id` (chave primária, inteiro).
- Linha 104: Coluna `chave` (string até 50, única, obrigatória).
- Linha 105: Coluna `valor` (texto, opcional) — valor da configuração.
- Linha 106: Coluna `descricao` (string até 200, opcional).
- Linha 107: Coluna `data_atualizacao` (DateTime, autualiza automaticamente).
- Linha 108: Linha em branco.
- Linha 109: Início de `__repr__` retornando a chave.
- Linha 110: Retorna representação textual com `chave`.
- Linha 111: Linha em branco.
- Linha 112: Decorador `@staticmethod` para método utilitário.
- Linha 113: Define `get_valor(chave, default=None)`.
- Linha 114: Docstring de `get_valor`.
- Linha 115: Busca primeira configuração com a `chave` informada.
- Linha 116: Retorna o valor ou `default` se não encontrada.
- Linha 117: Linha em branco.
- Linha 118: Decorador `@staticmethod` para método de escrita.
- Linha 119: Define `set_valor(chave, valor, descricao=None)`.
- Linha 120: Docstring de `set_valor`.
- Linhas 121–130: Lê/atualiza ou cria configuração e `commit` no banco; retorna o registro.
- Linha 131: Linha em branco.
- Linha 132: Linha em branco.
- Linha 133: Define a classe `ItemCarrinho`, herda de `db.Model`.
- Linha 134: Docstring do modelo `ItemCarrinho`.
- Linha 135: Define nome da tabela `itens_carrinho`.
- Linha 136: Linha em branco.
- Linha 137: Coluna `id` (chave primária, inteiro).
- Linha 138: Coluna `session_id` (string até 100) — identifica a sessão do usuário.
- Linha 139: Coluna `produto_id` (FK para `produtos.id`, obrigatório).
- Linha 140: Coluna `quantidade` (inteiro, padrão 1).
- Linha 141: Coluna `tamanho` (string até 10, opcional).
- Linha 142: Coluna `data_adicao` (DateTime, padrão agora em UTC).
- Linha 143: Linha em branco.
- Linha 144: Comentário do relacionamento com `Produto`.
- Linha 145: Relacionamento ORM para acessar `produto` a partir do item.
- Linha 146: Linha em branco.
- Linha 147: Início de `__repr__` para item do carrinho.
- Linha 148: Retorna representação com `produto_id` e `quantidade`.
- Linha 149: Linha em branco.
- Linha 150: Início de `to_dict` (serialização do item do carrinho).
- Linha 151: Docstring de `to_dict`.
- Linhas 152–161: Retorna dicionário com dados do item e subtotal calculado.


# Xod-da-Preta-/app/database.py

- Linha 1: Importa `SQLAlchemy` para ORM com Flask.
- Linha 2: Importa `DeclarativeBase` (base declarativa do SQLAlchemy 2.x).
- Linha 3: Linha em branco.
- Linha 4: Define classe base `Base` herdando de `DeclarativeBase`.
- Linha 5: Docstring da classe base.
- Linha 6: `pass` pois não há customização adicional.
- Linha 7: Linha em branco.
- Linha 8: Comentário indicando a instância global.
- Linha 9: Cria `db = SQLAlchemy(model_class=Base)` usando a base customizada.
- Linha 10: Linha em branco.
- Linha 11: Define `init_db(app)` para inicializar o banco com a app Flask.
- Linhas 12–17: Docstring com propósito e argumento da função.
- Linha 18: Comentário de configuração.
- Linha 19: Chama `db.init_app(app)` para vincular a app ao ORM.
- Linha 20: Linha em branco.
- Linha 21: Entra no contexto da aplicação Flask.
- Linha 22: Comentário sobre evitar importação circular.
- Linha 23: Importa modelos após contexto para registrar as tabelas.
- Linha 24: Linha em branco.
- Linha 25: Comentário sobre criação de tabelas.
- Linha 26: Executa `db.create_all()` para criar as tabelas no banco.
- Linha 27: Linha em branco.
- Linha 28: `print` confirmando inicialização do banco.
- Linha 29: Linha em branco.
- Linha 30: Define `get_db()` que retorna a instância do ORM.
- Linhas 31–36: Docstring e retorno da instância `db`.
- Linha 37: Retorna `db`.


# Xod-da-Preta-/app/admin_routes.py

- Linhas 1–3: Docstring do módulo descrevendo rotas do painel administrativo.
- Linha 4: Linha em branco.
- Linha 5: Importa utilitários do Flask usados nas rotas/admin.
- Linha 6: Importa `secure_filename` para nomes seguros de arquivos.
- Linha 7: Importa `wraps` para criar decorator preservando metadados.
- Linha 8: Importa `os` para manipulação de caminhos/extensões.
- Linha 9: Importa `Path` (não é utilizado diretamente neste arquivo; presença é inócua).
- Linha 10: Importa a instância `db` para operações no banco.
- Linha 11: Importa modelos ORM usados no admin.
- Linha 12: Importa configurações globais `Config`.
- Linha 13: Importa `json` para serializar/deserializar listas de tamanhos.
- Linha 14: Linha em branco.
- Linha 15: Comentário introdutório do Blueprint admin.
- Linha 16: Cria `admin_bp` com prefixo de URL `/admin`.
- Linha 17: Linha em branco.
- Linha 18: Comentário sobre proteção de rotas com login.
- Linha 19: Define decorator `login_required` que exige sessão ativa.
- Linha 20: Aplica `@wraps(f)` para manter metadados da função.
- Linhas 21–26: Função interna verifica `session` e redireciona se não logado.
- Linha 27: Linha em branco.
- Linha 28: Comentário sobre função auxiliar de upload.
- Linha 29: Define `allowed_file(filename)`.
- Linha 30: Docstring do verificador de extensão.
- Linhas 31–32: Retorna True se extensão estiver em `ALLOWED_EXTENSIONS`.
- Linha 33: Linha em branco.
- Linha 34: Define `save_product_image(file)` para salvar upload com timestamp.
- Linha 35: Docstring da função de salvar imagem.
- Linhas 36–37: Verifica arquivo e extensão; normaliza nome com `secure_filename`.
- Linha 38: Comentário: adiciona timestamp.
- Linha 39: Import local de `datetime` (evita import global desnecessário).
- Linha 40: Formata timestamp `YYYYMMDDHHMMSS`.
- Linha 41: Separa nome e extensão do arquivo.
- Linha 42: Reconstrói nome com sufixo timestamp.
- Linha 43: Linha em branco.
- Linha 44: Resolve caminho destino dentro de `UPLOAD_FOLDER`.
- Linha 45: Salva arquivo no caminho calculado.
- Linha 46: Retorna nome do arquivo salvo.
- Linha 47: Retorna `None` se arquivo inválido.
- Linha 48: Linha em branco.
- Linhas 49–51: Cabeçalho de seção: Rotas de autenticação.
- Linha 52: Linha em branco.
- Linha 53: Define rota `/login` (GET/POST).
- Linha 54: Define função `login`.
- Linha 55: Docstring da página de login.
- Linhas 56–58: Se já logado, redireciona para `dashboard`.
- Linhas 60–63: Se POST, lê `username` e `password` do formulário.
- Linhas 64–66: Busca admin por username no banco.
- Linhas 67–76: Se encontrou e senha confere, cria sessão e atualiza `ultimo_login` (commit).
- Linhas 78–79: Feedback de sucesso e redireciona ao dashboard.
- Linhas 80–81: Caso contrário, exibe mensagem de erro.
- Linha 83: Renderiza template `admin/login.html` (GET inicial ou erro).
- Linhas 85–90: Rota `/logout` limpa sessão e redireciona ao login.
- Linhas 92–94: Cabeçalho de seção: Dashboard.
- Linhas 96–99: Define rotas `/` e `/dashboard` protegidas por `login_required`.
- Linha 100: Docstring da view `dashboard`.
- Linhas 101–105: Calcula contagens gerais (total/ativos/inativos) via ORM.
- Linhas 106–111: Monta dicionário de contagens por categoria de `Config`.
- Linhas 112–113: Busca últimos 5 produtos por `data_criacao` desc.
- Linhas 115–120: Renderiza `admin/dashboard.html` com métricas e lista.
- Linhas 122–124: Cabeçalho de seção: Gerenciar produtos.
- Linhas 126–131: Rota para listar produtos ordenados; renderiza `admin/produtos.html`.
- Linhas 133–135: Rota para criar produto (GET/POST) protegida.
- Linhas 136–149: Se POST, coleta campos do formulário e converte tipos.
- Linhas 150–153: Lê arquivo de imagem e salva (se houver).
- Linhas 154–167: Instancia `Produto` com dados; serializa tamanhos com `json.dumps`.
- Linhas 169–171: Adiciona à sessão e commita.
- Linhas 172–174: Feedback e redirect para lista de produtos.
- Linhas 175–177: Para GET, carrega subcategorias ativas ordenadas.
- Linhas 178–182: Renderiza `admin/produto_form.html` com opções (novo produto).
- Linhas 184–186: Rota para editar produto existente (GET/POST).
- Linha 187: Docstring da view de edição.
- Linha 188: Busca ou 404 o produto pelo `produto_id`.
- Linhas 190–203: Se POST, atualiza campos, converte tipos e JSON de tamanhos.
- Linhas 204–215: Se nova imagem enviada, remove antiga do disco e salva a nova.
- Linhas 216–219: Commit, feedback e redirect.
- Linhas 221–223: Converte tamanhos salvos para lista para preencher o formulário.
- Linhas 224–226: Carrega subcategorias ativas ordenadas.
- Linhas 227–232: Renderiza form com dados do produto e tamanhos marcados.
- Linhas 234–236: Rota POST para deletar produto; protegida.
- Linhas 237–240: Busca ou 404; guarda nome para mensagem.
- Linhas 241–246: Se houver imagem no disco, apaga o arquivo.
- Linhas 247–249: Remove registro do banco e commita.
- Linha 250: Feedback de exclusão.


# Xod-da-Preta-/app/main.py

- Linha 1: Importa Flask e utilidades de request, session e jsonify.
- Linha 2: Importa `Path` para resolver diretórios.
- Linha 3: Importa `Config` com configurações da aplicação.
- Linha 4: Importa `db` e `init_db` (o segundo não é utilizado diretamente aqui).
- Linha 5: Importa `admin_bp` para registrar o Blueprint do admin.
- Linha 6: Importa `uuid` para gerar IDs de sessão do carrinho.
- Linha 7: Linha em branco.
- Linha 8: Comentário: diretório base.
- Linha 9: Define `BASE_DIR` como pasta do arquivo atual.
- Linha 10: Linha em branco.
- Linhas 11–15: Cria a app Flask com pastas `templates` e `static` resolvidas.
- Linha 16: Linha em branco.
- Linhas 17–19: Carrega configurações da classe `Config` e inicializa aspectos dependentes.
- Linha 20: Linha em branco.
- Linhas 21–22: Inicializa o ORM com a app (`db.init_app`).
- Linha 23: Linha em branco.
- Linhas 24–28: No contexto da app, importa modelos e cria tabelas se não existirem.
- Linha 29: Linha em branco.
- Linha 30: Registra o Blueprint do admin na aplicação.
- Linhas 31–33: Comentários: seção de rotas do site.
- Linha 34: Linha em branco.
- Linhas 35–38: Rota `/` que renderiza `index.html`.
- Linhas 40–43: Rota `/about` que renderiza `about.html`.
- Linhas 45–48: Rota `/contact` que renderiza `contact.html`.
- Linhas 50–85: Rota `/shop` com filtros hierárquicos (categoria, subcategoria, tipo, preço) e renderiza `shop.html` com `hierarchy` de `Config` e subcategorias legadas.
  - Inclui construção de query base com `Produto.query.filter_by(ativo=True)` e encadeamentos condicionais por filtro.
- Linhas 87–106: Rota `/shop/<int:produto_id>` para página de produto; busca produto e até 4 relacionados da mesma categoria.
- Linhas 108–113: Seção de carrinho — utilitário `get_session_id()` cria/retorna um UUID na sessão.
- Linhas 115–125: Rota `/carrinho` que busca itens do carrinho da sessão e calcula total; renderiza `carrinho.html`.
- Linhas 127–170: Rota `POST /api/carrinho/adicionar` que valida entrada, garante produto ativo, agrega quantidade se item já existir (por tamanho) e retorna JSON com total de itens.
  - Usa `db.session.query(db.func.sum(...))` para somar quantidades.
- Linhas 172–198: Rota `DELETE /api/carrinho/remover/<int:item_id>` que remove item da mesma sessão e retorna contagem atualizada; rollback em exceções.
- Linhas 200–230: Rota `PUT /api/carrinho/atualizar/<int:item_id>` que ajusta quantidade, retorna subtotal do item e total de itens; rollback em exceções.
- Linhas 232–241: Rota `GET /api/carrinho/total` que retorna somente `total_itens` da sessão ativa.
- Linhas 243–251: Filtro Jinja `currency` para formatar valores como BRL (R$) com substituições de separadores.
- Linhas 253–261: Filtro Jinja `from_json` para converter string JSON em lista (ou lista vazia em caso de erro).
- Linhas 263–275: Context processor `inject_global_vars` injeta configurações gerais (nome, telefone, email, instagram) obtidas de `Configuracao` no contexto de todos os templates.
- Linhas 277–283: Execução da aplicação (debug) quando chamado diretamente (`__main__`).


# Xod-da-Preta-/app/config.py

- Linha 1: Importa `os` para acessar variáveis de ambiente.
- Linha 2: Importa `Path` para manipulação de caminhos.
- Linha 3: Importa `load_dotenv` para carregar `.env`.
- Linha 4: Linha em branco.
- Linha 5: Comentário: carregar variáveis de ambiente.
- Linha 6: Chama `load_dotenv()` para popular `os.environ` com o `.env` se existir.
- Linha 7: Linha em branco.
- Linha 8: Comentário: diretório base do projeto.
- Linha 9: Define `BASE_DIR` como pasta do arquivo atual.
- Linha 10: Linha em branco.
- Linha 11: Define a classe `Config` para agrupar configurações.
- Linha 12: Docstring da classe de configuração.
- Linha 13: Linha em branco.
- Linhas 14–15: Define `SECRET_KEY` com fallback de desenvolvimento.
- Linhas 17–18: Define URI do banco SQLite em arquivo `loja.db`; desativa track modifications.
- Linhas 20–22: Configurações de upload de imagens (pasta, tamanho máximo, extensões permitidas).
- Linhas 24–25: Configurações padrão do admin vindas do ambiente (ou fallback).
- Linhas 27–28: Paginação de produtos por página.
- Linhas 30–31: Lista de categorias disponíveis.
- Linhas 33–39: Hierarquia de categorias com 3 níveis para `Roupas`.
- Linhas 41–41: Comentário sobre categorias sem hierarquia.
- Linhas 43–43: Comentário: tamanhos disponíveis.
- Linha 44: Lista de tamanhos, incluindo `Único` (acentuação aparece corrompida no arquivo).
- Linha 45: Linha em branco.
- Linhas 46–51: `init_app(app)` — cria pastas de uploads e `instance` caso não existam.


# Xod-da-Preta-/app/populate_products.py

- Linhas 1–3: Docstring do script explicando uso (popular banco com exemplos).
- Linha 4: Linha em branco.
- Linha 5: Importa `app` da `main` para contexto de aplicação.
- Linha 6: Importa `db` para operações no banco.
- Linha 7: Importa o modelo `Produto`.
- Linha 8: Importa `json` para serializar tamanhos.
- Linha 9: Linha em branco.
- Linha 10: Define `limpar_produtos_exemplo()` para remover produtos de exemplo anteriores.
- Linha 11: Docstring explicativa.
- Linha 12: `print` indicando início da limpeza.
- Linha 13: Query de deleção filtrando `descricao` com marcador de exemplo.
- Linha 14: `db.session.commit()` para efetivar remoção.
- Linha 15: `print` confirmando remoção (string contém caracteres corrompidos, mas intenção é confirmar).
- Linha 16: Linha em branco.
- Linha 17: Define `criar_produtos_exemplo()` que insere vários produtos.
- Linha 18: Docstring do criador de exemplos.
- Linha 19: Linha em branco.
- Linhas 20–151: Lista `produtos_exemplo` com dicionários de produtos variados (Colares, Anéis, Pulseiras, Brincos, Roupas). Campos: `nome`, `descricao`, `preco`, `categoria`, `tamanhos` (JSON), `ativo`, `ordem`.
- Linha 153: `print` indicando quantos produtos serão criados.
- Linhas 155–159: Loop: instancia `Produto` com `**produto_data`, adiciona à sessão, imprime cada inserção (strings com caracteres corrompidos, mas informativas).
- Linha 161: `db.session.commit()` para gravar no banco.
- Linha 162: `print` confirmando quantidade total criada.
- Linha 164: Linha em branco.
- Linha 165: Define `mostrar_estatisticas()` para imprimir métricas do banco.
- Linha 166: Docstring explicativa.
- Linhas 167–169: Prints de cabeçalho formatado.
- Linhas 171–172: Calcula total e ativos via ORM.
- Linhas 174–176: Imprime totais.
- Linha 178: Lista de categorias para somatório.
- Linhas 179–181: Loop nas categorias imprimindo contagem por `filter_by`.
- Linha 183: Print de rodapé.
- Linha 185: Linha em branco.
- Linhas 186–193: Bloco `if __name__ == '__main__'`: título do script e instruções.
- Linhas 195–206: Abre `app.app_context()`, pergunta se deseja limpar, chama criação e mostra estatísticas.


# Xod-da-Preta-/app/setup_inicial.py

- Linhas 1–6: Docstring do script de setup inicial; alerta sobre apagar dados.
- Linha 7: Linha em branco.
- Linha 8: Importa `app` do módulo `main`.
- Linha 9: Importa `db` para operações de banco.
- Linha 10: Importa modelos `Produto`, `Admin`, `Configuracao`.
- Linha 11: Importa `json` para serializar tamanhos de produtos iniciais.
- Linha 12: Linha em branco.
- Linha 13: Define `init_database()` para recriar o esquema e dados padrão.
- Linha 14: Docstring da função de init.
- Linha 15: Linha em branco.
- Linhas 16–18: Entra no `app.app_context()` para executar operações de banco.
- Linha 19: `print` informando remoção de tabelas antigas.
- Linha 20: `db.drop_all()` apaga todas as tabelas.
- Linha 22: `print` informando criação de tabelas.
- Linha 23: `db.create_all()` recria o esquema.
- Linha 25: `print` informando criação de admin padrão.
- Linhas 26–31: Cria `Admin` com username/email, define senha hash e adiciona à sessão.
- Linha 33: `print` informando criação das configurações da loja.
- Linhas 34–40: Define tuplas `(chave, valor, descricao)` de configurações iniciais.
- Linhas 42–44: Loop: cria instâncias `Configuracao` e adiciona à sessão.
- Linha 46: `print` sobre criação de produtos de exemplo.
- Linhas 47–93: Lista `produtos_exemplo` com alguns produtos iniciais (Brincos, Roupas, Colares) com `imagem` definida.
- Linhas 95–97: Loop: cria `Produto` e adiciona à sessão.
- Linha 99: `print` informando salvamento no banco.
- Linha 100: `db.session.commit()` persiste todas as alterações.
- Linhas 102–108: Prints de resumo do que foi criado e instruções (alguns caracteres corrompidos).
- Linha 110: Linha em branco.
- Linhas 111–131: Bloco `if __name__ == '__main__'` com título, alerta, lista do que será feito e pergunta de confirmação.
- Linhas 133–141: Se usuário confirma, chama `init_database()` e imprime próximos passos; senão, cancela.

------------------------------------------------------main.py-------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, request, session, jsonify  # Importa classes/funções do Flask: criação do app, renderização de templates, acesso a parâmetros da requisição, sessão de usuário e respostas JSON.
from pathlib import Path  # Importa Path para manipular caminhos de arquivos/diretórios de forma multiplataforma.
from config import Config  # Importa a classe de configuração da aplicação (variáveis, constantes e helpers de config).
from database import db, init_db  # Importa a instância do SQLAlchemy (db) e a função init_db (não utilizada diretamente aqui).
from admin_routes import admin_bp  # Importa o Blueprint com as rotas da área administrativa para registro no app principal.
import uuid  # Importa uuid para gerar identificadores únicos (usado para identificar a sessão do carrinho).

# Diretório base  # | explicação: comentário apenas informativo; delimita a seção que define o diretório raiz do projeto relativo a este arquivo.
BASE_DIR = Path(__file__).resolve().parent  # Calcula o diretório onde este arquivo está localizado, resolvendo links e obtendo o pai como base do projeto.

# Criar aplicação Flask  # | explicação: comentário de seção indicando construção da instância do app.
app = Flask(  # Cria a instância principal do Flask; __name__ ajuda o Flask a localizar recursos (templates/estáticos).
    __name__,  # Passa o nome do módulo atual; o Flask usa para determinar a raiz do app.
    template_folder=str(BASE_DIR / "templates"),  # Define a pasta de templates HTML explicitamente (caminho absoluto convertido para string).
    static_folder=str(BASE_DIR / "static")  # Define a pasta de arquivos estáticos (CSS, JS, imagens) explicitamente.
)  # Fecha a chamada do construtor do Flask.

# Carregar configurações  # | explicação: seção que aplica configurações globais no app.
app.config.from_object(Config)  # Carrega as configurações a partir da classe Config (chaves como SECRET_KEY, DB URI, etc.).
Config.init_app(app)  # Executa inicialização adicional definida em Config (ex.: registrar filtros, loggers ou integrações).

# Inicializar banco de dados  # | explicação: prepara a extensão SQLAlchemy para uso com este app Flask.
db.init_app(app)  # Liga a instância do SQLAlchemy ao app, permitindo uso de models, sessões e comandos.

# Criar tabelas se não existirem  # | explicação: abre um contexto de aplicação para executar código que depende do app (como operações de DB).
with app.app_context():  # Entra no contexto da aplicação para que extensões como SQLAlchemy saibam qual app está ativo.
    # Importar modelos para garantir que sejam registrados  # | explicação: garante que os modelos sejam carregados para que o SQLAlchemy conheça suas tabelas.
    from models import Produto, Admin, Configuracao, Subcategoria  # Importa os modelos necessários; isso registra metadata das tabelas.
    db.create_all()  # Cria fisicamente as tabelas no banco caso ainda não existam, com base nos modelos importados.

# Registrar Blueprint do Admin  # | explicação: adiciona o conjunto de rotas do painel administrativo no app principal.
app.register_blueprint(admin_bp)  # Registra o blueprint 'admin_bp', ativando URLs/rotas definidas no módulo admin_routes.

# ========================================  # | explicação: separador visual de seções (sem efeito de execução).
# ROTAS DO SITE  # | explicação: cabeçalho da seção de rotas públicas do site.
# ========================================  # | explicação: separador visual de seções (sem efeito de execução).

@app.route("/")  # Define a rota HTTP GET para o caminho raiz; quando acessada, chama a função abaixo.
def home():  # Declara a função de view responsável por atender a rota "/" (página inicial).
    """Página inicial"""  # Docstring da função; descreve que esta view renderiza a página inicial.
    return render_template("index.html")  # Renderiza e retorna o template 'index.html' para o cliente.

@app.route("/about")  # Mapeia a URL '/about' para a função abaixo.
def about():  # Define a view da página "sobre".
    """Página sobre"""  # Docstring descritiva da view.
    return render_template("about.html")  # Renderiza o template 'about.html'.

@app.route("/contact")  # Mapeia a URL '/contact' para a função abaixo.
def contact():  # Define a view da página de contato.
    """Página de contato"""  # Docstring descritiva da view.
    return render_template("contact.html")  # Renderiza o template 'contact.html'.

@app.route("/shop")  # Mapeia a URL '/shop' para a função abaixo.
def shop():  # Define a view da listagem da loja com filtros.
    """Página da loja com filtros hierárquicos (3 níveis)"""  # Docstring descrevendo que há filtros (categoria/subcategoria/tipo).
    from models import Produto, Subcategoria  # Importa localmente para evitar import circular e carregar os modelos necessários.
    from config import Config  # Importa Config localmente para acessar CATEGORY_HIERARCHY ao renderizar.

    # Filtros da URL (3 níveis)  # | explicação: as variáveis abaixo leem parâmetros de query string para filtrar produtos.
    categoria_filtro = request.args.get('categoria')  # Nível 1: lê 'categoria' (ex.: Roupas, Brincos) da URL para filtrar.
    subcategoria_filtro = request.args.get('subcategoria')  # Nível 2: lê 'subcategoria' (ex.: Feminino/Masculino) da URL.
    tipo_filtro = request.args.get('tipo')  # Nível 3: lê 'tipo' (ex.: Vestido, Camisa) da URL.
    preco_filtro = request.args.get('preco')  # Lê filtro de faixa de preço (ex.: '0-50', '50-100', etc.).

    # Query base: produtos ativos  # | explicação: inicia uma consulta apenas para produtos marcados como ativos.
    query = Produto.query.filter_by(ativo=True)  # Cria a query base filtrando pela coluna 'ativo=True'.

    # Aplicar filtro de categoria (Nível 1)  # | explicação: se 'categoria' foi fornecida, restringe a consulta por essa coluna.
    if categoria_filtro:  # Verifica se o parâmetro de categoria existe.
        query = query.filter_by(categoria=categoria_filtro)  # Adiciona filtro exato na coluna 'categoria'.

    # Aplicar filtro de subcategoria (Nível 2 - Feminino/Masculino)  # | explicação: aplica filtro por subcategoria se fornecido.
    if subcategoria_filtro:  # Verifica se o parâmetro de subcategoria existe.
        query = query.filter_by(subcategoria=subcategoria_filtro)  # Restringe a consulta pela coluna 'subcategoria'.

    # Aplicar filtro de tipo (Nível 3 - Vestido/Camisa/etc.)  # | explicação: aplica filtro pelo tipo específico do produto.
    if tipo_filtro:  # Verifica se o parâmetro de tipo existe.
        query = query.filter_by(tipo=tipo_filtro)  # Restringe a consulta pela coluna 'tipo'.

    # Aplicar filtro de preço  # | explicação: aplica diferentes faixas de preço usando comparações na coluna 'preco'.
    if preco_filtro:  # Executa apenas se o filtro de preço foi informado.
        if preco_filtro == '0-50':  # Caso a faixa seja de 0 até 50 (inclusive).
            query = query.filter(Produto.preco <= 50)  # Filtra produtos com preço menor ou igual a 50.
        elif preco_filtro == '50-100':  # Faixa maior que 50 e até 100.
            query = query.filter(Produto.preco > 50, Produto.preco <= 100)  # Aplica intervalo aberto-fechado (50, 100].
        elif preco_filtro == '100-200':  # Faixa maior que 100 e até 200.
            query = query.filter(Produto.preco > 100, Produto.preco <= 200)  # Aplica intervalo (100, 200].
        elif preco_filtro == '200+':  # Faixa acima de 200.
            query = query.filter(Produto.preco > 200)  # Filtra produtos com preço estritamente maior que 200.

    # Ordenar e buscar  # | explicação: finaliza a consulta ordenando e materializando os resultados.
    produtos = query.order_by(Produto.ordem).all()  # Ordena pela coluna 'ordem' e executa a query retornando lista de Produtos.

    # Buscar subcategorias antigas (legado - manter compatibilidade)  # | explicação: carrega estrutura antiga de subcategorias ainda utilizada por templates/compatibilidade.
    subcategorias_legado = Subcategoria.query.filter_by(ativo=True).order_by(Subcategoria.categoria, Subcategoria.ordem).all()  # Consulta subcategorias ativas, ordenadas por categoria e ordem.

    return render_template(  # Renderiza o template da loja passando produtos e contexto de filtros/estrutura hierárquica.
        "shop.html",  # Nome do template.
        produtos=produtos,  # Lista de produtos filtrados/ordenados para exibir.
        categoria_filtro=categoria_filtro,  # Valor atual do filtro de categoria (para manter estado no UI).
        subcategoria_filtro=subcategoria_filtro,  # Valor atual do filtro de subcategoria.
        tipo_filtro=tipo_filtro,  # Valor atual do filtro de tipo.
        preco_filtro=preco_filtro,  # Valor atual do filtro de preço.
        subcategorias=subcategorias_legado,  # Legado  # | explicação: envia a lista do modelo antigo para compatibilidade de template.
        hierarchy=Config.CATEGORY_HIERARCHY  # Passa o dicionário/estrutura de hierarquia de categorias definido em Config.
    )  # Fecha a chamada de render_template.

@app.route("/shop/<int:produto_id>")  # Define rota com parâmetro de caminho inteiro 'produto_id' para a página de produto.
def shop_single(produto_id):  # View que exibe detalhes de um produto específico pelo seu ID.
    """Página de produto individual"""  # Docstring descritiva.
    from models import Produto  # Importa localmente o modelo Produto para uso nesta view.

    # Buscar produto pelo ID  # | explicação: tenta obter o produto; lança 404 automaticamente se não existir.
    produto = Produto.query.get_or_404(produto_id)  # Busca por chave primária; se None, retorna resposta 404.

    # Buscar produtos relacionados (mesma categoria)  # | explicação: seleciona itens da mesma categoria, excluindo o atual e apenas ativos.
    produtos_relacionados = Produto.query.filter(  # Inicia construção da query para relacionados.
        Produto.categoria == produto.categoria,  # Critério: mesma categoria do produto atual.
        Produto.id != produto.id,  # Critério: ID diferente do atual para não repetir o mesmo produto.
        Produto.ativo == True  # Critério: somente produtos ativos.
    ).limit(4).all()  # Limita a 4 itens e executa a consulta.

    return render_template(  # Renderiza a página de produto com o item e seus relacionados.
        "shop-single.html",  # Template de página individual.
        produto=produto,  # Objeto Produto principal a ser exibido.
        produtos_relacionados=produtos_relacionados  # Lista de até 4 produtos relacionados.
    )  # Fecha render_template.

# ========================================  # | explicação: separador de seção visual.
# ROTAS DO CARRINHO  # | explicação: cabeçalho para as rotas de carrinho de compras (HTML e API).
# ========================================  # | explicação: separador de seção visual.

def get_session_id():  # Declara helper para obter/criar um ID de sessão de carrinho persistido no cookie de sessão.
    """Obtém ou cria um ID de sessão único para o carrinho"""  # Docstring explicando a função.
    if 'cart_session_id' not in session:  # Verifica se ainda não há um identificador de carrinho na sessão.
        session['cart_session_id'] = str(uuid.uuid4())  # Gera UUID v4 e salva como string na sessão para identificar o carrinho do usuário.
    return session['cart_session_id']  # Retorna o ID de sessão do carrinho (existente ou recém-criado).

@app.route("/carrinho")  # Rota de página para visualizar o carrinho atual do usuário.
def carrinho():  # View que monta os itens do carrinho e calcula total para exibir no template.
    """Página do carrinho de compras"""  # Docstring descritiva.
    from models import ItemCarrinho  # Importa modelo de item do carrinho (contém refs a produto, quantidade, tamanho, sessão).

    session_id = get_session_id()  # Obtém o identificador único da sessão do carrinho.
    itens = ItemCarrinho.query.filter_by(session_id=session_id).all()  # Busca todos os itens do carrinho associados a esta sessão.

    # Calcular total  # | explicação: soma preço*quantidade de cada item; acessa relação item.produto.preco.
    total = sum(item.produto.preco * item.quantidade for item in itens)  # Gera o total bruto dos itens no carrinho atual.

    return render_template("carrinho.html", itens=itens, total=total)  # Renderiza o template do carrinho passando itens e total.

@app.route("/api/carrinho/adicionar", methods=['POST'])  # Define endpoint de API para adicionar itens via requisição POST com JSON.
def adicionar_ao_carrinho():  # Função que processa inclusão de produto ao carrinho na sessão atual.
    """Adiciona um produto ao carrinho"""  # Docstring explicando a ação da rota.
    from models import ItemCarrinho, Produto  # Importa modelos necessários: item do carrinho e produto.

    try:  # Inicia bloco para capturar e tratar exceções de forma a responder JSON de erro.
        data = request.get_json()  # Lê o corpo JSON da requisição (deve conter produto_id, quantidade, tamanho).
        produto_id = data.get('produto_id')  # Extrai o ID do produto a ser adicionado.
        quantidade = data.get('quantidade', 1)  # Extrai a quantidade (padrão 1 se não fornecida).
        tamanho = data.get('tamanho')  # Extrai variante/atributo 'tamanho' se aplicável (pode ser None).

        if not produto_id:  # Valida que o ID do produto foi informado.
            return jsonify({'success': False, 'message': 'Produto não especificado'}), 400  # Retorna erro 400 (requisição inválida).

        # Verificar se o produto existe  # | explicação: garante que o produto existe e está ativo antes de adicionar.
        produto = Produto.query.get(produto_id)  # Busca o produto por chave primária (pode retornar None).
        if not produto or not produto.ativo:  # Se produto não existe ou está inativo, bloqueia a adição.
            return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404  # Responde 404 (não encontrado).

        session_id = get_session_id()  # Obtém o ID de sessão do carrinho corrente.

        # Verificar se o item já existe no carrinho  # | explicação: tenta achar o mesmo produto/tamanho para somar quantidades.
        item_existente = ItemCarrinho.query.filter_by(  # Constrói consulta para identificar item igual já no carrinho.
            session_id=session_id,  # Mesma sessão.
            produto_id=produto_id,  # Mesmo produto.
            tamanho=tamanho  # Mesmo tamanho/variação.
        ).first()  # Obtém o primeiro correspondente ou None.

        if item_existente:  # Se já existe um item igual no carrinho,
            # Atualizar quantidade  # | explicação: incrementa a quantidade acumulando com a nova solicitada.
            item_existente.quantidade += quantidade  # Soma a quantidade recebida à quantidade atual do item.
        else:  # Caso contrário (ainda não existe item igual),
            # Criar novo item  # | explicação: instancia um novo ItemCarrinho com os dados fornecidos.
            novo_item = ItemCarrinho(  # Cria o objeto de item de carrinho.
                session_id=session_id,  # Relaciona à sessão do usuário.
                produto_id=produto_id,  # Associa ao produto escolhido.
                quantidade=quantidade,  # Define a quantidade inicial.
                tamanho=tamanho  # Define o tamanho/variação (pode ser None).
            )  # Fecha o construtor do ItemCarrinho.
            db.session.add(novo_item)  # Adiciona o novo item à sessão de transação do banco.

        db.session.commit()  # Confirma a transação, persistindo alterações (insert/update) no banco.

        # Contar total de itens no carrinho  # | explicação: agrega a soma das quantidades dos itens desta sessão.
        total_itens = db.session.query(db.func.sum(ItemCarrinho.quantidade)).filter_by(  # Monta query de agregação SUM sobre quantidades.
            session_id=session_id  # Filtra pelos itens da sessão corrente.
        ).scalar() or 0  # Extrai o valor escalar; se None (carrinho vazio), usa 0.

        return jsonify({  # Retorna resposta JSON de sucesso com mensagem e total de itens após inserção.
            'success': True,  # Indica operação bem-sucedida.
            'message': 'Produto adicionado ao carrinho',  # Mensagem informativa ao cliente.
            'total_itens': total_itens  # Total agregado de itens no carrinho.
        })  # Fecha o dicionário de resposta.

    except Exception as e:  # Captura qualquer exceção ocorrida no bloco try.
        db.session.rollback()  # Desfaz alterações pendentes na transação para manter consistência do banco.
        return jsonify({'success': False, 'message': str(e)}), 500  # Responde erro 500 com a mensagem da exceção para diagnóstico.

@app.route("/api/carrinho/remover/<int:item_id>", methods=['DELETE'])  # Define endpoint DELETE para remover item específico pelo ID.
def remover_do_carrinho(item_id):  # Função que processa a remoção de um item do carrinho.
    """Remove um item do carrinho"""  # Docstring da rota explicando a ação.
    from models import ItemCarrinho  # Importa o modelo do item do carrinho.

    try:  # Bloco para tratamento de exceções.
        session_id = get_session_id()  # Obtém o ID da sessão de carrinho.
        item = ItemCarrinho.query.filter_by(id=item_id, session_id=session_id).first()  # Busca item pelo ID garantindo que pertence à sessão atual.

        if not item:  # Se o item não foi encontrado,
            return jsonify({'success': False, 'message': 'Item não encontrado'}), 404  # Retorna 404 informando inexistência.

        db.session.delete(item)  # Marca o item para remoção no banco.
        db.session.commit()  # Confirma a remoção persistindo no banco.

        # Contar total de itens no carrinho  # | explicação: recalcula a soma de quantidades após a remoção.
        total_itens = db.session.query(db.func.sum(ItemCarrinho.quantidade)).filter_by(  # Agrega novamente sobre os itens restantes.
            session_id=session_id  # Filtra pela sessão atual.
        ).scalar() or 0  # Se não houver itens, retorna 0.

        return jsonify({  # Retorna JSON de sucesso pós-remoção.
            'success': True,  # Indica sucesso.
            'message': 'Item removido do carrinho',  # Mensagem ao cliente.
            'total_itens': total_itens  # Novo total de itens após a operação.
        })  # Fecha o dicionário de resposta.

    except Exception as e:  # Captura erros inesperados.
        db.session.rollback()  # Reverte transação para estado consistente.
        return jsonify({'success': False, 'message': str(e)}), 500  # Retorna erro 500 com mensagem.

@app.route("/api/carrinho/atualizar/<int:item_id>", methods=['PUT'])  # Define endpoint PUT para atualizar a quantidade de um item pelo ID.
def atualizar_carrinho(item_id):  # Função que trata atualização de quantidade de um item do carrinho.
    """Atualiza a quantidade de um item no carrinho"""  # Docstring descritiva da função.
    from models import ItemCarrinho  # Importa o modelo do item do carrinho.

    try:  # Inicia tratamento de exceções.
        data = request.get_json()  # Lê payload JSON com a nova quantidade.
        quantidade = data.get('quantidade', 1)  # Obtém valor de 'quantidade'; padrão 1 se ausente.

        if quantidade < 1:  # Validação: não permite quantidade menor que 1.
            return jsonify({'success': False, 'message': 'Quantidade inválida'}), 400  # Retorna 400 por entrada inválida.

        session_id = get_session_id()  # Obtém a sessão do carrinho.
        item = ItemCarrinho.query.filter_by(id=item_id, session_id=session_id).first()  # Busca o item garantindo que pertence à sessão atual.

        if not item:  # Se o item não existir,
            return jsonify({'success': False, 'message': 'Item não encontrado'}), 404  # Retorna 404.

        item.quantidade = quantidade  # Atualiza o campo 'quantidade' do item com o novo valor.
        db.session.commit()  # Confirma a alteração no banco.

        # Contar total de itens no carrinho  # | explicação: recalcula soma de quantidades após a atualização.
        total_itens = db.session.query(db.func.sum(ItemCarrinho.quantidade)).filter_by(  # Executa agregação SUM.
            session_id=session_id  # Filtra pela sessão.
        ).scalar() or 0  # Se sem itens, resulta em 0.

        subtotal = item.produto.preco * item.quantidade  # Calcula subtotal do item (preço unitário vezes quantidade atualizada).

        return jsonify({  # Responde com sucesso e dados atualizados.
            'success': True,  # Indica operação concluída.
            'message': 'Carrinho atualizado',  # Mensagem informativa.
            'subtotal': subtotal,  # Subtotal do item após a alteração.
            'total_itens': total_itens  # Total agregado de itens no carrinho.
        })  # Fecha dicionário de resposta.

    except Exception as e:  # Captura exceções.
        db.session.rollback()  # Reverte a transação em caso de erro.
        return jsonify({'success': False, 'message': str(e)}), 500  # Retorna 500 com mensagem da exceção.

@app.route("/api/carrinho/total")  # Endpoint GET que retorna apenas o total de itens no carrinho atual.
def carrinho_total():  # View que calcula e devolve o total de itens como JSON.
    """Retorna o total de itens no carrinho"""  # Docstring explicativa.
    from models import ItemCarrinho  # Importa o modelo de item do carrinho.

    session_id = get_session_id()  # Obtém o ID da sessão do carrinho.
    total_itens = db.session.query(db.func.sum(ItemCarrinho.quantidade)).filter_by(  # Soma as quantidades de todos os itens da sessão.
        session_id=session_id  # Filtra por sessão atual.
    ).scalar() or 0  # Extrai o valor numérico; se None, usa 0.

    return jsonify({'total_itens': total_itens})  # Retorna JSON contendo o total de itens.

# ========================================  # | explicação: separador de seção visual.
# FILTROS JINJA2 PERSONALIZADOS  # | explicação: cabeçalho para funções registradas como filtros de template.
# ========================================  # | explicação: separador de seção visual.

@app.template_filter('currency')  # Registra a função abaixo como filtro Jinja2 chamado 'currency'.
def currency_filter(value):  # Define função que formata números como moeda brasileira.
    """Formata valor como moeda brasileira"""  # Docstring explicando a função do filtro.
    try:  # Tenta converter e formatar o valor.
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')  # Converte para float e formata com 2 casas; ajusta separadores para padrão PT-BR.
    except (ValueError, TypeError):  # Trata casos em que value não é número ou é None.
        return "R$ 0,00"  # Retorna valor padrão de moeda.

@app.template_filter('from_json')  # Registra a função abaixo como filtro Jinja2 chamado 'from_json'.
def from_json_filter(value):  # Define função que converte string JSON em lista Python.
    """Converte string JSON para lista Python"""  # Docstring explicando a conversão esperada.
    import json  # Importa o módulo json localmente (escopo da função) para desserialização.
    try:  # Tenta interpretar a string JSON.
        return json.loads(value) if value else []  # Se houver valor, faz json.loads; caso contrário retorna lista vazia.
    except (ValueError, TypeError):  # Captura erros de parsing ou tipo inválido.
        return []  # Em caso de erro, retorna lista vazia para evitar quebrar o template.

# ========================================  # | explicação: separador de seção visual.
# CONTEXTO GLOBAL (disponível em todos os templates)  # | explicação: cabeçalho da seção que injeta variáveis globais.
# ========================================  # | explicação: separador de seção visual.

@app.context_processor  # Decora a função para que seu retorno seja mesclado no contexto de todos os templates renderizados.
def inject_global_vars():  # Função que injeta variáveis globais acessíveis em qualquer template.
    """Injeta variáveis globais em todos os templates"""  # Docstring descritiva da responsabilidade da função.
    from models import Configuracao  # Importa o modelo Configuracao para buscar valores dinâmicos armazenados no DB.
    
    return {  # Retorna um dicionário com chaves/valores que ficarão disponíveis nos templates.
        'loja_nome': Configuracao.get_valor('loja_nome', 'Xodó da Preta'),  # Nome da loja; busca no DB com default caso ausente.
        'loja_telefone': Configuracao.get_valor('loja_telefone', '55 11 954375056'),  # Telefone da loja; idem com valor padrão.
        'loja_email': Configuracao.get_valor('loja_email', 'contato@xododapreta.com'),  # E-mail de contato; idem.
        'loja_instagram': Configuracao.get_valor('loja_instagram', '@xododapreta'),  # Handle do Instagram; idem.
    }  # Fecha o dicionário devolvido ao contexto global.

# ========================================  # | explicação: separador de seção visual.
# EXECUTAR APLICAÇÃO  # | explicação: cabeçalho da seção de bootstrap do servidor de desenvolvimento.
# ========================================  # | explicação: separador de seção visual.

if __name__ == "__main__":  # Executa este bloco apenas quando o arquivo é invocado diretamente (não quando importado como módulo).
    app.run(debug=True)  # Inicia o servidor de desenvolvimento do Flask com debug ativo (hot reload e tracebacks detalhados; não usar em produção).

# Referência do arquivo comentado: :contentReference[oaicite:0]{index=0}  # | explicação: citação da origem do código analisado.


------------------------------------------------------models.py-----------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
from datetime import datetime  # Importa datetime para registrar timestamps de criação/atualização em colunas DateTime.
from database import db  # Importa a instância do SQLAlchemy usada para declarar modelos e operar o banco.
from werkzeug.security import generate_password_hash, check_password_hash  # Importa utilitários para gerar/verificar hash de senha de admins.


class Subcategoria(db.Model):  # Declara o modelo ORM 'Subcategoria' mapeado a uma tabela no banco via SQLAlchemy.
    """Modelo para subcategorias de produtos"""  # Docstring que descreve a finalidade desta classe (metadado, sem efeito em runtime).
    __tablename__ = 'subcategorias'  # Define explicitamente o nome da tabela no banco como 'subcategorias'.

    id = db.Column(db.Integer, primary_key=True)  # Coluna inteira auto-incremental que identifica unicamente a subcategoria.
    nome = db.Column(db.String(50), nullable=False)  # Coluna de texto curto para o nome; obrigatório (não nulo).
    categoria = db.Column(db.String(50), nullable=False)  # Categoria pai  # | explicação: string que agrupa subcategorias sob uma categoria principal; obrigatório.
    ativo = db.Column(db.Boolean, default=True)  # Flag booleana indicando se a subcategoria está ativa; padrão True.
    ordem = db.Column(db.Integer, default=0)  # Para ordenação  # | explicação: inteiro para controlar ordenação em listagens.
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp de criação; padrão é o horário UTC no momento da inserção.

    # Relacionamento com produtos  # | explicação: comentário existente; abaixo é estabelecido relacionamento ORM com Produto.
    produtos = db.relationship('Produto', backref='subcategoria_obj', lazy=True)  # Define relação 1:N com Produto; cria backref 'subcategoria_obj' acessível em Produto; lazy=True carrega lista sob demanda.

    def __repr__(self):  # Método de representação para depuração/logs.
        return f'<Subcategoria {self.categoria} - {self.nome}>'  # Retorna string legível contendo categoria e nome da subcategoria.

    def to_dict(self):  # Converte a instância em dicionário simples (útil para APIs/serialização).
        """Converte a subcategoria para dicionário"""  # Docstring que descreve a transformação realizada.
        return {  # Retorna um dict com campos selecionados da subcategoria.
            'id': self.id,  # Mapeia o id da subcategoria.
            'nome': self.nome,  # Mapeia o nome.
            'categoria': self.categoria,  # Mapeia a categoria pai.
            'ativo': self.ativo,  # Mapeia o status de atividade.
            'ordem': self.ordem  # Mapeia a posição preferida de ordenação.
        }  # Fecha o dicionário retornado.


class Produto(db.Model):  # Declara o modelo ORM 'Produto' representando itens vendáveis.
    """Modelo para produtos da loja"""  # Docstring descritiva do modelo.
    __tablename__ = 'produtos'  # Define explicitamente o nome da tabela como 'produtos'.

    id = db.Column(db.Integer, primary_key=True)  # Chave primária inteira auto-incremental do produto.
    nome = db.Column(db.String(100), nullable=False)  # Nome do produto (até 100 chars); obrigatório.
    descricao = db.Column(db.Text, nullable=True)  # Texto longo opcional com a descrição.
    preco = db.Column(db.Float, nullable=False)  # Preço numérico (float) obrigatório do produto.
    categoria = db.Column(db.String(50), nullable=False)  # Nível 1: Brincos, Roupas, Colares, etc.  # | explicação: classificação principal obrigatória.
    subcategoria = db.Column(db.String(50), nullable=True)  # Nível 2: Feminino, Masculino (para Roupas)  # | explicação: subclassificação textual opcional.
    tipo = db.Column(db.String(50), nullable=True)  # Nível 3: Vestido, Camisa, Saia, etc.  # | explicação: granularidade adicional opcional.
    subcategoria_id = db.Column(db.Integer, db.ForeignKey('subcategororias.id'), nullable=True)  # Legado - manter por compatibilidade  # possível erro de sintaxe: o nome da tabela de referência está escrito 'subcategororias' mas a tabela definida é 'subcategorias'; isso quebra a FK em runtime/migração.
    tamanhos = db.Column(db.String(200), nullable=True)  # JSON string: ["P", "M", "G"]  # | explicação: armazena string JSON com opções de tamanho; requer parsing para lista.
    imagem = db.Column(db.String(200), nullable=True)  # Nome do arquivo  # | explicação: caminho/nome do arquivo de imagem associado (normalmente relativo ao static).
    ordem = db.Column(db.Integer, default=0)  # Para ordenação personalizada  # | explicação: inteiro usado para ordenar listagens de produtos.
    ativo = db.Column(db.Boolean, default=True)  # Produto visível ou não  # | explicação: controla a exibição do produto no catálogo.
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp de criação do registro (UTC no momento do insert).
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp de atualização; atualizado automaticamente em updates.

    def __repr__(self):  # Representação legível do produto para debugging/logs.
        return f'<Produto {self.nome}>'  # Retorna string incluindo o nome do produto.

    def to_dict(self):  # Serializa a entidade Produto para dicionário (para APIs/templates).
        """Converte o produto para dicionário"""  # Docstring descritiva do método.
        return {  # Constrói e retorna um dicionário com campos selecionados.
            'id': self.id,  # ID do produto.
            'nome': self.nome,  # Nome do produto.
            'descricao': self.descricao,  # Descrição textual do produto.
            'preco': self.preco,  # Preço do produto.
            'categoria': self.categoria,  # Categoria (nível 1).
            'subcategoria': self.subcategoria,  # Subcategoria (nível 2) textual.
            'tipo': self.tipo,  # Tipo (nível 3) textual.
            'subcategoria_id': self.subcategoria_id,  # FK opcional para tabela de subcategorias (legado).
            'subcategoria_nome': self.subcategoria_obj.nome if self.subcategoria_obj else None,  # Nome da subcategoria via relacionamento; None se ausente.
            'tamanhos': self.tamanhos,  # JSON string com tamanhos disponíveis.
            'imagem': self.imagem,  # Nome/caminho de imagem do produto.
            'ordem': self.ordem,  # Posição preferida em listagens.
            'ativo': self.ativo,  # Flag de visibilidade do produto.
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y') if self.data_criacao else None  # Data de criação formatada pt-BR ou None se não houver.
        }  # Fecha o dicionário retornado.


class Admin(db.Model):  # Declara o modelo ORM 'Admin' para usuários administradores do sistema.
    """Modelo para administradores do sistema"""  # Docstring explicativa do modelo.
    __tablename__ = 'admins'  # Define a tabela como 'admins'.
    
    id = db.Column(db.Integer, primary_key=True)  # Chave primária inteira do admin.
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nome de usuário único; obrigatório para login/identificação.
    password_hash = db.Column(db.String(200), nullable=False)  # Hash da senha (nunca armazena a senha em texto claro); obrigatório.
    email = db.Column(db.String(120), unique=True, nullable=True)  # E-mail único opcional para contato/recuperação.
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp de criação do registro.
    ultimo_login = db.Column(db.DateTime, nullable=True)  # Armazena o último timestamp de login; opcional.
    
    def set_password(self, password):  # Método para definir a senha aplicando hash antes de persistir.
        """Define a senha (com hash)"""  # Docstring do método.
        self.password_hash = generate_password_hash(password)  # Gera hash do texto 'password' e salva em password_hash.

    def check_password(self, password):  # Método para verificar se uma senha em texto corresponde ao hash armazenado.
        """Verifica se a senha está correta"""  # Docstring do método.
        return check_password_hash(self.password_hash, password)  # Retorna True se a senha corresponder ao hash; caso contrário False.
    
    def __repr__(self):  # Representação legível do admin.
        return f'<Admin {self.username}>'  # Retorna string contendo o username do admin.


class Configuracao(db.Model):  # Modelo ORM para armazenar pares chave/valor de configuração da loja.
    """Modelo para configurações da loja"""  # Docstring do modelo.
    __tablename__ = 'configuracoes'  # Nome da tabela explicitamente definido.

    id = db.Column(db.Integer, primary_key=True)  # Chave primária da configuração.
    chave = db.Column(db.String(50), unique=True, nullable=False)  # Nome único da configuração; obrigatório.
    valor = db.Column(db.Text, nullable=True)  # Valor associado (texto arbitrário), opcional.
    descricao = db.Column(db.String(200), nullable=True)  # Descrição/ajuda opcional sobre o uso da configuração.
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp atualizado automaticamente em alterações.

    def __repr__(self):  # Representação legível da configuração.
        return f'<Configuracao {self.chave}>'  # Retorna string com a chave da configuração.

    @staticmethod  # Indica que o método abaixo não depende da instância (pode ser chamado via classe).
    def get_valor(chave, default=None):  # Recupera o valor de uma configuração por chave, com fallback 'default' se não existir.
        """Obtém o valor de uma configuração"""  # Docstring do método utilitário.
        config = Configuracao.query.filter_by(chave=chave).first()  # Executa consulta ORM filtrando por 'chave' e retorna o primeiro resultado ou None.
        return config.valor if config else default  # Retorna o valor armazenado se encontrado; caso contrário retorna o padrão fornecido.

    @staticmethod  # Método estático pois não usa 'self' nem estado de instâncias.
    def set_valor(chave, valor, descricao=None):  # Define/atualiza uma configuração pela chave; opcionalmente atualiza a descrição.
        """Define o valor de uma configuração"""  # Docstring do método utilitário de escrita.
        config = Configuracao.query.filter_by(chave=chave).first()  # Busca configuração existente com a mesma chave.
        if config:  # Se já existe um registro com a chave,
            config.valor = valor  # Atualiza o campo 'valor' existente.
            if descricao:  # Se uma descrição foi fornecida,
                config.descricao = descricao  # Atualiza também a descrição do registro.
        else:  # Caso não exista ainda,
            config = Configuracao(chave=chave, valor=valor, descricao=descricao)  # Cria nova instância de configuração com os valores fornecidos.
            db.session.add(config)  # Adiciona a nova configuração à sessão de transação.
        db.session.commit()  # Confirma (commit) a transação, persistindo as alterações no banco.
        return config  # Retorna o objeto de configuração criado/atualizado.


class ItemCarrinho(db.Model):  # Modelo ORM para representar um item adicionado ao carrinho (linha de carrinho).
    """Modelo para itens do carrinho de compras"""  # Docstring descritiva do modelo.
    __tablename__ = 'itens_carrinho'  # Define o nome da tabela como 'itens_carrinho'.

    id = db.Column(db.Integer, primary_key=True)  # Chave primária do item do carrinho.
    session_id = db.Column(db.String(100), nullable=False)  # ID da sessão do usuário  # | explicação: identifica a qual sessão (carrinho) o item pertence.
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)  # FK obrigatória referenciando o produto associado ao item.
    quantidade = db.Column(db.Integer, default=1)  # Quantidade do produto neste item; padrão 1.
    tamanho = db.Column(db.String(10), nullable=True)  # Tamanho selecionado (se aplicável)  # | explicação: variação escolhida (ex.: P/M/G); opcional.
    data_adicao = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp de quando o item foi adicionado ao carrinho.

    # Relacionamento com Produto  # | explicação: comentário existente; abaixo cria relacionamento para navegar do item ao Produto.
    produto = db.relationship('Produto', backref='itens_carrinho')  # Relacionamento N:1 para acessar o Produto; cria backref 'itens_carrinho' em Produto listando seus itens.

    def __repr__(self):  # Representação do item para logs/depuração.
        return f'<ItemCarrinho produto_id={self.produto_id} qtd={self.quantidade}>'  # Retorna string com produto_id e quantidade.

    def to_dict(self):  # Converte o item do carrinho em dicionário com dados do produto relacionado.
        """Converte o item do carrinho para dicionário"""  # Docstring explicando o retorno do método.
        return {  # Retorna dict com campos do item e alguns do produto associado.
            'id': self.id,  # ID do item no carrinho.
            'produto_id': self.produto_id,  # FK do produto associado.
            'produto_nome': self.produto.nome,  # Nome do produto via relacionamento.
            'produto_preco': self.produto.preco,  # Preço unitário do produto via relacionamento.
            'produto_imagem': self.produto.imagem,  # Nome/caminho da imagem do produto via relacionamento.
            'quantidade': self.quantidade,  # Quantidade do item.
            'tamanho': self.tamanho,  # Tamanho/variação selecionada (se houver).
            'subtotal': self.produto.preco * self.quantidade  # Valor parcial do item (preço unitário multiplicado pela quantidade).
        }  # Fecha o dicionário de retorno.

# Referência do arquivo comentado: :contentReference[oaicite:0]{index=0}  # | explicação: marca a origem do conteúdo analisado para rastreabilidade.

------------------------------------------------------admin_routes.py-----------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
"""  # Docstring de módulo: descreve o propósito geral do arquivo (metadado usado por ferramentas e help()).
Rotas do painel administrativo  # Parte do texto da docstring: indica que aqui ficam as rotas do admin.
"""  # Fecha a docstring do módulo.

from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # Importa utilitários do Flask: Blueprint (agrupa rotas), renderização de templates, acesso à req, redirecionamento, construção de URLs, mensagens flash e sessão.
from werkzeug.utils import secure_filename  # Importa função para sanitizar nomes de arquivos recebidos via upload (remove/normaliza caracteres perigosos).
from functools import wraps  # Importa wraps para preservar metadados de funções ao criar decorators.
import os  # Importa módulo padrão para operações de sistema de arquivos (ex.: splitext).
from pathlib import Path  # Importa Path para manipular caminhos de forma multiplataforma (aqui usado via Config, mas disponível).
from database import db  # Importa a instância do SQLAlchemy para operações de banco (session, commit, etc.).
from models import Produto, Admin, Configuracao, Subcategoria  # Importa modelos ORM usados nas consultas e operações CRUD.
from config import Config  # Importa configurações do app (ex.: diretórios de upload, extensões permitidas, listas de categorias).
import json  # Importa json para serializar/desserializar campos salvos como JSON (ex.: tamanhos).

# Criar Blueprint para rotas do admin  # Comentário explicativo de seção.
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')  # Cria Blueprint chamado 'admin' com prefixo '/admin' para namespacing das rotas.

# Decorator para proteger rotas (só admin logado acessa)  # Comentário explicativo do decorator abaixo.
def login_required(f):  # Define decorator que exige sessão de admin para acessar a rota.
    @wraps(f)  # Preserva nome/docstring/atributos da função original decorada.
    def decorated_function(*args, **kwargs):  # Função interna que envolverá a view original.
        if 'admin_logged_in' not in session:  # Verifica critério booleano: ausência de flag 'admin_logged_in' na sessão indica usuário não autenticado.
            flash('Você precisa estar logado para acessar esta página.', 'warning')  # Adiciona mensagem de alerta na fila de flashes.
            return redirect(url_for('admin.login'))  # Redireciona para a rota de login do admin.
        return f(*args, **kwargs)  # Se autenticado, delega a execução para a função original com os mesmos argumentos.
    return decorated_function  # Retorna o decorator configurado para uso nas rotas.

# Função auxiliar para upload de imagens  # Comentário de seção explicando utilitário de validação de arquivo.
def allowed_file(filename):  # Define helper que checa extensão do arquivo de upload.
    """Verifica se o arquivo tem extensão permitida"""  # Docstring do helper.
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS  # Obtém a extensão em minúsculas e verifica presença em Config.ALLOWED_EXTENSIONS.

def save_product_image(file):  # Define helper para salvar arquivo de imagem do produto e retornar o nome final salvo.
    """Salva imagem do produto e retorna o nome do arquivo"""  # Docstring do helper.
    if file and allowed_file(file.filename):  # Critério: só segue se o objeto existe e sua extensão for permitida.
        filename = secure_filename(file.filename)  # Normaliza o nome do arquivo para evitar caracteres/paths perigosos.
        # Adicionar timestamp para evitar conflitos  # Comentário explicando a estratégia de nome único.
        from datetime import datetime  # Importa datetime localmente para gerar timestamp (escopo restrito a esta função).
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Cria string de timestamp (ano-mês-dia-hora-minuto-segundo) para unicidade.
        name, ext = os.path.splitext(filename)  # Separa o nome base e a extensão preservando o ponto na extensão.
        filename = f"{name}_{timestamp}{ext}"  # Concatena nome base + '_' + timestamp + extensão para novo nome do arquivo.
        
        filepath = Config.UPLOAD_FOLDER / filename  # Constrói o caminho destino usando a pasta de upload definida em Config.
        file.save(filepath)  # Salva fisicamente o arquivo no caminho indicado (I/O em disco; cuidado com permissões).
        return filename  # Retorna o nome final salvo para persistência no banco.
    return None  # Caso arquivo inválido ou ausente, retorna None indicando que não houve gravação.

# ========================================  # Separador visual de seções (sem efeito de execução).
# ROTAS DE AUTENTICAÇÃO  # Cabeçalho da seção de autenticação do admin.
# ========================================  # Separador visual de seções (sem efeito de execução).

@admin_bp.route('/login', methods=['GET', 'POST'])  # Define rota '/admin/login' aceitando GET e POST para login.
def login():  # Declara a view do formulário de login e processamento da autenticação.
    """Página de login do admin"""  # Docstring descritiva da view.
    # Se já estiver logado, redireciona para dashboard  # Comentário explicando a verificação de sessão.
    if 'admin_logged_in' in session:  # Critério: se a flag de sessão existir, usuário já autenticado.
        return redirect(url_for('admin.dashboard'))  # Redireciona imediatamente para o dashboard.

    if request.method == 'POST':  # Se a requisição for POST (submissão do formulário de login),
        username = request.form.get('username')  # Lê o campo 'username' do formulário (None se ausente).
        password = request.form.get('password')  # Lê o campo 'password' do formulário (None se ausente).
        
        # Buscar admin no banco  # Comentário explicando a consulta ORM.
        admin = Admin.query.filter_by(username=username).first()  # Consulta o primeiro Admin com o username informado (ou None).

        if admin and admin.check_password(password):  # Critério: existe admin e a senha informada confere com o hash armazenado.
            # Login bem-sucedido  # Comentário informativo do bloco de sucesso.
            session['admin_logged_in'] = True  # Define flag de sessão indicando que o admin está autenticado.
            session['admin_id'] = admin.id  # Guarda ID do admin na sessão (pode ser usado para auditoria/consultas).
            session['admin_username'] = admin.username  # Guarda username na sessão para uso em templates/headers.
            
            # Atualizar último login  # Comentário explicando atualização de metadado de login.
            from datetime import datetime  # Importa datetime localmente para registrar timestamp UTC do último login.
            admin.ultimo_login = datetime.utcnow()  # Atualiza o campo 'ultimo_login' com horário atual em UTC.
            db.session.commit()  # Persiste a alteração no banco (transação com commit).

            flash('Login realizado com sucesso!', 'success')  # Enfileira mensagem de sucesso para feedback ao usuário.
            return redirect(url_for('admin.dashboard'))  # Redireciona ao dashboard após login.
        else:  # Se credenciais inválidas,
            flash('Usuário ou senha incorretos.', 'danger')  # Enfileira mensagem de erro (categoria 'danger').

    return render_template('admin/login.html')  # Em GET (ou após erro), renderiza o template de login.

@admin_bp.route('/logout')  # Define rota '/admin/logout' para finalizar sessão.
def logout():  # Declara view responsável por efetuar o logout.
    """Logout do admin"""  # Docstring descritiva da view.
    session.clear()  # Limpa todos os dados da sessão (remove flags e identificadores).
    flash('Logout realizado com sucesso!', 'info')  # Enfileira mensagem informativa de logout.
    return redirect(url_for('admin.login'))  # Redireciona ao formulário de login.

# ========================================  # Separador visual.
# DASHBOARD  # Cabeçalho da seção de dashboard.
# ========================================  # Separador visual.

@admin_bp.route('/')  # Mapeia a raiz do blueprint '/admin/' para o dashboard.
@admin_bp.route('/dashboard')  # Mapeia também '/admin/dashboard' para a mesma função.
@login_required  # Aplica o decorator de autenticação: bloqueia acesso a não logados.
def dashboard():  # Declara view do painel principal do admin.
    """Dashboard principal do admin"""  # Docstring da view.
    # Estatísticas  # Comentário de seção para métricas agregadas.
    total_produtos = Produto.query.count()  # Conta total de registros de produtos.
    produtos_ativos = Produto.query.filter_by(ativo=True).count()  # Conta produtos com flag 'ativo=True'.
    produtos_inativos = Produto.query.filter_by(ativo=False).count()  # Conta produtos com flag 'ativo=False'.
    
    # Produtos por categoria  # Comentário explicando o agrupamento manual por categoria configurada.
    categorias = {}  # Inicializa dict que mapeará categoria -> contagem de produtos.
    for categoria in Config.CATEGORIES:  # Itera pelas categorias definidas em Config (fonte de verdade para categorias).
        count = Produto.query.filter_by(categoria=categoria).count()  # Conta produtos cujo campo 'categoria' é igual ao iterado.
        categorias[categoria] = count  # Armazena a contagem no dicionário sob a chave da categoria.
    
    # Últimos produtos adicionados  # Comentário explicando ordenação por data.
    ultimos_produtos = Produto.query.order_by(Produto.data_criacao.desc()).limit(5).all()  # Busca 5 mais recentes pela data de criação em ordem decrescente.
    
    return render_template('admin/dashboard.html',  # Renderiza o template do dashboard do admin,
                         total_produtos=total_produtos,  # passando total de produtos para exibição.
                         produtos_ativos=produtos_ativos,  # passando contagem de ativos.
                         produtos_inativos=produtos_inativos,  # passando contagem de inativos.
                         categorias=categorias,  # passando dict de contagens por categoria.
                         ultimos_produtos=ultimos_produtos)  # passando lista dos últimos produtos.

# ========================================  # Separador visual.
# GERENCIAR PRODUTOS  # Cabeçalho da seção de CRUD de produtos.
# ========================================  # Separador visual.

@admin_bp.route('/produtos')  # Rota que lista produtos: '/admin/produtos'.
@login_required  # Protege a rota: requer login de admin.
def produtos():  # Declara view que lista produtos.
    """Lista todos os produtos"""  # Docstring da view.
    produtos = Produto.query.order_by(Produto.ordem, Produto.id.desc()).all()  # Busca todos os produtos ordenados por 'ordem' (asc) e depois 'id' (desc).
    return render_template('admin/produtos.html', produtos=produtos)  # Renderiza template com a lista obtida.

@admin_bp.route('/produtos/novo', methods=['GET', 'POST'])  # Rota para criar novo produto (form GET e submit POST).
@login_required  # Exige autenticação.
def produto_novo():  # Declara view de criação de produto.
    """Adicionar novo produto"""  # Docstring da view.
    if request.method == 'POST':  # Se envio de formulário,
        # Obter dados do formulário  # Comentário explicando extração dos campos.
        nome = request.form.get('nome')  # Lê campo 'nome'.
        descricao = request.form.get('descricao')  # Lê campo 'descricao'.
        preco = float(request.form.get('preco'))  # Lê e converte 'preco' para float (pode lançar ValueError se inválido).
        categoria = request.form.get('categoria')  # Lê 'categoria' (nível 1).
        subcategoria = request.form.get('subcategoria')  # Feminino/Masculino  # | explicação: campo textual opcional de nível 2.
        tipo = request.form.get('tipo')  # Vestido, Camisa, etc.  # | explicação: campo textual opcional de nível 3.
        subcategoria_id = request.form.get('subcategoria_id')  # Legado  # | explicação: possível referência por FK a Subcategoria.
        tamanhos = request.form.getlist('tamanhos')  # Lê múltiplos valores para tamanhos (lista de strings) do formulário.
        ativo = request.form.get('ativo') == 'on'  # Converte checkbox 'ativo' em booleano: True se 'on', senão False.
        ordem = int(request.form.get('ordem', 0))  # Converte 'ordem' para int, usando 0 como default.

        # Upload de imagem  # Comentário explicando o bloco de upload.
        imagem_file = request.files.get('imagem')  # Obtém o arquivo de upload sob a chave 'imagem' (None se não enviado).
        imagem_filename = save_product_image(imagem_file) if imagem_file else None  # Salva arquivo se presente e retorna nome; caso contrário None.

        # Criar produto  # Comentário explicando criação da instância ORM.
        produto = Produto(  # Instancia um Produto com os campos recebidos.
            nome=nome,  # Define nome.
            descricao=descricao,  # Define descrição.
            preco=preco,  # Define preço.
            categoria=categoria,  # Define categoria (nível 1).
            subcategoria=subcategoria if subcategoria else None,  # Define subcategoria ou None se vazio.
            tipo=tipo if tipo else None,  # Define tipo (nível 3) ou None se vazio.
            subcategoria_id=int(subcategoria_id) if subcategoria_id else None,  # Converte subcategoria_id para int se fornecido; senão None.
            tamanhos=json.dumps(tamanhos),  # Serializa lista de tamanhos para string JSON.
            imagem=imagem_filename,  # Define nome do arquivo de imagem salvo (ou None).
            ativo=ativo,  # Define flag de visibilidade.
            ordem=ordem  # Define ordem de exibição.
        )  # Fecha construção do objeto Produto.

        db.session.add(produto)  # Adiciona o novo produto à sessão de transação.
        db.session.commit()  # Efetiva a inserção no banco com commit.

        flash(f'Produto "{nome}" adicionado com sucesso!', 'success')  # Mensagem de sucesso informando o nome do produto.
        return redirect(url_for('admin.produtos'))  # Redireciona para a listagem de produtos.

    # Buscar todas as subcategorias para o formulário  # Comentário: prepara dados para o select do formulário.
    subcategorias = Subcategoria.query.filter_by(ativo=True).order_by(Subcategoria.categoria, Subcategoria.ordem).all()  # Busca subcategorias ativas, ordenadas por categoria e ordem.

    return render_template('admin/produto_form.html',  # Renderiza o template do formulário de produto,
                         categorias=Config.CATEGORIES,  # com a lista de categorias disponíveis (Config).
                         tamanhos_disponiveis=Config.SIZES,  # com tamanhos padrões configurados.
                         subcategorias=subcategorias,  # com subcategorias ativas para seleção.
                         produto=None)  # e None para indicar criação (não edição).

@admin_bp.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])  # Rota para editar um produto específico por ID.
@login_required  # Exige autenticação.
def produto_editar(produto_id):  # Declara view de edição, recebendo produto_id convertido para int pelo conversor da rota.
    """Editar produto existente"""  # Docstring da view.
    produto = Produto.query.get_or_404(produto_id)  # Carrega produto pelo ID ou retorna 404 se não encontrado.
    
    if request.method == 'POST':  # Se submit do formulário,
        # Atualizar dados  # Comentário explicando que os campos serão sobescritos.
        produto.nome = request.form.get('nome')  # Atualiza nome com valor do formulário.
        produto.descricao = request.form.get('descricao')  # Atualiza descrição.
        produto.preco = float(request.form.get('preco'))  # Atualiza preço convertendo para float.
        produto.categoria = request.form.get('categoria')  # Atualiza categoria (nível 1).
        produto.subcategoria = request.form.get('subcategoria') or None  # Atualiza subcategoria ou None se vazio.
        produto.tipo = request.form.get('tipo') or None  # Atualiza tipo (nível 3) ou None se vazio.
        subcategoria_id = request.form.get('subcategoria_id')  # Lê valor textual do formulário (pode ser vazio).
        produto.subcategoria_id = int(subcategoria_id) if subcategoria_id else None  # Converte para int se fornecido; senão None.
        produto.tamanhos = json.dumps(request.form.getlist('tamanhos'))  # Serializa lista de tamanhos selecionados para JSON.
        produto.ativo = request.form.get('ativo') == 'on'  # Atualiza flag 'ativo' com base no checkbox.
        produto.ordem = int(request.form.get('ordem', 0))  # Atualiza ordem, convertendo para int.

        # Upload de nova imagem (opcional)  # Comentário do bloco de substituição de imagem.
        imagem_file = request.files.get('imagem')  # Lê possível novo arquivo enviado.
        if imagem_file and imagem_file.filename:  # Critério: só processa se houve arquivo e ele tem nome (não vazio).
            # Deletar imagem antiga se existir  # Comentário explicando manutenção do storage.
            if produto.imagem:  # Se existe imagem anterior registrada,
                old_image_path = Config.UPLOAD_FOLDER / produto.imagem  # Constrói path completo da imagem antiga.
                if old_image_path.exists():  # Verifica se o arquivo físico realmente existe.
                    old_image_path.unlink()  # Exclui o arquivo do disco para evitar lixo.

            # Salvar nova imagem  # Comentário do fluxo de salvamento.
            produto.imagem = save_product_image(imagem_file)  # Salva novo arquivo e guarda o nome no produto.

        db.session.commit()  # Confirma as alterações no banco.

        flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'success')  # Mensagem de sucesso após atualização.
        return redirect(url_for('admin.produtos'))  # Volta para listagem.

    # Converter tamanhos de JSON para lista  # Comentário explicando a desserialização para preencher o formulário.
    tamanhos_produto = json.loads(produto.tamanhos) if produto.tamanhos else []  # Converte string JSON para lista; se None/vazio, usa lista vazia.

    # Buscar todas as subcategorias para o formulário  # Comentário: prepara select de subcategorias.
    subcategorias = Subcategoria.query.filter_by(ativo=True).order_by(Subcategoria.categoria, Subcategoria.ordem).all()  # Consulta subcategorias ativas ordenadas.

    return render_template('admin/produto_form.html',  # Renderiza template de edição,
                         categorias=Config.CATEGORIES,  # com categorias configuradas,
                         tamanhos_disponiveis=Config.SIZES,  # com tamanhos disponíveis,
                         subcategorias=subcategorias,  # com subcategorias ativas,
                         produto=produto,  # passando o objeto produto para popular o formulário,
                         tamanhos_produto=tamanhos_produto)  # e a lista de tamanhos marcados do produto.

@admin_bp.route('/produtos/<int:produto_id>/deletar', methods=['POST'])  # Rota para deletar um produto (POST para evitar deleção acidental por link).
@login_required  # Requer autenticação.
def produto_deletar(produto_id):  # Declara view que apaga produto por ID.
    """Deletar produto"""  # Docstring da view.
    produto = Produto.query.get_or_404(produto_id)  # Busca produto ou retorna 404 se inexistente.
    nome = produto.nome  # Salva o nome para usar na mensagem após a deleção.
    
    # Deletar imagem se existir  # Comentário explicando limpeza do storage.
    if produto.imagem:  # Se há imagem registrada,
        image_path = Config.UPLOAD_FOLDER / produto.imagem  # Monta caminho absoluto da imagem.
        if image_path.exists():  # Confirma existência do arquivo.
            image_path.unlink()  # Remove o arquivo do disco.

    db.session.delete(produto)  # Marca o objeto para remoção no banco.
    db.session.commit()  # Efetiva a remoção com commit.
    
    flash(f'Produto "{nome}" deletado com sucesso!', 'success')  # Mensagem de sucesso informando o nome deletado.
    return redirect(url_for('admin.produtos'))  # Redireciona para a listagem após deleção.

# ========================================  # Separador visual.
# CONFIGURAÇÕES  # Cabeçalho de seção para ajustes de configurações.
# ========================================  # Separador visual.

@admin_bp.route('/configuracoes', methods=['GET', 'POST'])  # Rota para visualizar/atualizar configurações da loja.
@login_required  # Exige autenticação.
def configuracoes():  # Declara view de configurações.
    """Configurações da loja"""  # Docstring da view.
    if request.method == 'POST':  # Se for submissão de formulário,
        # Atualizar configurações  # Comentário explicando atualização em lote.
        configs = [  # Lista de chaves de configuração que serão lidas do formulário.
            'loja_nome',  # Nome da loja.
            'loja_telefone',  # Telefone de contato.
            'loja_email',  # E-mail de contato.
            'loja_instagram',  # Handle do Instagram.
            'loja_endereco'  # Endereço físico.
        ]  # Fecha a lista de chaves.
        
        for config_key in configs:  # Itera em cada chave de configuração.
            valor = request.form.get(config_key)  # Lê o valor submetido para a chave atual.
            if valor:  # Se algum valor foi enviado (não vazio),
                Configuracao.set_valor(config_key, valor)  # Persiste/atualiza o valor no banco via método utilitário.

        flash('Configurações atualizadas com sucesso!', 'success')  # Mensagem de confirmação.
        return redirect(url_for('admin.configuracoes'))  # Redireciona para evitar reenvio do formulário (PRG pattern).
    
    # Buscar configurações atuais  # Comentário explicando a montagem do dict para o template.
    configs = {  # Constrói dicionário de configs atuais (com defaults quando ausentes).
        'loja_nome': Configuracao.get_valor('loja_nome', 'Xodó da Preta'),  # Busca valor ou usa default 'Xodó da Preta'.
        'loja_telefone': Configuracao.get_valor('loja_telefone', ''),  # Telefone ou string vazia se não definido.
        'loja_email': Configuracao.get_valor('loja_email', ''),  # Email ou vazio.
        'loja_instagram': Configuracao.get_valor('loja_instagram', ''),  # Instagram ou vazio.
        'loja_endereco': Configuracao.get_valor('loja_endereco', '')  # Endereço ou vazio.
    }  # Fecha o dicionário.

    return render_template('admin/config.html', configs=configs)  # Renderiza template de configurações com o dict 'configs'.

# ========================================  # Separador visual.
# GERENCIAR SUBCATEGORIAS  # Cabeçalho de seção para CRUD de subcategorias.
# ========================================  # Separador visual.

@admin_bp.route('/subcategorias')  # Rota para listar subcategorias.
@login_required  # Exige autenticação.
def subcategorias():  # Declara view que lista subcategorias.
    """Lista todas as subcategorias"""  # Docstring da view.
    subcategorias = Subcategoria.query.order_by(Subcategoria.categoria, Subcategoria.ordem).all()  # Busca todas as subcategorias ordenando por categoria e ordem.

    # Agrupar por categoria  # Comentário: monta estrutura {categoria: [subcats...]} para o template.
    subcategorias_por_categoria = {}  # Inicializa dict de agrupamento.
    for subcat in subcategorias:  # Itera cada subcategoria retornada.
        if subcat.categoria not in subcategorias_por_categoria:  # Se a categoria ainda não tem lista iniciada,
            subcategorias_por_categoria[subcat.categoria] = []  # Inicializa lista vazia para a categoria.
        subcategorias_por_categoria[subcat.categoria].append(subcat)  # Anexa a subcategoria à lista da categoria.

    return render_template('admin/subcategorias.html',  # Renderiza template com o agrupamento,
                         subcategorias_por_categoria=subcategorias_por_categoria,  # passando o dict agrupado,
                         categorias=Config.CATEGORIES)  # e a lista de categorias disponíveis.

@admin_bp.route('/subcategorias/nova', methods=['GET', 'POST'])  # Rota para criar nova subcategoria.
@login_required  # Exige autenticação.
def subcategoria_nova():  # Declara view de criação de subcategoria.
    """Adicionar nova subcategoria"""  # Docstring da view.
    if request.method == 'POST':  # Se envio do formulário,
        nome = request.form.get('nome')  # Lê campo 'nome' da subcategoria.
        categoria = request.form.get('categoria')  # Lê campo 'categoria' (categoria pai).
        ativo = request.form.get('ativo') == 'on'  # Converte checkbox 'ativo' para booleano.
        ordem = int(request.form.get('ordem', 0))  # Lê e converte 'ordem' para int (default 0).

        # Verificar se já existe  # Comentário: evita duplicidade de nome dentro da mesma categoria.
        existe = Subcategoria.query.filter_by(nome=nome, categoria=categoria).first()  # Procura subcategoria com mesmo nome e categoria.
        if existe:  # Se já houver uma igual,
            flash(f'Subcategoria "{nome}" já existe para a categoria "{categoria}".', 'warning')  # Mensagem de alerta ao usuário.
            return redirect(url_for('admin.subcategoria_nova'))  # Redireciona de volta ao formulário de criação.

        # Criar subcategoria  # Comentário explicando a criação da instância ORM.
        subcategoria = Subcategoria(  # Instancia Subcategoria com os dados informados.
            nome=nome,  # Define nome.
            categoria=categoria,  # Define categoria pai.
            ativo=ativo,  # Define status ativo/inativo.
            ordem=ordem  # Define ordem de exibição.
        )  # Fecha construção.

        db.session.add(subcategoria)  # Adiciona à sessão de transação do banco.
        db.session.commit()  # Efetiva a inserção.

        flash(f'Subcategoria "{nome}" adicionada com sucesso!', 'success')  # Mensagem de sucesso ao usuário.
        return redirect(url_for('admin.subcategorias'))  # Redireciona para a listagem de subcategorias.

    return render_template('admin/subcategoria_form.html',  # Em GET, renderiza template de criação,
                         categorias=Config.CATEGORIES,  # passando categorias disponíveis,
                         subcategoria=None)  # e None para indicar formulário em modo criação.

@admin_bp.route('/subcategorias/<int:subcategoria_id>/editar', methods=['GET', 'POST'])  # Rota para editar subcategoria por ID.
@login_required  # Exige autenticação.
def subcategoria_editar(subcategoria_id):  # Declara view de edição.
    """Editar subcategoria existente"""  # Docstring da view.
    subcategoria = Subcategoria.query.get_or_404(subcategoria_id)  # Busca subcategoria por ID ou 404 se não existir.

    if request.method == 'POST':  # Se foi submetido formulário,
        nome = request.form.get('nome')  # Lê novo nome.
        categoria = request.form.get('categoria')  # Lê nova categoria pai.

        # Verificar se já existe (exceto a atual)  # Comentário: checa duplicidade excluindo a própria subcategoria.
        existe = Subcategoria.query.filter(  # Constrói query com múltiplas condições.
            Subcategoria.nome == nome,  # Condição: mesmo nome.
            Subcategoria.categoria == categoria,  # Condição: mesma categoria.
            Subcategoria.id != subcategoria_id  # Condição: ID diferente (exclui o atual).
        ).first()  # Obtém primeiro resultado correspondente (ou None).

        if existe:  # Se encontrado duplicado,
            flash(f'Subcategoria "{nome}" já existe para a categoria "{categoria}".', 'warning')  # Mensagem de alerta.
            return render_template('admin/subcategoria_form.html',  # Reexibe formulário de edição,
                                 categorias=Config.CATEGORIES,  # passando categorias,
                                 subcategoria=subcategoria)  # e a subcategoria atual para preencher o form.

        # Atualizar dados  # Comentário indicando atualização dos campos.
        subcategoria.nome = nome  # Atualiza nome.
        subcategoria.categoria = categoria  # Atualiza categoria pai.
        subcategoria.ativo = request.form.get('ativo') == 'on'  # Atualiza flag ativo a partir do checkbox.
        subcategoria.ordem = int(request.form.get('ordem', 0))  # Atualiza ordem.

        db.session.commit()  # Salva alterações no banco.

        flash(f'Subcategoria "{subcategoria.nome}" atualizada com sucesso!', 'success')  # Mensagem de sucesso.
        return redirect(url_for('admin.subcategorias'))  # Redireciona para listagem.

    return render_template('admin/subcategoria_form.html',  # Em GET, renderiza formulário de edição,
                         categorias=Config.CATEGORIES,  # com categorias disponíveis,
                         subcategoria=subcategoria)  # e a subcategoria carregada para preencher os campos.

@admin_bp.route('/subcategorias/<int:subcategoria_id>/deletar', methods=['POST'])  # Rota para deletar subcategoria (POST).
@login_required  # Exige autenticação.
def subcategoria_deletar(subcategoria_id):  # Declara view que remove subcategoria por ID.
    """Deletar subcategoria"""  # Docstring da view.
    subcategoria = Subcategoria.query.get_or_404(subcategoria_id)  # Busca subcategoria ou 404.
    nome = subcategoria.nome  # Guarda o nome para mensagem.

    # Verificar se há produtos usando esta subcategoria  # Comentário: impede remoção se houver dependências.
    produtos_com_subcat = Produto.query.filter_by(subcategoria_id=subcategoria_id).count()  # Conta produtos que referenciam esta subcategoria.
    if produtos_com_subcat > 0:  # Critério: se houver ao menos um produto dependente,
        flash(f'Não é possível deletar a subcategoria "{nome}" pois existem {produtos_com_subcat} produto(s) associado(s).', 'danger')  # Mensagem de erro impedindo deleção.
        return redirect(url_for('admin.subcategorias'))  # Redireciona para a listagem sem remover.

    db.session.delete(subcategoria)  # Marca a subcategoria para remoção.
    db.session.commit()  # Confirma a operação no banco.

    flash(f'Subcategoria "{nome}" deletada com sucesso!', 'success')  # Mensagem de sucesso ao usuário.
    return redirect(url_for('admin.subcategorias'))  # Redireciona para a listagem de subcategorias.

@admin_bp.route('/api/subcategorias/<categoria>')  # Rota de API que retorna subcategorias ativas para uma categoria (uso em AJAX).
@login_required  # Exige autenticação para consumir a API (protege dados internos).
def api_subcategorias_por_categoria(categoria):  # Declara endpoint que recebe 'categoria' como parte da URL.
    """API para buscar subcategorias por categoria (para uso em AJAX)"""  # Docstring do endpoint.
    subcategorias = Subcategoria.query.filter_by(categoria=categoria, ativo=True).order_by(Subcategoria.ordem).all()  # Consulta subcategorias ativas da categoria informada, ordenando pela prioridade 'ordem'.
    return {  # Retorna diretamente um dict (Flask o serializa como JSON).
        'subcategorias': [subcat.to_dict() for subcat in subcategorias]  # Cria lista de dicts via to_dict() para cada subcategoria retornada.
    }  # Fecha o objeto de resposta JSON-like.

# Referência do arquivo comentado: :contentReference[oaicite:0]{index=0}  # | explicação: citação da origem do código analisado para rastreabilidade.
