from app import db

SERVICOS = ["banho", "tosa", "hospedagem", "consulta"]
STATUS_AGENDAMENTO = ["agendado", "concluido", "cancelado"]

class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    servico = db.Column(db.String(20), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="agendado")

    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)

    def __repr__(self):
        return f"<Agendamento {self.servico} {self.data}>"
