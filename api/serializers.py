from rest_framework import serializers
from .models import Appointment, Event, User, Event2
import datetime


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'phone_number', 'registration_date')


class AppointmentSerializer(serializers.ModelSerializer):
    def validate(self, data):
        date = data["date"]
        if date < datetime.date.today():
            raise serializers.ValidationError("Appointment date must be in the future")
        return data

    class Meta:
        model = Appointment
        fields = ('id', 'date', 'user')


class EventSerializerV2(serializers.Serializer):
    a = serializers.IntegerField()
    d = serializers.CharField()

    def create(self, **validated_data):
        event = Event(**validated_data)
        event.save()
        return event


class EventSerializerV3(serializers.ModelSerializer):

    class Meta:
        model = Event2
        fields = ['a', 'd']
