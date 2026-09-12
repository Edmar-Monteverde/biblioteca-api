from fastapi import FastAPI

from routers import libros, prestamos,autores
from exceptions import (LibroNoEncontradoError, ISBNExistenteError, LibroConPrestamosError)
from handlers import (manejar_libro_no_encontrado, manejar_isbn_existente, manejar_libro_con_prestamos)

## Creamos la app con fastaapi
app=FastAPI()

app.add_exception_handler(
    LibroNoEncontradoError,
    manejar_libro_no_encontrado
)##  FastAPI, cuando aparezca LibroNoEncontradoError, utiliza manejar_libro_no_encontrado.
 ## registamos el handle a nuestra aplicacion 


app.add_exception_handler(ISBNExistenteError, manejar_isbn_existente)

app.add_exception_handler(LibroConPrestamosError, manejar_libro_con_prestamos)
## Conecta los modelos que heredan de Base y crea en la base de datos las tablas que todavia no existen



app.include_router(libros.router)
app.include_router(prestamos.router)
app.include_router(autores.router)
