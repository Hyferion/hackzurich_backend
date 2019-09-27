from django.db import models


class ArtOfTransport(models.Model):
    type = models.CharField(max_length=255)


class User(models.Model):
    name = models.CharField(max_length=255)


class UserInstance(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    lat = models.FloatField()
    lng = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)


class UserPreferences(models.Model):
    art_transport = models.ForeignKey(ArtOfTransport, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Room(models.Model):
    identifier = models.CharField(max_length=255, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, null=True, blank=True, related_name="members")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Meetup(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
