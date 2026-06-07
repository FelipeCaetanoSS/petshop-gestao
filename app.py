import os
import re
from flask import Flask, render_template, request, url_for
from extensions import db


class PreviewMiddleware:
    """Configura SCRIPT_NAME com o prefixo dinâmico da plataforma.

    Funciona em 3 cenários:
    1. URL já vem com /preview/<id> no PATH_INFO (local/dev)
    2. Plataforma envia X-Forwarded-Prefix (proxy reverso)
    3. Plataforma envia SCRIPT_NAME no environ WSGI
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        script_name = environ.get('SCRIPT_NAME', '')

        # 1. Se a plataforma ja definiu SCRIPT_NAME, confia nela
        if script_name:
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
            return self.app(environ, start_response)

        # 2. X-Forwarded-Prefix (proxy reverso tipo nginx)
        forwarded_prefix = environ.get('HTTP_X_FORWARDED_PREFIX', '')
        if forwarded_prefix:
            fp = forwarded_prefix.rstrip('/')
            environ['SCRIPT_NAME'] = environ.get('SCRIPT_NAME', '') + fp
            if path_info.startswith(fp):
                environ['PATH_INFO'] = path_info[len(fp):]
            return self.app(environ, start_response)

        # 3. Deteccao automatica: URL com /preview/<id> no path
        match = re.match(r'^(/preview/[A-Za-z0-9_-]+)(/.*)?$', path_info)
        if match:
            environ['SCRIPT_NAME'] = script_name + match.group(1)
            environ['PATH_INFO'] = match.group(2) or '/'

        return self.app(environ, start_response)


class DebugMiddleware:
    """Loga o ambiente WSGI para depurar o que chega na Avelum.
    Remova depois de identificar o problema."""
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        import sys
        items = dict(
            PATH_INFO=environ.get("PATH_INFO", ""),
            SCRIPT_NAME=environ.get("SCRIPT_NAME", ""),
            HTTP_X_FORWARDED_PREFIX=environ.get("HTTP_X_FORWARDED_PREFIX", ""),
            HTTP_X_FORWARDED_HOST=environ.get("HTTP_X_FORWARDED_HOST", ""),
            HTTP_HOST=environ.get("HTTP_HOST", ""),
            REQUEST_URI=environ.get("REQUEST_URI", ""),
            RAW_URI=environ.get("RAW_URI", ""),
        )
        print(f"[DEBUG] {items}", file=sys.stderr)
        return self.app(environ, start_response)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petshop.db"
    app.config["SECRET_KEY"] = "petshop-secret-key"

    app.wsgi_app = PreviewMiddleware(DebugMiddleware(app.wsgi_app))

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
