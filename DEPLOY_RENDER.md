# 🚀 Deploy no Render - Passo a Passo

## ✅ Tudo Pronto!

Seu código já está no GitHub e configurado para o Render.

---

## 📋 Passo 1 - Acessar Render

1. Acesse: **https://render.com**
2. Faça login com sua conta GitHub
3. Clique em **"New +"** → **"Web Service"**

---

## 📋 Passo 2 - Conectar Repositório

1. Clique em **"Connect account"** (GitHub)
2. Procure por: **`site_de_unha`**
3. Clique em **"Connect"**

---

## 📋 Passo 3 - Configurar Web Service

Preencha as informações:

| Campo | Valor |
|-------|-------|
| **Name** | `agendamento-de-unha` (ou outro nome) |
| **Region** | Oregon (padrão) |
| **Branch** | `main` |
| **Root Directory** | (deixe em branco) |
| **Runtime** | `Python` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn nail_salon.wsgi:application --workers 2 --threads 4` |

---

## 📋 Passo 4 - Configurar Variáveis de Ambiente

Clique em **"Advanced"** e adicione:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `sua-chave-secreta-aqui` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*` |

**Importante:** Gere uma SECRET_KEY segura:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📋 Passo 5 - Escolher Plano

- **Free**: Grátis (limitado)
- **Starter**: $7/mês (recomendado)

Clique em **"Create Web Service"**

---

## 📋 Passo 6 - Aguardar Deploy

O Render vai:
1. Clonar seu repositório
2. Rodar `build.sh` (cria migrations e dados)
3. Iniciar o Gunicorn
4. Disponibilizar o site

**Tempo estimado:** 2-5 minutos

---

## 📋 Passo 7 - Acessar Site

Após o deploy, você verá:
```
https://agendamento-de-unha.onrender.com
```

**Clique no link para abrir!**

---

## 🎯 Configurar Admin

Após o deploy, crie o superusuário:

### Opção 1: Shell do Render
1. No dashboard do Render, vá em **"Shell"**
2. Execute:
```bash
python manage.py createsuperuser
```

### Opção 2: Django Admin
1. Acesse: `https://seusite.onrender.com/admin/`
2. Use as credenciais criadas

---

## 🔧 URLs Importantes

| URL | Descrição |
|-----|-----------|
| `/` | Site principal |
| `/gestao/login/` | Login admin |
| `/gestao/` | Dashboard admin |
| `/admin/` | Django admin |
| `/meus-agendamentos/` | Área do cliente |

---

## ⚠️ Problemas Comuns

### Erro: "Database is locked"
- O SQLite é limitado. Para produção, use PostgreSQL.

### Erro: "Static files not found"
- Verifique se `collectstatic` rodou no build
- Confira se `whitenoise` está no requirements.txt

### Erro: "Module not found"
- Verifique o `requirements.txt`
- Reinicie o deploy

---

## 🎨 Melhorias de Produção

### 1. Usar PostgreSQL (Recomendado)
Adicione ao `requirements.txt`:
```
psycopg2-binary>=2.9
```

Configure no `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}
```

### 2. Variáveis do Render
No Render, vá em **"Database"** e crie um PostgreSQL.

Adicione as vars:
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`

### 3. Auto Deploy
- O Render faz auto deploy a cada push no `main`
- Para desativar: Settings → Auto Deploy → Off

---

## 📊 Monitoramento

### Logs
- Acesse: **Render Dashboard → Logs**
- Veja erros em tempo real

### Métricas
- CPU usage
- Memory usage
- Request count

---

## 🎉 Site no Ar!

Seu site de agendamento está online!

**Compartilhe o link com seus clientes!**

---

## 📞 Suporte

- Docs Render: https://render.com/docs
- Django Docs: https://docs.djangoproject.com

**Dúvidas? Consulte os logs no Render!**
