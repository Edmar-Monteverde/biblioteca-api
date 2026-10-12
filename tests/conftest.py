from fastapi.testclient import TestClient
from sqlalchemy import create_engine , text
from sqlalchemy.orm import  Session

from database  import Base, get_db
from main import app

from config import settings
import pytest

TEST_DATABASE_URL=  f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/biblioteca_tests"


test_engine= create_engine(TEST_DATABASE_URL)


@pytest.fixture
def preparar_db():
    # Preparación
    connection = test_engine.connect()
    transaction = connection.begin()

    def override_get_db():
        db = Session(bind=connection,
                     join_transaction_mode='create_savepoint')###si esta conexion ya tiene una transaccion

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Ejecución del test
    yield connection

    # Limpieza
    app.dependency_overrides.pop(get_db, None)  # Quitamos el override
    transaction.rollback()                     # Deshacemos la transacción
    connection.close()                         # Cerramos la conexión

@pytest.fixture
def client():
    return TestClient(app) ## importamos la app de main.py y creamos un cliente de prueba para hacer peticiones a la API


@pytest.fixture
def libro_data():
    return {
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "precio": 25.50,
        "stock": 3,
        "categoria": "Programacion",
        "disponible": True,
        "isbn": "9780132350884",
    }

@pytest.fixture
def admin_autenticado(preparar_db,client,usuario_data):
    response1=client.post('/usuarios',json=usuario_data)
    usuario=response1.json()
    assert response1.status_code == 201

    connection= preparar_db
    connection.execute(
        text("UPDATE usuarios SET rol = 'admin' WHERE email = :email"),
        {"email": usuario["email"]},
    )

    response2= client.post('/usuarios/login',json=usuario_data)
    assert response2.status_code == 200
    token_data=response2.json()
    access_token= token_data['access_token']

    return {
            "id": usuario["id"],
            "headers": {
                "Authorization": f"Bearer {access_token}"
            }}





@pytest.fixture
def usuario_data():
    return {
        'email' : 'tests@gmail.com',
        'password': 'Clave12345',
    }



@pytest.fixture
def prestamo_creado(preparar_db, client, libro_data,admin_autenticado,usuario_autenticado):
    response1=client.post(
            "/libros",
            json=libro_data,headers=admin_autenticado['headers']
        )
    assert response1.status_code == 201

    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.post('/prestamos',json={ ## creamos el prestamos
                'libro_id': libro_id,
                  },headers= usuario_autenticado['headers'])

    assert response2.status_code == 201

    prestamo =response2.json()

    return prestamo


@pytest.fixture
def usuario_headers(preparar_db,client):
    usuario = {
        "email": "usuario@test.com",
        "password": "Clave12345",}


    response1=client.post('/usuarios',json=usuario)
    assert response1.status_code == 201



    response2= client.post('/usuarios/login',json=usuario)
    assert response2.status_code == 200
    token_data=response2.json()
    access_token= token_data['access_token']

    return {"Authorization": f"Bearer {access_token}"}



@pytest.fixture
def usuario_autenticado(preparar_db,client):
    usuario_data = {
        "email": "usuario@test.com",
        "password": "Clave12345",
    }

    response = client.post("/usuarios", json=usuario_data)
    assert response.status_code == 201

    usuario = response.json()

    response_login = client.post(
        "/usuarios/login",
        json=usuario_data,
    )
    assert response_login.status_code == 200

    token = response_login.json()["access_token"]

    return {
        "id": usuario["id"],
        "headers": {
            "Authorization": f"Bearer {token}"
        },
    }
