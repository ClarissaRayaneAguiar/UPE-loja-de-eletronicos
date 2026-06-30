from fastapi import APIRouter, HTTPException, Depends

from database import conectar
from schemas import (
    CategoriaBase,
    CategoriaResponse
)

from auth import validar_token

router = APIRouter()


@router.get(
    "/categorias",
    response_model=list[CategoriaResponse]
)
def listar_categorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias ORDER BY id")
    categorias = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return categorias


@router.get(
    "/categorias/{id}",
    response_model=CategoriaResponse
)
def buscar_categoria(id: int):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
    categoria = cursor.fetchone()
    conn.close()

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria nao encontrada"
        )

    return dict(categoria)


@router.post(
    "/categorias",
    response_model=CategoriaResponse
)
def criar_categoria(categoria: CategoriaBase, usuario: dict = Depends(validar_token)):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (categoria.nome,))
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.execute("SELECT * FROM categorias WHERE id = ?", (novo_id,))
    nova_categoria = dict(cursor.fetchone())
    conn.close()
    return nova_categoria


@router.put(
    "/categorias/{id}",
    response_model=CategoriaResponse
)
def editar_categoria(
    id: int,
    dados: CategoriaBase,
    usuario: dict = Depends(validar_token)
):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
    categoria = cursor.fetchone()

    if categoria is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Categoria nao encontrada"
        )

    cursor.execute("UPDATE categorias SET nome = ? WHERE id = ?", (dados.nome, id))
    conn.commit()
    cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
    categoria_atualizada = dict(cursor.fetchone())
    conn.close()
    return categoria_atualizada


@router.delete("/categorias/{id}")
def deletar_categoria(id: int, usuario: dict = Depends(validar_token)):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
    categoria = cursor.fetchone()

    if categoria is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Categoria nao encontrada"
        )

    cursor.execute("SELECT nome FROM produtos WHERE categoria_id = ?", (id,))
    produtos_vinculados = [row["nome"] for row in cursor.fetchall()]

    if produtos_vinculados:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail=f"Nao e possivel excluir: {len(produtos_vinculados)} produto(s) vinculado(s) — {', '.join(produtos_vinculados)}"
        )

    cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {
        "mensagem": "Categoria deletada"
    }