from django.conf import settings
from django.test import TestCase
from maximyprofile.mainapp.models import ProductCategory, Product
from django.test.client import Client

# Create your tests here.
from maximyprofile.authapp.models import ShopUser


class UserTestCase(TestCase):
    username = 'maximy'
    email = 'maximy.pro@gmail.com'
    password = '111'

    new_user_data = {
        'username': 'maximy_user',
        'first_name': 'Maksim',
        'last_name': 'Maksim',
        'email': 'maximy.pro@gmail.com',
        'password1': '111',
        'password2': '111',
        'age': 27,
    }

    def setUp(self) -> None:
        self.user = ShopUser.objects.create_superuser(self.username, self.email, self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 302)

    def test_register(self):

        response = self.client.post('/auth/register/',data=self.new_user_data)
        print(response.status_code)

        self.assertEqual(response.status_code,302)

        user = ShopUser.objects.get(username=self.new_user_data['username'])
        # verify / < str: email > / < str: activate_key > /
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{user.email}/{user.activation_key}/"

        response = self.client.get(activation_url)

        self.assertEqual(response.status_code,302)

        user.refresh_form_db()
        self.assertFalse(user.is_active)
        user.refresh_form_db()
        self.assertTrue(user.is_active)

    def tearDown(self) -> None:
        pass