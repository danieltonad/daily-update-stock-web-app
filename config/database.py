from deta import Deta

# init
deta =  Deta()


# connect to db
stocks_db =  deta.Base('stocks')