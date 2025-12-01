from django.contrib import admin
from .models import Fournisseur


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'actif', 'date_creation')
    list_filter = ('actif', 'date_creation', 'date_modification')
    search_fields = ('nom', 'adresse', 'telephone', 'email')
    list_editable = ('actif',)
    readonly_fields = ('date_creation', 'date_modification')
    ordering = ('nom',)
    date_hierarchy = 'date_creation'
