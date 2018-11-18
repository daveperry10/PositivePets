from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Pet(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    breed = models.CharField(max_length=250, blank=True)
    picture = models.FileField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def get_absolute_url(self):
        return reverse('positivepets:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Song(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=250)
    picture = models.FileField()
    birthday = models.DateField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

""" notes:
>>> album1.song_set.create(file_type='mp3', song_title='I love bacon')
>>> album1.song_set.all()
>>> album1.song_set.count()
"""