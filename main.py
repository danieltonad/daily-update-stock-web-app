from fastapi import FastAPI
from settings import settings
from services.stocks import Stocks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from jobs.update_stock import CronJobs


# init app
app = FastAPI(title=settings.APP_NAME)

# jinja template
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


#  register cron on start up
@app.on_event("startup")
async def startup_event():
    cron = CronJobs()
    cron.execute()

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
    stock = Stocks()
    stocks = await stock.get_saved_stocks()
    return templates.TemplateResponse("index.html", {"request": request, "data": {"stocks": stocks}})


@app.get("/stocks", tags=["Stocks Retrieve"])
async def retrieve_stock_data():
    stock = Stocks()
    return await stock.get_saved_stocks()



