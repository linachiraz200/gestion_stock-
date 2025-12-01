from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from utils.validators import validate_positive_number, validate_stock_quantity, validate_price


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Produit(models.Model):
    nom = models.CharField(max_length=100, db_index=True)
    quantite = models.IntegerField(
        db_index=True, 
        validators=[MinValueValidator(0)]
    )
    prix = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[validate_price]
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='produits')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['nom', 'category']),
            models.Index(fields=['quantite']),
        ]

    def clean(self):
        if self.quantite < 0:
            raise ValidationError('La quantité ne peut pas être négative.')
        if self.prix <= 0:
            raise ValidationError('Le prix doit être supérieur à zéro.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
    
    @property
    def is_low_stock(self):
        from django.conf import settings
        threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 5)
        return self.quantite <= threshold
    
    @property
    def stock_status(self):
        if self.is_low_stock:
            return 'Faible'
        return 'Normal'
    
    @property
    def total_value(self):
        return self.quantite * self.prix
