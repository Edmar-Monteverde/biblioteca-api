from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from security import decodificar_access_token
from exceptions import TokenInvalidoError,UsuarioInactivoError
from database import  get_db
from sqlalchemy.orm import Session
import models


security = HTTPBearer()
def obtener_usuario_actual(credenciales:HTTPAuthorizationCredentials = Depends(security), db:Session = Depends(get_db)) :
    token = credenciales.credentials ## obtenemos  el token 

    payload=decodificar_access_token(token) ## decodificamos
    sub= payload.get('sub')

    if sub is None:
        raise TokenInvalidoError()
    try:
        usuario_id= int(sub)

    except ValueError:
        raise  TokenInvalidoError()

    usuario_db= db.query(models.Usuario).filter(models.Usuario.id== usuario_id).first()
            
    if usuario_db is None: 
         raise TokenInvalidoError()
    
    if not usuario_db.activo:
         raise UsuarioInactivoError()

    return usuario_db

## obtenemos  un usuario perfectamente autenticado


    