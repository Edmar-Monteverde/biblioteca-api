##traduce excepciones de nuestra aplicación a respuestas HTTP
##  Decide CÓMO convertir ese error en una respuesta HTTP.

from fastapi.responses import JSONResponse  ##  Sirve para devolver un respuesta Json
from fastapi import Request ## para representar una peticion que esta procesandose

from exceptions import (LibroNoEncontradoError, ISBNExistenteError, LibroConPrestamosError,LibroSinStockError,
                        PrestamoYaDevueltoError,PrestamoNoEncontradoError,EmailExistenteError, CredencialesInvalidasError,
                        UsuarioInactivoError, TokenInvalidoError, TokenExpiradoError)


## handler libro
def manejar_libro_no_encontrado(request: Request,exc: LibroNoEncontradoError):
    return JSONResponse (
        status_code= 404,
        content={'detail': 'El libro que busca no existe'}

    ) ## Simplmente se construye la respuesta

def manejar_isbn_existente(request: Request, exc: ISBNExistenteError):
    return JSONResponse(
        status_code= 409,
        content={'detail': 'El ISBN ya esta registrado'}
    )

def manejar_libro_con_prestamos(request: Request, exc: LibroConPrestamosError):
    return JSONResponse(
        status_code= 409,
        content={'detail': 'No es posible eliminar este libro, tiene prestamos asociados'}
    )

def  manejar_libro_sin_stock(request: Request, exc: LibroSinStockError):
    return JSONResponse(
        status_code= 409,
        content={'detail': 'No es posible realizar el prestamo, el libro no tiene stock disponible'}
    )

def manejar_prestamo_no_encontrado(request: Request, exc: PrestamoNoEncontradoError):
    return JSONResponse(
        status_code= 404,
        content={'detail': 'El prestamo que busca no existe'}
    )

def manejar_prestamo_ya_devuelto(request: Request, exc: PrestamoYaDevueltoError):
    return JSONResponse(
        status_code= 409,
        content={'detail': 'El prestamo ya ha sido devuelto'}
    )

def manejar_email_existente(request:Request, exc: EmailExistenteError):
    return JSONResponse(
        status_code=409,
        content={'detail': 'El email ya existe'}
    )

def manejar_credenciales_invalidas(request:Request, exc: CredencialesInvalidasError):
    return JSONResponse(
        status_code = 401,
        content = {'detail': 'Credenciales Incorrectas'}

    )

def manejar_usuario_inactivo(request:Request, exc: UsuarioInactivoError):
    return JSONResponse(
        status_code= 403,
        content = {'detail': 'El usuario esta inactivo'}
    )

def manejar_token_expirado(resquest:Request, exc: TokenExpiradoError):
    return JSONResponse(
        status_code = 401,
        content = {'detail': 'Token inválido o expirado'}
    )

def manejar_token_invalido(request:Request, exc: TokenInvalidoError):
    return JSONResponse(
        status_code = 401,
        content = {'detail': 'Token inválido o expirado'}
    )