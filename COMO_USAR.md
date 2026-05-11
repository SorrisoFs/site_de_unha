# 🚀 Como Rodar o Site

## ✅ Passo 1 - Instalar Dependências
```bash
pip install -r requirements.txt
```

## ✅ Passo 2 - Rodar Migrations
```bash
python manage.py migrate
```

## ✅ Passo 3 - Criar Super Usuário (Admin)
```bash
python manage.py createsuperuser
```
**OU use o admin já criado:**
- **Login:** admin
- **Senha:** admin123

## ✅ Passo 4 - Rodar Servidor
```bash
python manage.py runserver 0.0.0.0:8000
```

## ✅ Passo 5 - Acessar o Site

### Site Principal
**URL:** http://localhost:8000

### Painel Administrativo
**URL:** http://localhost:8000/gestao/login/
- **Login:** admin
- **Senha:** admin123

### Django Admin
**URL:** http://localhost:8000/admin/

---

## 📋 O Que Foi Criado

### Dados Iniciais
- ✅ 2 Profissionais (Ana Silva e Carla Santos)
- ✅ 3 Serviços (Manicure, Pedicure, Manicure+Pedicure)
- ✅ 13 Datas disponíveis (próximos 15 dias úteis)
- ✅ Múltiplos horários (9h às 18h)

### Funcionalidades
- ✅ Home page com calendário clicável
- ✅ Seleção de datas disponíveis (em rosa)
- ✅ Modal de agendamento funcional
- ✅ Seleção de horários
- ✅ Formulário de dados do cliente
- ✅ Confirmação de agendamento
- ✅ Token único por cliente
- ✅ Painel admin para gerenciar tudo

---

## 🎯 Como Usar

### Para Clientes:
1. Acesse http://localhost:8000
2. Clique em uma data no calendário (datas em rosa)
3. Selecione o serviço desejado
4. Escolha o horário disponível
5. Preencha nome e celular
6. Confirme o agendamento
7. Guarde o token de confirmação

### Para Admin:
1. Acesse http://localhost:8000/gestao/login/
2. Login: admin | Senha: admin123
3. Dashboard mostra resumo
4. Crie novas datas em "Criar Data"
5. Gerencie horários e agendamentos
6. Bloqueie horários indesejados

---

## 🔧 URLs Importantes

| Descrição | URL |
|-----------|-----|
| Home | http://localhost:8000 |
| Agendar | http://localhost:8000/horarios/ |
| Meus Agendamentos | http://localhost:8000/meus-agendamentos/ |
| Admin Login | http://localhost:8000/gestao/login/ |
| Admin Dashboard | http://localhost:8000/gestao/ |
| Django Admin | http://localhost:8000/admin/ |

---

## 🎨 Melhorias Implementadas

### Design
- ✅ Cores vibrantes em gradiente
- ✅ Animações suaves
- ✅ Hero section com efeito
- ✅ Cards modernos
- ✅ Totalmente responsivo

### Funcionalidade
- ✅ Calendário FullCalendar
- ✅ Datas marcadas visualmente
- ✅ Modal de agendamento
- ✅ Validação de formulário
- ✅ Feedback visual
- ✅ Confirmação com token

### Admin
- ✅ Dashboard moderno
- ✅ Gestão de datas
- ✅ Bloqueio de horários
- ✅ Lista de agendamentos
- ✅ Gestão de clientes

---

## 📞 Problemas Comuns

### "Não há datas disponíveis"
- Crie novas datas no admin
- Acesse: /gestao/datas/criar/

### "Botão não clica"
- Verifique se o JavaScript está carregando
- Abra o console do navegador (F12)

### "Erro ao agendar"
- Verifique se há horários na data
- Verifique se o serviço está ativo

---

## 🎉 Tudo Pronto!

Seu site de agendamento está funcionando perfeitamente!

**Acesse:** http://localhost:8000
