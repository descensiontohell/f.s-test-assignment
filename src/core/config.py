import os
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    AUTH_TOKEN: str
    URL_BASE: str

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: str = (f"postgresql+asyncpg://"
                         f"{os.getenv('POSTGRES_USER')}:"
                         f"{os.getenv('POSTGRES_PASSWORD')}@"
                         f"{os.getenv('POSTGRES_SERVER')}/{os.getenv('POSTGRES_DB')}")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
