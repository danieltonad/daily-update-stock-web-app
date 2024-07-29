import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "Stock Daily Update"
    MG_CONN_STR: str = os.getenv("MG_CONN_STR")
    
settings = Settings()
    