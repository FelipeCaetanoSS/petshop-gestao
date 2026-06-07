from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.agendamento import Agendamento, SERVICOS, STATUS_AGENDAMENTO
from models.pet import Pet

agendamentos_bp = Blueprint("agendamentos", __name__, url_prefix="/agendamentos")


@agendamentos_bp.route("")
@agendamentos_bp.route("/")
def listar():
    agendamentos = Agendamento.query.order_by(Agendamento.data, Agendamento.hora).all()
    return render_template("agendamentos/lista.html", agendamentos=agendamentos)


@agendamentos_bp.route("/novo", methods=["GET", "POST"])
def criar():
    pets = Pet.query.order_by(Pet.nome).all()

    if request.method == "POST":
        pet_id = request.form.get("pet_id", "").strip()
        servico = request.form.get("servico", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()

        if not pet_id:
            flash("O pet é obrigatório.", "danger")
            return render_template("agendamentos/form.html", agendamento=None, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)

        if not servico:
            flash("O serviço é obrigatório.", "danger")
            return render_template("agendamentos/form.html", agendamento=None, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)

        if not data:
            flash("A data é obrigatória.", "danger")
            return render_template("agendamentos/form.html", agendamento=None, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)

        if not hora:
            flash("A hora é obrigatória.", "danger")
            return render_template("agendamentos/form.html", agendamento=None, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)

        agendamento = Agendamento(
            pet_id=int(pet_id),
            servico=servico,
            data=data,
            hora=hora,
            status=request.form.get("status", "agendado"),
        )
        db.session.add(agendamento)
        db.session.commit()
        flash("Agendamento cadastrado com sucesso!", "success")
        return redirect(url_for("agendamentos.listar"))

    return render_template("agendamentos/form.html", agendamento=None, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)


@agendamentos_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    agendamento = Agendamento.query.get_or_404(id)
    pets = Pet.query.order_by(Pet.nome).all()

    if request.method == "POST":
        pet_id = request.form.get("pet_id", "").strip()
        servico = request.form.get("servico", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()

        if not pet_id:
            flash("O pet é obrigatório.", "danger")
            return render_template("agendamentos/form.html", agendamento=agendamento, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)

        if not servico:
            flash("O serviço é obrigatório.", "danger")
            return render_template("agendamentos/form.html", agendamento=agendamento, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)

        if not data:
            flash("A data é obrigatória.", "danger")
            return render_template("agendamentos/form.html", agendamento=agendamento, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)

        if not hora:
            flash("A hora é obrigatória.", "danger")
            return render_template("agendamentos/form.html", agendamento=agendamento, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)

        agendamento.pet_id = int(pet_id)
        agendamento.servico = servico
        agendamento.data = data
        agendamento.hora = hora
        agendamento.status = request.form.get("status", "agendado")
        db.session.commit()
        flash("Agendamento atualizado com sucesso!", "success")
        return redirect(url_for("agendamentos.listar"))

    return render_template("agendamentos/form.html", agendamento=agendamento, pets=pets, servicos=SERVICOS, status_list=STATUS_AGENDAMENTO)


@agendamentos_bp.route("/<int:id>/excluir", methods=["GET", "POST"])
def excluir(id):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()
    flash("Agendamento excluído com sucesso!", "success")
    return redirect(url_for("agendamentos.listar"))
