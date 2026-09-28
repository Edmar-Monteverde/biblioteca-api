from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from security import hash_password
import models
from schemas import UsuarioCreate
from exceptions import EmailExistenteError

# logica para crear nuuevo usuario

def crear_usuario(usuario:UsuarioCreate, db:Session):
    hash_password_db= hash_password(usuario.password)

    usuario_db= models.Usuario(
        email=usuario.email,
        password_hash= hash_password_db,
        rol='usuario',
        activo= True

    )
    try:
        db.add(usuario_db)
        db.commit()
        db.refresh(usuario_db)

    except IntegrityError:
        db.rollback()
        raise  EmailExistenteError()
    except Exception:
        db.rollback()
        raise

    return usuario_db