from django.contrib.auth import get_user_model
from  rest_framework import serializers
from .models import Category, Event, Ticket

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',  'photo')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')



class EventSerializer(serializers.ModelSerializer):
    creator = UserDetailSerializer(read_only=True)
    attendants = UserDetailSerializer(many=True, read_only=True)
    tickets_count = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Event
        fields = ('__all__')
        read_only_fields = ['creator', 'attendants']



    # return only the last 3 attendants
    def to_representation(self, instance):
        data = super().to_representation(instance)
        attendants = data['attendants']
        data['attendants'] = attendants[-3:]
        return data

    # get total number of tickets
    def get_tickets_count(self, instance):
        return instance.attendants.count()



class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ('__all__')
        read_only_fields = ['owner', 'price', 'total_price', 'event']

