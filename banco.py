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
    conexao.row_factory = sqlite3.Row
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

    colunas_user = [linha[1] for  linha in cursor.execute("PRAGMA table_info(usuario)")]
    if "role" not in colunas_user:
        cursor.execute("""ALTER TABLE usuario ADD COLUMN role TEXT NOT NULL    DEFAULT 'user' CHECK (role in ('admin', 'gestor', 'user'))""")
        cursor.execute("UPDATE usuario SET role = 'admin' WHERE admin = 1")

    # Unidades e setores (um setor pertence a UMA unidade: unidades diferentes podem ter
    # setores com o mesmo nome, ex.: "Administração")
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS unidades (
               id_unidade   INTEGER PRIMARY KEY AUTOINCREMENT,
               nome_unidade TEXT NOT NULL UNIQUE COLLATE NOCASE,
               excluido     INTEGER NOT NULL DEFAULT 0 CHECK (excluido IN (0, 1))
           )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS setores (
               id_setor   INTEGER PRIMARY KEY AUTOINCREMENT,
               nome_setor TEXT NOT NULL COLLATE NOCASE,
               id_unidade INTEGER NOT NULL,
               excluido   INTEGER NOT NULL DEFAULT 0 CHECK (excluido IN (0, 1)),
               FOREIGN KEY (id_unidade) REFERENCES unidades (id_unidade),
               UNIQUE (id_unidade, nome_setor)
           )"""
    )
    # Exclusão lógica (igual a categorias.excluido): o registro fica no banco, só some das listas
    for tabela in ("unidades", "setores"):
        existentes = [linha[1] for linha in cursor.execute(f"PRAGMA table_info({tabela})")]
        if "excluido" not in existentes:
            cursor.execute(
                f"ALTER TABLE {tabela} ADD COLUMN excluido INTEGER NOT NULL DEFAULT 0 CHECK (excluido IN (0, 1))"
            )
    conexao.commit()

    _migrar_origem_para_chave_estrangeira(conexao)
    conexao.close()


def _migrar_origem_para_chave_estrangeira(conexao):
    """perifericos.unid_origem / setor_origem (texto livre) viram id_unidade_origem /
    id_setor_origem (chaves estrangeiras). Os textos já cadastrados são convertidos em
    unidades/setores. Só roda uma vez: depois da migração a coluna antiga não existe mais."""
    cursor = conexao.cursor()
    colunas = [linha[1] for linha in cursor.execute("PRAGMA table_info(perifericos)")]
    if "id_unidade_origem" in colunas or "unid_origem" not in colunas:
        return

    try:
        conexao.execute("BEGIN")

        # 1) cada par (unidade, setor) digitado antes vira um registro nas tabelas novas
        pares = cursor.execute(
            "SELECT DISTINCT TRIM(unid_origem), TRIM(setor_origem) FROM perifericos"
        ).fetchall()
        for unidade, setor in pares:
            unidade = unidade or "Sem unidade"
            setor = setor or "Sem setor"
            cursor.execute("INSERT OR IGNORE INTO unidades (nome_unidade) VALUES (?)", (unidade,))
            id_unidade = cursor.execute(
                "SELECT id_unidade FROM unidades WHERE nome_unidade = ?", (unidade,)
            ).fetchone()[0]
            cursor.execute(
                "INSERT OR IGNORE INTO setores (nome_setor, id_unidade) VALUES (?, ?)", (setor, id_unidade)
            )

        # 2) a tabela é refeita (o SQLite não troca o tipo de uma coluna com ALTER)
        sequencia = cursor.execute(
            "SELECT seq FROM sqlite_sequence WHERE name = 'perifericos'"
        ).fetchone()
        cursor.execute(
            """CREATE TABLE perifericos_novo (
                   id_periferico     INTEGER PRIMARY KEY AUTOINCREMENT,
                   categoria         TEXT NOT NULL,
                   marca             TEXT,
                   num_serie         TEXT,
                   disponivel        INTEGER DEFAULT 1 CHECK (disponivel IN (0, 1)),
                   manutencao        INTEGER DEFAULT 0 CHECK (manutencao IN (0, 1)),
                   inativo           INTEGER NOT NULL DEFAULT 0 CHECK (inativo IN (0, 1)),
                   id_unidade_origem INTEGER NOT NULL,
                   id_setor_origem   INTEGER NOT NULL,
                   unid_atual        TEXT NOT NULL,
                   setor_atual       TEXT NOT NULL,
                   transferido       INTEGER NOT NULL DEFAULT 0 CHECK (transferido IN (0, 1)),
                   icone             TEXT NOT NULL DEFAULT 'bi-pc-display',
                   FOREIGN KEY (categoria)         REFERENCES categorias (id_categoria),
                   FOREIGN KEY (id_unidade_origem) REFERENCES unidades (id_unidade),
                   FOREIGN KEY (id_setor_origem)   REFERENCES setores (id_setor)
               )"""
        )
        cursor.execute(
            """INSERT INTO perifericos_novo
                   (id_periferico, categoria, marca, num_serie, disponivel, manutencao, inativo,
                    id_unidade_origem, id_setor_origem, unid_atual, setor_atual, transferido, icone)
               SELECT p.id_periferico, p.categoria, p.marca, p.num_serie, p.disponivel, p.manutencao, p.inativo,
                      u.id_unidade, s.id_setor, p.unid_atual, p.setor_atual, p.transferido, p.icone
               FROM perifericos p
               JOIN unidades u ON u.nome_unidade = COALESCE(NULLIF(TRIM(p.unid_origem), ''), 'Sem unidade')
               JOIN setores  s ON s.id_unidade = u.id_unidade
                              AND s.nome_setor = COALESCE(NULLIF(TRIM(p.setor_origem), ''), 'Sem setor')"""
        )

        antes = cursor.execute("SELECT COUNT(*) FROM perifericos").fetchone()[0]
        depois = cursor.execute("SELECT COUNT(*) FROM perifericos_novo").fetchone()[0]
        if antes != depois:
            raise RuntimeError(f"Migração cancelada: {antes} equipamentos antes, {depois} depois.")

        cursor.execute("DROP TABLE perifericos")
        cursor.execute("ALTER TABLE perifericos_novo RENAME TO perifericos")
        if sequencia:
            cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'perifericos'", (sequencia[0],))
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise


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


def listar_unidades():
    """Unidades NÃO excluídas, em ordem alfabética (lista de dicionários, pronta para o tojson)."""
    conexao = conectar_banco()
    linhas = conexao.execute(
        "SELECT id_unidade, nome_unidade FROM unidades WHERE excluido = 0 ORDER BY nome_unidade COLLATE NOCASE"
    ).fetchall()
    conexao.close()
    return [dict(l) for l in linhas]


def listar_setores():
    """Setores NÃO excluídos (de unidades não excluídas), com o id da unidade (o JS filtra por unidade)."""
    conexao = conectar_banco()
    linhas = conexao.execute(
        """SELECT s.id_setor, s.nome_setor, s.id_unidade
           FROM setores s JOIN unidades u ON u.id_unidade = s.id_unidade
           WHERE s.excluido = 0 AND u.excluido = 0
           ORDER BY s.nome_setor COLLATE NOCASE"""
    ).fetchall()
    conexao.close()
    return [dict(l) for l in linhas]


def resolver_localizacao(cursor, id_unidade, id_setor):
    """Confere o par vindo do formulário e devolve (nome_unidade, nome_setor).
    - ambos vazios            -> ("", "")  (o chamador decide se isso é permitido)
    - setor da unidade certa  -> os nomes
    - qualquer outra coisa    -> None (id inexistente, EXCLUÍDO, ou setor de OUTRA unidade)"""
    id_unidade = (id_unidade or "").strip()
    id_setor = (id_setor or "").strip()
    if not id_unidade and not id_setor:
        return ("", "")
    if not (id_unidade.isdigit() and id_setor.isdigit()):
        return None
    linha = cursor.execute(
        """SELECT u.nome_unidade, s.nome_setor
           FROM setores s JOIN unidades u ON u.id_unidade = s.id_unidade
           WHERE s.id_setor = ? AND u.id_unidade = ? AND s.excluido = 0 AND u.excluido = 0""",
        (id_setor, id_unidade),
    ).fetchone()
    return (linha[0], linha[1]) if linha else None
