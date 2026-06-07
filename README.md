# Petshop Gestão

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

## Como Rodar (local)

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

## Deploy na Avelum Labs (Preview)

O sistema roda na Avelum Labs através de um proxy reverso que adiciona um prefixo dinâmico na URL:

```
https://workspace.avelum.com.br/preview/<hash>/
```

O `<hash>` é gerado automaticamente pela plataforma e varia a cada deploy.

### Como o roteamento funciona

O **DynamicPrefixMiddleware** em `app.py` detecta automaticamente o prefixo e configura o `SCRIPT_NAME` do Flask para que `url_for()` gere URLs corretas. O middleware funciona em 3 cenários:

1. **X-Forwarded-Prefix:** se a plataforma enviar este cabeçalho HTTP, o middleware usa o valor como prefixo.
2. **SCRIPT_NAME no environ WSGI:** se a plataforma já define `SCRIPT_NAME`, o middleware apenas ajusta o `PATH_INFO`.
3. **Detecção automática:** se nenhum dos dois estiver presente, o middleware analisa o `PATH_INFO` da requisição, compara com as rotas conhecidas do Flask e descobre qual parte é o prefixo.

### Requisitos para correta renderização de URLs

Para que os links sejam gerados com o prefixo (ex: `/preview/<hash>/tutores` em vez de apenas `/tutores`), é necessário que:

1. **Todos os templates** usem `{{ url('nome_rota') }}` em vez de URLs fixas. Isso já está implementado em todos os templates.
2. O **context_processor** injeta a função `url()` que delega para o `url_for()` do Flask, que por sua vez usa o `SCRIPT_NAME` configurado pelo middleware.

### Possíveis problemas

Se ao clicar em um link a URL mudar para `https://workspace.avelum.com.br/tutores` (sem o prefixo `/preview/<hash>/`), significa que:

1. O middleware não conseguiu detectar o prefixo na requisição inicial, ou
2. O `SCRIPT_NAME` não foi propagado corretamente para o `url_for()` durante a renderização do template.

**Solução:** Verificar se a plataforma está enviando o cabeçalho `X-Forwarded-Prefix`. Caso não esteja, configure a plataforma para enviá-lo, ou defina a variável de ambiente `SCRIPT_NAME` com o valor do prefixo (ex: `SCRIPT_NAME=/preview/<hash>`).

---

## Guia para criar novas rotas seguindo o padrão que funciona

Ao criar uma nova funcionalidade (ex: nova entidade, nova página), siga estes passos exatamente na ordem para garantir que o roteamento com prefixo funcione:

### 1. Criar o controller (Blueprint)

Arquivo: `controllers/minha_entidade_controller.py`

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.minha_entidade import MinhaEntidade

# Nome do blueprint: usar plural e semântico (ex: "produtos", "clientes")
# url_prefix: sempre começar com / e usar o mesmo nome do blueprint
meu_bp = Blueprint("minha_entidade", __name__, url_prefix="/minha-entidade")


@meu_bp.route("")
@meu_bp.route("/")
def listar():
    itens = MinhaEntidade.query.order_by(MinhaEntidade.nome).all()
    return render_template("minha_entidade/lista.html", itens=itens)


@meu_bp.route("/novo", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        # ... validar e salvar ...
        db.session.commit()
        flash("Item cadastrado com sucesso!", "success")
        return redirect(url_for("minha_entidade.listar"))

    return render_template("minha_entidade/form.html", item=None)


@meu_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = MinhaEntidade.query.get_or_404(id)
    if request.method == "POST":
        # ... atualizar ...
        db.session.commit()
        flash("Item atualizado com sucesso!", "success")
        return redirect(url_for("minha_entidade.listar"))
    return render_template("minha_entidade/form.html", item=item)


@meu_bp.route("/<int:id>/excluir", methods=["GET", "POST"])
def excluir(id):
    item = MinhaEntidade.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item excluído com sucesso!", "success")
    return redirect(url_for("minha_entidade.listar"))
```

**Regras importantes:**
- O `url_prefix` do blueprint **não** inclui o prefixo da plataforma (`/preview/<hash>/`). O middleware cuida disso automaticamente.
- Sempre defina a rota vazia `""` junto com `"/"` para aceitar a URL com e sem barra no final.
- Em redirects, SEMPRE use `url_for("minha_entidade.listar")`, nunca uma string fixa como `"/minha-entidade"`.

### 2. Registrar o Blueprint no `app.py`

Em `app.py`, dentro de `create_app()`, adicione o import e o registro **antes** da definição da rota `"/"`:

```python
from controllers.minha_entidade_controller import meu_bp
app.register_blueprint(meu_bp)
```

A ordem dos registros não importa, mas o registro precisa estar **antes da primeira requisição** (o que é garantido pois tudo está dentro de `create_app()`).

### 3. Criar os templates

Dentro de `templates/minha_entidade/`, crie `lista.html` e `form.html` seguindo o padrão:

**`lista.html`:**
```jinja
{% extends "base.html" %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Minha Entidade</h1>
    <a href="{{ url('minha_entidade.criar') }}" class="btn btn-primary">Novo</a>
</div>

{% if itens %}
<table class="table table-striped">
    <thead>
        <tr>
            <th>Nome</th>
            <th>Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for item in itens %}
        <tr>
            <td>{{ item.nome }}</td>
            <td>
                <a href="{{ url('minha_entidade.editar', id=item.id) }}" class="btn btn-sm btn-warning">Editar</a>
                <a href="{{ url('minha_entidade.excluir', id=item.id) }}" class="btn btn-sm btn-danger"
                   onclick="return confirm('Tem certeza?')">Excluir</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p class="text-muted">Nenhum item cadastrado ainda.</p>
{% endif %}
{% endblock %}
```

**`form.html`:**
```jinja
{% extends "base.html" %}
{% block content %}
<h1>{{ "Editar" if item else "Novo" }}</h1>

<form method="POST" action="{{ url('minha_entidade.criar') if not item else url('minha_entidade.editar', id=item.id) }}">
    <div class="mb-3">
        <label for="nome" class="form-label">Nome</label>
        <input type="text" class="form-control" id="nome" name="nome" required
               value="{{ item.nome if item else '' }}">
    </div>
    <div class="d-flex gap-2">
        <button type="submit" class="btn btn-success">Salvar</button>
        <a href="{{ url('minha_entidade.listar') }}" class="btn btn-secondary">Cancelar</a>
    </div>
</form>
{% endblock %}
```

**Regras de ouro para templates:**
- **NUNCA** use URLs fixas como `<a href="/minha-entidade">` ou `<form action="/minha-entidade/novo">`. Sempre use `{{ url('minha_entidade.listar') }}`.
- **NUNCA** use `{{ url_for('...') }}` diretamente. Use `{{ url('...') }}` — a função `url()` é injetada pelo context processor e já lida com o prefixo dinamicamente.
- O nome do endpoint segue o padrão `nome_do_blueprint.nome_da_funcao`. Ex: blueprint `minha_entidade` + função `listar` = `{{ url('minha_entidade.listar') }}`.

### 4. Adicionar link na navbar (`base.html`)

```jinja
<li class="nav-item">
    <a class="nav-link" href="{{ url('minha_entidade.listar') }}">Minha Entidade</a>
</li>
```

### 5. Adicionar link na página inicial (`index.html`)

```jinja
<div class="col-md-3 mb-3">
    <a href="{{ url('minha_entidade.listar') }}" class="btn btn-outline-primary btn-lg w-100">Minha Entidade</a>
</div>
```

### Checklist para nova rota

- [ ] Controller criado com `Blueprint("nome", __name__, url_prefix="/nome")`
- [ ] Blueprint registrado em `app.py` com `app.register_blueprint(...)`
- [ ] Rotas do CRUD (`""`, `"/"`, `"/novo"`, `"/<int:id>/editar"`, `"/<int:id>/excluir"`)
- [ ] Todos os `redirect()` usam `url_for("blueprint.funcao")`
- [ ] Todos os templates usam `{{ url('blueprint.funcao') }}` — **sem URLs fixas**
- [ ] Link adicionado na navbar em `base.html`
- [ ] Link adicionado na página inicial em `index.html`

---

## Arquitetura (MVC)

```
petshop-gestao/
├── app.py                 # criação da app Flask + DynamicPrefixMiddleware
├── models/                # models SQLAlchemy
│   ├── __init__.py
│   ├── tutor.py
│   ├── pet.py
│   └── agendamento.py
├── controllers/           # blueprints com as rotas
│   ├── __init__.py
│   ├── tutores_controller.py
│   ├── pets_controller.py
│   └── agendamentos_controller.py
├── templates/             # Jinja2 templates
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
└── README.md              # esta documentação
```

## Etapas do Projeto

| Etapa | Funcionalidade | Status |
|-------|---------------|--------|
| 1 | Estrutura do projeto + banco de dados | ✅ |
| 2 | CRUD Tutores | ✅ |
| 3 | CRUD Pets | ✅ |
| 4 | CRUD Agendamentos | ✅ |
| 5 | Agenda do Dia | ✅ |
| 6 | Navegação e Layout | ✅ |
