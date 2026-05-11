# 🔧 Troubleshooting - Render Deploy

## ✅ Correções Aplicadas

### 1. Runtime Python
- Alterado para: `python-3.12.0`
- Versão estável e compatível

### 2. Build Script
- Recriado com line endings Unix (LF)
- Comandos simplificados

### 3. Git Attributes
- Adicionado `.gitattributes`
- Garante line endings corretos

---

## 🚀 Como Resolver o Erro "null bytes"

### Opção 1: Rebuild no Render
1. Acesse: https://render.com
2. Vá no seu Web Service
3. Clique em **"Manual Deploy"**
4. Selecione a branch `main`
5. Clique em **"Deploy"**

### Opção 2: Recriar o Service
1. Delete o service atual no Render
2. Crie um novo Web Service
3. Conecte o repositório novamente
4. Configure:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn nail_salon.wsgi:application --workers 2 --threads 4`

---

## 📋 Verificações no Render

### 1. Logs de Build
No Render, vá em **"Logs"** e verifique:
- Se `build.sh` está rodando
- Se migrations estão aplicando
- Se `seed_data` está populando o banco

### 2. Erros Comuns

**Erro: "No module named 'whitenoise'"**
```bash
# Solução: requirements.txt já inclui whitenoise
```

**Erro: "Database is locked"**
```bash
# Solução: SQLite é limitado, use PostgreSQL no Render
```

**Erro: "Static files not found"**
```bash
# Solução: collectstatic roda no build.sh
```

---

## 🔍 Debug Passo a Passo

### 1. Verificar Build
```bash
# No shell do Render, execute:
python manage.py check
python manage.py migrate --check
python manage.py seed_data
```

### 2. Verificar Dados
```bash
# No shell do Render:
python manage.py shell
>>> from scheduling.models import Professional, Service
>>> print("Profissionais:", Professional.objects.count())
>>> print("Serviços:", Service.objects.count())
```

### 3. Verificar Admin
```bash
# Acesse: https://seusite.onrender.com/admin/
# Login: admin
# Senha: admin123
```

---

## 🎯 Configuração Correta

### Build Command
```bash
./build.sh
```

### Start Command
```bash
gunicorn nail_salon.wsgi:application --workers 2 --threads 4
```

### Environment Variables
```
SECRET_KEY=qualquer-coisa-aqui
DEBUG=False
ALLOWED_HOSTS=*
```

---

## 📞 Se Ainda Der Erro

### 1. Verifique os Logs
- Render Dashboard → Logs
- Veja a mensagem exata do erro

### 2. Recrie o Deploy
```bash
# No seu computador:
git pull origin main
git status
# Deve estar limpo
```

### 3. Teste Localmente
```bash
python manage.py runserver
# Acesse http://localhost:8000
# Deve funcionar
```

---

## ✅ Checklist Final

- [x] Python 3.12.0 no runtime.txt
- [x] build.sh com LF
- [x] .gitattributes configurado
- [x] requirements.txt completo
- [x] seed_data.py criado
- [x] Código no GitHub
- [ ] Deploy no Render (faça rebuild)

---

## 🎉 Após Rebuild

Seu site deve estar em:
- **Home:** https://agendamento-y0m6.onrender.com
- **Admin:** https://agendamento-y0m6.onrender.com/gestao/login/

**Login:** admin  
**Senha:** admin123

---

## 📞 Próximos Passos

1. **Acesse Render**
2. **Clique em "Manual Deploy"**
3. **Aguarde 2-5 minutos**
4. **Teste o site**

Se funcionar, **compartilhe o link**! 🎉
