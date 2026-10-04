## m Controlar hash  y verify_password

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from datetime import datetime,timedelta, timezone ### obtener fecha/hora, sumar 30min, trabajar en UTC
from config import settings
from exceptions import TokenExpiradoError, TokenInvalidoError


password_hasher= PasswordHasher() # Creamos una instancia
 ## creamos el hash del password
def hash_password(password:str) -> str:

    password_hash = password_hasher.hash(password)## recibimos un str y devolvemos un hash


    return password_hash

## funcion para verificar que el hash le pertenece a la password

def verify_password(password: str, password_hash: str) -> bool:
    ## verificamos primero el hash guardado en BD y luego la password
    try:
        verify=   password_hasher.verify(password_hash, password)

        return verify
    except VerifyMismatchError:
        return False



def crear_access_token(usuario_id:int)->str: ## crear JWt
    expiracion= datetime.now(timezone.utc) +timedelta(minutes=settings.MINUTES) 
              #  hora actual zona utc + los minutos de expiracion

    payload = {
        'sub' : str(usuario_id),
        'exp' : expiracion
    }

    token= jwt.encode(payload,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    ## al codidficar enviamos un algorithm especifico para crear la firma 
    return token


def decodificar_access_token(token:str):

    try:
        payload= jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        ## al decodificar enviamos una lista de alñgoritmos permitidos para verificar y 
        ## decodificar la firma del token
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiradoError()

    except jwt.InvalidTokenError:
        raise TokenInvalidoError()