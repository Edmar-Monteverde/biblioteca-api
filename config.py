from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings): ##lee variables  de entorno y convierte  y valida
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM:str
    MINUTES: int

    model_config  = SettingsConfigDict(env_file='.env')


settings = Settings()
