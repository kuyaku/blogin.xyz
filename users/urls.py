from django.urls import path, include
from .views import BloggerSignupView, BloggerRegisterView, CustomPasswordChangeView, send_email_verification

urlpatterns = [
    path('', include('allauth.urls')),
    path('signup/blogger/', BloggerSignupView.as_view(), name="blogger-signup"),
    path('signup/blogger/<uuid:pk>/register', BloggerRegisterView.as_view(), name='blogger-register'),
    path('password/change/', CustomPasswordChangeView.as_view(), name = 'account_change_password'),
    path('verify-email/', send_email_verification, name = 'account_confirm_email_new')
]