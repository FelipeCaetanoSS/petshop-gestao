from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petshop.db"
    app.config["SECRET_KEY"] = "petshop-secret-key"

    db.init_app(app)

    from controllers.tutores_controller import tutores_bp
    from controllers.pets_controller import pets_bp
    from controllers.agendamentos_controller import agendamentos_bp

    app.register_blueprint(tutores_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(agendamentos_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
