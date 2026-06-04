from extensions import db


class Tutor(db.Model):
    __tablename__ = "tutores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

    pets = db.relationship("Pet", backref="tutor", lazy=True)

    def __repr__(self):
        return f"<Tutor {self.nome}>"
