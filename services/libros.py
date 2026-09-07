from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

import models
from schemas import CreateLibro,LibroUpdate


def crear_libro(libro: CreateLibro, db: Session):
    libro_db=models.Libro(
        titulo= libro.titulo,
        autor= libro.autor,
        precio= libro.precio,
        stock=libro.stock,
        categoria=libro.categoria,
        disponible=libro.disponible
    )
    try:
        db.add(libro_db)
        db.commit()
        db.refresh(libro_db)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code= 409,
            detail='Conflicto con los datos existentes'
        )
    except Exception:
        db.rollback()
        raise
    


    return libro_db

def obtener_libro(libro_id: int,db: Session):
    libro=db.query(models.Libro).filter(models.Libro.id==libro_id).first()

    if libro is None:
        raise HTTPException(
        status_code=404,
        detail='Lo siento, el libro que buscas no existe'

        )

    return libro

def obtener_libros(db: Session):
    libros=db.query(models.Libro).all()

    return libros 


def actualizar_libro(libro_id: int, libro: LibroUpdate,db: Session):
    libro_actualizar=db.query(models.Libro).filter(models.Libro.id==libro_id).first()

    if libro_actualizar is None:
        raise HTTPException(
            status_code=404,
            detail='Lo siento, el libro que buscas no existe'

        )
    datos_actualizar=libro.model_dump(exclude_unset=True)

    ## Recorremos clave ,valor

    for campo,valor in datos_actualizar.items():
        setattr(libro_actualizar,campo,valor) ## indicamos el libro, el campo y el nuevo valor 
        # es decir libro_actualizar.precio=20 ejemplo

    try:
        db.commit()
        db.refresh(libro_actualizar)
    except Exception:
        db.rollback()
        raise

    return libro_actualizar



def eliminar_libro(libro_id: int, db: Session):
    libro=db.query(models.Libro).filter(models.Libro.id==libro_id).first()
    if libro is None:
        raise HTTPException(
            status_code= 404,
            detail='Lo siento, el libro que busca no existe'

        )
    try:

        db.delete(libro)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code= 409,
            detail='No se puede eliminar el libro porque tiene datos relacionados')

    except Exception:
        db.rollback()
        raise
    return {'mensaje': f'El libro con  id {libro_id} fue eliminado  correctamente '}