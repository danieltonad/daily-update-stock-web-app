import yfinance as yf
from requests import Session
from settings import settings
from logger import app_log
from pandas import read_csv, Series
import io, threading, json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.database import stocks_db
from utils import split_list
from trigger import trigger_pusher
from models.stock import stocks_serializer


RESULT_LOCK = threading.Lock()


results = []
golden_cross_data, death_cross_data = [], []

def fetch_us_symbols(limit = False):
    try:
        with Session() as session:
            respnse = session.get(settings.YF_SYMBOLS_URL)
            respnse.raise_for_status()
            
            # stream csv file
            csv_data = read_csv(io.StringIO(respnse.text))
            csv_data = csv_data[csv_data["country"] == "United States"]
            
            symbols_name = "Symbol"
            if symbols_name in csv_data.columns:
                symbols: list = csv_data[symbols_name].tolist()
                return symbols if not limit else symbols[:limit]
            else:
                raise ValueError(f"Unable to locate `{symbols_name}` in csv_data")
            
    except Exception as e:
        app_log(title="SYMBOLS_ERR", msg=e)
    
def calculate_moving_average(prices, window):
    return prices.rolling(window=window).mean()


def spot_crossover(series: Series):
    return True if len(series[series == True]) else False


# Fetch stock data
def fetch_stocks_data():
    from time import time
    start  = time()
    symbols = fetch_us_symbols()
    app_log(title="INFO", msg=f"Symbols: {len(symbols):,}")
    
    #get stock data details
    app_log(title="INFO", msg="Fetching data..")
    for symbol in symbols:
        custom_criteria(symbol)
        
    app_log(title="INFO", msg="completely fetched data..")
    
    # update data in background
    update_stocks(stocks=results)
    
    message, golden_msg,  death_msg = "", "", ""
    # trigger crossovers in background
    if golden_cross_data or death_cross_data:
        
        if golden_cross_data:
            golden_msg = "<b>Golden Cross: <b> " + ", ".join(golden_cross_data) + "."
        
        if death_cross_data:
            death_msg = "<b>Death Cross:<b> " + ", ".join(death_cross_data) + "."
        message = f"{golden_msg}\n\n{death_msg}" if golden_msg and death_msg else f"{golden_msg}\n{death_msg}"
        
        trigger_pusher(channel="stock-update-channel", event="crossover-event", message=message)
    
    print(f"Execution time: {time() - start:.2f}")

   
   
   
def custom_criteria(symbol: str):
    global results, golden_cross_data, death_cross_data
    ticker = yf.Ticker(symbol)
    ticker_info = ticker.info
    market_cap = int(ticker_info.get('marketCap', 0))
    try:
        if market_cap >= settings.MAX_VOLUME:
            history = ticker.history(period="1y")
            
            closed_price = history['Close']
            short_ma = calculate_moving_average(prices=closed_price, window=50)
            long_ma = calculate_moving_average(prices=closed_price, window=200)
            #  drop NaN
            closed_price.dropna()
            # spot on cross_over
            golden_cross = spot_crossover((short_ma.shift(1) < long_ma.shift(1)) & (short_ma > long_ma))
            death_cross = spot_crossover((short_ma.shift(1) > long_ma.shift(1)) & (short_ma < long_ma))

            if golden_cross or death_cross:
                if death_cross:
                    death_cross_data.append(symbol)
                
                if golden_cross:
                    golden_cross_data.append(symbol)
        
            with RESULT_LOCK:
                name = ticker_info.get("shortName")
                current_price = float(ticker_info.get("currentPrice", 0))
                volume = float(ticker_info.get("volume", 0))
                open = float(ticker_info.get("open", 0))
                day_high = float(ticker_info.get("dayHigh", 0))
                day_low = float(ticker_info.get("dayLow", 0))
                # 
                results.append({"key": symbol, "symbol": symbol, "name": name ,"price": current_price, "volume": volume, "open": open, "high": day_high, "low": day_low })
                
    except Exception as e:
        app_log(title=f"{symbol}_SYMBOL_ERR", msg=f"Error: {str(e)}")
    

def update_stocks(stocks: list):
    stock_chunked = split_list(data=stocks, size=20)
    
    for chunk in stock_chunked:
        stocks_db.put_many(chunk, expire_in=settings.EXPIRY)
    date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    app_log(title="INFO", msg=f"Updated Stock Data at [{date}]")



async def get_saved_stocks():
    stocks = stocks_db.fetch()._items
    return stocks_serializer(stocks)
    
    