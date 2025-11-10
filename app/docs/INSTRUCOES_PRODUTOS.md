# Como Popular o Banco de Dados com Produtos de Exemplo

Este guia explica como adicionar produtos de exemplo ao banco de dados para testar o sistema.

## Produtos Incluídos no Script

O script `populate_products.py` cria **20 produtos de exemplo** distribuídos nas 5 categorias:

### Colares (3 produtos)
- Colar Africano Ouro - R$ 89,90
- Colar Afro Miçangas Coloridas - R$ 65,00
- Colar Étnico Madeira - R$ 75,50

### Anéis (4 produtos)
- Anel Africano Dourado - R$ 45,00
- Anel Afro Prata - R$ 55,00
- Anel Tribal Bronze - R$ 38,90
- Anel Geométrico Afro - R$ 42,00

### Pulseiras (5 produtos)
- Pulseira Afro Colorida - R$ 35,00
- Pulseira Tribal Couro - R$ 48,50
- Pulseira Miçangas Africanas - R$ 29,90
- Pulseira Étnica Dourada - R$ 52,00
- Pulseira Afro Mix - R$ 39,90

### Brincos (3 produtos)
- Brincos Afro Argola Grande - R$ 58,00
- Brincos Tribal Colorido - R$ 42,50
- Brincos Étnico Madeira - R$ 36,00

### Roupas (4 produtos)
- Vestido Africano Estampado - R$ 159,90
- Camisa Afro Print - R$ 98,00
- Saia Midi Afro - R$ 89,90
- Calça Africana Wide Leg - R$ 125,00

---

## Como Executar o Script

### Opção 1: Executar diretamente (Recomendado)

1. Abra o terminal/prompt de comando

2. Navegue até a pasta do projeto:
   ```bash
   cd C:\Users\lucas\OneDrive\Desktop\xodo_da_preta\Xod-da-Preta-\app
   ```

3. Execute o script:
   ```bash
   python populate_products.py
   ```

4. O script irá perguntar se você quer remover produtos de exemplo anteriores:
   - Digite `s` para SIM (remove produtos antigos e adiciona novos)
   - Digite `n` para NÃO (apenas adiciona novos produtos)

5. Aguarde a conclusão. Você verá uma mensagem como:
   ```
   ✓ 20 produtos criados com sucesso!

   ESTATÍSTICAS DO BANCO DE DADOS
   Total de produtos: 20
   Produtos ativos: 20

   Produtos por categoria:
     • Colares: 3 produtos
     • Anéis: 4 produtos
     • Pulseiras: 5 produtos
     • Brincos: 3 produtos
     • Roupas: 4 produtos
   ```

### Opção 2: Executar via Python Shell

```bash
cd C:\Users\lucas\OneDrive\Desktop\xodo_da_preta\Xod-da-Preta-\app
python
```

Dentro do shell Python:
```python
from main import app
from database import db
from models import Produto
import json

# Criar contexto da aplicação
with app.app_context():
    # Aqui você pode adicionar produtos manualmente
    produto = Produto(
        nome="Meu Produto",
        descricao="Descrição do produto",
        preco=99.90,
        categoria="Anéis",
        tamanhos=json.dumps(["P", "M", "G"]),
        ativo=True,
        ordem=1
    )
    db.session.add(produto)
    db.session.commit()
    print("Produto criado!")
```

---

## Testando os Filtros

Após executar o script:

1. **Inicie o servidor** (se ainda não estiver rodando):
   ```bash
   python main.py
   ```

2. **Acesse a loja**:
   - URL: http://localhost:5000/shop

3. **Teste os filtros**:
   - Clique em "Todos" para ver todos os produtos
   - Clique em "Colares" para ver apenas colares
   - Clique em "Anéis" para ver apenas anéis
   - Clique em "Pulseiras" para ver apenas pulseiras
   - Clique em "Brincos" para ver apenas brincos
   - Clique em "Roupas" para ver apenas roupas

4. **Teste os filtros de preço**:
   - "Até R$ 50" - mostra produtos até R$ 50,00
   - "R$ 50-100" - mostra produtos entre R$ 50 e R$ 100
   - "Acima de R$ 100" - mostra produtos acima de R$ 100

---

## Gerenciar Produtos no Painel Admin

1. **Acesse o painel**: http://localhost:5000/admin/login

2. **Faça login** com suas credenciais de admin

3. **Vá para "Produtos"** para:
   - Ver todos os produtos
   - Editar produtos existentes
   - Adicionar novos produtos
   - Deletar produtos
   - Alterar ordem de exibição
   - Ativar/desativar produtos

---

## Observações Importantes

- Todos os produtos de exemplo têm `[Produto de exemplo]` na descrição
- Os produtos de exemplo **não têm imagens** - você pode adicionar imagens pelo painel admin
- Para **remover apenas** produtos de exemplo, use o filtro pela descrição no banco
- Os produtos são criados como **ativos** por padrão
- Tamanhos estão em formato JSON: `["P", "M", "G"]` ou `["Único"]`

---

## Problemas Comuns

### Erro: "No module named 'main'"
**Solução**: Certifique-se de estar na pasta `app`:
```bash
cd C:\Users\lucas\OneDrive\Desktop\xodo_da_preta\Xod-da-Preta-\app
```

### Erro: "Table doesn't exist"
**Solução**: Execute o servidor uma vez para criar as tabelas:
```bash
python main.py
```
Aguarde o servidor iniciar, depois pare (Ctrl+C) e execute o script.

### Produtos duplicados
**Solução**: Execute o script novamente e escolha `s` para remover produtos anteriores.

---

## Próximos Passos

Depois de popular o banco:

1. **Adicione imagens reais** aos produtos pelo painel admin
2. **Ajuste preços e descrições** conforme necessário
3. **Teste o sistema de carrinho** adicionando produtos
4. **Teste os filtros** por categoria e preço
5. **Compartilhe o link** da loja com sua equipe para feedback

---

Qualquer dúvida, consulte a documentação ou entre em contato!
