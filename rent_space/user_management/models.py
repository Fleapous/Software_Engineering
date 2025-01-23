from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    contactInfo = models.CharField(max_length=100)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')

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


class Log(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    duration = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.method} {self.path} - {self.status_code}"

class AdminUser(User):

    def approveUser(self):
        pass

    def removeUser(self):
        pass

    def moderateContent(self):
        pass

    def generateReports(self):
        pass
