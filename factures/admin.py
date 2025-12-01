from django.contrib import admin
from .models import Facture, FactureItem


class FactureItemInline(admin.TabularInline):
    model = FactureItem
    extra = 1


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client', 'date_creation', 'total_ttc']
    list_filter = ['date_creation']
    search_fields = ['numero', 'client__nom', 'client__prenom']
    inlines = [FactureItemInline]
    readonly_fields = ['numero', 'total_ht', 'total_ttc']


@admin.register(FactureItem)
class FactureItemAdmin(admin.ModelAdmin):
    list_display = ['facture', 'produit', 'quantite', 'prix_unitaire', 'total']