from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from datetime import datetime
from django.contrib.auth.models import AbstractUser,User


# User = get_user_model() 

# customizing user model
# class User(AbstractUser):
#     email = models.EmailField(max_length = 100,unique = True)
#     username = models.CharField(max_length = 30,unique = True)
#     password = models.CharField(max_length = 8,null = False)

#     def __str__(self):
#         return self.username

class Profile(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)#,primary_key = True)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    postId = models.UUIDField(primary_key = True, default = uuid.uuid4)
    user = models.CharField(max_length = 100)
    image= models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at  = models.DateTimeField(default = datetime.now)
    no_of_likes = models.IntegerField(default = 0)
   
    def __str__(self):
        return self.user
    

class LikePost(models.Model):
    post_id = models.CharField(max_length = 500)
    username = models.CharField(max_length = 100)
    # user_id = models.ForeignKey(profile,on_delete = models.CASCADE)

    def __str__(self):
        return self.username
    