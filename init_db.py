from app import create_app, db
from models import Tutor, Pet, Agendamento

app = create_app()

with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")
