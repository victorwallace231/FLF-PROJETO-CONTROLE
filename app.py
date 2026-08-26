from flask import Flask, render_template

app = Flask(__name__)

from routes.login import route_login
from routes.cadastro import route_cadastro

app.register_blueprint(route_login)
app.register_blueprint(route_cadastro)
@app.route('/')
def index():
    return render_template('login.html')
if '__name__' == '__main__':
    app.run(debug=True) 
