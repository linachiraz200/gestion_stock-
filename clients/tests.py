from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Client


class ClientModelTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@example.com",
            telephone="0123456789",
            adresse="123 Rue de la Paix"
        )

    def test_client_creation(self):
        self.assertEqual(self.client_obj.nom, "Dupont")
        self.assertEqual(self.client_obj.prenom, "Jean")
        self.assertEqual(self.client_obj.email, "jean.dupont@example.com")

    def test_client_str(self):
        expected = "Jean Dupont"
        self.assertEqual(str(self.client_obj), expected)


class ClientViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_client_list_requires_login(self):
        response = self.client.get(reverse('clients:liste_clients'))
        self.assertIn(response.status_code, [301, 302])  # Redirect to login
