from django.db import models
from django.core.validators import RegexValidator

class Client(models.Model):
    nom = models.CharField(max_length=100, verbose_name="الاسم", db_index=True)
    prenom = models.CharField(max_length=100, verbose_name="اللقب", db_index=True)
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    telephone = models.CharField(
        max_length=20, 
        verbose_name="رقم الهاتف",
        validators=[RegexValidator(r'^[+]?[0-9\s-()]+$', 'Format de téléphone invalide')]
    )
    adresse = models.TextField(verbose_name="العنوان")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"