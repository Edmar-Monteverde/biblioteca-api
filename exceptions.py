## Define QUÉ errores propios existen en la aplicación.

class LibroNoEncontradoError(Exception):
    pass

class ISBNExistenteError(Exception):
    pass

class LibroConPrestamosError(Exception):
    pass

class LibroSinStockError(Exception):
    pass

class PrestamoNoEncontradoError(Exception):
    pass

class PrestamoYaDevueltoError(Exception):
    pass

class EmailExistenteError(Exception):
    pass

class CredencialesInvalidasError(Exception):
    pass

class UsuarioInactivoError(Exception):
    pass

class TokenExpiradoError(Exception):
    pass

class TokenInvalidoError(Exception):
    pass
