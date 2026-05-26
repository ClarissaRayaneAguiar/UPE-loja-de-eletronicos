from fastapi import APIRouter
from data import categorias

router = APIRouter()

@router.get("/categorias")
def listar_categorias():
    return categorias