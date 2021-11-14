from django.http.request import HttpRequest
from django.test.testcases import TestCase
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList
from api.views import StockView, HistoryView, StatsView
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.request import Request
from django.core.management import call_command


class TestStockViewDB(TestCase):

    def test_should_save_query_to_db(self):
        json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                'High': '150.4', 'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
        user = User.objects.create_user(username='peter', password='spiderman')
        response = StockView.save_query_to_db(StockView, json, user)
        assert response is None

    def test_should_return_error_if_no_user(self):
        with self.assertRaises(IntegrityError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'High': '150.4', 'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            response = StockView.save_query_to_db(StockView, json, None)
            assert response is None

    def test_should_return_error_if_no_json(self):
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, None, user)
            assert response is None

    def test_should_return_error_if_no_symbol(self):
        with self.assertRaises(KeyError):
            json = {'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43', 'High': '150.4',
                    'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, json, user)
            assert response is None

    def test_should_return_error_if_no_date(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Time': '22:00:10', 'Open': '148.43', 'High': '150.4',
                    'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, json, user)
            assert response is None

    def test_should_return_error_if_no_time(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Open': '148.43', 'High': '150.4',
                    'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, json, user)
            assert response is None

    def test_should_return_error_if_no_open(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'High': '150.4',
                    'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, json, user)
            assert response is None

    def test_should_return_error_if_no_high(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, json, user)
            assert response is None

    def test_should_return_error_if_no_low(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'High': '150.4', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, json, user)
            assert response is None

    def test_should_return_error_if_no_close(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'High': '150.4', 'Low': '147.48', 'Volume': '63804008', 'Name': 'APPLE'}
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, json, user)
            assert response is None

    def test_should_return_error_if_no_name(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'High': '150.4', 'Low': '147.48', 'Close': '149.99', 'Volume': '63804008'}
            user = User.objects.create_user(
                username='peter', password='spiderman')
            response = StockView.save_query_to_db(StockView, json, user)
            assert response is None


class TestStockViewFiltering(TestCase):

    def test_should_filter_data(self):
        json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                'High': '150.4', 'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
        data = StockView.filter_relevant_data(StockView, json)
        assert data == {'name': 'APPLE', 'symbol': 'AAPL.US',
                        'open': '148.43', 'low': '147.48', 'high': '150.4', 'close': '149.99'}

    def test_should_return_error_if_no_name(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'High': '150.4', 'Low': '147.48', 'Close': '149.99', 'Volume': '63804008'}
            data = StockView.filter_relevant_data(StockView, json)
            assert data is None

    def test_should_return_error_if_no_symbol(self):
        with self.assertRaises(KeyError):
            json = {'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43', 'High': '150.4',
                    'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            data = StockView.filter_relevant_data(StockView, json)
            assert data is None

    def test_should_return_error_if_no_open(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'High': '150.4',
                    'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            data = StockView.filter_relevant_data(StockView, json)
            assert data is None

    def test_should_return_error_if_no_high(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            data = StockView.filter_relevant_data(StockView, json)
            assert data is None

    def test_should_return_error_if_no_low(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'High': '150.4', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}
            data = StockView.filter_relevant_data(StockView, json)
            assert data is None

    def test_should_return_error_if_no_close(self):
        with self.assertRaises(KeyError):
            json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
                    'High': '150.4', 'Low': '147.48', 'Volume': '63804008', 'Name': 'APPLE'}
            data = StockView.filter_relevant_data(StockView, json)
            assert data is None


class TestHistoryView(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'testdb.json', verbosity=0)

    def test_should_return_data(self):
        user = User.objects.get(username='peter')
        request = HttpRequest()
        request.user = user
        request.user.id = user.id

        response = HistoryView.get(HistoryView, request)

        assert type(response) == Response
        assert type(response.data) == ReturnList
        assert len(response.data) > 1

    def test_should_return_error_if_no_request(self):
        with self.assertRaises(AttributeError):
            response = HistoryView.get(HistoryView, None)
            assert response is None

    def test_should_return_error_if_no_user(self):
        with self.assertRaises(AssertionError):
            request = Request(None)
            response = HistoryView.get(HistoryView, request)


class TestStatsView(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'testdb.json', verbosity=0)

    def test_should_block_non_superusers(self):
        user = User.objects.get(username='peter')
        request = HttpRequest()
        request.user = user
        request.user.id = user.id

        response = StatsView.get(StatsView, request)
        assert response.status_code == 403

    def test_should_return_data(self):
        user = User.objects.get(username='admin')
        request = HttpRequest()
        request.user = user
        request.user.id = user.id

        response = StatsView.get(StatsView, request)
        assert type(response) == Response
        assert response.status_code == 200
        assert type(response.data) == list
        assert type(response.data[0][0]) == str
        assert type(response.data[0][1]) == int
        assert len(response.data) > 1
