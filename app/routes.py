from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Usuario
from app import db

routes = Blueprint('routes', __name__)

# LOGIN
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            return redirect(url_for('routes.painel'))
        else:
            return "E-mail ou senha inválidos!", 401
    return render_template('login.html')

# LOGOUT
@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

# CADASTRO
@routes.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if Usuario.query.filter_by(email=email).first():
            return "E-mail já cadastrado.", 400

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('routes.login'))
    return render_template('register.html')

# PAINEL
@routes.route('/painel')
def painel():
    if 'usuario_id' not in session:
        return redirect(url_for('routes.login'))

    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('painel.html', nome_consultor=usuario.nome)

# INDICAR ALUNO
@routes.route('/indicar')
def indicar_aluno():
    return render_template('indicar.html')

# AJUDA
@routes.route('/ajuda')
def ajuda():
    return render_template('ajuda.html')

# COMISSÕES
@routes.route('/comissoes')
def comissoes():
    return render_template('comissoes.html')

# VENDAS
@routes.route('/vendas')
def vendas():
    return render_template('vendas.html')

# PÁGINA DE GRADUAÇÃO GERAL
@routes.route('/facsu-graduacao')
def facsu_graduacao_padrao():
    return render_template('facsu_graduacao.html')

# PÁGINA DE GRADUAÇÃO DE SÃO LUÍS (COM OFERTAS)
@routes.route('/ofertas-facsu')
def ofertas_facsu():
    curso = request.args.get('curso')
    cidade = request.args.get('cidade')

    session['curso_selecionado'] = curso
    session['cidade_selecionada'] = cidade

    return render_template('facsu_graduacao_sao_luis.html', curso=curso, cidade=cidade)

# ETAPA 1 – DADOS PESSOAIS
@routes.route('/facsu-inscricao-dados', methods=['GET', 'POST'])
def facsu_inscricao_dados():
    if request.method == 'POST':
        session['dados_pessoais'] = request.form.to_dict()
        return redirect(url_for('routes.facsu_inscricao_endereco'))
    return render_template('facsu_dados_pessoais.html')

# ETAPA 2 – ENDEREÇO
@routes.route('/facsu-inscricao-endereco', methods=['GET', 'POST'])
def facsu_inscricao_endereco():
    if request.method == 'POST':
        session['endereco'] = request.form.to_dict()
        return redirect(url_for('routes.facsu_inscricao_confirmacao'))
    return render_template('facsu_inscricao_endereco.html')

# ETAPA 3 – CONFIRMAÇÃO
@routes.route('/facsu-inscricao-confirmacao', methods=['GET', 'POST'])
def facsu_inscricao_confirmacao():
    if request.method == 'POST':
        return redirect(url_for('routes.facsu_inscricao_finalizar'))
    return render_template('facsu_inscricao_confirmacao.html')

# ETAPA FINAL – INSCRIÇÃO CONCLUÍDA
@routes.route('/facsu-inscricao-finalizar', methods=['GET'])
def facsu_inscricao_finalizar():
    return render_template('inscricao_finalizada.html')

# ROTA INICIAL
@routes.route('/')
def home():
    return redirect(url_for('routes.login'))
