from django.shortcuts import render, redirect
from .models import Post, Category
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import Blogger, Post, Follow, Category, Tag, PublishedPost, Like, View
import random
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress

from django.core.exceptions import PermissionDenied

from django.http import Http404, JsonResponse, HttpResponseForbidden

from .forms import PostCreateForm, PostUpdateForm, BloggerUpdateForm

import string, random

User = get_user_model()

def index(request):
    all_posts = PublishedPost.objects.with_likes_count()
    all_categories = Category.objects.all()
    is_blogger = request.user.groups.filter(name = 'Bloggers').exists()
    context = {
        'post_list': all_posts,
        'category_list': all_categories,
        'is_blogger': is_blogger,
    }

    return render(request, 'index.html', context = context)

class BloggerDetailView(LoginRequiredMixin, DetailView):
    model = Blogger
    template_name = 'blogger_detail.html'
    context_object_name = 'blogger'

    login_url = reverse_lazy('account_login')
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_bloggers'] = Blogger.objects.filter(interests__in = self.object.interests.all()).distinct()
        context['my_blogs_list'] = PublishedPost.objects.filter(post__author = self.object)
        has_followed = Follow.objects.filter(follower = self.request.user, followedPerson = self.object).exists()
        context['has_followed'] = has_followed
        return context

class BlogDetailView(DetailView):
    model = PublishedPost
    template_name = 'blog_detail.html'
    context_object_name = 'blog'

    # login_url = reverse_lazy('account_login')
    # redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            has_liked = Like.objects.filter(user = self.request.user, post = self.object).exists()
            context['has_liked'] = has_liked
            # print("******* ", self.object.post.author)
            has_followed = Follow.objects.filter(follower = self.request.user, followedPerson = self.object.post.author).exists()
            context['has_followed'] = has_followed
        return context

class BlogListView(ListView):
    model = PublishedPost
    template_name = 'blog_list.html'
    context_object_name = 'blog_list'

    # login_url = reverse_lazy('account_login')
    # redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_liked_blogs'] = PublishedPost.objects.with_likes_count()
        context['top_viewed_blogs'] = PublishedPost.objects.with_views_count()
        # if (len(context['top_liked_blogs']) != 0):
        #     context['top_blog'] = random.choice(context['top_liked_blogs'])
        if self.request.user.is_authenticated:
            context['my_followedBloggers_blogs'] = self.getMyFollowedBloggersPosts(self.request.user)
        return context
    
    def getMyFollowedBloggersPosts(self, currentUser):
        followedBloggers = Follow.objects.filter(follower=currentUser).values_list('followedPerson', flat = True)
        posts_of_followed_bloggers = PublishedPost.objects.filter(post__author__in = followedBloggers)
        return posts_of_followed_bloggers


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    print('************** Creating new post *******************')
    model = Post
    template_name = 'new_blog.html'
    form_class = PostCreateForm

    login_url = reverse_lazy('account_login')
    redirect_field_name = 'next'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse('account_login'))
        return redirect(reverse('blogger-register', kwargs={'pk': str(self.request.user.id)}))

    def test_func(self):
        return self.request.user.groups.filter(name = 'Bloggers').exists()

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs = {'pk': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_blogger = Blogger.objects.filter(user = self.request.user).exists()
        context['is_blogger'] = is_blogger
        return context

    def form_valid(self, form):
        try:
            # form.instance.author = get_object_or_404(Blogger, user__id=self.request.user.id)
            form.instance.author = self.request.user.blogger
        except Blogger.DoesNotExist:
            print("register as blogger first")
            pass

        content = form.cleaned_data['content']
        form.instance.content = content
        # print(form.cleaned_data['image'])
        # form.instance.image = form.cleaned_data['image']

        title = form.cleaned_data['title']

        category_names = form.cleaned_data.get('category_names')
        categories = [Category.objects.get_or_create(name = name)[0] for name in category_names]

        tag_names = form.cleaned_data.get('tag_names')
        tags = [Tag.objects.get_or_create(name = name)[0] for name in tag_names]

        postInstance = form.save()
        postInstance.categories.set(categories)
        postInstance.tags.set(tags)

        if 'publish' in self.request.POST:
            published_post = PublishedPost(post = postInstance)
            published_post.save()
            
        return super().form_valid(form)

    def get_processed_tags_categories(self, modal, unprocessed_input):
        names_list = [name.strip().upper() for name in unprocessed_input.split(',') if name != '']
        processedResult = []
        for name in names_list:
            try:
                tag_category, created = modal.objects.get_or_create(name = name)
                processedResult.append(tag_category)
            except:
                print("already exists")
                pass

        return processedResult


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'new_blog.html'
    form_class = PostUpdateForm

    login_url = reverse_lazy('account_login')
    redirect_field_name = 'next'

    # checking if the user is same as the author of the post
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author.user:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs = {'pk': self.request.user.id})

    def get_initial(self):
        # Retrieve the existing post object
        post = self.get_object()

        # Get the existing category and tag names as a comma-separated string
        category_names = ', '.join(category.name for category in post.categories.all())
        tag_names = ', '.join(tag.name for tag in post.tags.all())

        # Return the initial data dictionary
        return {
            'category_names': category_names,
            'tag_names': tag_names,
            # ... other initial data if needed ...
        }

    def form_valid(self, form):
        try:
            form.instance.author = get_object_or_404(Blogger, user__id=self.request.user.id)
        except Blogger.DoesNotExist:
            print("register as blogger first")
            pass

        content = form.cleaned_data['content']
        form.instance.content = content
        # print(form.cleaned_data['image'])
        # form.instance.image = form.cleaned_data['image']

        title = form.cleaned_data['title']

        category_names = form.cleaned_data.get('category_names')
        categories = [Category.objects.get_or_create(name = name)[0] for name in category_names]

        tag_names = form.cleaned_data.get('tag_names')
        tags = [Tag.objects.get_or_create(name = name)[0] for name in tag_names]

        postInstance = form.save()
        postInstance.categories.set(categories)
        postInstance.tags.set(tags)

        if 'publish' in self.request.POST:
            published_post = PublishedPost(post = postInstance)
            published_post.save()
            
        return super().form_valid(form)
    
    def generateRandomString(self, length = 12):
        characters = string.ascii_letters + string.digits + string.ascii_lowercase + string.ascii_uppercase
        randomString = "".join(random.choice(characters) for _ in range(length))
        return randomString


    def get_processed_tags_categories(self, modal, unprocessed_input):
        names_list = [name.strip().upper() for name in unprocessed_input.split(',') if name != '']
        processedResult = []
        for name in names_list:
            try:
                tag_category, created = modal.objects.get_or_create(name = name)
                processedResult.append(tag_category)
            except:
                print("already exists")
                pass

        return processedResult


@login_required(login_url=reverse_lazy('account_login'), redirect_field_name = 'next')
def dashboard(request, pk):
    if str(request.user.id) != str(pk):
        raise PermissionDenied("Forbidden 403!")

    try:
        blogger = Blogger.objects.get(user__id = pk)
    except:
        return redirect(reverse('blogger-register', kwargs={'pk': request.user.id}))
    published_posts = PublishedPost.objects.filter(post__author = blogger)
    unpublished_posts = Post.objects.filter(author = blogger, post__isnull = True)
    is_blogger = request.user.groups.filter(name = 'Bloggers').exists()
    context = {
        'blogger': blogger,
        'published_posts': published_posts, 
        'unpublished_posts': unpublished_posts,
        'is_blogger': is_blogger,
    }
    return render(request, 'dashboard.html', context = context)

@login_required(login_url=reverse_lazy('account_login'), redirect_field_name = 'next')
def viewedPosts(request, pk):
    if str(request.user.id) != str(pk):
        raise PermissionDenied("Forbidden 403!")

    try:
        user = User.objects.get(id = pk)
    except:
        raise Http404

    viewed_posts = PublishedPost.objects.filter(views__user = user).distinct()
    is_blogger = request.user.groups.filter(name = 'Bloggers').exists()
    context = {
        'viewed_posts': viewed_posts,
        'is_blogger': is_blogger
    }
    return render(request, 'viewed_posts.html', context = context)


@login_required(login_url=reverse_lazy('account_login'), redirect_field_name = 'next')
def likedPosts(request, pk):
    if str(request.user.id) != str(pk):
        raise PermissionDenied("Forbidden 403")
    
    try:
        user = User.objects.get(id = pk)
    except:
        raise Http404

    liked_posts = PublishedPost.objects.filter(likes__user = user)
    is_blogger = request.user.groups.filter(name = 'Bloggers').exists()
    context = {
        'liked_posts': liked_posts,
        'is_blogger': is_blogger
    }
    return render(request, 'liked_posts.html', context = context)

@login_required(login_url=reverse_lazy('account_login'), redirect_field_name = 'next')
def like_action(request, pk):
    post = get_object_or_404(PublishedPost, id = pk)

    existing_like = Like.objects.filter(user = request.user, post = post).first()

    if existing_like:
        existing_like.delete()
        liked = False
    else:
        Like.objects.create(user = request.user, post = post)
        liked = True
    return JsonResponse({'liked': liked})


@login_required(login_url=reverse_lazy('account_login'), redirect_field_name = 'next')
def follow_action(request, pk):
    blogger = get_object_or_404(Blogger, id = pk)

    existing_follow = Follow.objects.filter(follower = request.user, followedPerson = blogger).first()
    if existing_follow:
        existing_follow.delete()
        follow = False
    else:
        Follow.objects.create(follower = request.user, followedPerson = blogger)
        follow = True
    return JsonResponse({'follow': follow})



def unpublish_action(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        try:
            post_to_unpublish = get_object_or_404(PublishedPost, id = post_id) 
            # ensure that only the author of the post can unpublish it
            if request.user != post_to_unpublish.post.author.user:
                return JsonResponse({'unpublished': False, 'error': 'You cannot unpublish this post.'}, status = 403)          
            post_to_unpublish.delete()
            return JsonResponse({'unpublised': True})
        except:
            return JsonResponse({'unpublished': False})

def publish_action(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        try:
            post_to_publish = get_object_or_404(Post, id = post_id)
            # ensure that only the author of the post can publish it
            if (post_to_publish.author.user != request.user):
                return HttpResponseForbidden("You don't have permission to publish it")

            PublishedPost.objects.create(post = post_to_publish)
            return JsonResponse({'published': True})
        except:
            return JsonResponse({'published': False})
    return JsonResponse({'error': 'Invalid request method'}, status = 400)

def delete_action(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        print(post_id)
        try:
            post_to_delete = get_object_or_404(Post, id = post_id)
            print(post_to_delete)
            # ensure that only the author of the post can delete it
            if (post_to_delete.author.user != request.user):
                return HttpResponseForbidden("You don't have permission to delete it")

            post_to_delete.delete()
            return JsonResponse({'deleted-post': True})
        except:
            return JsonResponse({"deleted-post": False})

    return JsonResponse({'error': 'Invalid request method'}, status = 400)


class BloggerProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = get_user_model()
    template_name = 'blogger_profile.html'

    login_url = reverse_lazy('account_login')
    redirect_field_name = 'next'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse('account_login'))
        return redirect(reverse('blogger-register', kwargs={'pk': str(self.request.user.id)}))

    def test_func(self):
        return self.request.user.groups.filter(name = 'Bloggers').exists()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogger = Blogger.objects.get(user__id = self.kwargs['pk'])
        context['blogger'] = blogger
        is_email_verified = EmailAddress.objects.filter(user = self.request.user, verified=True).exists()
        context['is_email_verified'] = is_email_verified
        return context

class BloggerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blogger
    form_class = BloggerUpdateForm

    template_name = 'blogger_profile_update.html'
    success_url = 'blogger-profile'

    login_url = reverse_lazy('account_login')
    redirect_field_name = 'next'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse('account_login'))
        return redirect(reverse('blogger-register', kwargs={'pk': str(self.request.user.id)}))

    def test_func(self):
        return self.request.user.groups.filter(name = 'Bloggers').exists()


    def get_object(self, queryset = None):
        return self.request.user.blogger

    def get_success_url(self):
        return reverse_lazy('blogger-profile', kwargs={'pk': str(self.request.user.id)})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        blogger = self.get_object()

        initial_values = {
            'username': blogger.user.username,
            'first_name': blogger.user.first_name,
            'last_name': blogger.user.last_name,
            'bio': blogger.bio,
            'user_interests': self.get_interests(blogger),
        }
        
        kwargs['initial'] = initial_values
        return kwargs
    
    def get_interests(self, blogger):
        interests = blogger.interests.all()
        return ', '.join(interest.name for interest in interests)

    def form_valid(self, form):
        user = self.request.user
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')

        if User.objects.filter(username=username).exclude(pk=user.id).exists():
            form.add_error('username', 'Username already taken!')
            return self.form_invalid(form)
    
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        blogger = user.blogger
        interest_name = form.cleaned_data.get('user_interests')
        categories = [Category.objects.get_or_create(name = name)[0] for name in interest_name]
        bio = form.cleaned_data.get('bio')

        blogger.bio = bio
        blogger.interests.set(categories)

        blogger.save()
        return super().form_valid(form)


