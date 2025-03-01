from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Define all the secret variables
    host_name : str


    class Config:
        env_file = ".env"

# settings = Settings()
# use -> setting.host_name    