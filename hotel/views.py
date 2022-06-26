import imp
from multiprocessing import context
from unicodedata import category
from urllib import request
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from .models import Room, Reservation
from .forms import AvailabilityForm
from hotel.reservation_fucntions.availability import check_availability
from hotel.reservation_fucntions.get_room_cat_url_list import get_room_cat_url_list
from hotel.reservation_fucntions.get_room_category_human_format import get_room_category_human_format
from hotel.reservation_fucntions.get_available_rooms import get_available_rooms


# Create your views here.

def RoomListView(request):
    room_category_url_list = get_room_cat_url_list()
    context={
        "room_list": get_room_cat_url_list,
    }
    return render(request, 'room_list_view.html', context)

class ReservationList(ListView):
    model = Reservation
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            reservation_list = Reservation.objects.all()
            return reservation_list
        else:
            reservation_list = Reservation.objects.filter(user=self.request.user)
            return reservation_list
        

class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        human_format_room_category = get_room_category_human_format(category)
        form = AvailabilityForm()
        if human_format_room_category is not None:
            context = {
                'room_category': human_format_room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')
        
    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

        available_rooms = get_available_rooms(category, data['check_in'], data['check_out'] )

        if available_rooms is not None:
            room = available_rooms[0]
            reservation = Reservation.objects.create(
                user=request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
         )
            reservation.save()
            return HttpResponse(reservation)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')

class CancelReservationView(DeleteView):
    model = Reservation
    template_name = 'reservation_cancel_view.html'
    success_url = reverse_lazy('hotel:ReservationList')

        