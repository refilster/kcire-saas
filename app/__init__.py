from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'sua_chave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import routes
    app.register_blueprint(routes)

    return app
