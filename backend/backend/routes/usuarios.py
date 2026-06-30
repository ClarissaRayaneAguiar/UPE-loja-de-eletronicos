from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
import bcrypt

from database import conectar
from email_service import enviar_email_boas_vindas

router = APIRouter()


@router.post("/usuarios")
def criar_usuario(body: dict, background_tasks: BackgroundTasks):
    nome = body.get("nome")
    email = body.get("email")
    senha = body.get("senha")

    if not nome or not email or not senha:
        return JSONResponse(
            status_code=422,
            content={"erro": "Nome, email e senha sao obrigatorios"}
        )

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone() is not None:
        conn.close()
        return JSONResponse(
            status_code=409,
            content={"erro": "Este email ja esta em uso"}
        )

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)", (nome, email, senha_hash))
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.execute("SELECT id, nome, email FROM usuarios WHERE id = ?", (novo_id,))
    novo_usuario = dict(cursor.fetchone())
    conn.close()

    background_tasks.add_task(enviar_email_boas_vindas, email, nome)

    return novo_usuario