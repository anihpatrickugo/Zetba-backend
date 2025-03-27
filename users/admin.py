from django.contrib import admin
from .models import CustomUser, Notifications

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'balance', 'photo', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'balance')
    list_filter = ('is_active', 'is_staff')
    ordering = ('first_name', 'last_name', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notifications)
admin.site.site_header = 'Zetba Event Management System'


