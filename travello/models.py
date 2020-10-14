from django.db import models

# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

class Flights(models.Model):
    name_f =models.CharField(max_length=100)
    city_name = models.ForeignKey(Destination, on_delete=models.CASCADE)
