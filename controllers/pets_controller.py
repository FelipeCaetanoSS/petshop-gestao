from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.pet import Pet
from models.tutor import Tutor

pets_bp = Blueprint("pets", __name__, url_prefix="/pets")


@pets_bp.route("")
@pets_bp.route("/")
def listar():
    pets = Pet.query.order_by(Pet.nome).all()
    return render_template("pets/lista.html", pets=pets)


@pets_bp.route("/novo", methods=["GET", "POST"])
def criar():
    tutores = Tutor.query.order_by(Tutor.nome).all()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        especie = request.form.get("especie", "").strip()
        tutor_id = request.form.get("tutor_id", "").strip()

        if not nome:
            flash("O nome do pet é obrigatório.", "danger")
            return render_template("pets/form.html", pet=None, tutores=tutores)

        if not especie:
            flash("A espécie do pet é obrigatória.", "danger")
            return render_template("pets/form.html", pet=None, tutores=tutores)

        if not tutor_id:
            flash("O tutor do pet é obrigatório.", "danger")
            return render_template("pets/form.html", pet=None, tutores=tutores)

        idade = request.form.get("idade", "").strip()
        idade = int(idade) if idade else None

        pet = Pet(
            nome=nome,
            especie=especie,
            raca=request.form.get("raca", "").strip(),
            idade=idade,
            tutor_id=int(tutor_id),
        )
        db.session.add(pet)
        db.session.commit()
        flash("Pet cadastrado com sucesso!", "success")
        return redirect(url_for("pets.listar"))

    return render_template("pets/form.html", pet=None, tutores=tutores)


@pets_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    pet = Pet.query.get_or_404(id)
    tutores = Tutor.query.order_by(Tutor.nome).all()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        especie = request.form.get("especie", "").strip()
        tutor_id = request.form.get("tutor_id", "").strip()

        if not nome:
            flash("O nome do pet é obrigatório.", "danger")
            return render_template("pets/form.html", pet=pet, tutores=tutores)

        if not especie:
            flash("A espécie do pet é obrigatória.", "danger")
            return render_template("pets/form.html", pet=pet, tutores=tutores)

        if not tutor_id:
            flash("O tutor do pet é obrigatório.", "danger")
            return render_template("pets/form.html", pet=pet, tutores=tutores)

        idade = request.form.get("idade", "").strip()
        idade = int(idade) if idade else None

        pet.nome = nome
        pet.especie = especie
        pet.raca = request.form.get("raca", "").strip()
        pet.idade = idade
        pet.tutor_id = int(tutor_id)
        db.session.commit()
        flash("Pet atualizado com sucesso!", "success")
        return redirect(url_for("pets.listar"))

    return render_template("pets/form.html", pet=pet, tutores=tutores)


@pets_bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    pet = Pet.query.get_or_404(id)

    if pet.agendamentos:
        flash(
            f"Não é possível excluir {pet.nome} pois possui "
            f"{len(pet.agendamentos)} agendamento(s) vinculado(s).",
            "danger",
        )
        return redirect(url_for("pets.listar"))

    db.session.delete(pet)
    db.session.commit()
    flash("Pet excluído com sucesso!", "success")
    return redirect(url_for("pets.listar"))
