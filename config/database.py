from deta import Deta, base



class Database:
    deta = None
    stocks_db: base
    
    def __init__(self) -> None:
        self.deta =  Deta()
        self.stocks_db = self.deta.Base('stocks')