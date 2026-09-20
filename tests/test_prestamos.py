
## tests de prestamos
import pytest



def test_crear_prestamo(preparar_db,client):
    response1= client.post('/libros', json={ ## creamos el libro
        "titulo": "Clean Code",
                "autor": "Robert C. Martin",
                "precio": 25.50,
                "stock": 3,
                "categoria": "Programacion",
                "disponible": True,
                "isbn": "9780132350884",
    })
    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.post('/prestamos',json={ ## creamos el prestamos
        'libro_id': libro_id,
        'usuario':'Alejandra'
    })

    prestamo=response2.json()


    response3= client.get(f'/libros/{libro_id}') ## consultamos el libro para confirmar que el sotck bajo
    libro=response3.json()

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert prestamo["libro_id"] == libro_id
    assert prestamo['usuario'] == 'Alejandra'
    assert prestamo['devuelto'] is False 
    assert response3.status_code == 200
    assert libro['stock'] == 2

def test_crear_prestamo_libro_no_existente(preparar_db,client):
    
    response2=client.post('/prestamos',json={ ## creamos el prestamos
            'libro_id': 99,
            'usuario':'Alejandra'
        })

    prestamo = response2.json()
    assert response2.status_code == 404
    assert prestamo['detail'] == 'El libro que busca no existe'


def test_libro_sin_stock(preparar_db,client):
    response1= client.post('/libros', json={ ## creamos el libro
            "titulo": "Clean Code",
                    "autor": "Robert C. Martin",
                    "precio": 25.50,
                    "stock": 0,
                    "categoria": "Programacion",
                    "disponible": False,
                    "isbn": "9780132350884",
        })

    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.post('/prestamos',json={ ## creamos el prestamos
            'libro_id': libro_id,
            'usuario':'Alejandra' })
    prestamo =response2.json()

    assert response1.status_code == 201 
    assert response2.status_code == 409
    assert prestamo['detail'] == 'No es posible realizar el prestamo, el libro no tiene stock disponible'


def test_devolver_prestamo(prestamo_creado,client):
    prestamo_id= prestamo_creado['id']
    libro_id = prestamo_creado['libro_id']
    


    devolucion=client.patch(f'/prestamos/{prestamo_id}/devolver') ## devolvemos el prestamo
    prestamo_devuelto=devolucion.json()

    consultar_libro=client.get(f'/libros/{libro_id}') ## consultamos el libro para confirmar que el sotck subio
    libro=consultar_libro.json()

    
    assert prestamo_creado['devuelto'] is False
    assert devolucion.status_code == 200
    assert prestamo_devuelto['devuelto'] is True
    assert consultar_libro.status_code == 200
    assert libro['stock'] == 3

def test_prestamo_ya_devuelto(prestamo_creado,client):
  
    prestamo_id=prestamo_creado['id']
    libro_id= prestamo_creado['libro_id']   
       
    primera_devolucion=client.patch(f'/prestamos/{prestamo_id}/devolver') ## devolvemos el prestamo
    

    segunda_devolucion=client.patch(f'/prestamos/{prestamo_id}/devolver') ## devolvemos el prestamo
    prestamo_devuelto2=segunda_devolucion.json()

    consulta_libro=client.get(f'/libros/{libro_id}') ## consultamos el libro para confirmar que el sotck no volvio a subio
    libro=consulta_libro.json()

    
   
    assert primera_devolucion.status_code == 200 
    assert segunda_devolucion.status_code == 409
    assert prestamo_devuelto2['detail'] == 'El prestamo ya ha sido devuelto'
    assert consulta_libro.status_code == 200
    assert libro['stock'] == 3

def test_devolver_prestamo_no_existente(preparar_db,client):
    response1=client.patch('/prestamos/999/devolver') ## devolvemos el prestamo
    error=response1.json()

    assert response1.status_code == 404
    assert error['detail'] == 'El prestamo que busca no existe'