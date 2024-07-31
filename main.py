from fastapi import FastAPI
from settings import settings
from services.stocks import get_saved_stocks, fetch_stocks_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from jobs.update_stock import cron_execute


# init app
app = FastAPI(title=settings.APP_NAME)

# jinja template
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


#  register cron on start u
@app.on_event("startup")
async def startup_event():
    from services.stocks import fetch_stocks_data
    # fetch_stocks_data()
    cron_execute()

# cors 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index(request: Request):
    stocks = await get_saved_stocks()
    return templates.TemplateResponse("index.html", {"request": request, "data": {"stocks": stocks}})


@app.get("/stocks", tags=["Stocks Retrieve"])
async def retrieve_stock_data():
    return await get_saved_stocks()



