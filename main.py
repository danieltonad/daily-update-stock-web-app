from fastapi import FastAPI
from settings import settings
from trigger import trigger_pusher

app = FastAPI(title=settings.APP_NAME)



@app.get("/")
async def root():
    from services.stocks import fetch_stocks_data
    from time import time
    
    start  = time()
    results, crossovers = fetch_stocks_data()
    
    print(f"Time: {start - time():.2f}")
    
    return {"results": results, "crossovers": crossovers}

@app.get("/pusher")
async def test_pusher():
    await trigger_pusher(event="test-event", channel="test_channel", message="Tesing Mic 1234")