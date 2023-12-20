from django.contrib import admin
from .models import Blogger, Comment, View, Like, Post, Follow, Category, Tag, PublishedPost
# Register your models here.

admin.site.register(Blogger)
admin.site.register(Comment)
admin.site.register(View)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(PublishedPost)