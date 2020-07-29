from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=64, blank=True)
    starting_bid = models.FloatField()
    image = models.URLField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField()
    subscribers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title} (id: {self.id})"


class Bid(models.Model):
    value = models.IntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.value}"


class Comment(models.Model):
    text = models.CharField(max_length=512)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user}: {self.text} – {self.listing.title}"
