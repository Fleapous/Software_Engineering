from django.contrib.auth.models import AbstractUser
from django.db import models
from rent_space.space_booking.models import Booking, AdSpace


# Create your models here.
class User(AbstractUser):
    contactInfo = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    receivedPayments = models.ManyToManyField('Payment', related_name='received_payments')
    myPayments = models.ManyToManyField('Payment', related_name='my_payments')
    ratings = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    spaces = models.ManyToManyField('AdSpace', related_name='user_spaces')
    # name, email, password (inherited from AbstractUser)
