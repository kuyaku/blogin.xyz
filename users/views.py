from django.shortcuts import render, redirect
from allauth.account.views import SignupView, PasswordChangeView
from .forms import BloggerSignupForm, BloggerRegisterForm
from django.urls import reverse_lazy, reverse
from blogs.models import Category, Blogger
from django.contrib.auth.models import Group

from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from django.utils.crypto import get_random_string

from django.views.generic import CreateView

from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model

# Create your views here.

class BloggerSignupView(SignupView):
    template_name = 'account/blogger_signup.html'
    form_class = BloggerSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        interests = form.cleaned_data['interests']
        user_interests = [Category.objects.get_or_create(name = name)[0] for name in interests] 
        bio = form.cleaned_data.get('bio')
        # profile_picture = form.cleaned_data.get('profile_picture')
        response = super().form_valid(form)
        user = self.user
        try:
            blogger = Blogger.objects.create(user = user, bio = bio, profile_picture = profile_picture)
            group = Group.objects.get(name = 'Bloggers')
            blogger.interests.set(user_interests)
            user.groups.add(group)
        except:
            pass
        return response

class BloggerRegisterView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'account/blogger_register.html'
    form_class = BloggerRegisterForm

    login_url = reverse_lazy('account_login')
    redirect_field_name = 'next'

    def get_success_url(self):
        return reverse_lazy('blogger-profile-update', kwargs={'pk': str(self.request.user.id)})

    def handle_no_permission(self):
        return redirect(reverse('home'))

    def test_func(self):
        return not (self.request.user.groups.filter(name = 'Bloggers').exists())

    def form_valid(self, form):
        interests = form.cleaned_data['interests']
        user_interests = [Category.objects.get_or_create(name = name)[0] for name in interests]
        bio = form.cleaned_data.get('bio')
        # profile_picture = form.cleaned_data.get('profile_picture')
        user = self.request.user

        try:
            blogger_instance = Blogger.objects.create(user = user, bio = bio, profile_picture = profile_picture,)
            blogger_instance.interests.set(user_interests)
            group = Group.objects.get(name = 'Bloggers')
            user.groups.add(group)
        except:
            print("Error while registering as blogger")
            pass
        
        return redirect(self.success_url)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('home')
    # success_url = reverse_lazy('blogger-signup')

@login_required(login_url=reverse_lazy('account_login'), redirect_field_name = 'next')
def send_email_verification(request):
    try:
        email_address = EmailAddress.objects.get(user = request.user)
    except EmailAddress.DoesNotExist:
        email_address = None
    if email_address and not email_address.verified:
        send_email_confirmation(request, request.user)
        context = {
            'email': email_address
        }
        return render(request, 'account/verification_sent.html', context = context)
    return redirect('home')

