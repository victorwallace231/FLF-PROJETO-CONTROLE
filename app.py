from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = '14082017'

#Capturando as rotas dos arquivos de rotas
from routes.login import route_login
from routes.cadastro import route_cadastro
from routes.dashboard import route_dashboard
from routes.updateuser import route_updateuser
from routes.deleteuser import route_deleteuser
from routes.createitem import route_createitem
from routes.deleteitem import route_deleteitem
from routes.updateitem import route_updateitem

#registrando os blueprints das rotas
app.register_blueprint(route_login)
app.register_blueprint(route_dashboard)
app.register_blueprint(route_cadastro)
app.register_blueprint(route_updateuser)
app.register_blueprint(route_deleteuser)
app.register_blueprint(route_createitem)
app.register_blueprint(route_deleteitem)
app.register_blueprint(route_updateitem)

#Rota principal do sistema
@app.route('/')
def index():
    return render_template('cadastro.html')
if __name__ == "__main__":
    app.run(debug=True) 
