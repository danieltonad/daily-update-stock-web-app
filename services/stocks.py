import yfinance as yf
from requests import Session
from settings import settings
from logger import app_log
from pandas import read_csv
import io, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
# from pytickersymbols import PyTickerSymbols



RESULT_LOCK = threading.Lock()


results = []

def fetch_us_symbols(limit: bool | int = False):
    try:
        with Session() as session:
            respnse = session.get(settings.YF_SYMBOLS_URL)
            respnse.raise_for_status()
            
            # stream csv file
            csv_data = read_csv(io.StringIO(respnse.text))
            csv_data = csv_data[csv_data["country"] == "United States"]
            
            symbols_name = "Name"
            if symbols_name in csv_data.columns:
                symbols: list = csv_data[symbols_name].tolist()
                return symbols if not limit else symbols[:limit]
            else:
                raise ValueError(f"Unable to locate `{symbols_name}` in csv_data")
            
    except Exception as e:
        app_log(title="FETCH_SYMBOLS_ERR", msg=e)


# Fetch stock data
def fetch_stocks_data():
    symbols = fetch_us_symbols()
    app_log(title="INFO", msg=f"Symbols: {len(symbols):,}")
    custom_criteria('AAPL')
    
    # multi-thread stock data details
    # with ThreadPoolExecutor() as executor:
    #     app_log(title="INFO", msg="Fetching data..")
    #     futures = [executor.submit(custom_criteria, symbol) for symbol in symbols]
    #     app_log(title="INFO", msg="completely fetched data..")
    
    return results
    
def custom_criteria(symbol: str):
    global result
    ticker = yf.Ticker(symbol)
    market_cap = int(ticker.info.get('marketCap', 0))
    try:
        # print(f"{market_cap:,}")
        if market_cap >= settings.MAX_VOLUME:
            history = ticker.history(period="1y")
            short_ma = history['Close'].rolling(window=50).mean()
            long_ma = history['Close'].rolling(window=200).mean()
            golden_cross = "(short_ma[-2] < long_ma[-2]) and (short_ma[-1] > long_ma[-1])"
            death_cross = "(short_ma[-2] > long_ma[-2]) and (short_ma[-1] < long_ma[-1])"
            print({'symbol': symbol, 'golden_cross': golden_cross, 'death_cross': death_cross})
        
        #     with RESULT_LOCK:
        #         results.append([symbol, highest_volume, highest_volume_date])
        # app_log(title="FETCHED", msg=f"{symbol}")
    except Exception as e:
        app_log(title=f"{symbol}_SYMBOL_ERR", msg=f"Error: {str(e)}")
    