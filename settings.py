import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "Stock Daily Update"
    DB_CONN_STR: str = os.getenv("DB_CONN_STR")
    YF_SYMBOLS_URL: str = os.getenv("YF_SYMBOLS_URL")
    PUSHER_APP_ID: str = os.getenv("PUSHER_APP_ID")
    PUSHER_KEY: str = os.getenv("PUSHER_KEY")
    PUSHER_SECRET: str = os.getenv("PUSHER_SECRET")
    PUSHER_CLUSTER: str = os.getenv("PUSHER_CLUSTER")
    MAX_VOLUME: int = 20_000_000_000
    
settings = Settings()
    