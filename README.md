# 🐾 Petshop Gestão

> Projeto proposto no curso da **Avelum Labs** — [Avelum IA](https://avelum.ai)

Sistema web CRUD para gestão de um petshop. Cadastro de tutores, pets e agendamentos de serviços.

**Stack:** Python + Flask + SQLAlchemy + Jinja2 + SQLite + Bootstrap

---

## Funcionalidades

- **Tutores:** cadastrar, listar, editar e excluir (com proteção ao excluir tutores com pets vinculados)
- **Pets:** cadastrar, listar, editar e excluir (vinculados a um tutor)
- **Agendamentos:** cadastrar, listar, editar e excluir (vinculados a um pet, com tipo de serviço e status)
- **Agenda do Dia:** visualização dos agendamentos filtrados por data, ordenados por horário

## Entidades e Relacionamentos

```
Tutor (1) ──── (N) Pet (1) ──── (N) Agendamento
```

## Como Rodar

```bash
# 1. Clone o repositório
git clone <url>
cd petshop-gestao

# 2. Crie um virtualenv (opcional, mas recomendado)
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicialize o banco de dados
python init_db.py

# 5. Execute o servidor
python app.py
```

Acesse: http://localhost:5000

---

## Etapas do Projeto

O projeto foi construído seguindo este plano:

| Etapa | Funcionalidade | Status |
|-------|---------------|--------|
| 1 | Estrutura do projeto + banco de dados | ✅ |
| 2 | CRUD Tutores | ✅ |
| 3 | CRUD Pets | ✅ |
| 4 | CRUD Agendamentos | ✅ |
| 5 | Agenda do Dia | ✅ |
| 6 | Navegação e Layout | ✅ |

> Cada etapa foi implementada, testada e validada antes de passar para a próxima.
