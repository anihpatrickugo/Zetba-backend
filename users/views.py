from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .models import Notifications, TopUp, Withdrawal
from .serializers import NotificationSerializer

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000" # your callback url
    client_class = OAuth2Client


class NotificationView(APIView, ListModelMixin, RetrieveModelMixin):
    """
    List all notifications
    """
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer



    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        notifications = Notifications.objects.filter(user=request.user).order_by('-time')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class TopUpView(APIView):
    """
    Top up user balance
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        amount = request.data.get('amount')
        refrence = request.data.get('reference')

        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=401)
        if not refrence:
            return Response({'error': 'Reference is required'}, status=400)
        if not amount:
            return Response({'error': 'Amount is required'}, status=400)
        if amount <= 0:
            return Response({'error': 'Amount must be greater than 0'}, status=400)

        top_up = TopUp.objects.create(user=user, amount=amount, reference=refrence)
        top_up.save()

        user.balance += top_up.amount
        user.save()

        # Create a notification for the user
        notification = Notifications.objects.create(
            user=user,
            title='Top Up Successful',
            description=f'Your account has been credited with {top_up.amount} Naira.',
        )
        notification.save()

        return Response({'message': 'Balance updated successfully'}, status=200)

