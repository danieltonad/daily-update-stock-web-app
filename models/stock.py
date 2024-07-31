
class StockSerializer:

    def serialize_one(self, stock: dict):
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

    def serialize_many(self, stocks: list):
        stocks = sorted(stocks, key=lambda x: x['price'], reverse=True)
        return [self.stock_serializer(stock) for stock in stocks]