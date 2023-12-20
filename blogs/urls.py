from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('blogs/', views.BlogListView.as_view(), name = 'blog-list'),
    path('blogs/<uuid:pk>/', views.BlogDetailView.as_view(), name = 'blog-detail'),
    path('bloggers/<uuid:pk>/', views.BloggerDetailView.as_view(), name = 'blogger-detail'),
    path('blogger/<uuid:pk>/profile/', views.BloggerProfileView.as_view(), name = 'blogger-profile'),
    path('blogger/<uuid:pk>/profile/update/', views.BloggerUpdateView.as_view(), name = 'blogger-profile-update'),
    path('blog/create/', views.PostCreateView.as_view(), name = 'blog-create'),
    path('blog/<uuid:pk>/update/', views.PostUpdateView.as_view(), name = 'blog-update'),
    path('bloggers/<uuid:pk>/dashboard/', views.dashboard, name='dashboard'),
    path('bloggers/<uuid:pk>/viewed-posts/', views.viewedPosts, name = 'viewed-posts'),
    path('bloggers/<uuid:pk>/liked-posts/', views.likedPosts, name = 'liked-posts'),
    path('blogs/<uuid:pk>/like_action/', views.like_action, name = 'like-action'),
    path('bloggers/<uuid:pk>/follow_action/', views.follow_action, name = 'follow-action'),
    path('bloggers/<uuid:pk>/dashboard/unpublish-action/', views.unpublish_action, name = "unpublish-action"),
    path('bloggers/<uuid:pk>/dashboard/publish-action/', views.publish_action, name = "publish-action"),
    path('bloggers/<uuid:pk>/dashboard/delete-action/', views.delete_action, name = "delete-action"),
]
