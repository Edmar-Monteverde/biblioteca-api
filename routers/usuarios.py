from sqlalchemy.orm import Session
from schemas import (UsuarioCreate,UsuarioResponse,UsuarioLogin, TokenResponse)
from fastapi import APIRouter,Depends
from database import  get_db
from dependencies import obtener_usuario_actual

from services import usuarios as service_usuarios
from security import crear_access_token


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

@router.post('/login',response_model= TokenResponse)
def  hacer_login(usuario:UsuarioLogin,db:Session = Depends(get_db)):
    usuario_db=  service_usuarios.login_usuario(usuario,db)
    token=crear_access_token(usuario_db.id)
    return  {
        "access_token": token,
        "token_type": "bearer",}


## endpoint con dependecia Usuario_actual 

@router.get('/me',response_model=UsuarioResponse,status_code=200)
def obtener_mi_usuario(usuario_actual=Depends(obtener_usuario_actual)):
    return usuario_actual
