from fastapi.testclient import TestClient
from sqlalchemy import create_engine
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
def usuario_data():
    return {
        'email' : 'tests@gmail.com',
        'password': 'Clave12345',
    }


    
@pytest.fixture
def prestamo_creado(preparar_db, client, libro_data):
    response1=client.post(
            "/libros",
            json=libro_data
        )
    assert response1.status_code == 201

    libro_creado=response1.json()
    libro_id= libro_creado['id']

    response2=client.post('/prestamos',json={ ## creamos el prestamos
                'libro_id': libro_id,
                'usuario':'Alejandra'  })

    assert response2.status_code == 201

    prestamo =response2.json()

    return prestamo