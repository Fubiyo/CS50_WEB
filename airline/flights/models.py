from django.db import models

# Create your models here.
# ManyToMany field should be used to connect two models

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals") # use related names when having multiple of same objects as fields for another object?
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
    
class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers") # django automatically creates a reverse relation when u use a many to many field --
    # -- therefore technically although u cant see it. class Flight(models.Model) has a data field called like
    # passengers = models.ManyToManyField('Passenger', related_name='flights')

    def __str__(self):
            return f"{self.first} {self.last}"