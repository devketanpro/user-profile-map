from django.urls import path
from django.contrib.auth.views import LoginView
from .views import SignUpView, UserProfileDetailView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='user_profile'),
]
