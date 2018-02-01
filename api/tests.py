from django.test import TestCase
from .models import Readings

from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

class ModelTestCase(TestCase):
    """This class defines the test suite for the readings model"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.readings_title = "My Test Project"
        self.readings_script = "Hello world"
        self.readings_test = 1
        self.readings = Readings(title=self.readings_title,
                                 script=self.readings_script,
                                 test=self.readings_test)

    def test_model_can_create_a_readings(self):
        """Test the readings model can create a reading."""
        old_count = Readings.objects.count()
        self.readings.save()
        new_count = Readings.objects.count()
        self.assertNotEqual(old_count,new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views"""

    def setUp(self):
        """Define the test client and other test variables"""
        self.client = APIClient()
        self.readings_data = {
            'title':'My Test Project',
            'script':'Hello world',
            'test':1
        }
        self.response = self.client.post(
            reverse('create'),
            self.readings_data,
            format="json"
        )

    def test_api_can_create_a_readings(self):
        """Test the api has reading creation capability"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_reading(self):
        """Test the api can get a given reading"""
        readings = Readings.objects.get()
        response = self.client.get(
            reverse('details',
                    kwargs={'pk': readings.id}), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, readings)