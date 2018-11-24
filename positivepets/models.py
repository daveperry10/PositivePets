from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # add additional fields in here
    #objects = MyManager
    city = models.CharField(max_length=250, null=True)
    picture = models.ImageField(null=True)
    birthday = models.DateField(null=True)
    #picture = models.ImageField('picture', upload_to='/media/', null=True, blank=True)

    def __str__(self):
        return self.email


class Pet(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    breed = models.CharField(max_length=250, blank=True)
    picture = models.FileField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('positivepets:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Chat(models.Model):
    comment = models.CharField(max_length=2000)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    timestamp = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('positivepets:chatmessage-create')

    def __str__(self):
        return self.song_title
