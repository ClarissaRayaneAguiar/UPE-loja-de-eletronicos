from fastapi import FastAPI

from routes.produtos import router as produtos_router
from routes.categorias import router as categorias_router

app = FastAPI()

app.include_router(produtos_router)
app.include_router(categorias_router)

@app.get("/")
def home():
    return {
        "mensagem": "API da loja funcionando"
    }