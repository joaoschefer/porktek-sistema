import sqlite3


def conectar():
    return sqlite3.connect("sistema_suinos.db")


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
            data_chegada TEXT NOT NULL,
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
            quantidade INTEGER NOT NULL,
            causa TEXT,
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lote_id) REFERENCES lotes(id)
        )
    """)

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