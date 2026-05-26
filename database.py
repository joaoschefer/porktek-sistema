import sqlite3


def conectar():
    return sqlite3.connect("sistema_suinos.db")


def migrar_tabela_mortes(cursor):
    cursor.execute("PRAGMA table_info(mortes)")
    colunas = cursor.fetchall()
    nomes_colunas = [coluna[1] for coluna in colunas]

    if not nomes_colunas or "quantidade" not in nomes_colunas:
        return

    expressao_mossa = "0"
    if "mossa" in nomes_colunas:
        expressao_mossa = "CAST(COALESCE(NULLIF(mossa, ''), 0) AS INTEGER)"

    cursor.execute("ALTER TABLE mortes RENAME TO mortes_antiga")
    cursor.execute("""
        CREATE TABLE mortes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lote_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            mossa INTEGER NOT NULL,
            causa TEXT,
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lote_id) REFERENCES lotes(id)
        )
    """)
    cursor.execute(f"""
        INSERT INTO mortes (id, lote_id, data, mossa, causa, observacao, criado_em)
        SELECT id, lote_id, data, {expressao_mossa}, causa, observacao, criado_em
        FROM mortes_antiga
    """)
    cursor.execute("DROP TABLE mortes_antiga")


def migrar_tabela_lotes(cursor):
    cursor.execute("PRAGMA table_info(lotes)")
    colunas = cursor.fetchall()
    nomes_colunas = [coluna[1] for coluna in colunas]

    if not nomes_colunas:
        return

    data_chegada_obrigatoria = any(
        coluna[1] == "data_chegada" and coluna[3] == 1
        for coluna in colunas
    )

    if not data_chegada_obrigatoria:
        return

    cursor.execute("ALTER TABLE lotes RENAME TO lotes_antiga")
    cursor.execute("""
        CREATE TABLE lotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            data_chegada TEXT,
            data_finalizacao TEXT,
            quantidade_inicial INTEGER NOT NULL,
            quantidade_atual INTEGER NOT NULL,
            peso_medio_inicial REAL,
            peso_medio_atual REAL,
            mortalidade_total INTEGER DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'ativo',
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        INSERT INTO lotes (
            id,
            codigo,
            data_chegada,
            data_finalizacao,
            quantidade_inicial,
            quantidade_atual,
            peso_medio_inicial,
            peso_medio_atual,
            mortalidade_total,
            status,
            observacao,
            criado_em
        )
        SELECT
            id,
            codigo,
            data_chegada,
            data_finalizacao,
            quantidade_inicial,
            quantidade_atual,
            peso_medio_inicial,
            peso_medio_atual,
            mortalidade_total,
            status,
            observacao,
            criado_em
        FROM lotes_antiga
    """)
    cursor.execute("DROP TABLE lotes_antiga")


def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            data_chegada TEXT,
            data_finalizacao TEXT,
            quantidade_inicial INTEGER NOT NULL,
            quantidade_atual INTEGER NOT NULL,
            peso_medio_inicial REAL,
            peso_medio_atual REAL,
            mortalidade_total INTEGER DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'ativo',
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    migrar_tabela_lotes(cursor)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chegadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lote_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            peso_medio REAL,
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lote_id) REFERENCES lotes(id)       
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mortes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lote_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            mossa INTEGER NOT NULL,
            causa TEXT,
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lote_id) REFERENCES lotes(id)
        )
    """)

    migrar_tabela_mortes(cursor)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS racoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lote_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            quantidade_kg REAL NOT NULL,
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lote_id) REFERENCES lotes(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lote_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            peso_medio REAL,
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lote_id) REFERENCES lotes(id)
        )
    """)

    conexao.commit()
    conexao.close()
