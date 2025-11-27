from django.contrib import admin
from .models import Fournisseur, Produit, Facture

admin.site.register(Fournisseur)
admin.site.register(Produit)
admin.site.register(Facture)

