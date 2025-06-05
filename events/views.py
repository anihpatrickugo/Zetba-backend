from datetime import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser


from .models import Event, Ticket, Category, BookMark
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
        # print(self.request.data.get("photo"))
        category = get_object_or_404(Category, name=self.request.data.get('category'))
        serializer.save(creator=self.request.user, category=category)




    def get_queryset(self):
        # check that user is authenticated
        if self.request.user.is_anonymous:
            raise PermissionDenied("You are not allowed")
        return Event.objects.filter(creator=self.request.user).order_by('-id')


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

        # check if event exists
        event = Event.objects.get(pk=event_id)
        if not event:
            raise PermissionDenied("Event does not exist")

        # check if event attendants is full
        if event.attendants.count() >= event.seats:
            raise PermissionDenied("Event is full")

        # check if user is already attending the event
        if self.request.user in event.attendants.all():
            raise PermissionDenied("You are already attending this event")


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


class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'


    def get_object(self):
        # check that user is authenticated
        if self.request.user.is_anonymous:
            raise PermissionDenied("You are not allowed to see the ticket")

        # check if ticket exists
        ticket = Ticket.objects.get(owner=self.request.user, pk=self.kwargs['pk'])
        if not ticket:
            raise PermissionDenied("Ticket does not exist")
        return ticket

class ListBookMarks(generics.ListAPIView):
    """
    List all bookmarks and create new bookmark
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # check that user is authenticated
        if self.request.user.is_anonymous:
            raise PermissionDenied("You are not allowed to see the bookmarks")

        #fetch all bookmarked event
        bookmarks = Event.objects.filter(bookmark__user=self.request.user)
        return bookmarks





class CreateBookMarkAPIView(APIView):
    def post(self, request, *args, **kwargs):
        """Handles POST requests and prints the data to the terminal."""

        try:
            # Attempt to access request.data (DRF's parsed data)
            event_pk = request.data.get("event")

            # get event
            event = Event.objects.get(pk=event_pk)

            # fetch all bookmarked event
            bookmark = BookMark.objects.filter(user=self.request.user, event=event)

            if not bookmark:
                # add it to bookmarks
                BookMark.objects.create(user=self.request.user, event=event)
                return Response({"message": "Bookmark successfully added"}, status=status.HTTP_201_CREATED)
            else:
                # remove it from bookmarks
                bookmark.delete()
                return Response({"message": "Bookmark successfully removed"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response("Error processing data", status=status.HTTP_400_BAD_REQUEST)


