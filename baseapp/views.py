from . import models
from django.core.exceptions import FieldError
from . import serializers
from .rest_exceptions import AlreadyExist, InvalidParam, AlreadyOccupied, DoesntExists, Forbidden, NotEnoughMoney
from .utils import make_valid_dict
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from .models import OrderStatuses
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.conf import settings
from account.models import Status
from .permission import IsSuperUser


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]


class UserDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(balance__card_number=username)
        except ValueError:
            user = User.objects.get(username=username)
        if self.request.user.username == user.username:
            ser = serializers.UserSerializer(user)
            return Response(ser.data)
        raise Forbidden(detail='Invalid username.')


class BikeList(ListAPIView, CreateModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BikeSerializer
    lookup_field = 'id'

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)

    def get_queryset(self):
        queryset = models.Bike.objects.all()
        params = make_valid_dict(self.request.query_params)
        if params:
            try:
                queryset = queryset.filter(**params)
                if not queryset:
                    raise FieldError
            except (FieldError, ValueError):
                raise InvalidParam
        return queryset


class BikeDetail(RetrieveAPIView, UpdateModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Bike.objects.all()
    serializer_class = serializers.BikeSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class BikePlaceList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BikePlaceSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = models.BikePlace.objects.all()
        params = make_valid_dict(self.request.query_params)
        if params:
            try:
                queryset = queryset.filter(**params)
                if not queryset:
                    raise FieldError
            except (FieldError, ValueError):
                raise InvalidParam
        return queryset


class BikePlaceDetail(RetrieveUpdateAPIView):
    queryset = models.BikePlace.objects.all()
    serializer_class = serializers.BikePlaceSerializer
    lookup_field = 'id'

    def put(self, request, id, *args, **kwargs):
        bike_place_data = request.data
        try:
            bike_place = models.BikePlace.objects.get(id=id)
        except models.BikePlace.DoesNotExist:
            raise DoesntExists
        if bike_place_data['bike'] is not None:
            if bike_place.status != 1:
                raise AlreadyOccupied
            try:
                order = models.Order.active.get(bike__id=bike_place_data['bike'])
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
        if not isinstance(self.request.user, AnonymousUser):
            queryset = queryset.filter(user=self.request.user)
        if self.request.query_params:
            try:
                queryset = queryset.filter(**params)
                if not queryset:
                    raise FieldError
            except (FieldError, ValueError):
                raise InvalidParam
        return queryset

    def post(self, *args, **kwargs):
        order = serializers.OrderSerializer(data=self.request.data)
        if order.is_valid():
            try:
                models.Bike.objects.get(bike__id=order.data['bike'])
            except (models.Bike.DoesNotExist, NameError):
                raise DoesntExists
            if not models.Order.objects.all().filter(status__lt=models.OrderStatuses.FINISHED,
                                                     bike__id=order.data['bike']) and \
                    not models.Order.objects.all().filter(status__lt=models.OrderStatuses.FINISHED,
                                                          user=self.request.user):
                if self.request.user.balance.balance > settings.MINIMUM_BALANCE and \
                        self.request.user.balance.status != Status.BLOCKED:
                    return self.create(*args, **kwargs)
                raise NotEnoughMoney
            raise AlreadyExist
        raise InvalidParam


class StationList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.StationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = models.Station.objects.all()
        params = make_valid_dict(self.request.query_params)
        if params:
            try:
                queryset = queryset.filter(**params)
                if not queryset:
                    raise FieldError
            except (FieldError, ValueError):
                raise InvalidParam
        return queryset
