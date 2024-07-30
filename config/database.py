from deta import Deta
from settings import settings

# init
deta =  Deta()


# connect to db
stocks_db =  deta.Base('stocks')