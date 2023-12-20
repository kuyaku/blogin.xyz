from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from django import forms
from blogs.models import Blogger

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',)


class BloggerSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": 'Last Name'}))
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Bio"}))
    interests = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Interests (Comma separated)"}))

    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        if interests:
            return [name.strip().upper() for name in interests.split(',') if name != '']
        return []
    
class BloggerRegisterForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Bio"}))
    interests = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Interests (Comma separated)"}))
    class Meta:
        model = Blogger
        fields = ('bio', 'interests',)
    
    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        if interests:
            return [name.strip().upper() for name in interests.split(',') if name != '']
        return []

    