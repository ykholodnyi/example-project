from typing import Optional, Dict, Any

from pydantic import BaseSettings, PostgresDsn, validator


class PostgresPsycopgDsn(PostgresDsn):
    allowed_schemes = {
        *PostgresDsn.allowed_schemes,
        "postgresql+psycopg2",
    }


class Settings(BaseSettings):
    DEBUG: bool = False

    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: str
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: Optional[str] = None
    POSTGRESQL_DATABASE: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresPsycopgDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRESQL_USER"),
            password=values.get("POSTGRESQL_PASSWORD"),
            host=values.get("POSTGRESQL_HOST"),
            port=values.get("POSTGRESQL_PORT"),
            path=f"/{values.get('POSTGRESQL_DATABASE') or ''}",
        )


settings = Settings()
