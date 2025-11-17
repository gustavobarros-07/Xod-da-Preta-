# 📁 Scripts do Projeto - Xodó da Preta

Esta pasta contém scripts utilitários para manutenção e desenvolvimento do projeto.

## 📂 Estrutura

```
scripts/
├── maintenance/          # Scripts de manutenção (seguros)
│   └── update_schema.py  # Atualiza schema do banco (não-destrutivo)
├── dev/                  # Scripts de desenvolvimento
│   ├── DANGER_reset_database.py    # ⚠️ APAGA TUDO (destrutivo)
│   ├── populate_products.py        # Adiciona produtos de exemplo
│   └── popular_subcategorias.py    # Popula subcategorias padrão
└── README.md            # Esta documentação
```

---

## 🔧 Scripts de Manutenção

### `maintenance/update_schema.py`

**✅ SEGURO - NÃO-DESTRUTIVO**

Atualiza o schema do banco de dados adicionando novos campos e tabelas sem apagar dados existentes.

**Uso:**
```bash
python scripts/maintenance/update_schema.py
```

**O que faz:**
- ✅ Adiciona campos: `destaque`, `visualizacoes`, `imagens_adicionais` (tabela produtos)
- ✅ Adiciona campo: `parent_id` (tabela subcategorias) - para hierarquia
- ✅ Cria tabela: `produto_visualizacoes` (analytics)
- ✅ Cria tabela: `conteudo_pagina` (CMS)
- ✅ Cria tabela: `cupons` (sistema de cupons de desconto)

**Características:**
- ✅ Preserva todos os dados existentes
- ✅ Idempotente (pode executar múltiplas vezes)
- ✅ Seguro para produção

---

## 🛠️ Scripts de Desenvolvimento

### `dev/DANGER_reset_database.py`

**🚨 PERIGO - DESTRUTIVO**

Reseta completamente o banco de dados. **APAGA TODOS OS DADOS!**

**Uso:**
```bash
python scripts/dev/DANGER_reset_database.py
```

**O que faz:**
- ❌ APAGA todas as tabelas (`db.drop_all()`)
- ✅ Recria todas as tabelas do zero
- ✅ Cria usuário admin padrão (admin/admin123)
- ✅ Adiciona configurações iniciais da loja
- ✅ Cria 6 produtos de exemplo

**Quando usar:**
- ✅ Primeira instalação do projeto
- ✅ Reset completo em ambiente de desenvolvimento
- ❌ **NUNCA em produção!**

**Proteções:**
- Requer confirmação dupla: `'SIM APAGAR TUDO'` + `'CONFIRMO'`

---

### `dev/populate_products.py`

**✅ SEGURO**

Adiciona produtos de exemplo ao banco de dados para testes.

**Uso:**
```bash
python scripts/dev/populate_products.py
```

**O que faz:**
- ✅ Adiciona produtos de exemplo para todas as categorias
- ✅ Permite limpar produtos de exemplo anteriores

**Quando usar:**
- ✅ Após setup inicial para ter dados de teste
- ✅ Para resetar produtos de demonstração

---

### `dev/popular_subcategorias.py`

**⚠️ MODERADO**

Popula a tabela de subcategorias com valores padrão da categoria Roupas.

**Uso:**
```bash
python scripts/dev/popular_subcategorias.py
```

**O que faz:**
- ✅ Cria 3 subcategorias padrão:
  - Roupas → Feminino
  - Roupas → Masculino
  - Roupas → Unissex
- ⚠️ Permite apagar subcategorias existentes antes de criar

**Quando usar:**
- ✅ Primeira instalação
- ✅ Para resetar subcategorias padrão
- ⚠️ Cuidado se já tiver subcategorias customizadas

---

## 📋 Fluxo de Instalação Recomendado

### 1️⃣ Primeira Instalação (Novo Projeto)

```bash
# 1. Resetar banco completo (cria estrutura + admin + configs)
python scripts/dev/DANGER_reset_database.py

# 2. Popular subcategorias
python scripts/dev/popular_subcategorias.py

# 3. Adicionar mais produtos de exemplo (opcional)
python scripts/dev/populate_products.py

# 4. Iniciar servidor
python main.py
```

### 2️⃣ Atualizar Schema (Projeto Existente)

```bash
# Atualizar schema sem perder dados
python scripts/maintenance/update_schema.py
```

### 3️⃣ Adicionar Produtos de Teste

```bash
# Adicionar produtos de exemplo
python scripts/dev/populate_products.py
```

---

## ⚠️ IMPORTANTE

### Scripts SEGUROS (pode usar em produção):
- ✅ `maintenance/update_schema.py`

### Scripts APENAS para DESENVOLVIMENTO:
- 🚨 `dev/DANGER_reset_database.py` - **NUNCA em produção!**
- ⚠️ `dev/populate_products.py` - Apenas dados de teste
- ⚠️ `dev/popular_subcategorias.py` - Pode sobrescrever dados

---

## 🔗 Relacionamento entre Scripts

```
DANGER_reset_database.py
    ↓ (cria estrutura completa)

popular_subcategorias.py
    ↓ (adiciona subcategorias)

populate_products.py
    ↓ (adiciona produtos)

[BANCO COMPLETO COM DADOS DE TESTE]
```

**OU**

```
[Banco existente com dados reais]
    ↓
update_schema.py
    ↓ (adiciona novos campos/tabelas)

[Banco atualizado preservando dados]
```

---

## 📞 Suporte

Para mais informações sobre o projeto, consulte a documentação principal ou entre em contato com a equipe de desenvolvimento.
