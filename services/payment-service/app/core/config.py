from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    user_service_url: str = "http://user-service:8001"
    product_service_url: str = "http://product-service:8002"

    kafka_bootstrap_servers: str = "kafka:29092"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()