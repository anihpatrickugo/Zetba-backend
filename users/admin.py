from django.contrib import admin
from .models import CustomUser, Notifications, TopUp, Withdrawal

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'balance', 'photo', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'balance')
    list_filter = ('is_active', 'is_staff')
    ordering = ('first_name', 'last_name', 'email')

class CustomTopUpAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reference', 'date', 'time')
    search_fields = ('user__username', 'user__email', 'reference')
    list_filter = ('date',)
    ordering = ('-date', '-time')

class CustomWithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reference', 'date', 'time')
    search_fields = ('user__username', 'user__email', 'reference')
    list_filter = ('date',)
    ordering = ('-date', '-time')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notifications)
admin.site.register(TopUp, CustomTopUpAdmin)
admin.site.register(Withdrawal, CustomWithdrawalAdmin)
admin.site.site_header = 'Zetba Event Management System'


