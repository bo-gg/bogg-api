from unittest import skip

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from track.models import CalorieEntry


class APITest(APITestCase):

    def setUp(self):
        self.admin_username = 'admin@admin.com'
        self.admin_password = 'testadmin'
        User.objects.create_superuser(self.admin_username, 'admin@admin.com', self.admin_password)
        self.client.login(username=self.admin_username, password=self.admin_password)

        self.consumption_payload = {
            'entry_type': 'C',
            'calories': 100,
            'note': 'silica gel',
            'dt_occurred': str(timezone.now())
        }

        self.exercise_payload = {
            'entry_type': 'E',
            'calories': -200,
            'note': 'ran from hungry wolves',
            'dt_occurred': str(timezone.now())
        }


    def test_consumption_post(self):
        """ Ensure we can post a plan, and that it is returned in a queued state. """
        response = self.client.post('/api/entries/', self.consumption_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'expected 201 (created) response')
        payload = response.json()
        self.assertEqual(payload['entry_type'], 'C', 'entry didn\'t have an id of 1')
        self.assertEqual(CalorieEntry.objects.count(), 1, 'a single plan wasn\'t created')
        self.assertEqual(CalorieEntry.objects.first().calories, 100)

    def test_daily_entry_get(self):
        date_str = str(timezone.now().date())
        self.client.post('/api/entries/', self.consumption_payload, format='json')
        self.client.post('/api/entries/', self.exercise_payload, format='json')
        response = self.client.get('/api/daily/{}/'.format(date_str), format='json')
        payload = response.json()
        self.assertEqual(payload['calories_consumed'], 100, 'incorrect daily entry calories_consumed')
        self.assertEqual(payload['calories_expended'], -200, 'incorrect daily entry calories_expended')
        self.assertEqual(payload['net_calories'], -100, 'incorrect daily entry net_calories')


    def test_date_created_works(self):
        print 'i ensured date created worked well'
        pass

    def test_yesterday_daily_entry_get(self):
        pass
