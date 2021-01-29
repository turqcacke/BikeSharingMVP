from . import models
from django.core.exceptions import FieldError
from . import serializers
from .rest_exceptions import AlreadyExist, InvalidParam, AlreadyOccupied, DoesntExists
from .utils import make_valid_dict
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from .models import OrderStatuses
from rest_framework import permissions



class UserList(ListAPIView, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'id'


class BikeList(ListAPIView, CreateModelMixin):
    serializer_class = serializers.BikeSerializer
    lookup_field = 'id'

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)

    def get_queryset(self):
        queryset = models.Bike.objects.all()
        params = make_valid_dict(self.request.query_params)
        if params:
            try:
                return queryset.filter(**params)
            except (FieldError, ValueError):
                raise InvalidParam
        return queryset


class BikeDetail(RetrieveAPIView, UpdateModelMixin):
    queryset = models.Bike.objects.all()
    serializer_class = serializers.BikeSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class BikePlaceList(ListCreateAPIView):
    serializer_class = serializers.BikePlaceSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = models.BikePlace.objects.all()
        params = make_valid_dict(self.request.query_params)
        if params:
            try:
                return queryset.filter(**params)
            except (FieldError, ValueError):
                raise InvalidParam
        return queryset


class BikePlaceDetail(RetrieveAPIView, UpdateModelMixin):
    queryset = models.BikePlace.objects.all()
    serializer_class = serializers.BikePlaceSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        bike_place_ser = serializers.BikePlaceSerializer(data=request.data)
        bike_place_ser.is_valid()
        try:
            bike_place = models.BikePlace.objects.get(id=bike_place_ser.data['id'])
        except models.BikePlace.DoesNotExist:
            raise DoesntExists
        print(bike_place_ser.data)
        if bike_place_ser.data['bike'] is not None:
            if bike_place.status != 1:
                raise AlreadyOccupied
            try:
                order = models.Order.active.get(bike__id=bike_place_ser.data['bike'])
                order.status = OrderStatuses.FINISHED
                order.save()
            except models.Order.DoesNotExist:
                pass
        return self.update(request, *args, **kwargs)


class OrderList(ListCreateAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = models.Order.objects.all()
        params = make_valid_dict(self.request.query_params)

        if self.request.query_params:
            try:
                return queryset.filter(**params)
            except (FieldError, ValueError):
                raise InvalidParam
        return queryset

    def post(self, *args, **kwargs):
        order = serializers.OrderSerializer(data=self.request.data)
        if order.is_valid():
            print(order.data)
            if not models.Order.objects.all().filter(status__lt=models.OrderStatuses.FINISHED,
                                                     bike__id=order.data['bike'],
                                                     user=self.request.user):
                return self.create(*args, **kwargs)
        raise AlreadyExist


class StationList(ListAPIView):
    serializer_class = serializers.StationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = models.Station.objects.all()
        params = make_valid_dict(self.request.query_params)
        if params:
            try:
                return queryset.filter(**params)
            except (FieldError, ValueError):
                raise InvalidParam
        return queryset
