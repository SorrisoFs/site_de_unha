# 💅 Nail Salon - Sistema de Agendamento

Sistema moderno e elegante para agendamento de salão de beleza com interface chamativa e UX otimizada.

## ✨ Melhorias Implementadas

### Design System Moderno
- **Cores Vibrantes**: Gradientes em tons de rosa e vermelho (coral)
- **Animações Suaves**: Transições fluidas em todos os elementos
- **Efeitos Visuais**: Hover effects, sombras dinâmicas e microinterações
- **Tipografia Moderna**: Fonte Inter para melhor legibilidade

### Home Page Aprimorada
- **Hero Section Animada**: Gradiente animado com efeito de pulso
- **Call-to-Action Destacado**: Botões com efeitos de hover e sombra
- **Cards de Serviços**: Design moderno com ícones e preços em destaque
- **Calendário Interativo**: FullCalendar com marcação de datas disponíveis
- **Como Funciona**: Seção explicativa com ícones animados

### Experiência do Usuário (UX)
- **Navegação Intuitiva**: Menu fixo com efeito de scroll
- **Feedback Visual**: Loading states e mensagens de confirmação
- **Formulários Otimizados**: Validação em tempo real
- **Modal de Agendamento**: Interface limpa e objetiva
- **Suporte Mobile**: Totalmente responsivo

### Painel Administrativo
- **Dashboard Moderno**: Cards estatísticos com gradientes
- **Gestão de Eventos**: Criar/remover datas e horários
- **Lista de Agendamentos**: Tabela organizada com filtros
- **Ações Rápidas**: Acesso rápido às funcionalidades principais
- **Controle de Clientes**: Histórico completo de agendamentos

### Calendário de Agendamento
- **Seleção por Data**: Clique na data desejada
- **Horários Disponíveis**: Visualização clara dos slots
- **Múltiplos Profissionais**: Suporte a vários profissionais
- **Status em Tempo Real**: Atualização automática
- **Confirmação Imediata**: Token de agendamento único

## 🚀 Funcionalidades

### Para Clientes
- ✅ Agendamento online 24/7
- ✅ Seleção de data e horário
- ✅ Escolha de serviços
- ✅ Confirmação imediata
- ✅ Token de agendamento
- ✅ Consulta de agendamentos
- ✅ Cancelamento de horários

### Para Administradores
- ✅ Dashboard com métricas
- ✅ Criar/remover datas
- ✅ Bloquear horários
- ✅ Gerenciar agendamentos
- ✅ Controle de clientes
- ✅ Relatórios de serviços
- ✅ Múltiplos profissionais

## 🎨 Paleta de Cores

```css
Primary: #ff6b6b (Coral)
Primary Light: #ff8e8e
Primary Dark: #ee5a5a
Gradient: linear-gradient(135deg, #ff6b6b, #ff8e8e, #ffa5a5)
Background: linear-gradient(135deg, #f5f7fa, #c3cfe2)
```

## 🛠️ Tecnologias

- **Backend**: Django
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite/PostgreSQL
- **Calendário**: FullCalendar.js
- **Ícones**: Font Awesome
- **Framework CSS**: Bootstrap 4

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- 📱 Smartphones
- 📱 Tablets
- 💻 Desktops
- 🖥️ TVs

## 🎯 Melhorias de Performance

- Carregamento otimizado
- CSS minificado
- Imagens otimizadas
- Cache estratégico
- Lazy loading

## 🔐 Segurança

- CSRF Protection
- Autenticação de usuários
- Tokens únicos
- Validação de dados
- HTTPS ready

## 📊 Estrutura de Arquivos

```
site_de_unha/
├── scheduling/           # App principal
│   ├── templates/        # Templates HTML
│   ├── views.py          # Views do Django
│   ├── models.py         # Modelos de dados
│   └── urls.py           # Rotas
├── static/
│   └── css/
│       └── styles.css    # CSS personalizado
└── nail_salon/
    └── settings.py       # Configurações
```

## 🚀 Como Usar

### 1. Configuração Inicial
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### 2. Criar Dados Iniciais
```bash
python manage.py shell
>>> from scheduling.models import Professional, Service
>>> # Criar profissionais e serviços
```

### 3. Rodar Servidor
```bash
python manage.py runserver
```

### 4. Acessar Sistema
- **Site**: http://localhost:8000
- **Admin**: http://localhost:8000/gestao/login/

## 🎨 Personalização

### Alterar Cores
Edite `static/css/styles.css`:
```css
:root {
  --primary-color: #ff6b6b;
  --primary-light: #ff8e8e;
  --gradient-4: linear-gradient(135deg, #ff6b6b, #ff8e8e, #ffa5a5);
}
```

### Alterar Logo
Edite `templates/scheduling/base.html`:
```html
<a class="navbar-brand">Seu Logo</a>
```

## 📞 Suporte

Para dúvidas ou sugestões, entre em contato.

## 📝 Licença

Uso livre para fins comerciais e pessoais.

---

**Desenvolvido com 💖 para Nail Salon**
