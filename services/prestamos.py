from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

import models
from schemas import CreatePrestamo

## logica de la aplicacion en prestamos

def crear_prestamo(prestamo: CreatePrestamo, db: Session):
    libro=(db.query(models.Libro).filter(models.Libro.id== prestamo.libro_id).first())
    ## Comprobamos si el libro existe
    if libro is None:
        raise HTTPException(
            status_code=404,
            detail="Lo siento, el libro que busca no existe"
    )
    ## si tiene suficiente stock
    if libro.stock == 0:
        raise HTTPException(
            status_code=409,
            detail="Lo siento, el libro no tiene stock disponible"
    ) ## no permitimos prestar
    
    
    prestamo_db= models.Prestamo(
        libro_id= prestamo.libro_id,
        usuario= prestamo.usuario
     ) 
    libro.stock -=1 
    if libro.stock== 0:
        libro.disponible = False
        ## Ya no esta disponible esta agotado

    try:
        db.add(prestamo_db)
        db.commit()
        db.refresh(prestamo_db)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code= 409,
            detail='Conflicto con los datos existentes'
        )

    except Exception:
        db.rollback()
        raise


    return prestamo_db



def devolver_prestamo(prestamo_id: int, db: Session):
    prestamo=(db.query(models.Prestamo).filter(models.Prestamo.id==prestamo_id).first())
    if prestamo is None:
        raise HTTPException(
            status_code=404,
            detail="Lo siento, el prestamo que busca no existe"
        )
    if prestamo.devuelto:
        raise HTTPException(
            status_code=409,
            detail="El prestamo ya ha sido devuelto "
                )

        ## aumentamos un valor al stock por el libro que devolvio 
        ## con relationship consigo acceder a libro y a sus atributos
    prestamo.libro.stock +=1

    # Volvemos a poner el libro disponible
    prestamo.libro.disponible= True
    prestamo.devuelto= True
    try:
        db.commit()
        db.refresh(prestamo)
    except Exception:
        db.rollback()
        raise
    return prestamo
