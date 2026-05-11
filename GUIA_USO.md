# 🚀 Guia Rápido - Nail Salon

## Para o Administrador

### 1. Acessar o Painel Admin
```
URL: http://seusite.com/gestao/login/
Login: seu_email@email.com
Senha: sua_senha
```

### 2. Criar Disponibilidade de Datas

#### Passo 1: Criar Data
```
1. No dashboard, clique em "Criar Data"
2. Selecione a data desejada
3. Escolha o profissional
4. Defina os horários (ex: 09:00 às 18:00)
5. Intervalo de 30 em 30 minutos
6. Salvar
```

#### Passo 2: Gerenciar Horários
```
- Visualizar todos horários gerados
- Bloquear horários indesejados
- Liberar horários bloqueados
- Status: Disponível (verde) / Bloqueado (vermelho)
```

### 3. Criar Agendamento Manual
```
1. Clique em "Agendamento Rápido"
2. Selecione cliente ou crie novo
3. Escolha data e horário
4. Selecione serviço
5. Confirmar
```

### 4. Gerenciar Clientes
```
- Listar todos clientes
- Buscar por nome/telefone
- Ver histórico completo
- Editar dados
```

### 5. Visualizar Agendamentos
```
- Dashboard: visão geral
- Filtros: data, status
- Cancelar/confirmar
- Exportar lista
```

---

## Para o Cliente

### 1. Acessar Site
```
URL: http://seusite.com
```

### 2. Agendar Horário
```
1. Clique em "Agendar Agora"
2. Escolha a data no calendário (datas em rosa)
3. Selecione o serviço desejado
4. Escolha o horário disponível
5. Preencha nome e celular
6. Confirmar agendamento
```

### 3. Consultar Agendamento
```
1. Clique em "Meus Agendamentos"
2. Digite seu código (token)
3. Visualize seus horários
4. Cancele se necessário
```

### 4. Cancelar Agendamento
```
1. Acesse "Meus Agendamentos"
2. Localize o agendamento
3. Clique em "Cancelar"
4. Confirme o cancelamento
```

---

## Funcionalidades

### Cliente
- ✅ Agendar online 24/7
- ✅ Escolher data e horário
- ✅ Ver serviços disponíveis
- ✅ Receber token único
- ✅ Consultar agendamentos
- ✅ Cancelar horários

### Administrador
- ✅ Dashboard com métricas
- ✅ Criar datas disponíveis
- ✅ Gerenciar horários
- ✅ Bloquear horários
- ✅ Agendamento manual
- ✅ Listar clientes
- ✅ Histórico completo
- ✅ Múltiplos profissionais

---

## Estrutura de Dados

### Profissionais
```
- Nome
- Especialidade
- Status (ativo/inativo)
```

### Serviços
```
- Nome
- Descrição
- Duração (minutos)
- Preço
- Status (ativo/inativo)
```

### Datas
```
- Data
- Profissional
- Disponibilidade
- Observações
```

### Horários (TimeSlots)
```
- Data
- Hora início
- Hora fim
- Status (disponível/reservado/bloqueado)
```

### Agendamentos
```
- Cliente
- Serviço
- Horário
- Status (confirmado/concluído/cancelado)
- Observações
```

---

## Dicas para Admin

### Criar Datas Semanais
```python
# Exemplo: Criar datas para uma semana
Segunda a Sexta: 09:00 às 18:00
Sábado: 09:00 às 14:00
Intervalo: 30 minutos
```

### Bloquear Almoço
```
1. Acesse a data
2. Localize horário de almoço (12:00-13:00)
3. Clique em "Bloquear"
4. Confirmar
```

### Adicionar Feriados
```
1. Criar data do feriado
2. Marcar como "Indisponível"
3. Ou bloquear todos horários
```

---

## Perguntas Frequentes

### O cliente pode cancelar?
Sim, através da área "Meus Agendamentos".

### Como recebo os dados?
Os dados ficam no banco e você acessa pelo admin.

### Posso bloquear um horário específico?
Sim, no detalhe da data você pode bloquear/desbloquear.

### O sistema envia lembrete?
Não automaticamente. Você pode entrar em contato.

### Posso ter múltiplas profissionais?
Sim, crie quantos profissionais precisar.

### Como excluo um agendamento?
No admin, marque como "Cancelado".

---

## URLs Importantes

```
Home: /
Agendar: /horarios/
Meus Agendamentos: /meus-agendamentos/
Admin Login: /gestao/login/
Admin Dashboard: /gestao/
Criar Data: /gestao/datas/criar/
Agendamentos: /gestao/agendamentos/
Clientes: /gestao/clientes/
```

---

## Suporte

Dúvidas? Consulte:
- `README.md` - Visão geral
- `MELHORIAS.md` - Detalhes das melhorias
- Código fonte - Comentários explicativos

---

**Versão**: 2.0  
**Última atualização**: 2024  
**Status**: ✅ Pronto para produção
