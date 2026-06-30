import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "loja.db")

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria_id INTEGER NOT NULL,
            preco REAL NOT NULL,
            descricao TEXT NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO categorias (nome) VALUES ('Processador')")
        cursor.execute("INSERT INTO categorias (nome) VALUES ('Placa de Video')")
        cursor.execute("INSERT INTO categorias (nome) VALUES ('Armazenamento')")

    cursor.execute("SELECT COUNT(*) FROM produtos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO produtos (nome, categoria_id, preco, descricao) VALUES ('Ryzen 7 7800X3D', 1, 2999.90, 'Processador AMD 8 nucleos')")
        cursor.execute("INSERT INTO produtos (nome, categoria_id, preco, descricao) VALUES ('RTX 4070', 2, 4200.00, 'Placa de video NVIDIA 12GB')")

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        hash_admin = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES ('Administrador', 'admin@upe.com', ?)", (hash_admin,))

    conn.commit()
    conn.close()