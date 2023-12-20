from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.functions import Coalesce
from django.urls import reverse

from ckeditor.fields import RichTextField
import uuid

User = get_user_model()

class BloggerManager(models.Manager):
    def with_follower_count(self):
        return self.annotate(num_followers = Coalesce(models.Count('my_followers'), 0)).order_by('-num_followers')

class Blogger(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='blogger')
    bio = models.TextField(max_length = 200)
    profile_picture = models.ImageField(upload_to='avatars/', null=True, blank = True)
    interests = models.ManyToManyField('Category', blank=True, related_name='bloggers')

    objects = BloggerManager()

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return revese('blogger-detail', args=[str(self.id)])

    def has_followed(self, user):
        return self.my_followers.filter(user = user).exists()


class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length = 50)
    # slug = models.SlugField(unique = True, max_length=100)
    category_image = models.ImageField(upload_to='categories/', null = True, blank = True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 50)
    # slug = models.SlugField(unique = True, max_length=100)

    def __str__(self):
        return self.name



class PostManager(models.Manager):
    def with_likes_count(self):
        return self.annotate(num_likes=Coalesce(models.Count('likes'), 0)).order_by('-num_likes')

    def with_views_count(self):
        return self.annotate(num_views=Coalesce(models.Count('views'), 0)).order_by('-num_views')

class Post(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    author = models.ForeignKey('Blogger', on_delete = models.CASCADE, related_name = 'my_blogs')
    title = models.CharField(max_length = 300)
    sub_title = models.CharField(max_length = 300, blank=True, null=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    categories = models.ManyToManyField('Category', blank=True, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ImageField(upload_to='posts/', blank = True, null = True)
    # slug = models.SlugField(unique = True, max_length=500)

    objects = PostManager()

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_short_description(self):
        if len(self.content) < 200:
            return self.content
        return self.content[:200] + '...'
    
    def get_very_short_description(self):
        if len(self.content) < 100:
            return self.content
        return self.content[:100] + '...'
    
    def get_very_very_short_description(self):
        if len(self.content) < 60:
            return self.content
        return self.content[:60] + '...'
    
    def get_absolute_url(self):
        return reverse('blog-detail', args = [str(self.id)])
    
    def get_short_heading(self):
        if len(self.title) < 50:
            return self.title
        return self.title[:50] + '...'

    def get_short_heading2(self):
        if len(self.title) < 70:
            return self.title
        return self.title[:70] + '...'

    def get_short_heading3(self):
        if len(self.title) < 100:
            return self.title
        return self.title[:100] + '...'

class PublishedPostManager(models.Manager):
    def with_likes_count(self):
        return self.annotate(num_likes = Coalesce(models.Count('likes'), 0)).order_by('-num_likes')

    def with_views_count(self):
        return self.annotate(num_views = Coalesce(models.Count('views'), 0)).order_by('-num_views')

class PublishedPost(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    post = models.OneToOneField('Post', on_delete = models.CASCADE, related_name='post')
    posted_at = models.DateTimeField(auto_now_add=True)

    objects = PublishedPostManager()

    def __str__(self):
        return f'{self.post}'

    def get_absolute_url(self):
        return reverse('blog-detail', args = [str(self.id)])

    def get_date(self):
        return self.posted_at.date()
    
    def get_date_of_view(self, user):
        try:
            latest_view = View.objects.filter(user = user, post = self).latest('created_at')
            return latest_view.created_at.date()
        except:
            return None
        
    def get_date_of_like(self, user):
        try:
            likedAt = Like.objects.filter(user = user, post = self).latest('created_at')
            return likedAt.created_at.date()
        except:
            return None
    

class View(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'my_views')
    post = models.ForeignKey('PublishedPost', on_delete = models.CASCADE, related_name = 'views')


    def __str__(self):
        return f'{self.user} viewed {self.post}'


class Like(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'my_likes')
    post = models.ForeignKey('PublishedPost', on_delete = models.CASCADE, related_name = 'likes')

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user} liked {self.post}'

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'my_comments')
    body = models.TextField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('PublishedPost', on_delete = models.CASCADE, related_name = 'comments')

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'ifollows')
    followedPerson = models.ForeignKey('Blogger', on_delete = models.CASCADE, related_name = 'my_followers')

    def __str__(self):
        return f'{self.follower} follows {self.followedPerson}'

