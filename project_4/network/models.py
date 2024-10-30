from django.contrib.auth.models import AbstractUser
from django.db import models

 # user = qristaan
 # password = qristaan

class User(AbstractUser):
    
    username = models.CharField(max_length=64, unique=True) # Used for Djangos authenticate
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __str__(self):
        return f"User = {self.username}" 

class Post(models.Model):
    # poster = models.ForeignKey(User, on_delete=models.CASCADE)
    # likes = models.IntegerField(default=0)
    # timestamp = models.DateTimeField(auto_now_add=True)
    pass

# class Profile(models.Model):
#     pass
#     # user
#     # followers
####  Might not need this model?
    

class Following(models.Model):
    # follower
    # following

    # set restriction so that followers and following ...
    # ... cannot be the same person
    pass

class Follower(models.Model):
    # following
    # follower
    pass

class Comment(models.Model):
    # commenter
    # comment
    # post commented on
    pass
