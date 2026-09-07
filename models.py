from database import Base
from sqlalchemy import Column,Integer,String,Float,Boolean,ForeignKey
from sqlalchemy.orm import relationship



## Modelos de Sql
class Libro(Base):
    __tablename__='libros'
    id= Column(Integer, primary_key=True, autoincrement= True)
    titulo=Column(String(100),nullable=False)
    autor=Column(String(100),nullable=False)
    precio=Column(Float,nullable=False)
    stock=Column(Integer,nullable=False)
    categoria=Column(String(100),nullable=False)
    disponible=Column(Boolean,default=True)
    isbn=Column(String(20),nullable=False,unique=True)

    prestamos= relationship('Prestamo', back_populates='libro')

## realaizamos un conexion de tablas con foreingnkey

class Prestamo(Base):
    __tablename__='prestamos'
    id= Column(Integer, primary_key=True, autoincrement= True)
    libro_id= Column(Integer,ForeignKey('libros.id'),nullable=False)
    usuario= Column(String(100),nullable=False )
    devuelto = Column(Boolean, default=False, nullable=False)

    libro= relationship('Libro', back_populates='prestamos')

    ## relationship nos permite navegar esa relacion desde python /orm
    #back_population nos indica el otro lado de esta relacion 