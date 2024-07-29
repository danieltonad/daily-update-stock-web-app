from fastapi import FastAPI
from settings import settings

app = FastAPI(title=settings.APP_NAME)