"""
URL configuration for testproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy

from django.views.generic.base import RedirectView

from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularJSONAPIView




urlpatterns = [
    path("admin/", admin.site.urls),
    path('user/', include('users.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('swagger-ui'), permanent=True), name='index_redirect'),
    path('', include('events.urls')),
    path('api/schema/json/', SpectacularJSONAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)