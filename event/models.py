from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField( max_length=50)
    location = models.CharField( max_length=50)
    date = models.DateTimeField()
    image = models.FileField(upload_to='event_image', null=True)
    guest = models.TextField()
    
   
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_name = models.CharField(max_length=50)
    price = models.IntegerField()
    