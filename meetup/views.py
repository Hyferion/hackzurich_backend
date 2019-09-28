import random
import string

from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from meetup.models import User, Room, UserInstance, Meetup
from meetup.serializers import UserSerializer, RoomSerializer, UserInstanceSerializer, MeetupSerializer

from meetup.logic.traveltime_client import get_overlap
from meetup.logic.polygon_maths import fit_circle
from meetup.logic.gmaps_client import get_nearby_places


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
            querysetowner = Room.objects.filter(owner=user)
            querysetmember = Room.objects.filter(members=user)
            return querysetowner | querysetmember
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        roomidentifier = randomStringDigits()

        serializer.is_valid(raise_exception=True)
        serializer.save(identifier=roomidentifier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MeetupList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = MeetupSerializer

    def get_queryset(self):
        queryset = Meetup.objects.all()
        room = self.request.query_params.get('room', None)
        if room is not None:
            querysetroom = Meetup.objects.filter(room_id=room)
            return querysetroom
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@api_view(['POST'])
def add_member_to_room(request):
    if request.method == 'POST':
        try:
            user = request.data.get('user')
            identifier = request.data.get('room')
        except AttributeError:
            return Response(status.HTTP_400_BAD_REQUEST)

        room = Room.objects.get(identifier=identifier)
        user = UserInstance.objects.get(userid=user)

        room.members.add(user)
        room.save()

        return Response(status.HTTP_200_OK)


def format_members(members):
    departure_searches = []
    for member in members:
        departure_searches.append({'id': str(member.userid_id),
                                   'coords': {
                                       'lat': member.lat,
                                       'lng': member.lng
                                   },
                                   'transportation': {"type": 'public_transport'},
                                   'departure_time': '2019-09-27T08:00:00Z',
                                   'travel_time': 900})
    return departure_searches


def reverse_coord_order(coord):
    return [coord[1], coord[0]]


@api_view(['POST'])
def submit_meetup(request):
    if request.method == 'POST':
        try:
            category = request.data.get('category')
            # time = request.data.get('time')
            room_identifier = request.data.get('room')
        except AttributeError:
            return Response(status.HTTP_400_BAD_REQUEST)

        # get room object
        room = Room.objects.get(identifier=room_identifier)

        # get all members of room
        members = room.members.all()

        # put members' locations in correct format
        departure_searches = format_members(members)

        # find overlapping area
        overlap_coords = get_overlap(departure_searches)

        # fit circle to overlap region
        centroid, radius = fit_circle(overlap_coords)

        # get list of POIs ranked by importance
        places = get_nearby_places(
            reverse_coord_order(centroid), radius, category)

        # pick the top place
        place = places['results'][0]

        # create meetup
        location = place['geometry']['location']

        r = Room.objects.get(identifier=room_identifier)

        meetup = Meetup.objects.create(room_id=r,
                                       lat=location['lat'], lng=location['lng'], name=place['name'], type=category)

        serializer = MeetupSerializer(meetup)

        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
