from django.db import models
from django.core.validators import RegexValidator

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100, unique=True, db_index=True)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^[+]?[0-9\s-()]+$', 'Format de téléphone invalide')]
    )
    email = models.EmailField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['nom']
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

    def __str__(self):
        return self.nom
