from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import AdSpace, Rating
from user_management.models import User


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

    def test_update_score(self):
        # Test updating the score of the rating
        adspace = AdSpace.objects.create(location="Test Location", size=100, price=50.00, availability=True,
                                         photos="http://example.com/image.jpg")
        user = User.objects.create_user(username='testuser2', password='testpassword')
        rating = Rating.objects.create(client=user, adSpace=adspace, rating=3, description="Test Comment", title="my comment")
        new_score = 4
        rating.updateScore(new_score)
        updated_rating = Rating.objects.get(pk=rating.pk)
        self.assertEqual(updated_rating.rating, new_score)

    def test_update_comment(self):
        # Test updating the comment of the rating
        adspace = AdSpace.objects.create(location="Test Location", size=100, price=50.00, availability=True,
                                         photos="http://example.com/image.jpg")
        user = User.objects.create_user(username='testuser2', password='testpassword')
        rating = Rating.objects.create(client=user, adSpace=adspace, rating=3, description="Test Comment", title="my comment")
        new_comment = "Updated Test Comment"
        rating.updateComment(new_comment)
        updated_rating = Rating.objects.get(pk=rating.pk)
        self.assertEqual(updated_rating.description, new_comment)

# class RatingTestCase(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create(username='test_user')
#
#         # Create a test ad space
#         self.ad_space = AdSpace.objects.create(location='Test Ad Space')
#
#         # Create a test rating
#         self.rating = Rating.objects.create(client=self.user, adSpace=self.ad_space, score=3, comment='Test Comment')
#
#     def test_update_score(self):
#         # Update the score of the rating
#         new_score = 4
#         self.rating.updateScore(new_score)
#
#         # Retrieve the updated rating from the database
#         updated_rating = Rating.objects.get(pk=self.rating.pk)
#
#         # Check if the score was updated successfully
#         self.assertEqual(updated_rating.score, new_score)
#
#     def test_update_comment(self):
#         # Update the comment of the rating
#         new_comment = 'Updated Test Comment'
#         self.rating.updateComment(new_comment)
#
#         # Retrieve the updated rating from the database
#         updated_rating = Rating.objects.get(pk=self.rating.pk)
#
#         # Check if the comment was updated successfully
#         self.assertEqual(updated_rating.comment, new_comment)