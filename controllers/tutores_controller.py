from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.tutor import Tutor

tutores_bp = Blueprint("tutores", __name__, url_prefix="/tutores")


@tutores_bp.route("")
@tutores_bp.route("/")
def listar():
    tutores = Tutor.query.order_by(Tutor.nome).all()
    return render_template("tutores/lista.html", tutores=tutores)


@tutores_bp.route("/novo", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if not nome:
            flash("O nome do tutor é obrigatório.", "danger")
            return render_template("tutores/form.html", tutor=None)

        tutor = Tutor(
            nome=nome,
            telefone=request.form.get("telefone", "").strip(),
            email=request.form.get("email", "").strip(),
        )
        db.session.add(tutor)
        db.session.commit()
        flash("Tutor cadastrado com sucesso!", "success")
        return redirect(url_for("tutores.listar"))

    return render_template("tutores/form.html", tutor=None)


@tutores_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    tutor = Tutor.query.get_or_404(id)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if not nome:
            flash("O nome do tutor é obrigatório.", "danger")
            return render_template("tutores/form.html", tutor=tutor)

        tutor.nome = nome
        tutor.telefone = request.form.get("telefone", "").strip()
        tutor.email = request.form.get("email", "").strip()
        db.session.commit()
        flash("Tutor atualizado com sucesso!", "success")
        return redirect(url_for("tutores.listar"))

    return render_template("tutores/form.html", tutor=tutor)


@tutores_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    tutor = Tutor.query.get_or_404(id)

    if tutor.pets:
        flash(
            f"Não é possível excluir {tutor.nome} pois possui "
            f"{len(tutor.pets)} pet(s) vinculado(s).",
            "danger",
        )
        return redirect(url_for("tutores.listar"))

    db.session.delete(tutor)
    db.session.commit()
    flash("Tutor excluído com sucesso!", "success")
    return redirect(url_for("tutores.listar"))
