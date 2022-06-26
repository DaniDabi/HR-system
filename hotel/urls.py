
from django.urls import path
from .views import RoomListView, ReservationList , RoomDetailView, CancelReservationView
app_name = 'hotel'

urlpatterns= [
    path('', RoomListView, name='RoomListView'),
    path('reservation_list/', ReservationList.as_view(), name='ReservationList'),
    path('room/<category>', RoomDetailView.as_view(), name= 'RoomDetailView'),
    path('reservation/cancel/<pk>', CancelReservationView.as_view(), name='CancelReservationView'),
]