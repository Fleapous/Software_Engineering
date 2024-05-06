from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user_management.models import User
from .serializers import NotApprovedAdSpaceSerializer
from .models import AdSpace, Rating, Booking, Payment
from django.urls import reverse


class AdSpaceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_not_approved_adspace_list(self):
        # Creating some AdSpace objects
        adspace1 = AdSpace.objects.create(owner=self.user, location='Location 1', size='10', price=10, availability=True, isApproved=False)
        adspace2 = AdSpace.objects.create(owner=self.user, location='Location 2', size='10', price=20, availability=True, isApproved=False)
        adspace3 = AdSpace.objects.create(owner=self.user, location='Location 3', size='10', price=30, availability=True, isApproved=True)
        url = reverse('get-unapproved-adspaces')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        queryset = AdSpace.objects.filter(isApproved=False)
        serializer = NotApprovedAdSpaceSerializer(queryset, many=True)
        self.assertEqual(data, serializer.data)

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
        rating = Rating.objects.create(client=user, adSpace=adspace, rating=3, description="Test Comment",
                                       title="my comment")
        new_score = 4
        rating.updateScore(new_score)
        updated_rating = Rating.objects.get(pk=rating.pk)
        self.assertEqual(updated_rating.rating, new_score)

    def test_update_comment(self):
        # Test updating the comment of the rating
        adspace = AdSpace.objects.create(location="Test Location", size=100, price=50.00, availability=True,
                                         photos="http://example.com/image.jpg")
        user = User.objects.create_user(username='testuser2', password='testpassword')
        rating = Rating.objects.create(client=user, adSpace=adspace, rating=3, description="Test Comment",
                                       title="my comment")
        new_comment = "Updated Test Comment"
        rating.updateComment(new_comment)
        updated_rating = Rating.objects.get(pk=rating.pk)
        self.assertEqual(updated_rating.description, new_comment)

    def test_fetch_bookings(self):
        client = APIClient()
        adspace = AdSpace.objects.create(location="Test Location", size=100, price=50.00, availability=True,
                                         photos="http://example.com/image.jpg")
        booking1 = Booking.objects.create(client=self.user, adSpace_id=1, bookingDate='2024-04-30T12:00:00',
                                          status=True)
        booking2 = Booking.objects.create(client=self.user, adSpace_id=1, bookingDate='2024-05-01T10:00:00',
                                          status=False)

        client = APIClient()

        response = client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        first_entry = data[0]
        self.assertIn('id', first_entry)
        self.assertEqual(first_entry['id'], adspace.id)
        self.assertIn('bookings', first_entry)
        self.assertIsInstance(first_entry['bookings'], list)

        bookings_list = first_entry['bookings']
        self.assertEqual(len(bookings_list), 2)

        for booking in bookings_list:
            self.assertIn('client', booking)
            self.assertIn('client', booking)
            self.assertEqual(booking['client'], self.user.id)
            self.assertIn('adSpace', booking)
            self.assertEqual(booking['adSpace'], adspace.id)
            self.assertIn('bookingDate', booking)
            self.assertIn('status', booking)

    # def test_create_booking(self):
    #     data = {
    #         "client": 1,
    #         "adSpace": 1,
    #         "bookingDate": '2024-04-30T12:00:00',
    #         "status": True
    #     }
    #     response = self.client.post('/new-booking/', data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Booking.objects.count(), 1)
    #     booking = Booking.objects.get()
    #     self.assertEqual(booking.bookingDate, data['bookingDate'])

    def test_delete_booking(self):
        client = APIClient()
        booking = Booking.objects.create(client=self.user, adSpace_id=1, bookingDate='2024-04-30T12:00:00', status=True)
        booking_id = booking.pk
        response = client.delete(f'/api/bookings/{booking_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(pk=booking_id)


class PaymentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test payment
        self.payment_data = {
            'amount': 100.0,
            'paymentStatus': True,
        }
        self.payment = Payment.objects.create(**self.payment_data)

        # URL endpoints
        self.payment_list_url = '/api/payments/'
        self.payment_detail_url = f'/api/payments/{self.payment.pk}/'
        self.payment_update_url = f'/api/payments/{self.payment.pk}/update/'
        self.payment_create_url = '/api/create/payments/'

    def test_create_payment(self):
        response = self.client.post(self.payment_create_url, self.payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)
        payment = Payment.objects.latest('id')
        self.assertEqual(payment.amount, self.payment_data['amount'])

    def test_update_payment(self):
        updated_data = {
            'amount': 150.0,
            'paymentStatus': False,
        }
        response = self.client.put(self.payment_update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.amount, updated_data['amount'])

    def test_delete_payment(self):
        response = self.client.delete(self.payment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payment.objects.count(), 0)
