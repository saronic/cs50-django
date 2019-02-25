from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger


# Create your views here.
def index(request):
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)


def flight(request, flight_id):
    try:
        the_flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("flight does not exist")
    context = {
        "flight": the_flight,
        "passengers": the_flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=the_flight).all()
    }
    return render(request, "flights/flight.html", context)


def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger_id"])
        passenger = Passenger.objects.get(pk=passenger_id)
        the_flight = Flight.objects.get(pk=flight_id)
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"msg": "No passenger"})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"msg": "No Flight"})

    passenger.flights.add(the_flight)

    return HttpResponseRedirect(reverse("flight"), (flight_id,))
