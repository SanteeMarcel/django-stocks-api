# encoding: utf-8

from rest_framework import serializers

from api.models import UserRequestHistory


class UserRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequestHistory
        exclude = ['id', 'user']

class HistoryCounterSerializer(serializers.Serializer):
    name = serializers.CharField()
    times_requested = serializers.IntegerField()
