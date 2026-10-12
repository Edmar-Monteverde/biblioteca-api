
import pytest
### Testes de  libros

def test_libro_no_encontrado(preparar_db,client):
    response = client.get("/libros/999") ## creamos la peticion  get  para probar si falla 

    assert response.status_code == 404 ## la respuesta debe ser 404, ya que el libro con id 999 no existe


def test_crear_libro(preparar_db,client,libro_data,admin_autenticado):
    response=client.post(
        "/libros",
        json=libro_data,headers=admin_autenticado['headers']
    )
    data=response.json()
    assert response.status_code == 201 ## la creacion es correctaa?
    assert data['titulo']== libro_data['titulo'] ## la api realmente me devuelve el titulo que espero 
    assert data['isbn']== libro_data['isbn']## la api me devuelte el isbn que espero


def test_crear_libro_isbn_duplicado(preparar_db,client,libro_data, admin_autenticado):

    response1= client.post('/libros', 
                           json=libro_data,headers=admin_autenticado['headers'])
    
    response2= client.post('/libros', 
                           json=libro_data,headers=admin_autenticado['headers'])
    
    assert response1.status_code== 201
    assert response2.status_code==409
    assert response2.json()['detail'] == 'El ISBN ya esta registrado'


   
def test_obtener_libro_existente(preparar_db,client,libro_data,admin_autenticado):
    response1=client.post('/libros', 
                           json=libro_data,headers=admin_autenticado['headers'])

    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.get(f'/libros/{libro_id}')

    data=response2.json()

    assert response1.status_code == 201
    assert response2.status_code == 200
    assert data['id'] == libro_id
    assert data["titulo"] == libro_data['titulo']

## Actualizar 

def test_actualizar_libro(preparar_db,client,libro_data, admin_autenticado):
    response1=client.post('/libros', 
                               json=libro_data,headers=admin_autenticado['headers'])
    
    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.patch(f'/libros/{libro_id}',json={
        'precio': 30,
    },headers=admin_autenticado['headers'])

    data=response2.json()

    assert response1.status_code == 201
    assert response2.status_code == 200
    assert libro_creado['precio'] == 25.50
    assert data['precio'] == 30.0

def test_actualizar_libro_no_existente(preparar_db,client,admin_autenticado):
    actualizar_libro=client.patch('/libros/999',json={
        'precio': 30,

    },headers=admin_autenticado['headers'])

    data=actualizar_libro.json()

    assert actualizar_libro.status_code == 404
    assert data['detail'] == 'El libro que busca no existe'

##DELETE

def test_eliminar_libro(preparar_db,client,libro_data,admin_autenticado):
     response1=client.post('/libros', 
                            json=libro_data,headers=admin_autenticado['headers'])
        
     libro_creado=response1.json()
     libro_id= libro_creado['id']

     response2=client.delete(f'/libros/{libro_id}',headers=admin_autenticado['headers'])

     response3 = client.get(f"/libros/{libro_id}") 



     assert response1.status_code == 201
     assert response2.status_code == 200
     assert response3.status_code == 404 


def test_eliminar_libro_no_existente(preparar_db,client,admin_autenticado):
    eliminar_libro=client.delete('/libros/999',headers=admin_autenticado['headers'])

    data=eliminar_libro.json()

    assert eliminar_libro.status_code == 404
    assert data['detail'] == 'El libro que busca no existe'


@pytest.mark.parametrize(
    "campo, valor",
    [
        ("precio", -10),
        ("titulo", "A"),
        ('stock',-3),
        ('autor','B'),
        ('categoria','C')
    ],
)
def test_crear_libro_datos_invalidos(
    preparar_db, client,admin_autenticado, libro_data, campo, valor
):
    libro_data_2=libro_data.copy()
    libro_data_2[campo] = valor

    response1= client.post('/libros',json=libro_data_2,headers=admin_autenticado['headers'])

    data=response1.json()
    

    assert response1.status_code == 422
    assert data['detail'][0]['loc'] == ["body", campo] ##   lista de errores, el primero,en la ubicacion loc
