from extensions import db


class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(20), nullable=False)
    raca = db.Column(db.String(50))
    idade = db.Column(db.Integer)

    tutor_id = db.Column(db.Integer, db.ForeignKey("tutores.id"), nullable=False)

    agendamentos = db.relationship("Agendamento", backref="pet", lazy=True)

    def __repr__(self):
        return f"<Pet {self.nome}>"
