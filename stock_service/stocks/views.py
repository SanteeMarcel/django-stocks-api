# encoding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import csv


class StockView(APIView):
    """
    Receives stock requests from the API service.
    """

    def get(self, request, *args, **kwargs):
        stock_code = request.GET.get("stock_code", "EmptyError")

        if stock_code == "EmptyError":
            json = {"Error": "Stock code is empty"}
            status = 204
            return Response(json, status)

        try:
            with requests.Session() as s:
                stock_raw_info = s.get(
                    f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv')
                json, status = self.decoder(stock_raw_info.content)
        except Exception as e:
            json = {"Error": "Unable to fetch stock information"}
            status = 500
        finally:
            return Response(json, status=status)

    def decoder(self, data):
        decoded = data.decode('utf-8')
        rows = [x for x in csv.reader(
            decoded.splitlines(), delimiter=',')]
        symbol, date, time, open, high, low, close, volume, name = rows[1]
        if open == 'N/D':
            json = {"Error": "Unable to find stock"}
            status = 404
        else:
            json = {"Symbol": f"{symbol}", "Date": f"{date}", "Time": f"{time}", "Open": f"{open}",
                    "High": f"{high}", "Low": f"{low}", "Close": f"{close}", "Volume": f"{volume}", "Name": f"{name}"}
            status = 200
        return json, status
