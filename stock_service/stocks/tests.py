from django.test.testcases import SimpleTestCase
from stocks.views import StockView


class TestStockView(SimpleTestCase):

    def test_should_not_get_stocks(self):
        stock_raw_info = b'Symbol,Date,Time,Open,High,Low,Close,Volume,Name\r\nTOXI.DS,N/D,N/D,N/D,N/D,N/D,N/D,N/D,TOXI.DS\r\n'
        json, status = StockView.decoder(StockView, stock_raw_info)
        assert status == 404
        assert json['Error'] == 'Unable to find stock'

    def test_should_get_stocks(self):
        stock_raw_info = b'Symbol,Date,Time,Open,High,Low,Close,Volume,Name\r\nAAPL.US,2021-11-12,22:00:10,148.43,150.4,147.48,149.99,63804008,APPLE\r\n'
        json, status = StockView.decoder(StockView, stock_raw_info)
        assert status == 200
        assert json['symbol'] == 'AAPL.US'
        assert json['date'] == '2021-11-12'
        assert json['time'] == '22:00:10'
        assert json['open'] == '148.43'
        assert json['high'] == '150.4'
        assert json['low'] == '147.48'
        assert json['close'] == '149.99'
        assert json['volume'] == '63804008'
        assert json['name'] == 'APPLE'
