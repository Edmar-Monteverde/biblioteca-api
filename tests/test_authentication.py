import pytest
from datetime import datetime,timedelta,timezone
import jwt
from config import settings
from security import crear_access_token
from sqlalchemy import text



def test_token_valido(preparar_db,usuario_data,client):
    response1= client.post('/usuarios',json=usuario_data)
    assert response1.status_code == 201

    response2=client.post('/usuarios/login',json=usuario_data)
    assert response2.status_code ==200

    data=response2.json()
    token=data["access_token"] ## obtenemos el token de acceso del usuario logueado

    headers={"Authorization": f"Bearer {token}"}  ## creamos el diccionario completo y introducimos el token de acceso en el header de la peticion


    response3=client.get('/usuarios/me',headers=headers)
    data3=response3.json()

    assert response3.status_code == 200
    assert data3['email'] == usuario_data['email']




def test_token_invalido(client):


    token_invalido='invalido'

    headers= {"Authorization": f"Bearer {token_invalido}"}

    response2=client.get('/usuarios/me',headers=  headers)
    data=response2.json()

    assert response2.status_code == 401 
    assert data['detail'] == 'Token inválido o expirado'


def test_token_expirado(client):
    expiracion=datetime.now(timezone.utc) - timedelta(minutes=1) ## modificamos el tiempo de expiracion 

    payload = {
            'sub' : str(1),
            'exp' : expiracion
        }

    token_expirado= jwt.encode(payload,settings.SECRET_KEY,algorithm=settings.ALGORITHM) ## creamos un nuevo token expirado

    headers= {"Authorization": f"Bearer {token_expirado}"}

    response1=client.get('/usuarios/me',headers= headers)
    data=response1.json()

    assert response1.status_code == 401
    assert data['detail'] == 'Token inválido o expirado'


def test_token_usuario_inexistente(client):
    token = crear_access_token(9999999) ## usamos la funcion crear token  pero con el usuario_id inexistente

    headers= {"Authorization": f"Bearer {token}"}

    response=client.get('/usuarios/me',headers= headers)
    data=response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token inválido o expirado'



def test_token_usuario_inactivo(preparar_db, client, usuario_data):
    response1=client.post('/usuarios',json=usuario_data)
    data=response1.json()
    assert response1.status_code == 201

    connection= preparar_db

    connection.execute(text('UPDATE usuarios set activo = False where email = :email'),{'email' : data['email']})

    usuario_id= data['id']

    token= crear_access_token(usuario_id)

    headers= {"Authorization": f"Bearer {token}"}

    response2=client.get('/usuarios/me',headers= headers )
    data2=response2.json()

    assert response2.status_code == 403
    assert data2['detail'] == 'El usuario esta inactivo'


def test_sin_token(client):

    response=client.get('/usuarios/me')
    data=response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Not authenticated'
