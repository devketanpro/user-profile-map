from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import FormView,CreateView
from django.views.generic import DetailView
from .forms import SignupForm, LoginForm
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(CreateView):
    """
    This class-based view handles user registration and location saving
    """
    form_class = SignupForm
    success_url = reverse_lazy('map')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        if latitude and longitude:
            user.location = Point(float(longitude), float(latitude))
        user.save()
        return redirect(self.success_url)


class LoginView(FormView):
    """
    This class handles user login with form validation and authentication
    """
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        # Authenticate the user and log them in
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, 'Invalid username or password')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    """
    This class logs out a user and redirects to the map
    """
    def get(self, request):
        logout(request)
        return redirect('map')

    
@method_decorator(login_required, name='dispatch')
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    """
    This class-based view shows user profile detail to authenticated users
    """
    model = UserProfile
    template_name = 'user_profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context