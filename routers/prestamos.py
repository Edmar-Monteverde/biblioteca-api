from sqlalchemy.orm import Session
from schemas import (ResponsePrestamo,CreatePrestamo)
from fastapi import APIRouter,Depends
from database import  get_db
from services import prestamos as prestamos_service



router= APIRouter(
    prefix='/prestamos',
    tags=['Prestamos']
)


## endpoints de prestamos

### peticion de prestamos
## Services crear prestamo

@router.post('',response_model= ResponsePrestamo, status_code= 201)
def crear_prestamo(prestamo:CreatePrestamo, db:Session=Depends(get_db)):
   return prestamos_service.crear_prestamo(prestamo,db)


## Devolver un prestamos
@router.patch('/{prestamo_id}/devolver',response_model=ResponsePrestamo, status_code=200)
def devolver_prestamo(prestamo_id:int, db:Session=Depends(get_db)):
   return prestamos_service.devolver_prestamo(prestamo_id,db)