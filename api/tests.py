import datetime
from django.test import TestCase
from django.utils import timezone
from .models import User, Appointment
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import include, path, reverse, reverse_lazy
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase


class SportAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create(
            first_name='Vincent',
            last_name='Haguet',
            email='vhaguet@me.com',
            registration_date='2022-10-21'
        )

        cls.appointment = Appointment.objects.create(user_id=cls.user.id, date='2023-04-01')

        cls.user_2 = User.objects.create(
            first_name='Philippe',
            last_name='Haguet',
            email='phaguet@me.com',
            registration_date='2022-09-21')

        cls.appointment_2 = Appointment.objects.create(user_id=cls.user_2.id, date='2023-04-02')

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestUser(SportAPITestCase):

    url = reverse_lazy('user-list')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'registration_date': user.registration_date,
            } for user in [self.user, self.user_2]
        ]
        self.assertEqual(response.json(), expected)

    def test_create(self):
        category_count = User.objects.count()
        data = {'first_name': 'Vinc',
                'last_name': 'Haguet',
                'email': 'vhaguet@me.com',
                'phone_number': '0784566778',
                'registration_date': '2022-10-31'
                }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), category_count+1)

    def test_list_filter(self):
        response = self.client.get(self.url + '1/')
        self.assertEqual(response.status_code, 200)
        expected = {
            'id': self.user.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'registration_date': self.user.registration_date,
        }
        self.assertEqual(expected, response.json())

    def test_delete(self):
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        data = {
            'id': self.user.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'phone_number': "0784444444",
            'registration_date': self.user.registration_date,
        }
        response = self.client.put(reverse('user-detail', kwargs={'pk': self.user.pk}), data=data)
        self.assertEqual(response.status_code, 200)


class TestAppointment(SportAPITestCase):

    url = reverse_lazy('appointment-list')

    def get_appointment_detail_data(self, appointments):
        return [
            {'id': appointment.pk,
                # 'user': 'http://testserver/users/' + str(appointment.user_id) + '/',
                'user': appointment.user_id,
                'date': appointment.date,
             } for appointment in appointments
        ]

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_appointment_detail_data([self.appointment, self.appointment_2]), response.json())

    def test_list_filter(self):
        response = self.client.get(self.url + '1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_appointment_detail_data([self.appointment]), [response.json()])

    def test_create(self):
        appointment_count = Appointment.objects.count()
        data = {
            'date': '2023-12-08',
            'user': self.user.id}

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Appointment.objects.count(), appointment_count+1)

    def test_create_in_the_past(self):
        appointment_count = Appointment.objects.count()
        data = {
            'date': '2019-12-08',
            'user': self.user.id}

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Appointment.objects.count(), appointment_count)

    def test_delete(self):
        response = self.client.delete(reverse('appointment-detail', kwargs={'pk': self.appointment.pk}))
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        data = {'date': '2024-10-12',
                'id': self.appointment.id,
                'user': self.user.id
                }
        response = self.client.put(reverse('appointment-detail', kwargs={'pk': self.appointment.pk}), data=data)
        self.assertEqual(response.status_code, 200)
