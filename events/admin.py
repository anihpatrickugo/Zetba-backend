from django.contrib import admin
from .models import Event, Category, Ticket, BookMark

# Register your models here.



class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location_name', 'date', 'time', 'price', 'seats', 'creator')
    list_filter = ('category', 'location_name', 'date', 'time', 'price', 'seats', 'creator')

class TicketAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(BookMark)

