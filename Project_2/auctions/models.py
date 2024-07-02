from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return {self.email}
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    startBid = models.IntegerField()
    image = models.ImageField()
    
    def __str__(self):
        return f"{self.title}, Start Bid: {self.startBid}"
class Bids(models.Model):
    pass

class Comments(models.Model):
    pass
