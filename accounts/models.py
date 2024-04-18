from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="images/", blank=True)
    following_num = models.PositiveIntegerField(default=0)
    follower_num = models.PositiveIntegerField(default=0)
    
class FollowRelationship(models.Model):
    following = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="my_following", related_query_name="my_following")
    follower = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="my_follower", related_query_name="my_follower")
