# Scripts do Projeto - Xodo da Preta

Esta pasta contem scripts utilitarios para manutencao e desenvolvimento do projeto.

## Estrutura

```
scripts/
├── maintenance/             # Scripts de manutencao (seguros)
│   └── update_schema.py     # Atualiza schema do banco (nao-destrutivo)
├── dev/                     # Scripts de desenvolvimento
│   ├── DANGER_reset_database.py   # APAGA TUDO (destrutivo)
│   ├── populate_products.py       # Adiciona produtos de exemplo
│   └── popular_subcategorias.py   # Popula subcategorias padrao
└── README.md
```

---

## Scripts de Manutencao

### `maintenance/update_schema.py`

**SEGURO - NAO-DESTRUTIVO**

Atualiza o schema do banco de dados adicionando novos campos e tabelas sem apagar dados existentes.

**Uso:**
```bash
python scripts/maintenance/update_schema.py
```

**O que faz:**
- Adiciona campos: `destaque`, `visualizacoes`, `imagens_adicionais` (tabela produtos)
- Adiciona campo: `parent_id` (tabela subcategorias) - para hierarquia
- Cria tabela: `produto_visualizacoes` (analytics)
- Cria tabela: `conteudo_pagina` (CMS)
- Cria tabela: `cupons` (sistema de cupons de desconto)

**Caracteristicas:**
- Preserva todos os dados existentes
- Idempotente (pode executar varias vezes)
- Seguro para producao

---

## Scripts de Desenvolvimento

### `dev/DANGER_reset_database.py`

**PERIGO - DESTRUTIVO**

Reseta completamente o banco de dados. **APAGA TODOS OS DADOS!**

**Uso:**
```bash
python scripts/dev/DANGER_reset_database.py
```

**O que faz:**
- Apaga todas as tabelas (`db.drop_all()`)
- Recria todas as tabelas do zero
- Cria usuario admin padrao usando `ADMIN_USERNAME`/`ADMIN_PASSWORD` do `.env`
- Adiciona configuracoes iniciais da loja
- Cria 6 produtos de exemplo

**Quando usar:**
- Primeira instalacao do projeto
- Reset completo em ambiente de desenvolvimento
- Nunca em producao

**Protecoes:**
- Requer confirmacao dupla: `SIM APAGAR TUDO` + `CONFIRMO`

---

### `dev/populate_products.py`

**SEGURO**

Adiciona produtos de exemplo ao banco de dados para testes.

**Uso:**
```bash
python scripts/dev/populate_products.py
```

**O que faz:**
- Adiciona produtos de exemplo para todas as categorias
- Permite limpar produtos de exemplo anteriores

**Quando usar:**
- Apos setup inicial para ter dados de teste
- Para resetar produtos de demonstracao

---

### `dev/popular_subcategorias.py`

**MODERADO**

Popula a tabela de subcategorias com valores padrao da categoria Roupas.

**Uso:**
```bash
python scripts/dev/popular_subcategorias.py
```

**O que faz:**
- Cria subcategorias padrao:
  - Roupas > Feminino
  - Roupas > Masculino
  - Roupas > Unissex
- Permite apagar subcategorias existentes antes de criar

**Quando usar:**
- Primeira instalacao
- Para resetar subcategorias padrao
- Cuidado se ja houver subcategorias customizadas
