from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Define all the secret variables
    host_name : str


    class Config:
        env_file = ".env"
    # use -> Setting.host_name