from django.contrib import admin
from .models import Event , Ticket

# Register your models here.

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name','date')
    inlines = [TicketInline]
