from flask import Flask
from app.routes import routes  # importa as rotas para registrar

app = Flask(__name__)
app.register_blueprint(routes)
