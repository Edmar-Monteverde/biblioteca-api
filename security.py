## m Controlar hash  y verify_password

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


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

