from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import hashlib
import os

from routes.produtos import router as produtos_router
from routes.categorias import router as categorias_router
from routes.usuarios import router as usuarios_router
from auth import autenticar_usuario, criar_token, SECRET_KEY
from database import criar_tabelas, DB_PATH

app = FastAPI()

# 🔁 Força recriação do banco de dados no Render (apaga o antigo)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
criar_tabelas()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produtos_router)
app.include_router(categorias_router)
app.include_router(usuarios_router)


@app.post("/login")
def login(body: dict):
    email = body.get("email")
    senha = body.get("senha")

    if not email or not senha:
        return JSONResponse(
            status_code=401,
            content={"erro": "Email e senha sao obrigatorios"}
        )

    usuario = autenticar_usuario(email, senha)

    if not usuario:
        return JSONResponse(
            status_code=401,
            content={"erro": "Credenciais invalidas"}
        )

    token = criar_token(email)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"]
        }
    }


@app.get("/")
def home():
    return {
        "mensagem": "API da loja funcionando"
    }

@app.get("/debug")
def debug_info():
    key_hash = hashlib.sha256(SECRET_KEY.encode()).hexdigest()[:10]
    return {
        "key_hash": key_hash,
        "server_time": datetime.utcnow().isoformat()
    }