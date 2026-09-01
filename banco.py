import sqlite3

# Função para conectar ao banco de dados
def conectar_banco():
    conexao= sqlite3.connect("Database_Controle.db")
    return conexao
