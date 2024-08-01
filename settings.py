import os
from dotenv import load_dotenv
from logger import Logger

load_dotenv()

class Settings(Logger):
    APP_NAME: str = "Stock Daily Update"
    DB_CONN_STR: str = os.getenv("DB_CONN_STR")
    YF_SYMBOLS_URL: str = os.getenv("YF_SYMBOLS_URL")
    PUSHER_APP_ID: str = os.getenv("PUSHER_APP_ID")
    PUSHER_KEY: str = os.getenv("PUSHER_KEY")
    PUSHER_SECRET: str = os.getenv("PUSHER_SECRET")
    PUSHER_CLUSTER: str = os.getenv("PUSHER_CLUSTER")
    MAX_VOLUME: int = 20_000_000_000
    EXPIRY: int = 86_4000
    STOCK_LIMIT: int = 100
    CRON_MINUTE: int = 19

    