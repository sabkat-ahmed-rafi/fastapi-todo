from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET: str
    PASSWORD_RESET_SECRET: str
    EMAIL_VERIFICATION_SECRET: str | None = None
    API_KEY: str
    FRONTEND_URL: str = "http://localhost:3000"

    STORAGE_PROVIDER: str = "local"
    STORAGE_PATH: str = "./uploads"

    EMAIL_PROVIDER: str = "resend"
    RESEND_API_KEY: str
    EMAIL_FROM: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
