from sqlalchemy.orm import Session
from schemas import (ResponsePrestamo,CreatePrestamo)
from fastapi import APIRouter,Depends
from database import  get_db
from services import prestamos as prestamos_service
from dependencies import obtener_usuario_actual, requerir_admin




router= APIRouter(
    prefix='/prestamos',## direccion  de nuestro endpoint
    tags=['Prestamos']
)


## endpoints de prestamos

### peticion de prestamos
## Services crear prestamo
@router.get('',response_model=list[ResponsePrestamo], status_code=200)
def consultar_todos_prestamos(db:Session =Depends(get_db), usuario_admin=Depends(requerir_admin)):
   return prestamos_service.consultar_prestamos(db)


## consultar mis prorios prestamos
@router.get("/mis-prestamos",response_model=list[ResponsePrestamo], status_code=200)
def consultar_mis_prestamos(db: Session = Depends(get_db), usuario_actual=Depends(obtener_usuario_actual)):
   return  prestamos_service.consultar_mis_prestamos(db,usuario_actual)


@router.post('',response_model= ResponsePrestamo, status_code= 201)
def crear_prestamo(prestamo:CreatePrestamo, db:Session=Depends(get_db),usuario_actual = Depends(obtener_usuario_actual)):
   return prestamos_service.crear_prestamo(prestamo,db,usuario_actual)


## Devolver un prestamos
@router.patch('/{prestamo_id}/devolver',response_model=ResponsePrestamo, status_code=200)
def devolver_prestamo(prestamo_id:int, db:Session=Depends(get_db), usuario_actual= Depends(obtener_usuario_actual)):
   return prestamos_service.devolver_prestamo(prestamo_id,db,usuario_actual)
