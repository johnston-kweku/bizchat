# user/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, Business

@receiver(post_save, sender=UserProfile)
def create_business(sender, instance, created, **kwargs):
    if created:
        Business.objects.create(user_profile=instance)
