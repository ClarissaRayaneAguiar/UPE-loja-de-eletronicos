from fastapi import APIRouter, HTTPException

from data import produtos

from schemas import (
    ProdutoCreate,
    ProdutoResponse
)

router = APIRouter()

@router.get("/produtos")
def listar_produtos():
    return produtos

@router.get(
    "/produtos/{id}",
    response_model=ProdutoResponse
)
def buscar_produto(id: int):

    for produto in produtos:

        if produto["id"] == id:
            return produto

    raise HTTPException(
        status_code=404,
        detail="Produto não encontrado"
    )

@router.post(
    "/produtos",
    response_model=ProdutoResponse
)
def criar_produto(produto: ProdutoCreate):

    novo_id = len(produtos) + 1

    novo_produto = {
        "id": novo_id,
        "nome": produto.nome,
        "categoria_id": produto.categoria_id,
        "preco": produto.preco,
        "descricao": produto.descricao
    }

    produtos.append(novo_produto)

    return novo_produto

@router.put(
    "/produtos/{id}",
    response_model=ProdutoResponse
)
def editar_produto(
    id: int,
    dados: ProdutoCreate
):

    for produto in produtos:

        if produto["id"] == id:

            produto["nome"] = dados.nome
            produto["categoria_id"] = dados.categoria_id
            produto["preco"] = dados.preco
            produto["descricao"] = dados.descricao

            return produto

    raise HTTPException(
        status_code=404,
        detail="Produto não encontrado"
    )

@router.delete("/produtos/{id}")
def deletar_produto(id: int):

    for produto in produtos:

        if produto["id"] == id:

            produtos.remove(produto)

            return {
                "mensagem": "Produto deletado"
            }

    raise HTTPException(
        status_code=404,
        detail="Produto não encontrado"
    )