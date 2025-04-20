from flask import Flask
from app.models import db  # <-- Aqui importa corretamente agora
from app.routes import routes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'kcire-top-segredo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(routes)

    return app
