from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, Mock
from .models import UserRequestHistory
from requests import RequestException

class StockViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('stock-view')

    @patch('requests.Session.get')
    def test_get_stock_success(self, mock_get):
        mock_response = Mock()
        expected_data = {
            "date": "2023-07-12",
            "time": "12:34:56",
            "name": "Test Stock",
            "symbol": "TST",
            "open": 100.0,
            "high": 110.0,
            "low": 90.0,
            "close": 105.0
        }
        mock_response.json.return_value = expected_data
        mock_response.status_code = status.HTTP_200_OK
        mock_get.return_value = mock_response

        response = self.client.get(self.url, {'stock': 'TST'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'TST')

    @patch('requests.Session.get')
    def test_get_stock_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"detail": "Not found"}
        mock_response.status_code = status.HTTP_404_NOT_FOUND
        mock_get.return_value = mock_response

        response = self.client.get(self.url, {'stock': 'INVALID'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found')

    def test_get_stock_no_code(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Error'], 'Stock code is empty')

    @patch('requests.Session.get')
    def test_get_stock_service_unavailable(self, mock_get):
        mock_get.side_effect = RequestException

        response = self.client.get(self.url, {'stock': 'TST'})

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['error'], 'Unable to fetch stock information')

class HistoryViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('history-view')

    def test_get_history_no_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_history_with_data(self):
        UserRequestHistory.objects.create(
            user=self.user,
            date="2023-07-12T12:34:56Z",
            name="Test Stock",
            symbol="TST",
            open=100.0,
            high=110.0,
            low=90.0,
            close=105.0
        )
        
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['symbol'], 'TST')

class StatsViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.superuser = User.objects.create_superuser(username='myadmin', password='adminpassword')
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.url = reverse('stats-view')

    def test_stats_unauthorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'You are not authorized to access this endpoint')

    def test_stats_no_data(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_stats_with_data(self):
        UserRequestHistory.objects.create(
            user=self.user,
            date="2023-07-12T12:34:56Z",
            name="Test Stock",
            symbol="TST",
            open=100.0,
            high=110.0,
            low=90.0,
            close=105.0
        )
        
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Stock')
