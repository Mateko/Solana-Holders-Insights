from pydantic import BaseSettings
from typing import List
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR: str = ""
    PROJECT_NAME: str = "Solana Holders Insights"
    DESCRIPTION: str = "An app that provides insights into top holders to not let u get rugged!"

    MYSQL_SERVER: str = "default"
    MYSQL_USER: str = "default"
    MYSQL_PASSWORD: str = "default"
    MYSQL_DB: str = "default"

    HELIUS_API_KEY: str = ''
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}"
    )


core_settings = Settings()
