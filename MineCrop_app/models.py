from django.db import models
from django.utils import timezone

class Coordinate(models.Model):
    lng = models.CharField(max_length = 30, default=None, null=True)
    lat = models.CharField(max_length = 30, default=None, null=True)

    def __str__(self):
        return 'id:{2}, long={0}, lat={1}'.format(self.lng, self.lat, self.id)

class Tweet(models.Model):
    coordinates = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, default=None, null=True)
    userid = models.IntegerField()
    name = models.CharField(max_length = 200, default=None)
    tweet = models.CharField(max_length =  300, default=None)
    location = models.CharField(max_length = 200, default=None)
    date = models.DateTimeField(default=None, null=True)
    isTrained = models.NullBooleanField(default=None)

    class Meta:
        unique_together = ('userid', 'tweet',)

    def __str__(self):
        return self.tweet


class MinedTweet(models.Model):
    userid = models.IntegerField()
    username = models.CharField(max_length=200, default=None)
    tweet = models.CharField(max_length=300, default=None)
    date = models.DateTimeField(default=None)

    def __str__(self):
        return self.tweet

class TrainModel(models.Model):
    label = models.CharField(max_length = 300)
    tweet = models.CharField(max_length = 300)

    def __str__(self):
        return self.label

class StopWord(models.Model):
    words = models.CharField(max_length=180, default=None)

    def __str__(self):
        return self.words

class HashtagKeyword(models.Model):
    hashtag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.hashtag

class Address(models.Model):
    coordinates = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, default=None, null=True)
    city = models.CharField(max_length = 200)
    place = models.CharField(max_length = 200)

class Product(models.Model):
    name = models.CharField(max_length = 200)

class Farmer(models.Model):
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, default=None, null=True)
    name = models.CharField(max_length = 300)

class FarmerProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, default=None, null=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.SET_NULL, default=None, null=True)
    description = models.CharField(max_length = 300)
