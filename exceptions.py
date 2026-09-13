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