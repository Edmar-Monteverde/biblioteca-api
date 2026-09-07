from pydantic import BaseModel,Field


## Modelos de pydantic
class CreateLibro(BaseModel):
    titulo: str=Field(min_length=2)
    autor: str=Field(min_length=2)
    precio: float=Field(gt=0)
    stock: int=Field(ge=0)
    categoria: str=Field(min_length=2)
    disponible: bool=Field(default= True)


class ResponseLibro(BaseModel):
    id:int
    titulo:str
    autor: str
    precio:float
    stock: int
    categoria: str
    disponible: bool

class LibroUpdate(BaseModel):
    titulo: str |None =Field(default=None, min_length=2)
    autor: str|None =Field(default=None, min_length=2)
    precio: float|None=Field(default=None,gt=0)
    stock: int|None=Field(default=None,ge=0)
    categoria: str|None=Field(default=None,min_length=2)
    disponible: bool|None=None

##modelos pydantic para prestamos
class CreatePrestamo(BaseModel):
    libro_id: int=Field(gt=0)
    usuario: str=Field(min_length=2)
   


class ResponsePrestamo(BaseModel):
    id:int
    libro_id: int
    usuario:str
    devuelto:bool
