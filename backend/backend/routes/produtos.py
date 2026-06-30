from fastapi import APIRouter, HTTPException, Query, Depends

from database import conectar

from schemas import (
    ProdutoCreate,
    ProdutoResponse
)

from auth import validar_token

router = APIRouter()


@router.get("/produtos")
def listar_produtos(
    nome: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT p.*, c.id as cat_id, c.nome as cat_nome
        FROM produtos p
        JOIN categorias c ON p.categoria_id = c.id
    """
    params = []

    if nome:
        query += " WHERE LOWER(p.nome) LIKE ?"
        params.append(f"%{nome.lower()}%")

    query += " ORDER BY p.id"

    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]

    if nome:
        cursor.execute("SELECT COUNT(*) FROM produtos WHERE LOWER(nome) LIKE ?", (f"%{nome.lower()}%",))
        total = cursor.fetchone()[0]

    pages = max((total + limit - 1) // limit, 1)

    inicio = (page - 1) * limit

    if nome:
        cursor.execute("""
            SELECT p.*, c.id as cat_id, c.nome as cat_nome
            FROM produtos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE LOWER(p.nome) LIKE ?
            ORDER BY p.id
            LIMIT ? OFFSET ?
        """, (f"%{nome.lower()}%", limit, inicio))
    else:
        cursor.execute("""
            SELECT p.*, c.id as cat_id, c.nome as cat_nome
            FROM produtos p
            JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.id
            LIMIT ? OFFSET ?
        """, (limit, inicio))

    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        produto = dict(row)
        produto["categoria"] = {
            "id": produto.pop("cat_id"),
            "nome": produto.pop("cat_nome")
        }
        data.append(produto)

    return {
        "data": data,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }


@router.get(
    "/produtos/{id}",
    response_model=ProdutoResponse
)
def buscar_produto(id: int):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()
    conn.close()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto nao encontrado"
        )

    return dict(produto)


@router.post(
    "/produtos",
    response_model=ProdutoResponse
)
def criar_produto(produto: ProdutoCreate, usuario: dict = Depends(validar_token)):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categorias WHERE id = ?", (produto.categoria_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Categoria nao encontrada"
        )

    cursor.execute(
        "INSERT INTO produtos (nome, categoria_id, preco, descricao) VALUES (?, ?, ?, ?)",
        (produto.nome, produto.categoria_id, produto.preco, produto.descricao)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (novo_id,))
    novo_produto = dict(cursor.fetchone())
    conn.close()
    return novo_produto


@router.put(
    "/produtos/{id}",
    response_model=ProdutoResponse
)
def editar_produto(
    id: int,
    dados: ProdutoCreate,
    usuario: dict = Depends(validar_token)
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categorias WHERE id = ?", (dados.categoria_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Categoria nao encontrada"
        )

    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Produto nao encontrado"
        )

    cursor.execute(
        "UPDATE produtos SET nome = ?, categoria_id = ?, preco = ?, descricao = ? WHERE id = ?",
        (dados.nome, dados.categoria_id, dados.preco, dados.descricao, id)
    )
    conn.commit()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    produto_atualizado = dict(cursor.fetchone())
    conn.close()
    return produto_atualizado


@router.delete("/produtos/{id}")
def deletar_produto(id: int, usuario: dict = Depends(validar_token)):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Produto nao encontrado"
        )

    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {
        "mensagem": "Produto deletado"
    }