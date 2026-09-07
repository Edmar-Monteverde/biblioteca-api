from sqlalchemy.orm import Session
from schemas import (CreateLibro,ResponseLibro,LibroUpdate)
from fastapi import APIRouter,Depends
from database import  get_db


from services import libros as services_libros

router= APIRouter(
    prefix='/libros',
    tags=['Libros']
)


## endpoint de libro

@router.post('',response_model=ResponseLibro, status_code=201)
def crear_libro(libro:CreateLibro, db:Session=Depends(get_db)):
  return services_libros.crear_libro(libro, db)

## Buscar un libro

@router.get('/{libro_id}',response_model=ResponseLibro,status_code=200)
def obtener_libro(libro_id:int,db:Session=Depends(get_db)):
   return services_libros.obtener_libro(libro_id, db)

## consulta todos los libros

@router.get('',response_model=list[ResponseLibro],status_code=200)
def obtener_libros(db:Session=Depends(get_db)):
    return services_libros.obtener_libros(db)

## Actualizar un libro
@router.patch('/{libro_id}',response_model=ResponseLibro,status_code=200)
def actualizar_libro(libro_id:int, libro:LibroUpdate,db:Session=Depends(get_db)):
    return services_libros.actualizar_libro(libro_id,libro,db)


## Eliminar un libro

@router.delete('/{libro_id}',status_code=200)
def eliminar_libro(libro_id:int, db:Session=Depends(get_db)):
  return services_libros.eliminar_libro(libro_id,db)