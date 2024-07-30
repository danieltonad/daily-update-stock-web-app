from fastapi import FastAPI, BackgroundTasks
from settings import settings
from trigger import trigger_pusher
from services.stocks import get_saved_stocks, fetch_stocks_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from models.action import Action

# init app
app = FastAPI(title=settings.APP_NAME)

# jinja template
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/stocks", tags=["Stocks Retrieve"])
async def test_pusher():
    return await get_saved_stocks()



@app.get("/pusher")
async def retrieve_stocks_data():
    await trigger_pusher(event="test-event", channel="test-channel", message="Tesing Mic 1234")
    

#  deta custom crom
@app.post("/__space/v0/actions")
async def actions(action: Action, background_tasks: BackgroundTasks):
    if action.event.id == "stock_data_update":
        background_tasks.add_task(fetch_stocks_data, background_tasks)