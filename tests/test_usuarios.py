import pytest
from sqlalchemy import text
from security import verify_password


## testS para usuarios

def test_crear_usuario(preparar_db, client, usuario_data):
    response= client.post('/usuarios', json= usuario_data)

    data= response.json()

    assert response.status_code == 201
    assert data['email'] == 'tests@gmail.com'
    assert data['rol'] == 'usuario'
    assert data['activo'] is True
    assert 'password' not in data 
    assert 'password_hash' not in data


def test_crear_usuario_email_duplicado(preparar_db,client, usuario_data):
    response1= client.post('/usuarios',json=usuario_data)

    response2= client.post('/usuarios',json=usuario_data)
    data=response2.json()

    assert response1.status_code == 201
    assert response2.status_code == 409
    assert data['detail'] == 'El email ya existe'


@pytest.mark.parametrize('campo,valor',
[
    ('email', 'edmar.com'),
    ('password' , '1234')
])
def test_crear_usuario_datos_invalidos(preparar_db,client,usuario_data,campo,valor):
    usuario_data_2= usuario_data.copy()
    usuario_data_2[campo] = valor

    response1= client.post('/usuarios', json=usuario_data_2)
    data=response1.json()


    assert response1.status_code == 422
    assert data['detail'][0]['loc'] == ["body", campo] ##   lista de errores, el primero,en la ubicacion loc
    


def  test_password_se_guarda_hasheada(preparar_db,client,usuario_data):
    response1= client.post('/usuarios',json=usuario_data)

    assert response1.status_code == 201
    
    connection=preparar_db

    resultado= connection.execute(text("SELECT password_hash FROM usuarios WHERE email = :email"),
    {"email": usuario_data["email"]},
)
    fila=resultado.fetchone()

    hash_guardado=fila.password_hash

    verificacion= verify_password(usuario_data['password'],hash_guardado)

    assert hash_guardado != usuario_data['password']
    assert verificacion is True

