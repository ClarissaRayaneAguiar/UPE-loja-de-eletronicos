from pydantic import BaseModel, Field

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1)
    categoria_id: int
    preco: float = Field(..., gt=0)
    descricao: str = Field(..., min_length=10)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=1)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int