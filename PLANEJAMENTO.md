# Planejamento — Sistema CRUD Petshop

## 1. Visão Geral

Sistema web para gestão de um petshop com cadastro de tutores, pets e agendamentos de serviços.

**Stack:** Python + Flask + Jinja2 + SQLite  
**Autenticação:** Não (sistema aberto)  
**Público-alvo:** Funcionários do petshop (uso interno)

---

## 2. Entidades e Relacionamentos

```
Tutor (1) ──── (N) Pet (1) ──── (N) Agendamento
```

### Tutor
| Campo     | Tipo     | Restrições            |
|-----------|----------|-----------------------|
| id        | INTEGER  | PK, auto increment    |
| nome      | TEXT     | NOT NULL              |
| telefone  | TEXT     | —                     |
| email     | TEXT     | —                     |

### Pet
| Campo     | Tipo     | Restrições                     |
|-----------|----------|--------------------------------|
| id        | INTEGER  | PK, auto increment             |
| nome      | TEXT     | NOT NULL                       |
| especie   | TEXT     | NOT NULL, enum: cão/gato/outro |
| raca      | TEXT     | —                              |
| idade     | INTEGER  | —                              |
| tutor_id  | INTEGER  | FK → Tutor(id), NOT NULL       |

### Agendamento
| Campo     | Tipo     | Restrições                                |
|-----------|----------|-------------------------------------------|
| id        | INTEGER  | PK, auto increment                        |
| pet_id    | INTEGER  | FK → Pet(id), NOT NULL                    |
| servico   | TEXT     | NOT NULL, enum: banho/tosa/hospedagem/consulta |
| data      | TEXT     | NOT NULL (ISO: YYYY-MM-DD)                |
| hora      | TEXT     | NOT NULL (HH:MM)                          |
| status    | TEXT     | NOT NULL, DEFAULT 'agendado', enum: agendado/concluido/cancelado |

---

## 3. Regras de Negócio

- **Pet obrigatoriamente vinculado a um tutor** no momento da criação.
- **Agendamento obrigatoriamente vinculado a um pet.**
- **Proteção ao excluir tutor:** se o tutor possui pets cadastrados, o sistema **impede a exclusão** e exibe uma mensagem de aviso com a quantidade de pets vinculados.
- **Agenda do dia:** exibe agendamentos filtrados por data (hoje por padrão), ordenados por horário.
- **Validação:** campos NOT NULL (nome do pet, tutor do pet, pet do agendamento, serviço, data, hora) são validados no backend.

---

## 4. Etapas de Implementação

### Etapa 1 — Estrutura do Projeto e Banco de Dados
- [ ] Criar estrutura de diretórios
- [ ] Criar `requirements.txt` (flask)
- [ ] Criar `app.py` com configuração do Flask
- [ ] Criar `models.py` com as 3 tabelas (SQLite via sqlite3 nativo ou Flask-SQLAlchemy — **a decidir**)
- [ ] Criar script de inicialização do banco (`init_db.py`)

### Etapa 2 — CRUD Tutores
- [ ] Rota GET `/tutores` — listar todos
- [ ] Rota GET/POST `/tutores/novo` — formulário de criação
- [ ] Rota GET/POST `/tutores/<id>/editar` — formulário de edição
- [ ] Rota POST `/tutores/<id>/excluir` — excluir com proteção (impedir se tiver pets)
- [ ] Templates: `lista_tutores.html`, `form_tutor.html`

### Etapa 3 — CRUD Pets
- [ ] Rota GET `/pets` — listar todos (com nome do tutor)
- [ ] Rota GET/POST `/pets/novo` — formulário com select de tutores
- [ ] Rota GET/POST `/pets/<id>/editar`
- [ ] Rota POST `/pets/<id>/excluir`
- [ ] Templates: `lista_pets.html`, `form_pet.html`

### Etapa 4 — CRUD Agendamentos
- [ ] Rota GET `/agendamentos` — listar todos
- [ ] Rota GET/POST `/agendamentos/novo` — formulário com select de pets
- [ ] Rota GET/POST `/agendamentos/<id>/editar`
- [ ] Rota POST `/agendamentos/<id>/excluir`
- [ ] Templates: `lista_agendamentos.html`, `form_agendamento.html`

### Etapa 5 — Agenda do Dia
- [ ] Rota GET `/agenda` — exibe agendamentos de hoje
- [ ] Campo para selecionar data e filtrar
- [ ] Ordenação por horário
- [ ] Template: `agenda.html`

### Etapa 6 — Navegação e Layout (se aplicável)
- [ ] Menu de navegação entre as seções
- [ ] Estilo básico (CSS opcional, pode ser só HTML funcional)
- [ ] Mensagens flash para feedback (sucesso/erro)

---

## 5. Decisões Técnicas (a definir)

---

## 6. Estrutura de Diretórios (MVC)

```
petshop-gestao/
├── app.py                 # criação da app Flask
├── models/
│   ├── __init__.py
│   ├── tutor.py
│   ├── pet.py
│   └── agendamento.py
├── controllers/
│   ├── __init__.py
│   ├── tutores_controller.py
│   ├── pets_controller.py
│   └── agendamentos_controller.py
├── templates/
│   ├── base.html          # layout base com Bootstrap + navbar
│   ├── index.html         # página inicial
│   ├── tutores/
│   │   ├── lista.html
│   │   └── form.html
│   ├── pets/
│   │   ├── lista.html
│   │   └── form.html
│   └── agendamentos/
│       ├── lista.html
│       ├── form.html
│       └── agenda.html
├── init_db.py             # criação das tabelas
├── requirements.txt       # dependências
├── PLANEJAMENTO.md        # este arquivo
└── README.md              # documentação do projeto
```
