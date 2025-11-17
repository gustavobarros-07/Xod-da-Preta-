# 🚀 Guia de Deploy - Xodó da Preta

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Servidor com Linux (Ubuntu 20.04+ recomendado)
- Domínio configurado (opcional, mas recomendado)

---

## 🔐 1. CONFIGURAÇÃO INICIAL (OBRIGATÓRIO)

### 1.1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd Xod-da-Preta-
```

### 1.2. Criar arquivo .env

```bash
cp .env.example .env
```

### 1.3. Gerar SECRET_KEY forte

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado e cole no arquivo `.env`:

```env
SECRET_KEY=<CHAVE_GERADA_AQUI_64_CARACTERES>
```

### 1.4. Configurar credenciais de admin

Edite o arquivo `.env` e defina uma senha forte:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Sua$enhaForte123!
```

**⚠️ IMPORTANTE:** Use uma senha forte com:
- Mínimo 12 caracteres
- Letras maiúsculas e minúsculas
- Números
- Símbolos especiais

---

## 🐍 2. AMBIENTE PYTHON

### 2.1. Criar ambiente virtual

```bash
cd app
python3 -m venv venv
```

### 2.2. Ativar ambiente virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 2.3. Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🗄️ 3. BANCO DE DADOS

O banco de dados SQLite será criado automaticamente na pasta `instance/loja.db` quando você rodar a aplicação pela primeira vez.

```bash
# O banco será criado automaticamente aqui:
instance/loja.db
```

**📌 Backup do banco:**
```bash
# Fazer backup
cp instance/loja.db instance/loja_backup_$(date +%Y%m%d_%H%M%S).db

# Restaurar backup
cp instance/loja_backup_YYYYMMDD_HHMMSS.db instance/loja.db
```

---

## 🧪 4. TESTAR LOCALMENTE

```bash
# Certificar-se de estar na pasta app/
cd app

# Rodar aplicação
python main.py
```

Acesse: `http://localhost:5000`

**Teste o painel admin:**
- URL: `http://localhost:5000/admin`
- Usuário: definido no .env
- Senha: definida no .env

---

## 🌐 5. DEPLOY EM PRODUÇÃO

### Opção A: Gunicorn + Nginx (Recomendado)

#### 5.1. Instalar Gunicorn

```bash
pip install gunicorn
```

#### 5.2. Criar arquivo wsgi.py

```python
# app/wsgi.py
from main import app

if __name__ == "__main__":
    app.run()
```

#### 5.3. Testar Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

#### 5.4. Criar serviço systemd

```bash
sudo nano /etc/systemd/system/xododapreta.service
```

Conteúdo:

```ini
[Unit]
Description=Xodó da Preta - Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/caminho/para/Xod-da-Preta-/app
Environment="PATH=/caminho/para/Xod-da-Preta-/app/venv/bin"
ExecStart=/caminho/para/Xod-da-Preta-/app/venv/bin/gunicorn --workers 3 --bind unix:xododapreta.sock --log-level info wsgi:app

[Install]
WantedBy=multi-user.target
```

#### 5.5. Iniciar serviço

```bash
sudo systemctl start xododapreta
sudo systemctl enable xododapreta
sudo systemctl status xododapreta
```

#### 5.6. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/xododapreta
```

Conteúdo:

```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/caminho/para/Xod-da-Preta-/app/xododapreta.sock;
    }

    location /static {
        alias /caminho/para/Xod-da-Preta-/app/static;
        expires 30d;
    }

    location /instance {
        deny all;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/xododapreta /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5.7. Configurar SSL com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

---

### Opção B: Deploy em PythonAnywhere (Mais Simples)

1. Criar conta em [PythonAnywhere](https://www.pythonanywhere.com/)
2. Upload dos arquivos via Git ou Web interface
3. Criar Web App > Flask
4. Configurar arquivo .env
5. Instalar requirements.txt
6. Configurar caminho do código
7. Reload da aplicação

---

### Opção C: Deploy no Render.com (Gratuito)

1. Criar conta em [Render.com](https://render.com/)
2. New > Web Service
3. Conectar repositório Git
4. Configurar:
   - **Build Command:** `cd app && pip install -r requirements.txt`
   - **Start Command:** `cd app && gunicorn wsgi:app`
5. Adicionar variáveis de ambiente (SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD)
6. Deploy!

---

## 📊 6. MONITORAMENTO E LOGS

### Ver logs em tempo real

```bash
# Logs do systemd
sudo journalctl -u xododapreta -f

# Logs da aplicação (se configurou logging)
tail -f /caminho/para/logs/xodo_da_preta.log
```

### Comandos úteis

```bash
# Reiniciar aplicação
sudo systemctl restart xododapreta

# Ver status
sudo systemctl status xododapreta

# Parar aplicação
sudo systemctl stop xododapreta

# Recarregar Nginx
sudo systemctl reload nginx
```

---

## 🔧 7. MANUTENÇÃO

### Atualizar código

```bash
# Fazer backup do banco primeiro!
cp instance/loja.db instance/loja_backup.db

# Atualizar código
git pull origin main

# Instalar novas dependências (se houver)
pip install -r requirements.txt

# Reiniciar aplicação
sudo systemctl restart xododapreta
```

### Backup automático do banco

Criar script de backup:

```bash
#!/bin/bash
# backup_db.sh

DATA=$(date +%Y%m%d_%H%M%S)
ORIGEM="/caminho/para/instance/loja.db"
DESTINO="/caminho/para/backups/loja_$DATA.db"

cp $ORIGEM $DESTINO

# Manter apenas últimos 30 backups
ls -t /caminho/para/backups/loja_*.db | tail -n +31 | xargs rm -f
```

Adicionar ao crontab:

```bash
crontab -e

# Backup diário às 3h da manhã
0 3 * * * /caminho/para/backup_db.sh
```

---

## 🐛 8. TROUBLESHOOTING

### Erro: "SECRET_KEY não definida"

✅ Verifique se o arquivo `.env` existe e contém `SECRET_KEY=...`

### Erro: "RuntimeError: ADMIN_PASSWORD deve estar definido"

✅ Adicione `ADMIN_USERNAME` e `ADMIN_PASSWORD` ao `.env`

### Erro 500: Internal Server Error

✅ Verifique os logs: `sudo journalctl -u xododapreta -n 50`

### Permissões de arquivo

```bash
# Dar permissões corretas
sudo chown -R www-data:www-data /caminho/para/Xod-da-Preta-/
sudo chmod -R 755 /caminho/para/Xod-da-Preta-/
```

### Banco de dados corrompido

```bash
# Restaurar do backup
cp instance/loja_backup.db instance/loja.db
sudo systemctl restart xododapreta
```

---

## 📈 9. OTIMIZAÇÕES DE PRODUÇÃO

### 9.1. Variáveis de ambiente para produção

```env
FLASK_ENV=production
FLASK_DEBUG=False
```

### 9.2. Workers do Gunicorn

Fórmula: `(2 x núcleos_CPU) + 1`

Exemplo para 2 CPUs:
```bash
gunicorn --workers 5 --bind unix:xododapreta.sock wsgi:app
```

### 9.3. Cache estático no Nginx

Já configurado na configuração acima (`expires 30d`).

---

## ✅ 10. CHECKLIST PRÉ-PRODUÇÃO

- [ ] `.env` configurado com SECRET_KEY forte
- [ ] ADMIN_PASSWORD definida (senha forte)
- [ ] Backup do banco de dados configurado
- [ ] SSL/HTTPS configurado
- [ ] Logs sendo salvos e monitorados
- [ ] Testado o painel admin
- [ ] Testado o carrinho de compras
- [ ] Testado formulário de contato via WhatsApp
- [ ] Verificado todas as páginas (404, 500, etc)
- [ ] Firewall configurado (portas 80, 443 abertas)

---

## 📞 SUPORTE

Em caso de problemas, verifique:

1. Logs da aplicação: `/caminho/para/logs/xodo_da_preta.log`
2. Logs do systemd: `sudo journalctl -u xododapreta`
3. Logs do Nginx: `/var/log/nginx/error.log`

---

**Última atualização:** Novembro 2024
**Versão:** 1.0.0
