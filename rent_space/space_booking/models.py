from django.db import models

from user_management.models import User


class AdSpace(models.Model):
    location = models.CharField(max_length=100)
    size = models.FloatField()
    price = models.FloatField()
    availability = models.BooleanField()
    photos = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spaces_owned', null=True, blank=True)
    isApproved = models.BooleanField(default=False)

    def checkAvailability(self):
        pass

    def updateAvailability(self):
        pass


class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    adSpace = models.ForeignKey(AdSpace, on_delete=models.CASCADE)
    bookingDate = models.DateTimeField()
    status = models.BooleanField()

    def makePayment(self):
        pass

    def issueRefund(self):
        pass

    def updateStatus(self):
        pass


class Rating(models.Model):
    title = models.CharField(max_length=100)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    adSpace = models.ForeignKey(AdSpace, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(6)])
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def updateScore(self, new_rating):
        self.rating = new_rating
        self.save(update_fields=['rating'])

    def updateComment(self, new_comment):
        self.description = new_comment
        self.save(update_fields=['description'])


class Payment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_payments', null=True, blank=True)
    amount = models.FloatField()
    paymentStatus = models.BooleanField()
    spaceOwnerId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_payments', null=True,
                                     blank=True)

    def processPayment(self):
        pass

    def validatePayment(self):
        pass
