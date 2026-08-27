from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = '14082017'

#Capturando as rotas dos arquivos de rotas
from routes.login import route_login
from routes.cadastro import route_cadastro
from routes.dashboard import route_dashboard

#registrando os blueprints das rotas
app.register_blueprint(route_login)
app.register_blueprint(route_dashboard)
app.register_blueprint(route_cadastro)

#Rota principal do sistema
@app.route('/')
def index():
    return render_template('cadastro.html')
if __name__ == "__main__":
    app.run(debug=True) 
