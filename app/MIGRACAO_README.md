# Documentação - Scripts de Migração

## 📋 Status dos Arquivos de Migração

### ✅ Arquivo Atual (USE ESTE)

**`migrate_hierarquia.py`** - Migração Final (3 Níveis)
- **Status**: ✅ ATIVO - Este é o script atual que deve ser usado
- **O que faz**: Adiciona as colunas `subcategoria` e `tipo` para suportar hierarquia de 3 níveis
- **Quando usar**: Se você ainda não rodou este script, execute-o UMA VEZ
- **Seguro**: Sim, as colunas são nullable e não afetam produtos existentes

### 📦 Arquivos Legados (NÃO USE)

**`migrate_database.py`** - Migração Antiga (DESCONTINUADO)
- **Status**: ⚠️ OBSOLETO - Não usar
- **O que fazia**: Primeira tentativa de adicionar subcategorias usando Foreign Key
- **Por que está obsoleto**: Foi substituído pelo sistema de hierarquia com campos string
- **Pode deletar?**: Não recomendado (manter para histórico/rollback se necessário)

**`migrate_subcategorias.py`** - População de Subcategorias (DESCONTINUADO)
- **Status**: ⚠️ OBSOLETO - Não usar
- **O que fazia**: Populava a tabela `subcategorias` (sistema antigo)
- **Por que está obsoleto**: O novo sistema usa CATEGORY_HIERARCHY em config.py
- **Pode deletar?**: Não recomendado (manter para histórico/rollback se necessário)

---

## 🎯 Sistema Atual (Hierarquia de 3 Níveis)

### Estrutura

```
Nível 1: Categoria (String, NOT NULL)
└── Exemplo: "Roupas", "Brincos", "Colares"

Nível 2: Subcategoria (String, NULLABLE)
└── Exemplo: "Feminino", "Masculino"

Nível 3: Tipo (String, NULLABLE)
└── Exemplo: "Vestido", "Camisa", "Saia"
```

### Campos no Banco de Dados

```sql
produtos:
  - categoria VARCHAR(50) NOT NULL      # Nível 1
  - subcategoria VARCHAR(50) NULL       # Nível 2
  - tipo VARCHAR(50) NULL               # Nível 3
  - subcategoria_id INTEGER NULL        # LEGADO (compatibilidade)
```

### Configuração (config.py)

```python
CATEGORY_HIERARCHY = {
    'Roupas': {
        'Feminino': ['Vestido', 'Saia', 'Macacão', 'Jaqueta'],
        'Masculino': ['Camisa', 'Bata', 'Conjunto', 'Jaqueta']
    }
    # Outras categorias não têm hierarquia
}
```

---

## 🚀 Como Usar

### Se você AINDA NÃO migrou:

1. Execute APENAS o migrate_hierarquia.py:
   ```bash
   cd app
   python migrate_hierarquia.py
   ```

2. Responda 's' quando perguntado

3. Pronto! O banco está atualizado

### Se você JÁ migrou:

- Não faça nada! Seu banco já está atualizado
- Os scripts antigos ficam para histórico

---

## 🔄 Compatibilidade com Produtos Antigos

### Produtos criados antes da migração:

```python
{
  'categoria': 'Brincos',        # ✅ Tem
  'subcategoria': None,          # ✅ NULL (ok)
  'tipo': None                   # ✅ NULL (ok)
}
```

**Resultado**: Aparece normalmente no filtro de "Brincos", sem subcategoria

### Produtos de Roupas novos:

```python
{
  'categoria': 'Roupas',         # ✅ Nível 1
  'subcategoria': 'Feminino',    # ✅ Nível 2
  'tipo': 'Vestido'              # ✅ Nível 3
}
```

**Resultado**: Aparece em todos os 3 níveis de filtro

---

## 📁 Organização Recomendada

```
app/
├── migrate_hierarquia.py          # ✅ USAR ESTE
├── migrations_legacy/             # 📦 Mover arquivos antigos aqui
│   ├── migrate_database.py        # Histórico
│   └── migrate_subcategorias.py   # Histórico
└── MIGRACAO_README.md             # Este arquivo
```

### Mover arquivos antigos para pasta de histórico:

```bash
# Windows
mkdir migrations_legacy
move migrate_database.py migrations_legacy\
move migrate_subcategorias.py migrations_legacy\

# Linux/Mac
mkdir migrations_legacy
mv migrate_database.py migrate_subcategorias.py migrations_legacy/
```

---

## ⚠️ Avisos Importantes

1. **NÃO execute migrate_database.py ou migrate_subcategorias.py** - Eles são obsoletos
2. **Execute migrate_hierarquia.py APENAS UMA VEZ** - Rodar múltiplas vezes é seguro, mas desnecessário
3. **Sempre faça backup** antes de rodar qualquer script de migração
4. **Produtos antigos continuam funcionando** - As novas colunas são nullable

---

## 🐛 Troubleshooting

### "Erro: no such column: produtos.subcategoria"
**Solução**: Execute `python migrate_hierarquia.py`

### "Erro: duplicate column name"
**Solução**: Você já migrou! Não precisa fazer nada

### "Produtos antigos não aparecem"
**Solução**: Isso NÃO deve acontecer. Verifique se tem filtro ativo na URL

---

## 📞 Dúvidas?

- Leia este arquivo primeiro
- Verifique se já executou migrate_hierarquia.py
- Produtos antigos devem continuar funcionando normalmente
