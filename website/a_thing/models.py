from django.db import models
from django.conf import settings


# Create your models here.
class Family(models.Model):
    family_name = models.CharField(max_length=250)

    def __str__(self):
        return self.family_name


class Person(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=250)
    person_logo = models.CharField(max_length=1000)
    person_bio = models.CharField(max_length=500)

    def __str__(self):
        return self.person_name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

