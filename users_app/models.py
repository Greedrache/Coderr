from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    file = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=20, blank=True)  
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

