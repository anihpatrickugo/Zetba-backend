
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import json

import logging
logger = logging.getLogger('my_app')

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

        # verify paystack transfer
        try:
            response = paystack_verify_transfer(refrence)
            if response['status'] == False:
                return Response({'error': 'Invalid reference'}, status=400)
            else:
                data = response['data']
                if data['status'] != 'success':
                    return Response({'error': 'Payment not successful'}, status=400)
                else:
                    # check if the payment already in database
                    top_up = TopUp.objects.filter(reference=refrence).first()
                    if top_up:
                        return Response({'error': 'Payment already exist in database'}, status=400)

                    verified_amount = int(data['amount']) / 100
                    top_up = TopUp.objects.create(user=user, amount=verified_amount, reference=refrence)
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

        except Exception as e:
            return Response({'error': 'Payment failed'}, status=400)





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
            logger.info("Paystack webhook received without signature header.")
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
            logger.error(f"Invalid JSON payload received by Paystack webhook: {raw_payload.decode()}")
            return Response({"detail": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST)

        # 5. Process the event (asynchronous processing recommended)
        event_type = payload.get('event')
        transaction_data = payload.get('data')

        reference = transaction_data.get('reference')
        amnt = transaction_data.get('amount')
        amount = amnt / 100 if amnt else None  # Convert to Naira
        customer_email = transaction_data.get('customer', {}).get('email')

        # check if the payment already in database
        withdrawal = Withdrawal.objects.get(reference=reference)
        if not withdrawal:
            logger.error("Withdrawal not found in database")
            return Response({'error': 'Withdawal does not exist in database'}, status=400)

        user = withdrawal.user

        if event_type == 'transfer.success':

            logger.info(
                f"Processing successful Paystack withdrawal for reference: {reference}, Amount: {amount}, Email: {customer_email}")
            # Your business logic here:

            # - Update order status in your database
            withdrawal.status = 'completed'  # Assuming you have a status field
            withdrawal.save()

            logger.info("Withdrawal Completed successful")

            # Create a notification for the user
            notification = Notifications.objects.create(
                user=user,
                title='Withdawal Successfully Completed',
                description=f'Your Withdrawal of {withdrawal.amount} naira has been completed successfuly.',
            )
            notification.save()


        elif event_type == 'transfer.failed':
            logger.info(
                f"Paystack withdrawal failed for reference: {reference}, Amount: {amount}, Email: {customer_email}")
            # Your business logic here:

            # - Update order status in your database
            withdrawal.status = 'failed'  # Assuming you have a status field
            withdrawal.save()

            # - refund user
            user.balance += amount
            user.save()

            logger.info("Withdrawal Failed")

            # Create a notification for the user
            notification = Notifications.objects.create(
                user=user,
                title='Withdawal Failed',
                description=f'Your Withdrawal of {withdrawal.amount} naira has Failed.',
            )
            notification.save()

        elif event_type == 'transfer.reversed':
            logger.info(
                f"Paystack withdrawal f for reference: {reference}, Amount: {amount}, Email: {customer_email} was reversed")
            # Your business logic here:

            # - Update order status in your database
            withdrawal.status = 'reversed'  # Assuming you have a status field
            withdrawal.save()

            # - refund user
            user.balance += amount
            user.save()

            logger.info("Withdrawal Reversed")

            # Create a notification for the user
            notification = Notifications.objects.create(
                user=user,
                title='Withdawal Reversed',
                description=f'Your Withdrawal of {withdrawal.amount} naira was reversed.',
            )
            notification.save()


        else:
            logger.error("Received unhandled Paystack event type: {event_type}")

        # 5. Acknowledge receipt
        return Response({"status": "success", "message": "Webhook received"}, status=status.HTTP_200_OK)
