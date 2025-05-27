from pydantic_settings import BaseSettings


class Settings(BaseSettings):

# DB
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "pomodoro"
    DB_DRIVER: str = "postgresql+psycopg2"
# CACHE
    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
# JWT
    JWT_SECRET_KEY: str = "secret_key"
    JWT_ENCODE_ALGORHYTM: str = "HS256"
# GOOGLE
    GOOGLE_CLIENT_ID: str = "706308476866-c8022qlad4p84194jm18rbc3trlhufdg.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET_KEY: str = "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"
    GOOGLE_REDIRECT_URI: str = "http://127.0.0.1:8000/auth/google"
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"
#YANDEX
    YANDEX_CLIENT_ID: str = "25222cf340894f20b0481fe5293b9a54"
    YANDEX_CLIENT_SECRET: str = "c672c1b88fa04d70983717fb2b29bd63"
    YANDEX_REDIRECT_URI: str = "http://127.0.0.1:8000/auth/yandex"
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"



    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    
    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    

    @property
    def yandex_redirect_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}"