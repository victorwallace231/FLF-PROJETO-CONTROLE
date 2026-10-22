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
    # SQLite só aplica FOREIGN KEY quando essa opção é ativada em cada conexão.
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def iniciar_banco():
    """Prepara o esquema e aplica migrações idempotentes sem perder registros.

    Pode rodar em toda inicialização: os dados de equipamentos e o histórico são
    preservados; migrações já aplicadas não são repetidas.
    """
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
    _migrar_localizacao_atual_para_chave_estrangeira(conexao)
    conexao.close()


def _migrar_origem_para_chave_estrangeira(conexao):
    """perifericos.unid_origem / setor_origem (texto livre) viram id_unidade_origem /
    id_setor_origem (chaves estrangeiras). Os textos já cadastrados são convertidos em
    unidades/setores. Só roda uma vez: depois da migração a coluna antiga não existe mais."""
    cursor = conexao.cursor()
    colunas = [linha[1] for linha in cursor.execute("PRAGMA table_info(perifericos)")]
    if "id_unidade_origem" in colunas or "unid_origem" not in colunas:
        return

    # A tabela emprestimos referencia perifericos. Desabilitamos temporariamente a
    # validação durante a reconstrução da tabela e reativamos logo depois.
    conexao.execute("PRAGMA foreign_keys = OFF")
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
    finally:
        conexao.execute("PRAGMA foreign_keys = ON")


def _migrar_localizacao_atual_para_chave_estrangeira(conexao):
    """Converte a localização atual dos equipamentos de nomes para IDs.

    Mantém os IDs e os demais dados dos equipamentos. Se um nome antigo de unidade
    ou setor não existir no cadastro, cria o registro necessário para que a migração
    preserve a localização que estava salva. A função é idempotente.
    """
    cursor = conexao.cursor()
    colunas = [linha[1] for linha in cursor.execute("PRAGMA table_info(perifericos)")]

    # Já migrado.
    if "id_unidade_atual" in colunas and "id_setor_atual" in colunas:
        return

    # Banco incompleto ou inesperado: não tenta adivinhar como converter os dados.
    if "unid_atual" not in colunas or "setor_atual" not in colunas:
        raise RuntimeError(
            "Não foi possível migrar a localização atual: as colunas antigas "
            "unid_atual/setor_atual não foram encontradas."
        )

    def garantir_unidade(nome, id_unidade_origem):
        nome = (nome or "").strip()
        if not nome and id_unidade_origem:
            existe = cursor.execute(
                "SELECT id_unidade FROM unidades WHERE id_unidade = ?", (id_unidade_origem,)
            ).fetchone()
            if existe:
                return existe["id_unidade"]
        if not nome:
            nome = "Sem unidade"
        linha = cursor.execute(
            "SELECT id_unidade FROM unidades WHERE nome_unidade = ? COLLATE NOCASE", (nome,)
        ).fetchone()
        if linha:
            return linha["id_unidade"]
        cursor.execute("INSERT INTO unidades (nome_unidade) VALUES (?)", (nome,))
        return cursor.lastrowid

    def garantir_setor(nome, id_unidade, id_setor_origem):
        nome = (nome or "").strip()
        if not nome and id_setor_origem:
            linha = cursor.execute(
                "SELECT id_setor FROM setores WHERE id_setor = ? AND id_unidade = ?",
                (id_setor_origem, id_unidade),
            ).fetchone()
            if linha:
                return linha["id_setor"]
        if not nome:
            nome = "Sem setor"
        linha = cursor.execute(
            "SELECT id_setor FROM setores WHERE id_unidade = ? AND nome_setor = ? COLLATE NOCASE",
            (id_unidade, nome),
        ).fetchone()
        if linha:
            return linha["id_setor"]
        cursor.execute(
            "INSERT INTO setores (nome_setor, id_unidade) VALUES (?, ?)", (nome, id_unidade)
        )
        return cursor.lastrowid

    # Captura os registros antes de reconstruir a tabela.
    equipamentos = cursor.execute(
        """SELECT id_periferico, categoria, marca, num_serie, disponivel, manutencao, inativo,
                  id_unidade_origem, id_setor_origem, unid_atual, setor_atual, transferido, icone
           FROM perifericos ORDER BY id_periferico"""
    ).fetchall()
    sequencia = cursor.execute(
        "SELECT seq FROM sqlite_sequence WHERE name = 'perifericos'"
    ).fetchone()

    conexao.execute("PRAGMA foreign_keys = OFF")
    try:
        conexao.execute("BEGIN")
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
                   id_unidade_atual  INTEGER NOT NULL,
                   id_setor_atual    INTEGER NOT NULL,
                   transferido       INTEGER NOT NULL DEFAULT 0 CHECK (transferido IN (0, 1)),
                   icone             TEXT NOT NULL DEFAULT 'bi-pc-display',
                   FOREIGN KEY (categoria)          REFERENCES categorias (id_categoria),
                   FOREIGN KEY (id_unidade_origem)  REFERENCES unidades (id_unidade),
                   FOREIGN KEY (id_setor_origem)    REFERENCES setores (id_setor),
                   FOREIGN KEY (id_unidade_atual)   REFERENCES unidades (id_unidade),
                   FOREIGN KEY (id_setor_atual)     REFERENCES setores (id_setor)
               )"""
        )

        for item in equipamentos:
            id_unidade_atual = garantir_unidade(item["unid_atual"], item["id_unidade_origem"])
            id_setor_atual = garantir_setor(item["setor_atual"], id_unidade_atual, item["id_setor_origem"])
            # Se só havia o setor como referência, garante que a unidade gravada seja
            # a unidade à qual esse setor realmente pertence.
            setor = cursor.execute(
                "SELECT id_unidade FROM setores WHERE id_setor = ?", (id_setor_atual,)
            ).fetchone()
            if setor and setor["id_unidade"] != id_unidade_atual:
                id_unidade_atual = setor["id_unidade"]

            cursor.execute(
                """INSERT INTO perifericos_novo (
                       id_periferico, categoria, marca, num_serie, disponivel, manutencao, inativo,
                       id_unidade_origem, id_setor_origem, id_unidade_atual, id_setor_atual,
                       transferido, icone
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    item["id_periferico"], item["categoria"], item["marca"], item["num_serie"],
                    item["disponivel"], item["manutencao"], item["inativo"],
                    item["id_unidade_origem"], item["id_setor_origem"],
                    id_unidade_atual, id_setor_atual, item["transferido"], item["icone"],
                ),
            )

        antes = len(equipamentos)
        depois = cursor.execute("SELECT COUNT(*) FROM perifericos_novo").fetchone()[0]
        if antes != depois:
            raise RuntimeError(
                f"Migração da localização cancelada: {antes} equipamentos antes, {depois} depois."
            )

        cursor.execute("DROP TABLE perifericos")
        cursor.execute("ALTER TABLE perifericos_novo RENAME TO perifericos")
        if sequencia:
            cursor.execute(
                "UPDATE sqlite_sequence SET seq = ? WHERE name = 'perifericos'", (sequencia[0],)
            )
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.execute("PRAGMA foreign_keys = ON")


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
        """SELECT s.id_setor, s.nome_setor, s.id_unidade, u.nome_unidade
           FROM setores s JOIN unidades u ON u.id_unidade = s.id_unidade
           WHERE s.excluido = 0 AND u.excluido = 0
           ORDER BY s.nome_setor COLLATE NOCASE"""
    ).fetchall()
    conexao.close()
    return [dict(l) for l in linhas]


def listar_unidades_filtro():
    """Lista todas as unidades para filtros, inclusive as excluídas logicamente."""
    conexao = conectar_banco()
    linhas = conexao.execute(
        """SELECT id_unidade, nome_unidade, excluido
           FROM unidades ORDER BY nome_unidade COLLATE NOCASE"""
    ).fetchall()
    conexao.close()
    return [dict(l) for l in linhas]


def listar_setores_filtro():
    """Lista todos os setores para filtros, com a unidade e o estado de exclusão."""
    conexao = conectar_banco()
    linhas = conexao.execute(
        """SELECT s.id_setor, s.nome_setor, s.id_unidade, u.nome_unidade,
                  s.excluido, u.excluido AS unidade_excluida
           FROM setores s JOIN unidades u ON u.id_unidade = s.id_unidade
           ORDER BY u.nome_unidade COLLATE NOCASE, s.nome_setor COLLATE NOCASE"""
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
