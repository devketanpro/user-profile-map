import json

import folium
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.db.models.functions import AsGeoJSON
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, RedirectView, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView

from .forms import EditProfileForm, LoginForm, SignupForm
from .models import UserProfile


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


class LogoutView(LoginRequiredMixin, RedirectView):
    """
    This view logs out the user and redirects to login.
    """
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class UserProfileDetailView(DetailView):
    """
    This class-based view shows user profile detail to authenticated users
    """
    model = UserProfile
    template_name = 'user_profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Edit user profile view, requires login, update user data
    """
    template_name = 'edit_profile.html'
    form_class = EditProfileForm

    def get_success_url(self):
        messages.success(self.request, 'Profile updated successfully.')
        return reverse_lazy('user_profile', kwargs={'pk': self.request.user.pk})

    def get_object(self):
        return self.request.user


class UserMapListView(LoginRequiredMixin, TemplateView):
    """
    This class-based view shows a map with markers of user locations
    """
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all UserProfile instances that have a location
        users_with_location = UserProfile.objects.filter(location__isnull=False)

        # If there are no users with locations, return an empty context
        if not users_with_location.exists():
            return context

        # Convert the user locations to GeoJSON
        user_locations_geojson = users_with_location.annotate(
            location_geojson=AsGeoJSON('location')
        ).values('location_geojson')

        # Create a Folium map centered on the first user's location
        first_user_location = users_with_location.first().location
        map_center = [first_user_location.y, first_user_location.x]
        map_obj = folium.Map(location=map_center, zoom_start=10)

        # Add a marker for each user location
        for user_location_geojson in user_locations_geojson:
            location_dict = json.loads(user_location_geojson['location_geojson'])
            location = Point(location_dict['coordinates'], srid=4326)
            folium.Marker([location.y, location.x]).add_to(map_obj)

        context['map'] = map_obj._repr_html_()
        return context

    
class UserProfileJsonView(View):
    """
    Returns JSON data of a user profile if exists, else error
    """
    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(pk=kwargs['pk'])
            data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'home_address': user.home_address,
                'phone_number': user.phone_number,
            }
            return JsonResponse(data, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error":"User Does Not Exists"}, status=404)