from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserList.as_view(), name='user_list'),
    path('user/<str:username>/', views.UserDetail.as_view(), name='user_detail'),
    path('bike/', views.BikeList.as_view(), name='bike_list'),
    path('bike/<int:id>/', views.BikeDetail().as_view(), name='bike_detail'),
    path('bike_place/', views.BikePlaceList().as_view(), name='bike_place_list'),
    path('bike_place/<int:id>/', views.BikePlaceDetail().as_view(), name='bike_place_detail'),
    path('order/', views.OrderList.as_view(), name='order_list'),
    path('station/', views.StationList.as_view(), name='stations_list')
]
