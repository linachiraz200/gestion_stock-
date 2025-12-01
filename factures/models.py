from django.db import models
from django.contrib.auth.models import User
from clients.models import Client
from produits.models import Produit
from decimal import Decimal


class Facture(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    total_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tva = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    total_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.numero:
            last_facture = Facture.objects.order_by('-id').first()
            if last_facture:
                last_num = int(last_facture.numero.split('-')[1])
                self.numero = f"FAC-{last_num + 1:06d}"
            else:
                self.numero = "FAC-000001"
        super().save(*args, **kwargs)

    def calculate_totals(self):
        self.total_ht = sum(item.total for item in self.items.all())
        self.total_ttc = self.total_ht * (Decimal('1') + self.tva / Decimal('100'))
        self.save()
    
    @property
    def montant_tva(self):
        return self.total_ttc - self.total_ht

    def __str__(self):
        return f"{self.numero} - {self.client}"


class FactureItem(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
        self.facture.calculate_totals()

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"