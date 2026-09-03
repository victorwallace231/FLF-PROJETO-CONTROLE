from flask import Flask, render_template
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
from routes.createitem import route_createitem
from routes.deleteitem import route_deleteitem
from routes.updateitem import route_updateitem
from routes.emprestimo import route_emprestimo
from routes.devolucao import route_devolucao

#registrando os blueprints das rotas
app.register_blueprint(route_login)
app.register_blueprint(route_dashboard)
app.register_blueprint(route_cadastro)
app.register_blueprint(route_updateuser)
app.register_blueprint(route_deleteuser)
app.register_blueprint(route_createitem)
app.register_blueprint(route_deleteitem)
app.register_blueprint(route_updateitem)
app.register_blueprint(route_emprestimo)
app.register_blueprint(route_devolucao)

#Rota principal do sistema
@app.route('/')
def index():
    return render_template('cadastro.html')
if __name__ == "__main__":
    app.run(debug=True) 
