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
    
    connection=preparar_db ## aprovechamos la connection para acceder a la BD

    resultado= connection.execute(text("SELECT password_hash FROM usuarios WHERE email = :email"), ## hacemos la consulta directamente
    {"email": usuario_data["email"]}, ## en sql 
)
    fila=resultado.fetchone() ## obtenemos solo la filla de nuestra consulta 

    hash_guardado=fila.password_hash 

    verificacion= verify_password(usuario_data['password'],hash_guardado) ## verificamos que el hash le pertenece a la password 

    assert hash_guardado != usuario_data['password']
    assert verificacion is True



def test_login_correcto(preparar_db,client,usuario_data):
    response1=client.post('/usuarios',json=usuario_data)
    assert response1.status_code == 201

    response2=client.post('/usuarios/login', json=usuario_data)
    data=response2.json()
    assert response2.status_code ==200
    assert data['activo'] is True
    assert data["email"] == usuario_data["email"]


def test__login_password_incorrecta(preparar_db,client,usuario_data):
    response1=client.post('/usuarios',json=usuario_data)
    assert response1.status_code == 201

    usuario_data2=usuario_data.copy()
    usuario_data2['password'] = 'incorrecta123'

    response2=client.post('/usuarios/login', json=usuario_data2)
    data=response2.json()


    assert response2.status_code == 401
    assert data['detail'] == 'Credenciales Incorrectas'

    

def test_login_email_inexistente(preparar_db,client,usuario_data):
   response=client.post('/usuarios/login', json=usuario_data)
   data=response.json()

   assert response.status_code == 401
   assert data['detail'] == 'Credenciales Incorrectas'



def test_login_usuario_inactivo(preparar_db,client,usuario_data):
    response1=client.post('/usuarios',json=usuario_data)
    data=response1.json()
    assert response1.status_code ==  201


    connection= preparar_db

    connection.execute(text('UPDATE usuarios set activo = False where email = :email'),{'email' : data['email']})

    response2=client.post('/usuarios/login', json=usuario_data)
    data2=response2.json()

    assert response2.status_code == 403
    assert data2['detail'] == 'El usuario esta inactivo'