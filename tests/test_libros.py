
### Testes de  libros

def test_libro_no_encontrado(preparar_db,client):
    response = client.get("/libros/999") ## creamos la peticion  get  para probar si falla 

    assert response.status_code == 404 ## la respuesta debe ser 404, ya que el libro con id 999 no existe


def test_crear_libro(preparar_db,client,libro_data):
    response=client.post(
        "/libros",
        json=libro_data
    )
    data=response.json()
    assert response.status_code == 201 ## la creacion es correctaa?
    assert data['titulo']== libro_data['titulo'] ## la api realmente me devuelve el titulo que espero 
    assert data['isbn']== libro_data['isbn']## la api me devuelte el isbn que espero


def test_crear_libro_isbn_duplicado(preparar_db,client,libro_data):

    response1= client.post('/libros', 
                           json=libro_data)
    
    response2= client.post('/libros', 
                           json=libro_data)
    
    assert response1.status_code== 201
    assert response2.status_code==409
    assert response2.json()['detail'] == 'El ISBN ya esta registrado'


def test_obtener_libro_existente(preparar_db,client,libro_data):
    response1=client.post('/libros', 
                           json=libro_data)

    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.get(f'/libros/{libro_id}')

    data=response2.json()

    assert response1.status_code == 201
    assert response2.status_code == 200
    assert data['id'] == libro_id
    assert data["titulo"] == libro_data['titulo']


def test_actualizar_libro(preparar_db,client,libro_data):
    response1=client.post('/libros', 
                               json=libro_data)
    
    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.patch(f'/libros/{libro_id}',json={
        'precio': 30,

    },)

    data=response2.json()

    assert response1.status_code == 201
    assert response2.status_code == 200
    assert libro_creado['precio'] == 25.50
    assert data['precio'] == 30.0


def test_eliminar_libro(preparar_db,client,libro_data):
     response1=client.post('/libros', 
                            json=libro_data)
        
     libro_creado=response1.json()
     libro_id= libro_creado['id']

     response2=client.delete(f'/libros/{libro_id}')

     response3 = client.get(f"/libros/{libro_id}") 



     assert response1.status_code == 201
     assert response2.status_code == 200
     assert response3.status_code == 404 