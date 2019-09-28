from rest_framework import serializers

from meetup.models import User, UserInstance, Room, Meetup


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


class UserInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInstance
        fields = ('userid', 'lat', 'lng', 'last_update')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('identifier', 'name', 'owner', 'created_at', 'members')
        read_only_fields = ('identifier',)


class MeetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meetup
        fields = ('lat', 'lng', 'name', 'type')
