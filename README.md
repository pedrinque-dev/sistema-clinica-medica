# Sistema de Gestão para Clínicas Médicas

Sistema web completo para gestão de clínicas médicas, desenvolvido como projeto de estudo aplicado, cobrindo autenticação com perfis de acesso, cadastro de pacientes e médicos, agendamento de consultas com calendário visual, prontuário eletrônico simples e controle de permissões por função.

## Funcionalidades

- Autenticação com três perfis de acesso: Administrador, Médico e Recepcionista
- Controle de permissões por perfil em cada módulo do sistema
- Cadastro, edição, exclusão e busca de pacientes
- Cadastro de médicos vinculado a especialidades
- Agendamento de consultas, com validação de conflito de horário por médico
- Calendário visual de consultas, com navegação por mês via JavaScript
- Histórico de consultas por paciente
- Prontuário eletrônico simples, vinculado a cada consulta
- Dashboard com resumo diário (métricas gerais para Admin/Recepção, agenda do dia para Médico)
- Cadastro e gestão de funcionários pelo próprio sistema, incluindo ativação/desativação de acesso
- Design responsivo, com identidade visual própria

## Tecnologias utilizadas

- **Back-end**: Django (Python)
- **Front-end**: HTML5, CSS3, JavaScript puro
- **Framework CSS**: Bootstrap 5 (customizado)
- **Banco de dados**: PostgreSQL
- **Controle de versão**: Git e GitHub

## Como rodar o projeto localmente

### Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL instalado e em execução

### Passo a passo

1. Clone o repositório:
   ```bash
   git clone https://github.com/pedrinque-dev/sistema-clinica-medica.git
   cd sistema-clinica-medica
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie o banco de dados no PostgreSQL:
   ```sql
   CREATE DATABASE clinica_db;
   ```

5. Copie o arquivo de variáveis de ambiente de exemplo e preencha com seus dados:
   ```bash
   cp .env.example .env
   ```

6. Aplique as migrations:
   ```bash
   python manage.py migrate
   ```

7. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

8. No painel `/admin/`, defina o campo **perfil** desse usuário como "Administrador".

9. Rode o servidor:
   ```bash
   python manage.py runserver
   ```

10. Acesse `http://127.0.0.1:8000/`.

## Estrutura do projeto

```
clinica-medica/
├── accounts/       # Autenticação, perfis de usuário e gestão de funcionários
├── pacientes/       # Cadastro e histórico de pacientes
├── medicos/         # Cadastro de médicos e especialidades
├── consultas/        # Agendamento, calendário e prontuário
├── dashboard/       # Tela inicial com resumo
├── core/            # Configurações gerais do projeto Django
├── static/           # CSS e JavaScript customizados
├── templates/        # Template base compartilhado
└── requirements.txt  # Dependências do projeto
```

## Perfis de acesso

| Ação                          | Administrador | Recepcionista | Médico |
|-------------------------------|:--------------:|:--------------:|:------:|
| Gerenciar pacientes           | ✅              | ✅              | 👁️ (só quem já atendeu) |
| Gerenciar médicos             | ✅              | 👁️              | 👁️      |
| Gerenciar consultas           | ✅              | ✅              | 👁️ (só a própria agenda) |
| Preencher prontuário          | ✅              | ❌              | ✅      |
| Gerenciar funcionários        | ✅              | ❌              | ❌      |

👁️ = apenas visualização · ✅ = acesso completo · ❌ = sem acesso