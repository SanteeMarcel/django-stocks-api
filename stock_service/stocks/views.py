# encoding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import csv
import logging
from rest_framework import status as http_status

logger = logging.getLogger(__name__)

class StockView(APIView):
    """
    Receives stock requests from the API service.
    """

    def get_stock_data(self, stock_code):
        logger.info(f"Received stock_code: {stock_code}")

        if not stock_code:
            json_response = {"Error": "Stock code is empty"}
            response_status = http_status.HTTP_400_BAD_REQUEST
            logger.warning(f"Response JSON: {json_response}, Status: {response_status}")
            return json_response, response_status

        try:
            with requests.Session() as s:
                url = f"https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv"
                logger.info(f'Calling {url=}')
                stock_raw_info = s.get(url)
                stock_raw_info.raise_for_status()
                logger.info(f"Fetched raw stock info: {stock_raw_info.content[:100]}")
                json_response, response_status = self.decoder(stock_raw_info.content)
        except requests.RequestException as e:
            logger.error(f"RequestException occurred: {e}")
            json_response = {"Error": "Unable to fetch stock information"}
            response_status = http_status.HTTP_503_SERVICE_UNAVAILABLE
        except csv.Error as e:
            logger.error(f"CSV Error occurred: {e}")
            json_response = {"Error": "Error processing stock information"}
            response_status = http_status.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            json_response = {"Error": "An unexpected error occurred"}
            response_status = http_status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            logger.info(f"Response JSON: {json_response}, Status: {response_status}")
            return json_response, response_status

    def decoder(self, data):
        logger.info(f"Decoding data...")
        decoded = data.decode('utf-8')
        logger.info(f"Decoded data: {decoded[:100]}")
        rows = [x for x in csv.reader(decoded.splitlines(), delimiter=',')]
        logger.info(f"CSV rows: {rows}")
        symbol, date, time, open_price, high, low, close, volume, name = rows[1]
        
        if open_price == 'N/D':
            json_response = {"Error": "Unable to find stock"}
            response_status = http_status.HTTP_404_NOT_FOUND
        else:
            json_response = {
                "symbol": symbol,
                "date": date,
                "time": time,
                "open": open_price,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
                "name": name
            }
            response_status = http_status.HTTP_200_OK
        
        logger.info(f"Decoded JSON: {json_response}, Status: {response_status}")
        return json_response, response_status

    def get(self, request, *args, **kwargs):
        stock_code = request.GET.get("stock_code", None)
        json_response, response_status = self.get_stock_data(stock_code)
        return Response(json_response, status=response_status)
