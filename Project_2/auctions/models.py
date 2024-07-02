from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    startBid = models.IntegerField()
    image = models.ImageField()
class Bids(models.Model):
    pass

class Comments(models.Model):
    pass
