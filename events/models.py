from django.db import models
from .managers import EventManager

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=100)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField()
    photo = models.ImageField(upload_to='events')
    seats = models.IntegerField()
    attendants = models.ManyToManyField('users.CustomUser', through='Ticket', related_name='events')
    creator = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)


    # used by algolia search

    def get_photo(self):
        """Returns the absolute URL of the event photo."""
        if self.photo:
            return self.photo.url
        # You can return a default placeholder image URL if no photo exists
        return "https://yourdomain.com/static/placeholder.png"

    def get_category_name(self):
        return self.category.name

    def get_creator_name(self):
        return self.creator.username

    def get_date(self):
        return self.date.strftime('%Y-%m-%d') if self.date else None

    def get_time(self):
        return self.time.strftime('%H:%M:%S') if self.time else None




class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    price = models.FloatField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.owner.username} - {self.event.title}"


class BookMark(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


