import re
import sqlite3
from flask import Blueprint, request, session, jsonify
from banco import conectar_banco

# Rota chamada por fetch() (sem recarregar a página) quando o usuário adiciona um ícone novo
route_create_icone = Blueprint('create_icone', __name__)


@route_create_icone.route('/create_icone', methods=['POST'])
def create():
    if not session.get("usuario_email"):
        return jsonify(ok=False, erro="Sua sessão expirou. Entre novamente."), 401

    classe = request.form.get("classe", "").strip().lower()
    nome = request.form.get("nome", "").strip()

    # Aceita "mouse", "bi-mouse" ou "bi bi-mouse"
    classe = classe.replace("bi bi-", "bi-")
    if classe and not classe.startswith("bi-"):
        classe = "bi-" + classe

    if not re.fullmatch(r"bi-[a-z0-9]+(-[a-z0-9]+)*", classe) or len(classe) > 60:
        return jsonify(ok=False, erro="Nome de ícone inválido. Use algo como bi-mouse2."), 400

    if not nome:
        nome = classe[3:].replace("-", " ").capitalize()

    conexao = conectar_banco()
    try:
        conexao.execute("INSERT INTO icones (classe, nome) VALUES (?, ?)", (classe, nome[:40]))
        conexao.commit()
    except sqlite3.IntegrityError:
        return jsonify(ok=False, erro="Esse ícone já está na lista."), 409
    finally:
        conexao.close()

    return jsonify(ok=True, classe=classe, nome=nome[:40])
