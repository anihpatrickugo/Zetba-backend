from  django.urls import path

from .views import ListEvent, DetailEvent, ListCreateEvent, RetrieveUpdateDestroyEvent, ListCreateTicket,TicketDetailView, ListBookMarks, CreateBookMarkAPIView, ListCategory


urlpatterns = [
    path('categories/', ListCategory.as_view(), name='category_list'),

    path('events/', ListEvent.as_view(), name='event_list'),
    path('events/<int:pk>/', DetailEvent.as_view(), name='event_detail'),

    path('my-events/', ListCreateEvent.as_view(), name='my-event_list'),
    path('my-events/<int:pk>/', RetrieveUpdateDestroyEvent.as_view(), name='my-event_detail'),

    path('tickets/', ListCreateTicket.as_view(), name='ticket_list'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),

    path('bookmarks/', ListBookMarks.as_view(), name='bookmarks_list'),
    path('bookmark/', CreateBookMarkAPIView.as_view(), name='bookmark'),

]