from flask import Flask, render_template, redirect
from datetime import timedelta
app = Flask(__name__)
app.secret_key = '14082017'

app.config ['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

#Capturando as rotas dos arquivos de rotas
from routes.login import route_login
from routes.cadastro import route_cadastro
from routes.dashboard import route_dashboard
from routes.updateuser import route_updateuser
from routes.deleteuser import route_deleteuser
from routes.create_item import route_create_item
from routes.deleteitem import route_deleteitem
from routes.updateitem import route_updateitem
from routes.verifica_emprestimos import verifica_emprestimos
from routes.devolucao import route_devolucao
from routes.dashboard import route_equipamentos
from routes.create_emprestimo import create_emprestimo
from routes.login import route_logout
from routes.verifica_emprestimos import verifica_1emprestimo
from routes.update_emprestimo import update_emprestimo
from routes.user_historico import user_historico
from routes.create_categoria import create_categoria
from routes.recuperar_senha import recuperar_senha
from routes.redefinir_senha import redefinir_senha
from routes.delete_categoria import delete_categoria
from routes.update_categoria import update_categoria

#registrando os blueprints das rotas
app.register_blueprint(route_login)
app.register_blueprint(route_dashboard)
app.register_blueprint(route_cadastro)
app.register_blueprint(route_updateuser)
app.register_blueprint(route_deleteuser)
app.register_blueprint(route_create_item)
app.register_blueprint(route_deleteitem)
app.register_blueprint(route_updateitem)
app.register_blueprint(verifica_emprestimos)
app.register_blueprint(route_devolucao)
app.register_blueprint(route_equipamentos)
app.register_blueprint(create_emprestimo)
app.register_blueprint(route_logout)
app.register_blueprint(verifica_1emprestimo)
app.register_blueprint(update_emprestimo)
app.register_blueprint(user_historico)
app.register_blueprint(create_categoria)
app.register_blueprint(recuperar_senha)
app.register_blueprint(redefinir_senha)
app.register_blueprint(delete_categoria)
app.register_blueprint(update_categoria)

#Rota principal do sistema
@app.route('/')
def index():
    return redirect ('/cadastro')
if __name__ == "__main__":
    app.run(debug=True) 
