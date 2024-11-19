from datetime import *
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser



from .models import Event, Ticket, Category
from .serializers import EventSerializer, TicketSerializer, CategorySerializer

# Create your views here.

class ListCategory(generics.ListAPIView):
    """
    List all categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        return Category.objects.order_by('name')



class ListEvent(generics.ListAPIView):

    """
      filter all events by upcoming and popular events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        # filter by upcoming events
        if self.request.query_params.get('upcoming'):
            return Event.objects.upcomming()

        # filter by popular events
        if self.request.query_params.get('popular'):
            return Event.objects.popular()

        return Event.objects.open()



class DetailEvent(generics.RetrieveAPIView):
    """
          Get event detail
        """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class ListCreateEvent(generics.ListCreateAPIView):

    # filter by my events
    """
    List all events created by user and create new event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        event = Event.objects.get(pk=serializer.data.get('id'))
        # check if event attendants is full
        if event.attendants.count() >= event.seats:
            raise PermissionDenied("Event is full")

        # check if user is already attending the event
        if self.request.user in event.attendants.all():
            raise PermissionDenied("You are already attending this event")

        serializer.save(creator=self.request.user)

        # add user to attendees
        event.attendants.add(self.request.user)
        event.save()

        return super().perform_create(serializer)

    def get_queryset(self):
        # check that user is authenticated
        if self.request.user.is_anonymous:
            raise PermissionDenied("You are not allowed")
        return Event.objects.filter(creator=self.request.user)


class RetrieveUpdateDestroyEvent(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def perform_update(self, serializer):
        # check that request.user is the creator of the event
        if serializer.instance.creator != self.request.user:
            raise PermissionDenied("You can't update this event")
        return super().perform_update(serializer)


    def perform_destroy(self, instance):
        # check that request.user is the creator of the event
        if instance.creator != self.request.user:
            raise PermissionDenied("You can't delete this event")
        super().perform_destroy(instance)
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)





class ListCreateTicket(generics.ListCreateAPIView):
    """
    List all tickets and create new ticket
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # get the event id from the serializer class
        event_id = self.request.data.get('event_id')
        print(event_id)
        # check if event exists
        event = Event.objects.get(pk=event_id)
        if not event:
            raise PermissionDenied("Event does not exist")
        # check if user has enough balance
        if self.request.user.balance < event.price:
            raise PermissionDenied("You don't have enough balance")
        
        #subtract price from use balance and add to event creator balance
        self.request.user.balance -= event.price
        self.request.user.save()
        event.creator.balance += event.price
        event.creator.save()

        # create ticket
        serializer.save(owner=self.request.user, event=event,
                               price=event.price, total_price=event.price)

        return super().perform_create(serializer)


    def get_queryset(self):
        # check that user is authenticated
        if self.request.user.is_anonymous:
            raise PermissionDenied("Please login first")
        return super().get_queryset().filter(owner=self.request.user)

    def get_object(self, pk):
        if self.request.user.is_anonymous:
            raise PermissionDenied("You are not allowed to see the ticket")
        ticket  = Ticket.objects.get(owner=self.request.user, pk=pk)

         # check if ticket exists
        if not ticket:
            raise PermissionDenied("You don't have a ticket")
        return ticket




    
