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
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)


class Following(models.Model):

    # person A is following person B ...
    follower = models.ForeignKey(User, on_delete=models.CASCADE)

    # person B is being followed by person A
    following = models.ForeignKey(User, on_delete=models.CASCADE)

    # set restriction so that followers and following ...
    # ... cannot be the same person

    def valid_following(self):
        # return true if following and follower are not same person, else return false
        return self.follower != self.following
    
    class meta:
        unique_together = ('follower', 'following')
    

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    post_commented_on = models.ForeignKey(Post, on_delete=models.CASCADE)
    
# class Profile(models.Model):
#     pass
#     # user
#     # followers
####  Might not need this model?
    