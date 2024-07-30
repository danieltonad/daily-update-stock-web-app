
def stock_serializer(stock: dict):
    return {
        "key": stock.get("key"),
        "symbol": stock.get("symbol"),
		"name": stock.get('name'),
		"price": f"{stock.get('price'):,.2f}",
		"volume": f"{stock.get('volume'):,}",
		"open": f"{stock.get('open'):,.2f}",
		"high": f"{stock.get('high'):,.2f}",
		"low": f"{stock.get('low'):,.2f}"
    }

def stocks_serializer(stocks: list):
    return [stock_serializer(stock) for stock in stocks]