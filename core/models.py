from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# city and planet is unique
# integers are allowed in city and planet
class Location(models.Model):
    city = models.CharField(max_length=255)
    planet = models.CharField(max_length=255)
    capacity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['city','planet'], name='unique_location')
        ]

    def __str__(self):
        return self.city + ', ' + self.planet
    
    def serialize(self):
        return {
            "city" : self.city,
            "planet" : self.planet,
            "capacity" : self.capacity,
        }

    # returns total count of spaceships stationed at location
    def spaceship_stationed(self):
        return Spaceship.objects.filter(location=self.id).count()

# should name be unique?
class Spaceship(models.Model):
    status_choices = [
        ('decomissioned','decomissioned'),
        ('maintenance','maintenance'),
        ('operational','operational')
    ]
    
    name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(max_length=13, choices=status_choices, default='operational')

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "name": self.name,
            "model": self.model_name,
            "location": self.location.serialize(),
            "status": self.status,
        }