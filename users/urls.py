
from django.contrib import admin
from django.urls import path, include

from users.views import GoogleLogin


urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login')
]
