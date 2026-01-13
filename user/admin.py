from django.contrib import admin
from .models import UserProfile, Business, Services, Products

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'bio', 'profile_picture',
    ]
    
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]

@admin.register(Services)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'business', 'title', 'description'
    ]

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'business', 'title', 'description', 'image'
    ]

