from django.db import models
from dynamorm import DynaModel
from dynamorm.relationships import ManyToOne
from marshmallow import fields


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    registration_date = models.DateField()


class Appointment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date = models.DateField()


class Event(DynaModel):

    class Table:
        resource_kwargs = {
            'endpoint_url': 'http://localhost:8000'}
        name = 'Event'
        hash_key = 'a'
        read = 1
        write = 1

    class Schema:
        a = fields.Integer()
        d = fields.String()


class EventManager(models.Manager):
    def get_queryset(self):
        return list(Event.scan())

    def create(self, **validated_data):
        # event = Event(a=self.model.a, d=self.model.d)
        event = Event(**validated_data)
        event.save()
        return event


class Event2(models.Model):
    # a = models.ForeignKey(Appointment, on_delete=models.DO_NOTHING)
    a = models.IntegerField()
    d = models.CharField(max_length=20)

    objects = EventManager()

    class Meta:
        managed = False

    def save(self, *args, **kwargs):
        event = Event(a=self.a, d=self.d)
        event.save()
