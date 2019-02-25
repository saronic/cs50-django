from django.shortcuts import render
from django.test import TestCase, Client
from .models import Airport, Flight


class ModelsTestCase(TestCase):
    def setUp(self):
        a1 = Airport.objects.create(code="AA", city="City A")
        a2 = Airport.objects.create(code="BB", city="City B")

        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-300)

    def test_departure_count(self):
        a = Airport.objects.get(code="AA")
        self.assertTrue(a.departures.count() == 3)

    def test_is_valid_flight(self):
        a1 = Airport.objects.get(code="AA")
        a2 = Airport.objects.get(code="BB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight(self):
        a = Airport.objects.get(code="AA")
        f = Flight.objects.get(origin=a, destination=a)
        self.assertFalse(f.is_valid_flight())

    def test_duration(self):
        f = Flight.objects.get(duration=-300)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context["flights"].count() == 3)

    def valid_flight_page(self):
        ao = Airport.objects.get(code="AA")
        f = Flight.objects.get(origin=ao, destination=ao)
        c = Client()
        response = c.get(f"/{f.id}")
        self.assertTrue(response.status_code == 200)
