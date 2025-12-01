from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'actif', 'date_creation')
    list_filter = ('actif', 'date_creation', 'date_modification')
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    readonly_fields = ('date_creation', 'date_modification')
    list_editable = ('actif',)
    ordering = ('-date_creation',)
    date_hierarchy = 'date_creation'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
