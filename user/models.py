from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    def is_online(self):
        return timezone.now() - self.last_seen < timezone.timedelta(seconds=30)
    
    
class Business(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='business')
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title or "Unnamed Business"
    
class Services(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title

class Products(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title
    


