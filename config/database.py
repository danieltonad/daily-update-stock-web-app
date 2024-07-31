from deta import Deta, _Base



class Database:
    deta = None
    stocks_db: _Base
    
    def __init__(self) -> None:
        self.deta =  Deta()
        self.stocks_db = self.deta.Base('stocks')