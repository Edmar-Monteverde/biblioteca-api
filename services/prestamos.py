from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


import models
from schemas import CreatePrestamo
from exceptions import  (LibroNoEncontradoError,LibroSinStockError,PrestamoNoEncontradoError,PrestamoYaDevueltoError)

## logica de la aplicacion en prestamos

def crear_prestamo(prestamo: CreatePrestamo, db: Session):
    libro=(db.query(models.Libro).filter(models.Libro.id== prestamo.libro_id).first())
    ## Comprobamos si el libro existe
    if libro is None:
        raise LibroNoEncontradoError()
    ## si tiene suficiente stock
    if libro.stock == 0:
        raise LibroSinStockError() ## no permitimos prestar
    
    
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
        raise 

    except Exception:
        db.rollback()
        raise


    return prestamo_db



def devolver_prestamo(prestamo_id: int, db: Session):
    prestamo=(db.query(models.Prestamo).filter(models.Prestamo.id==prestamo_id).first())
    if prestamo is None:
        raise PrestamoNoEncontradoError()
    
    if prestamo.devuelto:
        raise PrestamoYaDevueltoError()

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
