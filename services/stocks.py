import yfinance as yf
from requests import Session
from settings import Settings
from pandas import read_csv, Series
from utils import Utils
import io
from datetime import datetime
from config.database import stocks_db
from trigger import Triggers
from models.stock import StockSerializer




class Stocks( Triggers, Utils, Settings, StockSerializer):
    results: list
    golden_cross_data: list
    death_cross_data: list
    symbols: list
    count: int
    total: int
    
    def __init__(self) -> None:
        super().__init__()
        self.results = []
        self.golden_cross_data = []
        self.death_cross_data = []
        self.symbols = []
        self.count = 0
        self.total = 0

    def __fetch_us_symbols(self, limit = False):
        try:
            with Session() as session:
                respnse = session.get(self.YF_SYMBOLS_URL)
                respnse.raise_for_status()
                
                # stream csv file
                csv_data = read_csv(io.StringIO(respnse.text))
                csv_data = csv_data[csv_data["country"] == "United States"]
                
                symbols_name = "Symbol"
                if symbols_name in csv_data.columns:
                    symbols: list = csv_data[symbols_name].tolist()
                    self.symbols = symbols if not limit else symbols[:limit]
                else:
                    raise ValueError(f"Unable to locate `{symbols_name}` in csv_data")
            
        except Exception as e:
            self.app_log(title="SYMBOLS_ERR", msg=e)
    
    def __calculate_moving_average(self, prices, window):
        return prices.rolling(window=window).mean()


    def __spot_crossover(self, series: Series):
        return True if len(series[series == True]) else False


    # Fetch stock data
    def fetch_stocks_data(self):
        from time import time
        start  = time()
        symbols = self.__fetch_us_symbols()
        self.total = len(symbols)
        self.app_log(title="INFO", msg=f"Symbols: {self.total:,}")
        
        #get stock data details
        self.app_log(title="INFO", msg="Fetching data..")
        for symbol in symbols:
            self.count += 1
            self.__detect_peak_volume_stocks(symbol)
            
        self.app_log(title="INFO", msg="completely fetched data..")
        
        # update data in background
        self.__update_stocks(stocks=self.results)
        
        message, golden_msg,  death_msg = "", "", ""
        
        # trigger crossovers in background
        if self.golden_cross_data or self.death_cross_data:
            
            if self.golden_cross_data:
                golden_msg = "<b>Golden Cross: </b> " + ", ".join(self.golden_cross_data) + "."
            
            if self.death_cross_data:
                death_msg = "<b>Death Cross:</b> " + ", ".join(self.death_cross_data) + "."
            message = f"{golden_msg}\n\n{death_msg}" if golden_msg and death_msg else f"{golden_msg}\n{death_msg}"
            
            trigger = Triggers()
            trigger.notify(channel="stock-update-channel", event="crossover-event", message=message)
        
        print(f"Execution time: {time() - start:.2f}")
        
        self.app_log(title="NEXT_CRON", msg=self.next_job_time())

   
   
   
    def __detect_peak_volume_stocks(self, symbol: str):
        ticker = yf.Ticker(symbol)
        ticker_info = ticker.info
        market_cap = int(ticker_info.get('marketCap', 0))
        try:
            if market_cap >= self.MAX_VOLUME:
                history = ticker.history(period="1y")
                
                closed_price = history['Close']
                short_ma = self.__calculate_moving_average(prices=closed_price, window=50)
                long_ma = self.__calculate_moving_average(prices=closed_price, window=200)
                #  drop NaN
                closed_price.dropna()
                # spot on cross_over
                golden_cross = self.__spot_crossover((short_ma.shift(1) < long_ma.shift(1)) & (short_ma > long_ma))
                death_cross = self.__spot_crossover((short_ma.shift(1) > long_ma.shift(1)) & (short_ma < long_ma))

                if golden_cross or death_cross:
                    if death_cross:
                        self.death_cross_data.append(symbol)
                    
                    if golden_cross:
                        self.golden_cross_data.append(symbol)
            
                name = ticker_info.get("shortName")
                current_price = float(ticker_info.get("currentPrice", 0))
                volume = float(ticker_info.get("volume", 0))
                open = float(ticker_info.get("open", 0))
                day_high = float(ticker_info.get("dayHigh", 0))
                day_low = float(ticker_info.get("dayLow", 0))
                # 
                self.results.append({"key": symbol, "symbol": symbol, "name": name ,"price": current_price, "volume": volume, "open": open, "high": day_high, "low": day_low })
                    
        except Exception as e:
            self.app_log(title=f"{symbol}_SYMBOL_ERR", msg=f"Error: {str(e)}")
        

    def __update_stocks(self, stocks: list):
        stock_chunked = self.split_list(data=stocks, size=20)
        
        for chunk in stock_chunked:
            stocks_db.put_many(chunk, expire_in=self.EXPIRY)
        date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self.app_log(title="INFO", msg=f"Updated Stock Data at [{date}]")



    async def get_saved_stocks(self):
        stocks = stocks_db.fetch()._items
        return self.serialize_many(stocks)
    
    