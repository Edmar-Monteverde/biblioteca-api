## Define QUÉ errores propios existen en la aplicación.

class LibroNoEncontradoError(Exception):
    pass

class ISBNExistenteError(Exception):
    pass

class LibroConPrestamosError(Exception):
    pass