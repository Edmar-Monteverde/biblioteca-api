from pydantic_settings import BaseSettings


class Settings(BaseSettings): ##lee variables  de entorno y convierte  y valida
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file = ".env" ###  donde buscar las variables 


settings = Settings()