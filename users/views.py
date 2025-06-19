
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import json



from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .models import Notifications, TopUp, Withdrawal
from .serializers import NotificationSerializer
from .payment import paystack_payment, paystack_verify_transfer
from .utils import generate_alphanumeric_code

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

class PaystackWebhookView(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]  # No permission checks required

    def post(self, request, *args, **kwargs):
        # 1. Get the raw request body
        raw_payload = request.body

        # 2. Extract signature header
        signature_header = request.headers.get('x-paystack-signature')

        # 3. VERIFY THE WEBHOOK SIGNATURE (CRITICAL!)
        # Implement your signature verification logic here using settings.PAYSTACK_SECRET_KEY
        if not signature_header:
            print("Paystack webhook received without signature header.")
            return Response({"detail": "Signature missing"}, status=status.HTTP_403_FORBIDDEN)

        # Example placeholder for actual verification
        # from django.conf import settings
        # if not self._verify_paystack_signature(raw_payload, signature_header, settings.PAYSTACK_SECRET_KEY):
        #     logger.warning(f"Invalid Paystack webhook signature for payload: {raw_payload.decode()}")
        #     return HttpResponseForbidden("Invalid signature")

        # 4. Parse the payload
        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError:
            print(f"Invalid JSON payload received by Paystack webhook: {raw_payload.decode()}")
            return Response({"detail": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST)

        # 5. Process the event (asynchronous processing recommended)
        event_type = payload.get('event')
        transaction_data = payload.get('data')

        if event_type == 'charge.success':
            reference = transaction_data.get('reference')
            amount = transaction_data.get('amount')
            customer_email = transaction_data.get('customer', {}).get('email')

            print(
                f"Processing successful Paystack payment for reference: {reference}, Amount: {amount}, Email: {customer_email}")
            # Your business logic here:

            # check if the payment already in database
            top_up = TopUp.objects.filter(reference=reference).first()
            if  not top_up:
                return Response({'error': 'Payment does not exist in database'}, status=400)

            verified_amount = int(amount) / 100
            top_up = TopUp.objects.get(amount=verified_amount, reference=reference)

            # - Update order status in your database
            top_up.status = 'completed'  # Assuming you have a status field
            top_up.save()

            # - Update user balance
            user = top_up.user
            user.balance += top_up.amount
            user.save()



            # Create a notification for the user
            notification = Notifications.objects.create(
                user=user,
                title='Top Up Successful',
                description=f'Your account has been credited with {top_up.amount} Naira.',
            )
            notification.save()

            # - Trigger other internal processes
            # Remember to make this idempotent!

        else:
            print(f"Received unhandled Paystack event type: {event_type}")

        # 5. Acknowledge receipt
        return Response({"status": "success", "message": "Webhook received"}, status=status.HTTP_200_OK)



class TopUpView(APIView):
    """
    Top up user balance
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        amount = request.data.get('amount')
        reference = request.data.get('reference')

        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=401)
        if not reference:
            return Response({'error': 'Reference is required'}, status=400)
        if not amount:
            return Response({'error': 'Amount is required'}, status=400)
        if amount <= 0:
            return Response({'error': 'Amount must be greater than 0'}, status=400)


        try:
            # check if the payment already in database
            top_up = TopUp.objects.filter(reference=reference).first()
            if top_up:
                return Response({'error': 'Payment already exist in database'}, status=400)

            verified_amount = amount / 100
            top_up = TopUp.objects.create(user=user, amount=amount, reference=reference)
            top_up.save()
            return Response({'message': 'Balance Created successfully'}, status=200)

        except Exception as e:
            return Response({'error': 'Topup failed'}, status=400)




class WithdrawalView(APIView):
    """
    Withdraw user balance
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        amount_str = request.data.get('amount')
        amount = int(amount_str) if amount_str else None
        recipient = request.data.get('recipient')

        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=401)
        if not recipient:
            return Response({'error': 'Recipient is required'}, status=400)
        if not amount:
            return Response({'error': 'Amount is required'}, status=400)
        if amount <= 0:
            return Response({'error': 'Amount must be greater than 0'}, status=400)
        if amount > user.balance:
            return Response({'error': 'Insufficient balance'}, status=400)

        # Generate a unique reference code
        reference = generate_alphanumeric_code()

        try:
            # Call the payment function
            response = paystack_payment(amount, recipient, reference)
        except Exception as e:
            return Response({'error': 'Payment failed'}, status=400)


        withdrawal = Withdrawal.objects.create(user=user, amount=amount, reference=reference)
        withdrawal.save()

        user.balance -= withdrawal.amount
        user.save()

        # Create a notification for the user
        notification = Notifications.objects.create(
            user=user,
            title='Withdrawal Successful',
            description=f'Your account has been debited with {withdrawal.amount} Naira.',
        )
        notification.save()

        return Response({'message': 'Balance updated successfully'}, status=200)