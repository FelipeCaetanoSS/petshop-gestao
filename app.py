import re
from flask import Flask, render_template, request, url_for
from extensions import db


class PreviewMiddleware:
    """Define SCRIPT_NAME com o prefixo /preview/<id> para que o Flask
    use url_for() corretamente, gerando URLs completas como:
    /preview/RzFmaIyQZGSpSUQxYBnpc/tutores
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        match = re.match(r'^(/preview/[A-Za-z0-9_-]+)(/.*)?$', path)

        if match:
            script_name = match.group(1)
            path_info = match.group(2) or '/'
            environ['SCRIPT_NAME'] = environ.get('SCRIPT_NAME', '') + script_name
            environ['PATH_INFO'] = path_info

        return self.app(environ, start_response)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petshop.db"
    app.config["SECRET_KEY"] = "petshop-secret-key"

    app.wsgi_app = PreviewMiddleware(app.wsgi_app)

    db.init_app(app)

    from models import Tutor, Pet, Agendamento

    from controllers.tutores_controller import tutores_bp
    from controllers.pets_controller import pets_bp
    from controllers.agendamentos_controller import agendamentos_bp

    app.register_blueprint(tutores_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(agendamentos_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.context_processor
    def inject_url_for():
        return dict(url=url_for)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
