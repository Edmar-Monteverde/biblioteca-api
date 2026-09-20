from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database  import Base, get_db
from main import app

from config import settings
import pytest

TEST_DATABASE_URL=  f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/biblioteca_tests"


test_engine= create_engine(TEST_DATABASE_URL)



TestingSessionLocal= sessionmaker(
    autocommit= False,
    autoflush=False,
    bind= test_engine
)

def get_test_db():
    db=TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db

#### terminamos de conerctar la db_tests 




@pytest.fixture
def preparar_db():
    ## esto lo hacemos para que cada ejecucion de tests empiece desde cero 
    Base.metadata.drop_all( bind=test_engine) ## Borro tablas de la base de datos de tests
    Base.metadata.create_all(bind=test_engine) ## creamos las  tablas dentro de la base de datos de prueba
    

    yield

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