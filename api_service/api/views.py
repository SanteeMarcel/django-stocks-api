import logging
import requests
from rest_framework import generics, status as http_status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer, HistoryCounterSerializer
from pika_utils import get_stock_data
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

logger = logging.getLogger(__name__)


@extend_schema(
    examples=[
        OpenApiExample(
            name='stock_info',
            value={
                'name': 'APPLE',
                'symbol': 'AAPL.US',
                'open': '148.43',
                'low': '147.48',
                'high': '150.4',
                'close': '149.99'})],
    parameters=[
        OpenApiParameter(
            name='stock',
            type=str,
            location=OpenApiParameter.QUERY),
    ])
class StockView(APIView):
    """
    Endpoint to allow users to query stocks.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRequestHistorySerializer

    def get(self, request, *args, **kwargs):

        logger.info("StockView GET request received")

        stock_code = request.GET.get("stock", None)
        logger.info(f"Received stock_code: {stock_code}")

        if not stock_code:
            json_response = {"Error": "Stock code is empty"}
            response_status = http_status.HTTP_400_BAD_REQUEST
            logger.warning(
                f"Response JSON: {json_response}, Status: {response_status}")
            return Response(json_response, status=response_status)

        try:
            with requests.Session() as s:
                logger.info("Sending request to stock service")
                # url = "http://127.0.0.1:8001/stock"
                # params = {'stock_code': stock_code}
                # response = s.get(url, params=params)
                response = get_stock_data(stock_code, request.user.id)
                logger.info(
                    f"Received response from stock service: {response}")
                response, status = response['response'], response['status']
                if status == http_status.HTTP_200_OK:
                    all_data = response
                    logger.info(f"Received data: {all_data}")

                    logger.info(f"User: {request.user}")

                    serializer = self.serializer_class(all_data)
                    data = serializer.data

                    logger.info(f"Serialized data: {data}")

                    self.save_query_to_db(all_data, request.user)

                    return Response(data=data, status=http_status.HTTP_200_OK)
                else:
                    error = response["Error"]
                    logger.error(
                        f"Error response from stock service: {status}, {error}")
                    return Response(data={"Error": error}, status=status)

        except requests.RequestException as e:
            logger.error(f"RequestException occurred: {e}")
            return Response({'error': 'Unable to fetch stock information'},
                            status=http_status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return Response({'error': 'An unexpected error occurred'},
                            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_query_to_db(self, all_data, user):
        logger.info("Saving query to DB")
        try:
            user_request_history = UserRequestHistory(
                user=user,
                date=f"{all_data['date']}T{all_data['time']}Z",
                name=all_data['name'],
                symbol=all_data['symbol'],
                open=all_data['open'],
                high=all_data['high'],
                low=all_data['low'],
                close=all_data['close']
            )
            user_request_history.save()
            logger.info("Query saved to DB")
        except Exception as e:
            logger.error(f"Error saving query to DB: {e}")


@extend_schema(
    examples=[
        OpenApiExample(
            name='stock_info',
            value={
                'name': 'APPLE',
                'symbol': 'AAPL.US',
                'open': '148.43',
                'low': '147.48',
                'high': '150.4',
                'close': '149.99'})],
)
class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    serializer_class = UserRequestHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserRequestHistory.objects.filter(
            user=self.request.user).order_by('-id')

    def get(self, request, *args, **kwargs):
        logger.info("HistoryView GET request received")

        user_id = request.user.id
        logger.info(f"Current user ID: {user_id}")

        queryset = self.get_queryset()

        if not queryset.exists():
            logger.info("No history found for the user")
            return Response(status=http_status.HTTP_204_NO_CONTENT)

        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"Serialized user history data: {serializer.data}")

        return Response(data=serializer.data, status=http_status.HTTP_200_OK)


class StatsView(APIView):
    """
    Allows superusers to see which stocks are most queried.
    """
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: HistoryCounterSerializer(many=True),
        }
    )
    def get(self, request, *args, **kwargs):
        logger.info("StatsView GET request received")

        if not request.user.is_superuser:
            logger.warning("Unauthorized access attempt by non-superuser")
            return Response({"error": "You are not authorized to access this endpoint"},
                            status=http_status.HTTP_403_FORBIDDEN)

        top_stocks = UserRequestHistory.objects.values('name').annotate(
            times_requested=Count('name')).order_by('-times_requested')

        if not top_stocks:
            logger.info("No stock queries found")
            return Response(status=http_status.HTTP_204_NO_CONTENT)

        NO_OF_TOP_STOCKS = 5
        top_stocks = top_stocks[:NO_OF_TOP_STOCKS]
        logger.info(f"Top queried stocks: {top_stocks}")

        return Response(data=top_stocks, status=http_status.HTTP_200_OK)
