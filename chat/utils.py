from user.models import UserProfile

def get_user_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile
