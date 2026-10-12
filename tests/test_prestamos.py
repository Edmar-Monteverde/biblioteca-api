
## tests de prestamos
import pytest



def test_crear_prestamo(preparar_db,client,libro_data, admin_autenticado, usuario_autenticado):
    response1= client.post('/libros', json=libro_data, headers= admin_autenticado['headers'])
    assert response1.status_code == 201
    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.post('/prestamos',json={ ## creamos el prestamos
        'libro_id': libro_id,
    },headers=usuario_autenticado['headers']) ##  introducimos solo el headers no el id

    assert response2.status_code == 201

    prestamo=response2.json()


    response3= client.get(f'/libros/{libro_id}') ## consultamos el libro para confirmar que el sotck bajo
    assert response3.status_code == 200
    libro=response3.json()


    assert prestamo["libro_id"] == libro_id
    assert prestamo['usuario_id'] == usuario_autenticado['id']
    assert prestamo['devuelto'] is False
    assert libro['stock'] == 2


def test_consultar_mis_prestamos(prestamo_creado,client,usuario_autenticado):
    response=client.get('/prestamos/mis-prestamos',headers=usuario_autenticado['headers'])
    data=response.json()

    assert response.status_code == 200
    assert prestamo_creado['id'] == data[0]['id'] ## confirmamos que el id del prestamo creado y devuelto sea igual
    assert data[0]['usuario_id'] == usuario_autenticado['id']## confirmamos que el usuario_id  sea igual al autenticado



def test_crear_prestamo_libro_no_existente(preparar_db,client,usuario_autenticado):

    response2=client.post('/prestamos',json={ ## creamos el prestamos
            'libro_id': 99,

        },headers=usuario_autenticado['headers'])

    prestamo = response2.json()
    assert response2.status_code == 404
    assert prestamo['detail'] == 'El libro que busca no existe'


def test_libro_sin_stock(preparar_db,client,libro_data,admin_autenticado,usuario_autenticado):
    response1= client.post('/libros', json={ ## creamos el libro
            "titulo": "Clean Code",
                    "autor": "Robert C. Martin",
                    "precio": 25.50,
                    "stock": 0,
                    "categoria": "Programacion",
                    "disponible": True,
                    "isbn": "9780132350884",
        },headers= admin_autenticado['headers'])

    assert response1.status_code == 201
    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.post('/prestamos',json={ ## creamos el prestamos
            'libro_id': libro_id },headers=usuario_autenticado['headers'])
    prestamo =response2.json()


    assert response2.status_code == 409
    assert prestamo['detail'] == 'No es posible realizar el prestamo, el libro no tiene stock disponible'


def test_devolver_prestamo(prestamo_creado,client,usuario_autenticado):
    prestamo_id= prestamo_creado['id']
    libro_id = prestamo_creado['libro_id']



    devolucion=client.patch(f'/prestamos/{prestamo_id}/devolver',headers=usuario_autenticado['headers']) ## devolvemos el prestamo
    assert devolucion.status_code == 200
    prestamo_devuelto=devolucion.json()

    consultar_libro=client.get(f'/libros/{libro_id}') ## consultamos el libro para confirmar que el sotck subio
    assert consultar_libro.status_code == 200
    libro=consultar_libro.json()


    assert prestamo_creado['devuelto'] is False
    assert prestamo_devuelto['devuelto'] is True
    assert libro['stock'] == 3
    assert prestamo_creado['usuario_id'] == usuario_autenticado['id']

def test_prestamo_ya_devuelto(prestamo_creado,client,usuario_autenticado):

    prestamo_id=prestamo_creado['id']
    libro_id= prestamo_creado['libro_id']

    primera_devolucion=client.patch(f'/prestamos/{prestamo_id}/devolver',headers=usuario_autenticado['headers']) ## devolvemos el prestamo


    segunda_devolucion=client.patch(f'/prestamos/{prestamo_id}/devolver',headers=usuario_autenticado['headers']) ## devolvemos el prestamo
    prestamo_devuelto2=segunda_devolucion.json()

    consulta_libro=client.get(f'/libros/{libro_id}') ## consultamos el libro para confirmar que el sotck no volvio a subio
    libro=consulta_libro.json()



    assert primera_devolucion.status_code == 200
    assert segunda_devolucion.status_code == 409
    assert prestamo_devuelto2['detail'] == 'El prestamo ya ha sido devuelto'
    assert consulta_libro.status_code == 200
    assert libro['stock'] == 3

def test_devolver_prestamo_no_existente(preparar_db,client,usuario_autenticado):
    response1=client.patch('/prestamos/999/devolver',headers=usuario_autenticado['headers']) ## devolvemos el prestamo
    error=response1.json()

    assert response1.status_code == 404
    assert error['detail'] == 'El prestamo que busca no existe'



def test_solo_propietario_devuelve_prestamo(prestamo_creado,client,admin_autenticado):
    prestamo_id=prestamo_creado['id']

    response1=client.patch(f'/prestamos/{prestamo_id}/devolver',headers=admin_autenticado['headers'])
    data=response1.json()

    assert response1.status_code == 403
    assert data['detail'] == 'Usuario no Autorizado'
    assert prestamo_creado['usuario_id'] != admin_autenticado['id']


def test_consultar_mis_prestamos_filtrar_por_usuario(prestamo_creado,client,admin_autenticado):
    libro_id=prestamo_creado['libro_id']

    response1=client.post('/prestamos',json={'libro_id': libro_id},headers =admin_autenticado['headers'] )
    assert response1.status_code ==201
    data =response1.json()

    response2=client.get('/prestamos/mis-prestamos',headers=admin_autenticado['headers'])

    assert response2.status_code== 200
    data2=response2.json()

    assert all(prestamo['usuario_id']==admin_autenticado['id'] for prestamo in data2 ) ## todos los prestamos deben pertenecer admin

    assert any(prestamo['id'] == data['id'] for prestamo in data2) # existe un prestamo cuyo id  coincida con el prestamo creado
                                                                    # por el admin

    assert not any(prestamo['id'] == prestamo_creado['id'] for prestamo in data2) ## en la consulta del admin no existe prestamo
                                                                                 # cuyo id coincida con el prestamos creado
                                                                                 # por el usuario


def test_admin_puede_consultar_todos_prestamos(client,prestamo_creado,admin_autenticado,):
    consulta_admin=client.get('/prestamos',headers=admin_autenticado['headers'])
    data=consulta_admin.json()


    assert consulta_admin.status_code ==200
    assert any(prestamo['id']== prestamo_creado['id'] for prestamo in data)


def test_usuario_no_puede_consultar_todos_prestamos(client, usuario_autenticado,):
    response = client.get("/prestamos",headers= usuario_autenticado['headers'],)
    data=response.json()

    assert response.status_code == 403
    assert data['detail'] == 'Usuario no Autorizado'



def test_consultar_mis_prestamos_vacio(client,usuario_autenticado):
    response= client.get('/prestamos/mis-prestamos',headers= usuario_autenticado['headers'])

    data=response.json()

    assert response.status_code == 200
    assert data == []
