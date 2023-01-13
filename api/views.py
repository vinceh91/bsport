from api.models import Appointment, Event, User, Event2
from api.serializers import AppointmentSerializer, EventSerializerV2, UserSerializer, EventSerializerV3
from rest_framework import response, viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event2.objects.all()
    # queryset = list(Event.scan())
    serializer_class = EventSerializerV3
