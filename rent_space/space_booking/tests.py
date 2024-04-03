from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import AdSpace


class AdSpaceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_adspace(self):
        data = {
            "location": "Test Location",
            "size": 100,
            "price": 50.00,
            "availability": True,
            "photos": "http://example.com/image.jpg"
        }
        response = self.client.post('/api/create-adspace/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AdSpace.objects.count(), 1)
        adspace = AdSpace.objects.get()
        self.assertEqual(adspace.location, data['location'])

    def test_get_adspace(self):
        adspace = AdSpace.objects.create(location="Test Location", size=100, price=50.00, availability=True,
                                         photos="http://example.com/image.jpg")
        response = self.client.get(f'/api/adspace/{adspace.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], adspace.location)

    def test_update_adspace(self):
        adspace = AdSpace.objects.create(location="Test Location", size=100, price=50.00, availability=True,
                                         photos="http://example.com/image.jpg")
        updated_data = {
            "location": "Updated Location",
            "size": 200,
            "price": 100.00,
            "availability": False,
            "photos": "http://example.com/updated_image.jpg"
        }
        response = self.client.put(f'/api/adspace/{adspace.pk}/update/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        adspace.refresh_from_db()
        self.assertEqual(adspace.location, updated_data['location'])

    def test_delete_adspace(self):
        adspace = AdSpace.objects.create(location="Test Location", size=100, price=50.00, availability=True,
                                         photos="http://example.com/image.jpg")
        response = self.client.delete(f'/api/adspace/{adspace.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AdSpace.objects.count(), 0)
