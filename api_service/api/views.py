# encoding: utf-8

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer
from django.db.models import Count

import requests


class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRequestHistorySerializer

    def get(self, request, *args, **kwargs):

        stock_code = request.GET.get("stock_code", "EmptyError")

        if stock_code == "EmptyError":
            json = {"Error": "Stock code is empty"}
            status = 204
            return Response(json, status)

        try:
            with requests.Session() as s:

                response = requests.request(
                    "GET", "http://127.0.0.1:8001/stock", data={'stock_code': f'{stock_code}'})
                if response.status_code == 200:

                    allData = response.json()

                    print(type(request.user))

                    self.save_query_to_db(allData, request.user)

                    serializer = self.serializer_class(allData)

                    data = serializer.data

                    return Response(data=data, status=200)
                else:
                    return Response(data=response.json(), status=response.status_code)

        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def save_query_to_db(self, allData, user):
        userRequestHistory = UserRequestHistory()
        userRequestHistory.user = user
        userRequestHistory.date = allData["Date"] + \
            "T" + allData["Time"] + "Z"
        userRequestHistory.name = allData["Name"]
        userRequestHistory.symbol = allData["Symbol"]
        userRequestHistory.open = allData["Open"]
        userRequestHistory.high = allData["High"]
        userRequestHistory.low = allData["Low"]
        userRequestHistory.close = allData["Close"]
        userRequestHistory.save()


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = self.queryset.filter(user_id=user_id)[::-1]
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=200)


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    permission_classes = (IsAuthenticated,)
    queryset = UserRequestHistory.objects.all()

    def get(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return Response({"error": "You are not authorized to access this endpoint"}, status=403)

        queryset = self.queryset.values('name').annotate(
            count=Count('name')).order_by('-count')[:5]

        return Response(data=queryset, status=200)
