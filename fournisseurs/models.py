from django.db import models

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_unitaire = models.FloatField()

    def __str__(self):
        return self.nom

class Facture(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='factures')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    total = models.FloatField(blank=True)
    date_facture = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # حساب الإجمالي تلقائياً
        self.total = float(self.quantite) * float(self.produit.prix_unitaire)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Facture {self.id} - {self.fournisseur}"
