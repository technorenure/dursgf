
from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save

class LocalGovt(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class RegType(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class GroupType(models.Model):
    name = models.CharField(max_length=200)

class Gallery(models.Model):
    image = models.FileField(upload_to='gallery')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.user.username


def create_profile(sender, instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance)

post_save.connect(create_profile,sender=User)

def update_profile(sender, instance, created,**kwargs):
    if created == False:
        instance.profile.save()

post_save.connect(update_profile,sender=User)

class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    picture = models.FileField(upload_to='images/team_images')
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    rank = models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.user.username

class SupportGroup(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,)
    full_name = models.CharField(max_length=200)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    home_address = models.CharField(max_length=200)
    ward = models.CharField(max_length=200)
    local_gov = models.ForeignKey(LocalGovt, on_delete=models.CASCADE)
    reg_type = models.ForeignKey(RegType, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name

class Registered(models.Model):
    number = models.IntegerField(default=0)