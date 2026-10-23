import os
import secrets
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, render_template, redirect

# Carrega as configurações locais do arquivo .env, caso exista.
# Em produção, as variáveis também podem ser definidas pelo servidor/Compose.
load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "").strip()

if not SECRET_KEY:
    if APP_ENV == "production":
        raise RuntimeError(
            "FLASK_SECRET_KEY não foi definida. Configure uma chave secreta forte "
            "nas variáveis de ambiente antes de iniciar em produção."
        )

    # Conveniência apenas para desenvolvimento local. Esta chave muda a cada
    # inicialização; sessões locais podem ser invalidadas quando o app reiniciar.
    SECRET_KEY = secrets.token_hex(32)
    print(
        "AVISO: FLASK_SECRET_KEY não definida. Foi gerada uma chave temporária "
        "para desenvolvimento; configure-a no .env para manter as sessões entre reinícios."
    )

app = Flask(__name__)
app.config.update(
    SECRET_KEY=SECRET_KEY,
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    # Secure deve ficar ligado em produção quando o site for acessado por HTTPS.
    SESSION_COOKIE_SECURE=(
        os.getenv("SESSION_COOKIE_SECURE", "1" if APP_ENV == "production" else "0")
        .strip()
        .lower()
        in ("1", "true", "yes", "on")
    ),
)

from banco import iniciar_banco, listar_unidades, listar_setores, listar_unidades_filtro, listar_setores_filtro
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
from routes.create_icone import route_create_icone
from routes.updateuser import route_updatetoadmin
from routes.updateuser import route_removeadmin
from routes.updateuser import route_update_user_adm
from routes.localizacoes import route_localizacoes

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
app.register_blueprint(route_create_icone)
app.register_blueprint(route_updatetoadmin)
app.register_blueprint(route_removeadmin)
app.register_blueprint(route_update_user_adm)
app.register_blueprint(route_localizacoes)

# Deixa as listas de unidades e setores disponíveis em TODOS os templates (os <select> de
# localização). São funções: o banco só é consultado onde o template realmente chama.
@app.context_processor
def injetar_localizacoes():
    return dict(
        lista_unidades=listar_unidades,
        lista_setores=listar_setores,
        lista_unidades_filtro=listar_unidades_filtro,
        lista_setores_filtro=listar_setores_filtro,
    )

# Garante a coluna/tabela de ícones no banco (só cria o que ainda não existe)
iniciar_banco()

#Rota principal do sistema
@app.route('/')
def index():
    return redirect ('/cadastro')
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000" if APP_ENV != "production" else "8080"))

    if APP_ENV == "production":
        # Servidor WSGI de produção (funciona no Windows e Linux).
        from waitress import serve

        host = os.getenv("HOST", "127.0.0.1")
        print(f"FLF Controle iniciado pelo Waitress em {host}:{port}")
        serve(app, host=host, port=port)
    else:
        # Servidor de desenvolvimento, restrito à própria máquina.
        app.run(debug=True, host="127.0.0.1", port=port)
