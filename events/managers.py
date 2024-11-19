from datetime import *
from django.utils import timezone
from django.db import models

class EventManager(models.Manager):
    def upcomming(self):
        return super().get_queryset().filter(date__gte=timezone.now()).order_by('date__year', 'date__month', 'date__day', 'time')

    def popular(self):
        return super().get_queryset().filter(date__gte=timezone.now()).order_by('-attendants').distinct()

    def open(self):
        return super().get_queryset().filter(date__gte=timezone.now()).order_by('-id')