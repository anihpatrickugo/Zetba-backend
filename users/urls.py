from django.views.decorators.csrf import csrf_exempt
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import GoogleLogin, NotificationView, TopUpView, WithdrawalView, PaystackWebhookView



urlpatterns = [

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),

    path('notifications/', NotificationView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/', NotificationView.as_view(), name='notification_detail'),

    path('paystack-webhook/', csrf_exempt(PaystackWebhookView.as_view()), name='paystack_webhook'),
    # path('topup/', TopUpView.as_view(), name='topup'),
    path('withdrawal/', WithdrawalView.as_view(), name='withdrawal')



]
