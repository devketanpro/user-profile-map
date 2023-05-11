from django.contrib.gis.geos import Point
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from .forms import LoginForm
from .models import UserProfile
from .views import LogoutView


class SignUpViewTestCase(TestCase):

    def setUp(self):
        self.signup_url = reverse('signup')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'latitude': '40.7128',
            'longitude': '-74.0060',
        }

    def test_signup_form_valid(self):
        response = self.client.post(self.signup_url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect to success URL
        user = UserProfile.objects.get(username=self.valid_data['username'])
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.location.x, float(self.valid_data['longitude']))
        self.assertEqual(user.location.y, float(self.valid_data['latitude']))

    def test_signup_form_invalid(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'testpassword456'  # Invalid password confirmation
        invalid_data['latitude'] = 'invalid_latitude'  # Invalid latitude
        response = self.client.post(self.signup_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Form validation error
        self.assertTemplateUsed(response, 'signup.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())


class LoginViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = UserProfile.objects.create_user(username='testuser', password='password123')

    def test_login_success(self):
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('map'))

    def test_login_failure(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_login_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertTrue(isinstance(response.context['form'], LoginForm))


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda x: None)
        self.user = UserProfile.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_user_logout(self):
        request = self.factory.get(reverse('logout'))
        request.user = self.user
        self.middleware.process_request(request)
        response = LogoutView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)


class UserProfileDetailViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.profile = UserProfile.objects.create(
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            home_address='123 Test St',
            phone_number='555-555-5555'
        )
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('user_profile', kwargs={'pk': self.profile.pk})

    def test_view_returns_200(self):
        # Ensure that the view returns 200 status code for authenticated users
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Ensure that the view uses the correct template
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user_profile.html')


class UserMapListViewTestCase(TestCase):
   
    def setUp(self):
        self.client = Client()
        self.user = mixer.blend(UserProfile)
        self.user.set_password('password123')
        self.user.save()
        self.profile = mixer.blend(UserProfile, location=Point(28.7041, 77.1025))
        self.url = reverse('map')
    
    def test_user_map_view(self):
        self.client.login(username=self.user.username, password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map.html')
        self.assertTrue('map' in response.context)
        self.assertTrue(response.context['map'])
        self.client.logout()


class UserProfileJsonViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.profile = UserProfile.objects.create(
            first_name='John',
            last_name='Doe',
            home_address='123 Main St',
            phone_number='555-555-1234',
        )

    def test_user_profile_json_view(self):
        response = self.client.get(reverse('user_profile_json', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'username': self.profile.username,
            'email': self.profile.email,
            'first_name': self.profile.first_name,
            'last_name': self.profile.last_name,
            'home_address': self.profile.home_address,
            'phone_number': self.profile.phone_number,
        })

    def test_user_profile_json_view_user_not_found(self):
        response = self.client.get(reverse('user_profile_json', kwargs={'pk': self.profile.pk + 1}))
        self.assertEqual(response.status_code, 404)