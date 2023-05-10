from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class SignupForm(UserCreationForm):
    """
    Signup form with extended fields for user profile creation
    """
    home_address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'home_address', 'phone_number', 'latitude', 'longitude')


class LoginForm(forms.Form):
    """
    A form for user login that includes a username and password field.

    Attributes:
        username (CharField): A field for the user's username.
        password (CharField): A field for the user's password.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    """
    Form to edit user profile fields
    """
    home_address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'home_address', 'phone_number']