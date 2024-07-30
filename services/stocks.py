import yfinance as yf
from requests import Session
from settings import settings
from logger import app_log
from pandas import read_csv, Series
import io, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
# from pytickersymbols import PyTickerSymbols



RESULT_LOCK = threading.Lock()


results = []
crossovers = []

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


def calculate_moving_average(prices, window):
    return prices.rolling(window=window).mean()

def spot_crossover(series: Series):
        return True if len(series[series == True]) else False

# Fetch stock data
def fetch_stocks_data() -> tuple:
    symbols = fetch_us_symbols(limit=100)
    app_log(title="INFO", msg=f"Symbols: {len(symbols):,}")
    # custom_criteria('AAPL')
    
    # multi-thread stock data details
    with ThreadPoolExecutor() as executor:
        app_log(title="INFO", msg="Fetching data..")
        futures = [executor.submit(custom_criteria, symbol) for symbol in symbols]
        app_log(title="INFO", msg="completely fetched data..")
    
    
    return results, crossovers
    
def custom_criteria(symbol: str):
    global results, crossovers
    ticker = yf.Ticker(symbol)
    ticker_info = ticker.info
    market_cap = int(ticker_info.get('marketCap', 0))
    try:
        if market_cap >= settings.MAX_VOLUME:
            history = ticker.history()
            
            closed_price = history['Close']
            short_ma = calculate_moving_average(prices=closed_price, window=50)
            long_ma = calculate_moving_average(prices=closed_price, window=200)
            #  drop NaN
            closed_price.dropna()
            # spot on cross_over
            golden_cross = spot_crossover((short_ma.shift(1) < long_ma.shift(1)) & (short_ma > long_ma))
            death_cross = spot_crossover((short_ma.shift(1) < long_ma.shift(1)) & (short_ma > long_ma))

            if golden_cross or death_cross:
                cross_type = "golden_cross" if golden_cross else "death_cross"
                crossovers.append({"symbol": symbol, "cross_type": cross_type })
        
            with RESULT_LOCK:
                name = ticker_info.get("shortName")
                current_price = float(ticker_info.get("currentPrice", 0))
                volume = float(ticker_info.get("volume", 0))
                open = float(ticker_info.get("open", 0))
                day_high = float(ticker_info.get("dayHigh", 0))
                day_low = float(ticker_info.get("dayLow", 0))
                # 
                results.append({"symbol": symbol, "name": name ,"price": current_price, "volume": volume, "open": open, "high": day_high, "low": day_low })
        
        app_log(title="FETCHED", msg=f"{symbol}")
    except Exception as e:
        app_log(title=f"{symbol}_SYMBOL_ERR", msg=f"Error: {str(e)}")
    