import os
import sqlite3

# Caminho absoluto do banco: funciona de qualquer pasta em que o Flask for iniciado
# (antes dependia da pasta atual e do "Database_Controle.db" com D maiúsculo, que só
# encontrava o arquivo no Windows).
_PASTA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(_PASTA, "database_controle.db")

# Ícones do Bootstrap Icons já disponíveis para escolher no cadastro de equipamento.
# (classe do ícone, nome exibido). Novos ícones podem ser adicionados pela própria tela.
ICONE_PADRAO = "bi-pc-display"
ICONES_INICIAIS = [
    ("bi-pc-display", "Computador"),
    ("bi-display", "Monitor"),
    ("bi-laptop", "Notebook"),
    ("bi-mouse", "Mouse"),
    ("bi-keyboard", "Teclado"),
    ("bi-easel", "Passador de slide"),
    ("bi-projector", "Projetor"),
    ("bi-hdmi", "Adaptador HDMI"),
    ("bi-usb-plug", "Adaptador USB"),
    ("bi-usb-drive", "Pen drive"),
    ("bi-plug", "Cabo / Extensão"),
    ("bi-ethernet", "Cabo de rede"),
    ("bi-headset", "Headset"),
    ("bi-headphones", "Fone de ouvido"),
    ("bi-mic", "Microfone"),
    ("bi-webcam", "Webcam"),
    ("bi-speaker", "Caixa de som"),
    ("bi-tv", "TV"),
    ("bi-tablet", "Tablet"),
    ("bi-router", "Roteador"),
    ("bi-printer", "Impressora"),
    ("bi-hdd", "HD / SSD"),
]


# Função para conectar ao banco de dados
def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    return conexao


def iniciar_banco():
    """Prepara o banco para o controle de ícones. Pode rodar quantas vezes quiser:
    só cria/adiciona o que ainda não existe e nunca mexe nos dados já cadastrados."""
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS icones (
               id_icone INTEGER PRIMARY KEY AUTOINCREMENT,
               classe   TEXT NOT NULL UNIQUE,
               nome     TEXT NOT NULL
           )"""
    )

    colunas = [linha[1] for linha in cursor.execute("PRAGMA table_info(perifericos)")]
    if "icone" not in colunas:
        cursor.execute(f"ALTER TABLE perifericos ADD COLUMN icone TEXT NOT NULL DEFAULT '{ICONE_PADRAO}'")

    cursor.executemany("INSERT OR IGNORE INTO icones (classe, nome) VALUES (?, ?)", ICONES_INICIAIS)

    conexao.commit()
    conexao.close()


def listar_icones():
    conexao = conectar_banco()
    icones = conexao.execute("SELECT classe, nome FROM icones ORDER BY id_icone").fetchall()
    conexao.close()
    return icones


def icone_valido(classe):
    """Devolve a classe se ela existir na tabela de ícones; senão, o ícone padrão."""
    conexao = conectar_banco()
    achou = conexao.execute("SELECT 1 FROM icones WHERE classe = ?", (classe,)).fetchone()
    conexao.close()
    return classe if achou else ICONE_PADRAO
