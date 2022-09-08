
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from . models import SupportGroup, Profile

def create_profile(sender, instance,created,**kwargs):
    if created:
        Profile.objects.Create(user=instance)

post_save.connect(create_profile,sender=User)

def update_profile(sender, instance, created,**kwargs):
    if created == False:
        instance.profile.save()

post_save.connect(update_profile,sender=User)

