from sqlalchemy.orm import Session
from schemas import (UsuarioCreate,UsuarioResponse,UsuarioLogin)
from fastapi import APIRouter,Depends
from database import  get_db

from services import usuarios as service_usuarios


router=APIRouter(
    prefix='/usuarios',
    tags=['Usuarios'],

)


## endpoint usuarios
## Crear usuarios

@router.post('',response_model= UsuarioResponse,status_code=201)
def crear_usuario(usuario:UsuarioCreate,db:Session=Depends(get_db)):

    return service_usuarios.crear_usuario(usuario,db)


## Hacer login

@router.post('/login',response_model= UsuarioResponse)
def  hacer_login(usuario:UsuarioLogin,db:Session = Depends(get_db)):
    return service_usuarios.login_usuario(usuario,db)