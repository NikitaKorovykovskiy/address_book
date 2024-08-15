from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    web_port: int = Field(..., env="WEB_PORT")
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    redis_db: int = Field(..., env="REDIS_DB")

    class Config:
        env_file = ".env"
class Address(BaseModel):
    address: str

class WriteAddress(Address):
    phone: str

class MessageResponse(BaseModel):
    message: str