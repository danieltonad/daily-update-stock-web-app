import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "Stock Daily Update"
    MG_CONN_STR: str = os.getenv("MG_CONN_STR")
    YF_SYMBOLS_URL: str = os.getenv("YF_SYMBOLS_URL")
    MAX_VOLUME: int = 20_000_000_000
    
settings = Settings()
    