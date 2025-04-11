
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from .models import Notifications
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()

class CustomUserDetailsSerializer(UserDetailsSerializer):
    phone = PhoneNumberField(region="NG")
    balance = serializers.IntegerField(read_only=True)
    photo = serializers.ImageField(read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('phone', 'balance', 'photo',)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'
