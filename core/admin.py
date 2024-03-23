from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Post, LikePost
# Register your models here.
# admin.site.register(User,UserAdmin)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)



