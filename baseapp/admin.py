from django.contrib import admin
from . import models


@admin.register(models.Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'bike_place')


@admin.register(models.BikePlace)
class BikePlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'bike', 'station', 'qrcode')


@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'get_bike_places')

    def get_bike_places(self, obj):
        return ''.join([str(bp) + ', ' if bp != obj.bike_place.all()[len(obj.bike_place.all()) - 1]
                        else str(bp) for bp in obj.bike_place.all()])


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'user', 'start', 'end', 'bike')
