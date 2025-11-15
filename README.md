# 🌟 Xodó da Preta - E-commerce de Moda Afro

> Plataforma de e-commerce desenvolvida para a marca **Xodó da Preta**, especializada em moda e acessórios afro autorais que celebram identidade, versatilidade e representatividade.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-lightblue.svg)](https://www.sqlite.org/)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Uso do Sistema](#uso-do-sistema)
- [Painel Administrativo](#painel-administrativo)
- [Deploy](#deploy)

---

## 🎯 Sobre o Projeto

O **Xodó da Preta** é uma plataforma de e-commerce desenvolvida como projeto acadêmico para uma cliente real que vende moda afro através do Instagram e Facebook. O objetivo é profissionalizar a operação, oferecendo:

- 🛍️ **Catálogo online** profissional de produtos
- 📱 **Checkout via WhatsApp** (sem pagamento online - adequado ao modelo de negócio)
- 🎨 **Design autêntico** que reflete a identidade da marca
- ⚙️ **Autonomia total** para a cliente gerenciar o site
- 📊 **Analytics** para acompanhar desempenho dos produtos

### Características do Negócio

- **Público-alvo:** Pessoas que apreciam moda afro autoral e inclusiva
- **Produtos:** Colares, anéis, brincos, pulseiras e roupas
- **Valores:** Sustentabilidade, economia circular, representatividade
- **Canais de venda:** WhatsApp e Instagram
- **Diferencial:** Produção consciente e design autoral

---

## ✨ Funcionalidades

### Para Clientes (Visitantes do Site)

- 🏠 **Home com Carrossel:** 3 slides customizáveis destacando valores da marca
- 🎯 **Produtos em Destaque:** Seção na home com até 4 produtos selecionados
- 🛒 **Catálogo Completo:** Navegação por categorias (Colares, Anéis, Brincos, Pulseiras, Roupas)
- 🔍 **Busca Avançada:** Pesquisa por nome, descrição ou categoria
- 📦 **Detalhes do Produto:** Página individual com imagens, descrição, preço e tamanhos
- 🛒 **Carrinho de Compras:** Adicionar/remover produtos, ajustar quantidades
- 💬 **Checkout via WhatsApp:** Finalização com mensagem formatada automática
- 📱 **Responsivo:** Design adaptado para mobile, tablet e desktop

### Para Administradores (Painel Admin)

#### 📊 Dashboard Premium
- **7 KPIs principais** com visualizações totais
- **Gráficos interativos (Chart.js)**
- **Top 10 produtos** mais visualizados
- **Quick Actions**

#### 📦 Gestão de Produtos
- CRUD completo
- Upload de imagens
- Categorias hierárquicas
- **Marcar como Destaque**
- Rastreamento de visualizações

#### 🎨 CMS (Sistema de Gerenciamento de Conteúdo)
Interface visual para editar **todo o conteúdo do site** sem código

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask 3.0**
- **SQLAlchemy**
- **SQLite**

### Frontend
- **Bootstrap 5.3**
- **Chart.js**
- **Custom Design System**

---

## 🚀 Instalação e Configuração

### Passo a Passo

1. **Clone o repositório**
2. **Crie ambiente virtual:** `python -m venv venv`
3. **Ative:** `venv\Scripts\activate` (Windows)
4. **Instale dependências:** `pip install -r requirements.txt`
5. **Execute migrações:** `python app/migrate_db.py`
6. **Rode servidor:** `python app/main.py`
7. **Acesse:** http://localhost:5000

---

## 📁 Estrutura do Projeto

```
Xod-da-Preta/
├── app/
│   ├── static/css/design-system.css
│   ├── templates/
│   ├── models.py
│   ├── main.py
│   ├── admin_routes.py
│   └── migrate_db.py
├── README.md
└── requirements.txt
```

---

## 🔐 Painel Administrativo

Acesse `/admin` com credenciais configuradas.

### Funcionalidades:
- Dashboard com métricas
- Gerenciar Produtos
- Gerenciar Conteúdo (CMS)
- Configurações

---

## 🌐 Deploy

Opções: Heroku, PythonAnywhere, VPS

---

**Desenvolvido com 💛 para celebrar a moda afro e a representatividade**
