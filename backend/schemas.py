from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    categoria_id: int
    preco: float
    descricao: str

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

class CategoriaBase(BaseModel):
    nome: str

class CategoriaResponse(CategoriaBase):
    id: int