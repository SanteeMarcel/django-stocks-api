from django.http.request import HttpRequest
from django.test.testcases import TestCase
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList
from api.views import StockView, HistoryView, StatsView
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.request import Request
from django.core.management import call_command

json = {'Symbol': 'AAPL.US', 'Date': '2021-11-12', 'Time': '22:00:10', 'Open': '148.43',
        'High': '150.4', 'Low': '147.48', 'Close': '149.99', 'Volume': '63804008', 'Name': 'APPLE'}


class TestStockViewDB(TestCase):

    def test_should_save_query_to_db(self):
        user = User.objects.create_user(username='peter', password='spiderman')
        response = StockView.save_query_to_db(StockView, json, user)
        assert response is None

    def test_should_return_error_if_no_user(self):
        with self.assertRaises(IntegrityError):
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
            user = User.objects.create_user(
                username='peter', password='spiderman')
            altered_json = (lambda d: d.pop('Symbol') and d)(json.copy())
            response = StockView.save_query_to_db(
                StockView, altered_json, user)
            assert response is None

    def test_should_return_error_if_no_date(self):
        with self.assertRaises(KeyError):
            user = User.objects.create_user(
                username='peter', password='spiderman')
            altered_json = (lambda d: d.pop('Date') and d)(json.copy())
            response = StockView.save_query_to_db(
                StockView, altered_json, user)
            assert response is None

    def test_should_return_error_if_no_time(self):
        with self.assertRaises(KeyError):
            user = User.objects.create_user(
                username='peter', password='spiderman')
            altered_json = (lambda d: d.pop('Time') and d)(json.copy())
            response = StockView.save_query_to_db(
                StockView, altered_json, user)
            assert response is None

    def test_should_return_error_if_no_open(self):
        with self.assertRaises(KeyError):
            user = User.objects.create_user(
                username='peter', password='spiderman')
            altered_json = (lambda d: d.pop('Open') and d)(json.copy())
            response = StockView.save_query_to_db(
                StockView, altered_json, user)
            assert response is None

    def test_should_return_error_if_no_high(self):
        with self.assertRaises(KeyError):
            user = User.objects.create_user(
                username='peter', password='spiderman')
            altered_json = (lambda d: d.pop('High') and d)(json.copy())
            response = StockView.save_query_to_db(
                StockView, altered_json, user)
            assert response is None

    def test_should_return_error_if_no_low(self):
        with self.assertRaises(KeyError):
            user = User.objects.create_user(
                username='peter', password='spiderman')
            altered_json = (lambda d: d.pop('Low') and d)(json.copy())
            response = StockView.save_query_to_db(
                StockView, altered_json, user)
            assert response is None

    def test_should_return_error_if_no_close(self):
        with self.assertRaises(KeyError):
            user = User.objects.create_user(
                username='peter', password='spiderman')
            altered_json = (lambda d: d.pop('Close') and d)(json.copy())
            response = StockView.save_query_to_db(
                StockView, altered_json, user)
            assert response is None

    def test_should_return_error_if_no_name(self):
        with self.assertRaises(KeyError):
            user = User.objects.create_user(
                username='peter', password='spiderman')
            altered_json = (lambda d: d.pop('Name') and d)(json.copy())
            response = StockView.save_query_to_db(
                StockView, altered_json, user)
            assert response is None


class TestStockViewFiltering(TestCase):

    def test_should_filter_data(self):
        data = StockView.filter_relevant_data(StockView, json)
        assert data == {'name': 'APPLE', 'symbol': 'AAPL.US',
                        'open': '148.43', 'low': '147.48', 'high': '150.4', 'close': '149.99'}

    def test_should_return_error_if_no_name(self):
        with self.assertRaises(KeyError):
            altered_json = (lambda d: d.pop('Name') and d)(json.copy())
            data = StockView.filter_relevant_data(StockView, altered_json)
            assert data is None

    def test_should_return_error_if_no_symbol(self):
        with self.assertRaises(KeyError):
            altered_json = (lambda d: d.pop('Symbol') and d)(json.copy())
            data = StockView.filter_relevant_data(StockView, altered_json)
            assert data is None

    def test_should_return_error_if_no_open(self):
        with self.assertRaises(KeyError):
            altered_json = (lambda d: d.pop('Open') and d)(json.copy())
            data = StockView.filter_relevant_data(StockView, altered_json)
            assert data is None

    def test_should_return_error_if_no_high(self):
        with self.assertRaises(KeyError):
            altered_json = (lambda d: d.pop('High') and d)(json.copy())
            data = StockView.filter_relevant_data(StockView, altered_json)
            assert data is None

    def test_should_return_error_if_no_low(self):
        with self.assertRaises(KeyError):
            altered_json = (lambda d: d.pop('Low') and d)(json.copy())
            data = StockView.filter_relevant_data(StockView, altered_json)
            assert data is None

    def test_should_return_error_if_no_close(self):
        with self.assertRaises(KeyError):
            altered_json = (lambda d: d.pop('Close') and d)(json.copy())
            data = StockView.filter_relevant_data(StockView, altered_json)
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
