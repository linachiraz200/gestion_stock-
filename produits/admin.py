from django.contrib import admin
from .models import Produit, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_count', 'date_creation')
    search_fields = ('name', 'description')
    readonly_fields = ('date_creation',)
    ordering = ('name',)
    
    def product_count(self, obj):
        return obj.produits.count()
    product_count.short_description = 'Nombre de produits'


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'category', 'quantite', 'prix', 'stock_status', 'date_creation')
    list_filter = ('category', 'date_creation', 'date_modification')
    search_fields = ('nom', 'category__name')
    list_editable = ('quantite', 'prix')
    readonly_fields = ('date_creation', 'date_modification', 'total_value')
    ordering = ('-date_creation',)
    date_hierarchy = 'date_creation'
    
    def stock_status(self, obj):
        return obj.stock_status
    stock_status.short_description = 'Statut Stock'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
