from django.db import models
from .managers import EventManager

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=100)
    location_latitude = models.FloatField()
    location_longitude = models.FloatField()
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField()
    photo = models.ImageField(upload_to='events')
    seats = models.IntegerField()
    attendants = models.ManyToManyField('users.CustomUser', through='Ticket', related_name='events')
    creator = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)


    objects = EventManager()

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    price = models.FloatField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.owner.username} - {self.event.title}"