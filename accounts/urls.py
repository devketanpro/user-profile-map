from django.urls import path
from .views import (
    SignUpView, UserProfileDetailView, LogoutView, 
    LoginView,EditProfileView, UserMapListView, UserProfileJsonView
)

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/<int:pk>/', UserProfileDetailView.as_view(), name='user_profile'),
    path('accounts/profile/<int:pk>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('user/<int:pk>/json/', UserProfileJsonView.as_view(), name='user_profile_json'),
    path('', UserMapListView.as_view(), name='map'),
]
