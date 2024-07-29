from fastapi import FastAPI
from settings import settings


app = FastAPI(title=settings.APP_NAME)



@app.get("/")
async def root():
    from services.stocks import fetch_stocks_data
    
    fetch_stocks_data()
    
    return settings.APP_NAME