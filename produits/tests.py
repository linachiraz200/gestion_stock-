from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Produit, Category


class ProduitModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.produit = Produit.objects.create(
            nom="Test Product",
            quantite=10,
            prix=99.50,
            category=self.category
        )

    def test_produit_creation(self):
        self.assertEqual(self.produit.nom, "Test Product")
        self.assertEqual(self.produit.quantite, 10)
        self.assertEqual(self.produit.prix, 99.50)

    def test_produit_str(self):
        self.assertEqual(str(self.produit), "Test Product")


class ProduitViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Test Category")
        self.produit = Produit.objects.create(
            nom="Test Product",
            quantite=10,
            prix=99.50,
            category=self.category
        )

    def test_produit_list_requires_login(self):
        response = self.client.get(reverse('produits:liste_produits'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_produit_list_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('produits:liste_produits'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")