from django.test import TestCase
from django.utils import timezone
import datetime
from events.models import Event, Category
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.


class EventTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="ugo", email="ugocee@gmail.com")
        category = Category.objects.create(name="Music")
        Event.objects.create(title="Music Concert", description="Music Concert", category=category,
                             location_name="Lagos", location_latitude=6.5244, location_longitude=3.3792,
                             date="2021-06-01", time="12:00:00", price=2000, photo="events/music.jpg",
                                seats=200, creator=user)

    def test_event_exist(self):
        event = Event.objects.get(title="Music Concert")
        self.assertEqual(event.title, "Music Concert")
        self.assertEqual(event.description, "Music Concert")
        self.assertEqual(event.category.name, "Music")
        self.assertEqual(event.location_name, "Lagos")
        self.assertEqual(event.location_latitude, 6.5244)
        self.assertEqual(event.location_longitude, 3.3792)
        self.assertEqual(event.date, datetime.date(2021, 6, 1))
        self.assertEqual(event.time, datetime.time(12, 0))
        self.assertEqual(event.price, 2000)
        self.assertEqual(event.photo, "events/music.jpg")
        self.assertEqual(event.seats, 200)
        self.assertEqual(event.creator.username, "ugo")


    def test_events_count(self):
        events = Event.objects.all()
        self.assertEqual(events.count(), 1)

