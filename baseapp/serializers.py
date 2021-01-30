from abc import ABC
from rest_framework import serializers
from account.models import Balance
from django.contrib.auth.models import User
from . import models


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['user', 'card_number', 'status', 'balance']


class UserSerializer(serializers.ModelSerializer):
    balance = BalanceSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'balance']


class BikePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BikePlace
        fields = ['id', 'status', 'station', 'bike']
        read_only_fields = ['qrcode', 'station', 'id']


class StationSerializer(serializers.ModelSerializer):
    bike_place = BikePlaceSerializer(many=True, read_only=True)

    class Meta:
        model = models.Station
        fields = ['id', 'status', 'longitude', 'latitude', 'bike_place']


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bike
        fields = ['id', 'status', 'bike_place']


class UsernameField(serializers.RelatedField, ABC):
    queryset = User.objects.all()

    def to_representation(self, value):
        return value.username


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    read_only_fields = ['start', 'end']

    class Meta:
        model = models.Order
        fields = ['id', 'user', 'status', 'start', 'end', 'bike']
