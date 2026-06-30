from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.produtos import router as produtos_router
from routes.categorias import router as categorias_router
from routes.usuarios import router as usuarios_router
from auth import autenticar_usuario, criar_token
from database import criar_tabelas

app = FastAPI()

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