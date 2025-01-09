from django.contrib import admin

from .models import User, Post, Following, Comment

# Register your models here.

# super user
# user: qristaan | pass: qristaan

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Comment)
