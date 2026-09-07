
from fastapi import APIRouter

router=APIRouter(
    prefix='/autores',
    tags=['Autores']
)


## Endpoits autores

@router.get('',status_code=200)
def mostrar_autores():
    return {'mensaje': 'Lista de autores'}

@router.get('/{autor_id}',status_code=200)
def mostrar_autor(autor_id:int):
    return {'autor_id': autor_id}
