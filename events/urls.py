from  django.urls import path

from .views import ListEvent, ListCreateEvent, RetrieveUpdateDestroyEvent, ListCreateTicket, ListCategory


urlpatterns = [
    path('categories/', ListCategory.as_view(), name='category_list'),

    path('events/', ListEvent.as_view(), name='event_list'),

    path('my-events/', ListCreateEvent.as_view(), name='my-event_list'),
    path('my-events/<int:pk>/', RetrieveUpdateDestroyEvent.as_view(), name='my-event_detail'),

    path('tickets/', ListCreateTicket.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', ListCreateTicket.as_view(), name='ticket_detail'),
]