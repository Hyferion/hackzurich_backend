from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)


class UserInstance(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    lat = models.FloatField()
    lng = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)


class UserPreferences(models.Model):