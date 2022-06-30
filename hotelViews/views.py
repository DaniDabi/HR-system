from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import ListView, View, DeleteView
from hotel.models import Room, Reservation
from .forms import AvailabilityForm
from reservation_fucntions.get_available_rooms import get_available_rooms


# Create your views here.

def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    room_values = room_categories.values()
    room_list = []
    for category in room_categories:
        room_category = room_categories.get(category)
        room_url = reverse('hotelViews:RoomDetailView', kwargs={'category': category})

        room_list.append((room_category, room_url))
    context = {
        "room_list": room_list,
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
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)
        
        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)

            context = {
                'room_category': room_category,
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
                check_out=data['check_out'],
         )
            reservation.save()
            return redirect('hotelViews:ReservationList')
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')

class CancelReservationView(DeleteView):
    model = Reservation
    template_name = 'reservation_cancel_view.html'
    success_url = reverse_lazy('hotelViews:ReservationList')



        