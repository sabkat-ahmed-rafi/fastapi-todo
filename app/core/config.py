from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET: str
    API_KEY: str

    STORAGE_PROVIDER: str = "local"
    STORAGE_PATH: str = "./uploads"

    EMAIL_PROVIDER: str = "resend"
    RESEND_API_KEY: str
    EMAIL_FROM: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
