from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    contactInfo = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    receivedPayments = models.ManyToManyField('Payment', related_name='received_payments')
    myPayments = models.ManyToManyField('Payment', related_name='my_payments')
    ratings = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    spaces = models.ManyToManyField('AdSpace', related_name='user_spaces')
    bookings = models.ManyToManyField('Booking', related_name='Bookings')

    # name, email, password (inherited from AbstractUser)

    def login(self):
        pass

    def logout(self):
        pass

    def updateAccount(self):
        pass

    def deleteAccount(self):
        pass

    def searchAdSpace(self):
        pass

    def bookAdSpace(self):
        pass

    def addAdSpace(self):
        pass

    def manageSpace(self):
        pass


class AdminUser(User):

    def approveUser(self):
        pass

    def removeUser(self):
        pass

    def moderateContent(self):
        pass

    def generateReports(self):
        pass
