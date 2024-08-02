from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.email}"
    
class Listing(models.Model):
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=64)
    description = models.TextField()
    startBid = models.IntegerField()
    image = models.ImageField(blank=True)
    watchlist = models.BooleanField(default=False)
    open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title}, Start Bid: {self.startBid}, auctioneer: {self.auctioneer}"
class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
        

class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

