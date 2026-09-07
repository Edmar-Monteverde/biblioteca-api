from fastapi import FastAPI,Depends,HTTPException
from database import Base, engine

from routers import libros, prestamos,autores

## Creamos la app con fastaapi
app=FastAPI()

## Conecta los modelos que heredan de Base y crea en la base de datos las tablas que todavia no existen

Base.metadata.create_all(bind=engine)

app.include_router(libros.router)
app.include_router(prestamos.router)
app.include_router(autores.router)
