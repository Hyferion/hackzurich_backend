import random
import string

from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from meetup.models import User, Room, UserInstance
from meetup.serializers import UserSerializer, RoomSerializer, UserInstanceSerializer


class UserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserInstanceList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = UserInstance.objects.all()
    serializer_class = UserInstanceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInstance.objects.all()
    serializer_class = UserInstanceSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def randomStringDigits(stringLength=5):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


class RoomList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            querysetowner = Room.objects.filter(creator=user)
            querysetmember = Room.objects.filter(members=user)
            return querysetowner | querysetmember
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        playlistIdentifier = randomStringDigits()

        serializer.is_valid(raise_exception=True)
        serializer.save(identifier=playlistIdentifier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['POST'])
def add_member_to_room(request):
    if request.method == 'POST':
        try:
            user = request.data.get('user')
            identifier = request.data.get('room')
        except AttributeError:
            return Response(status.HTTP_400_BAD_REQUEST)

        room = Room.objects.get(identifier=identifier)
        user = User.objects.get(id=user)

        room.members.add(user)
        room.save()

        return Response(status.HTTP_200_OK)
